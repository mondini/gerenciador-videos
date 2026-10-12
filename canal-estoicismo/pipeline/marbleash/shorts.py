"""Shorts verticais (1080x1920) cortados do vídeo final: faixa central com a cena inteira, título em Cinzel em
cima e legenda frase a frase (Inter, a palavra da vez em âmbar) embaixo. Decisões do criador em 12/10/2026.

Cada vídeo descreve os seus shorts em videos/MA-NNN-slug/shorts.txt, uma linha por short:
    NN | TÍTULO | subtítulo | peça | deixa de início | deixa de fim | crédito
  - peça: número do bloco ou 'pausa'; deixas de tempos.txt da peça. A deixa de fim é EXCLUSIVA (o short para
    antes dela); 'fim' = até o fim da narração da peça.
  - subtítulo e crédito podem ficar vazios.
O tempo de cada trecho no vídeo final vem da mesma linha do tempo do `ma juntar` (com os dissolves).
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import config, entrega, tempos
from .config import ffmpeg
from .projeto import DISSOLVE, Bloco

W, H = 1080, 1920
CENA_H = 608                      # 1080 x 608: a cena 16:9 inteira na largura do celular
CENA_Y = 656
CARVAO = (0x1A, 0x18, 0x16)
MARMORE = (0xED, 0xE6, 0xDA)
MARMORE_300 = (0xB8, 0xAF, 0xA2)
AMBAR = (0xFF, 0xB5, 0x47)        # amber-400: só thumbnails e capas de shorts
FONTES = config.CANAL / 'fontes-tipograficas'
ANTES, DEPOIS = 0.5, 1.2          # respiro antes da primeira frase e depois da última (s)


def _fonte(nome, tam):
    return ImageFont.truetype(str(FONTES / nome), tam)


@dataclass
class Short:
    numero: str
    titulo: str
    subtitulo: str
    peca: str
    inicio: str
    fim: str
    credito: str

    @property
    def arquivo(self):
        slug = re.sub(r'[^a-z0-9]+', '-', self.titulo.lower()).strip('-')
        return f'{self.numero}-{slug}.mp4'


def ler(arq) -> list[Short]:
    out = []
    for linha in Path(arq).read_text(encoding='utf-8').splitlines():
        if not linha.strip() or linha.lstrip().startswith('#'):
            continue
        partes = [p.strip() for p in linha.split('|')]
        if len(partes) != 7:
            raise SystemExit(f'{arq}: esperado 7 campos separados por "|": {linha!r}')
        out.append(Short(*partes))
    return out


def linha_do_tempo(final: Path, video: str):
    """{nome da peça: (Bloco, início no vídeo final)} a partir do nome do final (ex.: MA-001-...-1-abertura-2)."""
    nomes = final.stem[len(video) + 1:].split('-')
    pecas = [Bloco.peca(video, n) for n in nomes]
    durs = [entrega.duracao_video(b.trabalho / f'{b.nome}-video.mp4') for b in pecas]
    inis, _ = entrega.inicios(durs, entrega.juncoes(pecas), DISSOLVE)
    return {b.nome: (b, i) for b, i in zip(pecas, inis)}


def _frases(b: Bloco, ini_peca: float, t0: float, t1: float):
    """[(início, fim, texto, [(início, fim) por palavra] ou None)] no tempo do final, dentro de [t0, t1)."""
    linhas = [l for l in tempos.ler(b.arquivo_tempos) if not l[2].startswith('(palavra)')]
    base = ini_peca + b.entrada
    palavras = [(w, base + b.mapa(s), base + b.mapa(e)) for w, s, e in b.audio_info.get('palavras', [])]
    out = []
    for k, (_, seg, frase) in enumerate(linhas):
        a = base + b.mapa(seg)
        z = base + b.mapa(linhas[k + 1][1]) if k + 1 < len(linhas) else base + b.duracao
        if z <= t0 or a >= t1:
            continue
        a, z = max(a, t0), min(z, t1)
        toks = frase.split()
        ws = [(s, e) for _, s, e in palavras if a - 0.05 <= s < z]
        if len(ws) != len(toks):          # o transcritor juntou ou separou palavras: reparte a fala pelo tamanho de cada uma
            fala_fim = ws[-1][1] if ws else z - 0.3
            pesos = np.cumsum([0] + [len(t) + 1 for t in toks])
            ws = [(a + (fala_fim - a) * pesos[j] / pesos[-1], a + (fala_fim - a) * pesos[j + 1] / pesos[-1]) for j in range(len(toks))]
        out.append((a, z, frase, ws))
    return out


def _quebrar(draw, texto, fonte, largura):
    linhas, atual = [], ''
    for p in texto.split():
        teste = f'{atual} {p}'.strip()
        if draw.textlength(teste, font=fonte) <= largura or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    return linhas + ([atual] if atual else [])


def _fundo(sh: Short):
    """O quadro fixo: carvão, marca, título, subtítulo e crédito."""
    img = Image.new('RGB', (W, H), CARVAO)
    d = ImageDraw.Draw(img)
    marca = _fonte('Cinzel-SemiBold.ttf', 34)
    partes = [('MARBLE ', MARMORE_300), ('&', AMBAR), (' ASH', MARMORE_300)]
    larg = sum(d.textlength(t, font=marca) for t, _ in partes)
    x = (W - larg) / 2
    for t, c in partes:
        d.text((x, 210), t, font=marca, fill=c)
        x += d.textlength(t, font=marca)
    titulo = _fonte('Cinzel-Black.ttf', 88)
    linhas = _quebrar(d, sh.titulo, titulo, 920)
    sub = _fonte('CormorantGaramond-MediumItalic.ttf', 54) if sh.subtitulo else None
    alto = len(linhas) * 100 + (70 if sub else 0)
    y = CENA_Y - 60 - alto
    for l in linhas:
        d.text(((W - d.textlength(l, font=titulo)) / 2, y), l, font=titulo, fill=MARMORE)
        y += 100
    if sub:
        d.text(((W - d.textlength(sh.subtitulo, font=sub)) / 2, y + 4), sh.subtitulo, font=sub, fill=AMBAR)
    if sh.credito:
        f = _fonte('Inter-Regular.ttf', 26)
        d.text(((W - d.textlength(sh.credito, font=f)) / 2, CENA_Y + CENA_H + 22), sh.credito, font=f, fill=MARMORE_300)
    return np.asarray(img).copy()


def _legenda(frase, destaque):
    """Imagem RGBA da legenda (largura W), com a palavra `destaque` (índice) em âmbar."""
    fonte = _fonte('Inter-SemiBold.ttf', 50)
    img = Image.new('RGBA', (W, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    toks = frase.split()
    linhas, atual = [], []
    for i, t in enumerate(toks):
        if atual and d.textlength(' '.join(toks[j] for j in atual + [i]), font=fonte) > 900:
            linhas.append(atual)
            atual = []
        atual.append(i)
    linhas.append(atual)
    y = 10
    for idx in linhas[:3]:
        texto = ' '.join(toks[j] for j in idx)
        x = (W - d.textlength(texto, font=fonte)) / 2
        for j in idx:
            d.text((x, y), toks[j], font=fonte, fill=AMBAR if j == destaque else MARMORE)
            x += d.textlength(toks[j] + ' ', font=fonte)
        y += 66
    return np.asarray(img)


def renderizar(sh: Short, final: Path, video: str, saida: Path, avisar=print):
    linha = linha_do_tempo(final, video)
    nome = f'bloco{sh.peca}' if sh.peca.isdigit() else sh.peca
    if nome not in linha:
        raise SystemExit(f'short {sh.numero}: a peça {sh.peca} não está no vídeo final {final.name}')
    b, ini_peca = linha[nome]
    base = ini_peca + b.entrada
    t0 = base + b.deixas[sh.inicio] - ANTES
    fim_narr = base + (b.duracao if sh.fim == 'fim' else b.deixas[sh.fim])
    t1 = fim_narr + DEPOIS
    frases = _frases(b, ini_peca, t0 + ANTES, fim_narr)
    dur = t1 - t0
    fundo = _fundo(sh)
    cache = {}

    def legenda_em(t):
        for k, (a, z, texto, ws) in enumerate(frases):
            if a <= t < z:
                dest = -1
                if ws:
                    for j, (s, e) in enumerate(ws):
                        if s <= t:
                            dest = j
                return cache.setdefault((k, dest), _legenda(texto, dest))
        return None

    src = subprocess.Popen([ffmpeg(), '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', str(final),
                            '-vf', f'scale={W}:{CENA_H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    saida.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen([ffmpeg(), '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(config.FPS),
                            '-i', '-', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', str(final), '-map', '0:v', '-map', '1:a',
                            '-af', f'afade=t=in:d=0.3,afade=t=out:st={dur - 0.9:.3f}:d=0.9',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', str(saida)],
                           stdin=subprocess.PIPE)
    n_bytes = W * CENA_H * 3
    i = 0
    while True:
        bruto = src.stdout.read(n_bytes)
        if len(bruto) < n_bytes:
            break
        t = i / config.FPS
        luz = min(1.0, t / 0.4, (dur - t) / 0.9)          # a cena acende e apaga; o título fica
        q = fundo.copy()
        q[CENA_Y:CENA_Y + CENA_H] = (np.frombuffer(bruto, np.uint8).reshape(CENA_H, W, 3) * max(luz, 0)
                                     + np.array(CARVAO) * (1 - max(luz, 0))).astype(np.uint8)
        leg = legenda_em(t0 + t)
        if leg is not None:
            y0 = CENA_Y + CENA_H + (90 if sh.credito else 60)
            area = q[y0:y0 + leg.shape[0]].astype(np.float32)
            a = leg[..., 3:4] / 255.0
            q[y0:y0 + leg.shape[0]] = (area * (1 - a) + leg[..., :3] * a).astype(np.uint8)
        enc.stdin.write(q.tobytes())
        i += 1
    enc.stdin.close()
    enc.wait()
    src.wait()
    avisar(f'{saida.name}: {dur:.1f} s ({len(frases)} frases)')
    return dur

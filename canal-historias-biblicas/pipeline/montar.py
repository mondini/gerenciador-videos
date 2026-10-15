"""Monta o vídeo de um roteiro a partir do montagem.json: renderiza as cenas, junta com dissolves e põe o som.

Sem narração (montagem.json com "narracao": null), o tempo de cada cena sai das falas que ela cobre, a
~palavras_por_minuto, e as falas podem aparecer como legenda provisória. Cenas já renderizadas e iguais
(mesmo HTML, mesma duração, mesma legenda) não são refeitas.

Uso (na pasta do canal):
  .venv/bin/python -m pipeline.montar videos/XX-NNN-slug [--paralelo 4]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import imageio_ffmpeg

from pipeline import render, sons

PAUSA_FALA = 0.5      # silêncio depois de cada fala
PAUSA_RETICENCIAS = 0.35
PAUSA_MARCADA = 0.8   # [pause]
MARGEM = 0.5          # antes da primeira e depois da última fala de cada cena
MINIMO = 4.5          # nenhuma cena fica menos que isso na tela


def limpar(fala: str) -> str:
    return re.sub(r'\[[^\]]+\]\s*', '', fala).strip()


def duracao_fala(fala: str, ppm: float) -> float:
    palavras = len(limpar(fala).replace('...', ' ').split())
    return palavras * 60 / ppm + PAUSA_FALA + PAUSA_RETICENCIAS * fala.count('...') + PAUSA_MARCADA * fala.count('[pause]')


def linha_do_tempo(m: dict) -> list[dict]:
    """Para cada cena: duração visível (sem contar o dissolve de saída) e legendas no tempo da cena."""
    ppm, d = m['palavras_por_minuto'], m['dissolve_s']
    cenas = []
    for i, c in enumerate(m['cenas']):
        legendas, t = [], MARGEM
        for fala in c.get('falas', []):
            dur = duracao_fala(fala, ppm)
            if c.get('legenda', True) and m.get('legenda_provisoria'):
                legendas.append((round(t, 3), round(t + dur - PAUSA_FALA * 0.5, 3), limpar(fala)))
            t += dur
        visivel = c.get('segundos') or max(MINIMO, t + MARGEM + c.get('cauda_s', 0))
        ultima = i == len(m['cenas']) - 1
        cenas.append({'cena': c['cena'], 'visivel': round(visivel, 3), 'render': round(visivel + (0 if ultima else d), 3), 'legendas': legendas})
    return cenas


def _renderizar_lote(args):
    porta, tarefas = args
    chrome = render.Chrome(porta=porta)
    feitos = []
    try:
        for html, segundos, saida, legendas, assinatura in tarefas:
            inicio = time.time()
            render.renderizar(chrome, Path(html), segundos, Path(saida), legendas)
            Path(saida).with_suffix('.hash').write_text(assinatura)
            feitos.append(f'{Path(saida).name} ({time.time() - inicio:.0f} s)')
    finally:
        chrome.fechar()
    return feitos


def renderizar_cenas(pasta: Path, cenas: list[dict], paralelo: int) -> list[Path]:
    saidas, pendentes = [], []
    for c in cenas:
        html = pasta / 'cenas' / f'{c["cena"]}.html'
        saida = pasta / 'gravacoes' / f'{c["cena"]}.mp4'
        assinatura = hashlib.sha256((html.read_text() + json.dumps([c['render'], c['legendas']])).encode()).hexdigest()
        marca = saida.with_suffix('.hash')
        if not (saida.exists() and marca.exists() and marca.read_text() == assinatura):
            pendentes.append((str(html), c['render'], str(saida), c['legendas'], assinatura))
        saidas.append(saida)
    if pendentes:
        # cenas mais longas primeiro, distribuídas entre os Chromes
        pendentes.sort(key=lambda p: -p[1])
        lotes = [[] for _ in range(min(paralelo, len(pendentes)))]
        for i, p in enumerate(pendentes):
            lotes[i % len(lotes)].append(p)
        print(f'renderizando {len(pendentes)} cenas ({sum(p[1] for p in pendentes):.0f} s de vídeo) em {len(lotes)} Chromes…', flush=True)
        with ProcessPoolExecutor(len(lotes)) as ex:
            for feitos in ex.map(_renderizar_lote, [(9333 + i, lote) for i, lote in enumerate(lotes)]):
                for f in feitos:
                    print('  ' + f, flush=True)
    return saidas


def montar(pasta: Path, paralelo: int = 4) -> Path:
    m = json.loads((pasta / 'montagem.json').read_text())
    cenas = linha_do_tempo(m)
    total = sum(c['visivel'] for c in cenas)
    print(f'{len(cenas)} cenas, {total:.1f} s ({int(total // 60)} min {total % 60:.0f} s)', flush=True)
    videos = renderizar_cenas(pasta, cenas, paralelo)

    # som: música por código + vento de inverno até o fim da cena indicada
    trabalho = pasta / 'trabalho'
    trabalho.mkdir(exist_ok=True)
    musica = sons.musica(total, seed=m['musica']['seed'], dbfs=m['musica']['dbfs'])
    if m.get('vento'):
        fim, t = 0.0, 0.0
        for c in cenas:
            t += c['visivel']
            if c['cena'] == m['vento']['ate_cena']:
                fim = t
        v = sons.vento(fim + 2, dbfs=m['vento']['dbfs'])
        musica[:len(v)] += v[:len(musica)]
    sons.gravar_wav(trabalho / 'som.wav', musica)

    # vídeo: cadeia de dissolves, entrada e saída pelo preto
    d = m['dissolve_s']
    entradas, filtros, ant, offset = [], [], '0:v', 0.0
    for i, v in enumerate(videos):
        entradas += ['-i', str(v)]
    for i in range(1, len(videos)):
        offset += cenas[i - 1]['visivel']
        filtros.append(f'[{ant}][{i}:v]xfade=transition=fade:duration={d}:offset={offset:.3f}[x{i}]')
        ant = f'x{i}'
    filtros.append(f'[{ant}]fade=t=in:st=0:d=1.2,fade=t=out:st={total - 2.5:.3f}:d=2.5,format=yuv420p[v]')
    n = len(videos)
    filtros.append(f'[{n}:a]afade=t=out:st={total - 3:.3f}:d=3[a]')
    saida = pasta / m['saida']
    saida.parent.mkdir(parents=True, exist_ok=True)
    temp = saida.with_name(f'.{saida.name}.parcial.mp4')
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', *entradas, '-i', str(trabalho / 'som.wav'),
           '-filter_complex', ';'.join(filtros), '-map', '[v]', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-color_range', 'tv', '-r', str(render.FPS),
           '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-t', f'{total:.3f}', str(temp)]
    subprocess.run(cmd, check=True)
    temp.replace(saida)
    (trabalho / 'linha-do-tempo.json').write_text(json.dumps(cenas, ensure_ascii=False, indent=1))
    print(saida)
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pasta', type=Path)
    ap.add_argument('--paralelo', type=int, default=4)
    a = ap.parse_args()
    montar(a.pasta, a.paralelo)


if __name__ == '__main__':
    main()

"""Entrega: juntar blocos com áudio contínuo, simular a compressão do YouTube e comparar imagens."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import audio, config
from .config import FPS, ffmpeg


def duracao_video(arq) -> float:
    out = subprocess.run([ffmpeg(), '-hide_banner', '-i', str(arq)], capture_output=True, text=True).stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([0-9.]+)', out).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def concatenar(videos, saida):
    """Concatena mp4 do mesmo formato sem recomprimir."""
    lista = Path(saida).with_suffix('.txt')
    lista.write_text(''.join(f"file '{Path(v).resolve()}'\n" for v in videos), encoding='utf-8')
    subprocess.run([ffmpeg(), '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(lista), '-c', 'copy', str(saida)], check=True)
    lista.unlink()
    return Path(saida)


def montar(videos, juncoes, saida, dissolve, crf=14, preset='veryfast'):
    """Junta os vídeos com uma transição em cada junção (len(juncoes) == len(videos) - 1):
    'dissolve' (sobrepõe `dissolve` s), 'acende' (o seguinte nasce do escuro em `dissolve` s) ou 'corte'.
    Devolve o início de cada vídeo na montagem (s)."""
    durs = [duracao_video(v) for v in videos]
    entradas, filtros, inicios = [], [], [0.0]
    for i, v in enumerate(videos):
        entradas += ['-i', str(v)]
        f = f'[{i}:v]setpts=PTS-STARTPTS,fps={FPS},settb=AVTB'
        if i and juncoes[i - 1] == 'acende':
            f += f',fade=t=in:st=0:d={dissolve}'
        filtros.append(f + f'[p{i}]')
    atual, fim = '[p0]', durs[0]
    for i in range(1, len(videos)):
        saida_i = f'[m{i}]'
        if juncoes[i - 1] == 'dissolve':
            ini = fim - dissolve
            filtros.append(f'{atual}[p{i}]xfade=transition=fade:duration={dissolve}:offset={ini:.4f}{saida_i}')
        else:
            ini = fim
            filtros.append(f'{atual}[p{i}]concat=n=2:v=1{saida_i}')
        inicios.append(ini)
        atual, fim = saida_i, ini + durs[i]
    subprocess.run([ffmpeg(), '-y', '-v', 'error', *entradas, '-filter_complex', ';'.join(filtros), '-map', atual,
                    '-c:v', 'libx264', '-preset', preset, '-crf', str(crf), '-pix_fmt', 'yuv420p', str(saida)], check=True)
    return inicios, fim


def exportar_4k(entrada, saida, crf=16):
    """Amplia para 3840x2160 (lanczos) — o YouTube dá mais bitrate a vídeos 4K e os degradês sofrem menos."""
    subprocess.run([ffmpeg(), '-y', '-v', 'error', '-i', str(entrada), '-vf', 'scale=3840:2160:flags=lanczos',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-c:a', 'copy',
                    '-movflags', '+faststart', str(saida)], check=True)
    return Path(saida)


def simular_youtube(entrada, saida=None, mbps=4.0):
    """Recomprime como o YouTube faz em 1080p (~4 Mbps) para conferir faixas e blocos nos degradês."""
    entrada = Path(entrada)
    saida = Path(saida or entrada.with_name(entrada.stem + f'-youtube{mbps:g}mbps.mp4'))
    br = f'{mbps:g}M'
    subprocess.run([ffmpeg(), '-y', '-v', 'error', '-i', str(entrada), '-c:v', 'libx264', '-preset', 'medium', '-b:v', br,
                    '-maxrate', br, '-bufsize', f'{2 * mbps:g}M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
                    str(saida)], check=True)
    grafo = '[0:v]split[a][b];[1:v]split[c][d];[a][c]ssim;[b][d]psnr'
    out = subprocess.run([ffmpeg(), '-hide_banner', '-i', str(saida), '-i', str(entrada), '-lavfi', grafo,
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    ssim = re.search(r'SSIM .*All:([0-9.]+)', out)
    psnr = re.search(r'PSNR .*average:([0-9.inf]+)', out)
    return saida, (float(ssim.group(1)) if ssim else None), (psnr.group(1) if psnr else None)


def extrair_quadro(video, t) -> np.ndarray:
    raw = subprocess.run([ffmpeg(), '-v', 'error', '-ss', f'{t:.3f}', '-i', str(video), '-frames:v', '1', '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(config.H, config.W, 3)


def _rotulo(im, texto):
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype(config.fonte('Cinzel-Bold.ttf'), 26)
    except Exception:
        f = None
    d.rectangle([0, 0, 12 + 15 * len(texto), 40], fill=(0, 0, 0))
    d.text((8, 6), texto, fill=(255, 255, 255), font=f)
    return im


def lado_a_lado(a, b, saida, titulo_a='A', titulo_b='B', recorte=None, escala=0.5):
    """Imagem com A e B lado a lado (inteiras reduzidas, ou um recorte ampliado)."""
    ia, ib = Image.fromarray(a), Image.fromarray(b)
    if recorte:
        ia, ib = ia.crop(recorte), ib.crop(recorte)
        escala = 2.0
    w, h = int(ia.width * escala), int(ia.height * escala)
    ia = _rotulo(ia.resize((w, h), Image.LANCZOS if escala < 1 else Image.NEAREST), titulo_a)
    ib = _rotulo(ib.resize((w, h), Image.LANCZOS if escala < 1 else Image.NEAREST), titulo_b)
    s = Image.new('RGB', (2 * w + 8, h), (0, 0, 0))
    s.paste(ia, (0, 0))
    s.paste(ib, (w + 8, 0))
    s.save(saida)
    return Path(saida)


def comparar_imagens(a, b, saida_dif=None):
    """Diferença de pixels entre duas imagens: dict com idêntica, maior diferença, % de pixels diferentes."""
    A = np.asarray(Image.open(a).convert('RGB')).astype(np.int16)
    B = np.asarray(Image.open(b).convert('RGB')).astype(np.int16)
    d = np.abs(A - B).max(-1)
    res = {'identica': bool((d == 0).all()), 'maior': int(d.max()), 'pixels_diferentes_pct': float((d > 0).mean() * 100),
           'media': float(np.abs(A - B).mean())}
    if saida_dif and not res['identica']:
        Image.fromarray(np.clip(d * 16, 0, 255).astype(np.uint8)).save(saida_dif)
    return res


def mixar_video(vozes, duracao, saida_audio, ganho_ambiente_db):
    return audio.mixar(vozes, duracao, saida_audio, ganho_ambiente_db=ganho_ambiente_db)

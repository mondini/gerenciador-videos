"""Render: um quadro, stills de conferência e o bloco inteiro (em paralelo), com o ffmpeg."""
from __future__ import annotations

import multiprocessing as mp
import os
import subprocess
import sys
import time
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

from . import cache, lencol
from .config import FPS, H, W, ffmpeg
from .projeto import Bloco
from .quadro import Quadro


def quadro(bloco: Bloco, t: float) -> np.ndarray:
    """O quadro do instante t (segundos no vídeo do bloco), RGB uint8 (H x W x 3)."""
    q = Quadro(t, t - bloco.entrada, fim=bloco.fim, fade=bloco.fade, acende=bloco.acende, pano=bloco.pano)
    bloco.cena.quadro(q, bloco.deixas)
    return q.finalizar()


def preparar(bloco: Bloco, avisar=print) -> float:
    """Gera (ou lê do cache) o lençol e toda a arte do elenco. Devolve os segundos gastos."""
    t0 = time.time()
    lencol.dados(bloco.pano)
    elenco = bloco.elenco()
    for i, item in enumerate(elenco):
        item.preparar()
    dt = time.time() - t0
    avisar(f'arte e máscaras prontas ({len(elenco)} peças do elenco) em {dt:.1f}s')
    return dt


def stills(bloco: Bloco, tempos, pasta=None, prefixo=None):
    """Salva um PNG por tempo (segundos no vídeo do bloco). Devolve os caminhos."""
    pasta = Path(pasta or bloco.previas / 'stills')
    pasta.mkdir(parents=True, exist_ok=True)
    prefixo = prefixo or f'{bloco.nome}'
    out = []
    for t in tempos:
        p = pasta / f'{prefixo}_{float(t):06.2f}.png'
        Image.fromarray(quadro(bloco, float(t))).save(p)
        out.append(p)
    return out


# ---------------- render paralelo ----------------
_BLOCO = None


def _iniciar_processo(video, numero, caminho_pipeline):
    global _BLOCO
    if caminho_pipeline not in sys.path:
        sys.path.insert(0, caminho_pipeline)
    import cv2
    cv2.setNumThreads(1)                # o paralelismo vem dos processos
    _BLOCO = Bloco(video, numero)
    _BLOCO.cena


def _render_lote(indices):
    return [quadro(_BLOCO, i / FPS).tobytes() for i in indices]


def processos_padrao() -> int:
    return max(1, min(4, (os.cpu_count() or 2) - 1))


def renderizar(bloco: Bloco, saida, de=None, ate=None, processos=None, crf=14, preset='veryfast', avisar=print):
    """Renderiza o bloco (ou o trecho [de, ate) em segundos) num mp4 SEM som. Devolve estatísticas."""
    processos = processos or processos_padrao()
    i0 = int(round((de or 0) * FPS))
    i1 = bloco.n_quadros if ate is None else min(bloco.n_quadros, int(round(ate * FPS)))
    if i1 <= i0:
        raise SystemExit('Trecho vazio.')
    saida = Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    t_prep = preparar(bloco, avisar)
    cmd = [ffmpeg(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'libx264', '-preset', preset, '-crf', str(crf), '-pix_fmt', 'yuv420p', str(saida)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = i1 - i0
    t0 = time.time()
    ultimo_aviso = t0

    def progresso(feitos):
        nonlocal ultimo_aviso
        agora = time.time()
        if agora - ultimo_aviso > 15 or feitos == n:
            ultimo_aviso = agora
            avisar(f'  {feitos}/{n} quadros  ({(agora - t0) / max(feitos, 1) * FPS:.1f} s por segundo de vídeo)')

    if processos <= 1:
        for k, i in enumerate(range(i0, i1)):
            enc.stdin.write(quadro(bloco, i / FPS).tobytes())
            progresso(k + 1)
    else:
        cache.esquecer()                # o processo principal só repassa quadros ao ffmpeg
        lote = 6
        lotes = [list(range(a, min(a + lote, i1))) for a in range(i0, i1, lote)]
        ctx = mp.get_context('spawn')
        pipeline = str(Path(__file__).resolve().parents[1])
        with ProcessPoolExecutor(max_workers=processos, mp_context=ctx, initializer=_iniciar_processo,
                                 initargs=(bloco.video, bloco.numero, pipeline)) as ex:
            fila, prox, feitos = deque(), 0, 0
            while prox < len(lotes) or fila:
                while prox < len(lotes) and len(fila) < processos * 2:      # janela: limita a memória
                    fila.append(ex.submit(_render_lote, lotes[prox]))
                    prox += 1
                for fr in fila.popleft().result():
                    enc.stdin.write(fr)
                    feitos += 1
                progresso(feitos)
    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit(f'O ffmpeg falhou ao gravar {saida.name} (o arquivo pode estar incompleto): renderize de novo.')
    dt = time.time() - t0
    seg = n / FPS
    est = {'quadros': n, 'segundos_video': seg, 'segundos_render': dt, 'preparo': t_prep,
           's_por_segundo': dt / seg, 'processos': processos}
    avisar(f'{saida.name}: {n} quadros ({seg:.1f} s de vídeo) em {dt:.1f} s -> {dt / seg:.2f} s por segundo de vídeo '
           f'({processos} processo(s); preparo {t_prep:.1f} s)')
    return est


def juntar_audio(video_mudo, audio_arq, saida):
    """Junta o vídeo sem som com a trilha (cópia direta, sem recompressão)."""
    subprocess.run([ffmpeg(), '-y', '-v', 'error', '-i', str(video_mudo), '-i', str(audio_arq), '-map', '0:v', '-map', '1:a',
                    '-c', 'copy', '-movflags', '+faststart', '-shortest', str(saida)], check=True)
    return Path(saida)

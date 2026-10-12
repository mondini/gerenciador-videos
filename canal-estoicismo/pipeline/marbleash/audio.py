"""Áudio: pausas da narração, desaceleração, som ambiente e mixagem a -16 LUFS.

A narração do ElevenLabs não tem controle de velocidade (sai a ~155 palavras/min). Na montagem cada
pausa é alongada (+10% da pausa + 0,05 s), sem mudar o andamento da voz, para ficar em ~150 palavras/min.
(Até 12/10/2026 o ritmo era mais lento: andamento 0,92 e pausas +55% + 0,25 s, ~120 palavras/min.)
"""
from __future__ import annotations

import re
import subprocess
import wave
from pathlib import Path

import numpy as np

from .config import ffmpeg

SR = 44100

# Parâmetros aprovados do ritmo (vídeo 1). Ficam gravados no audio.json de cada bloco.
RITMO = {'tempo': 1.0, 'alonga': 0.10, 'acrescimo': 0.05, 'ruido_db': -38, 'pausa_min': 0.3}


def decodificar(caminho, sr=SR) -> np.ndarray:
    """Áudio mono em float32 (escala de int16)."""
    raw = subprocess.run([ffmpeg(), '-v', 'error', '-i', str(caminho), '-f', 's16le', '-ac', '1', '-ar', str(sr), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)


def tempo_padrao(v, sr) -> float:
    """Tempo impresso pelo ffmpeg -> amostra exata -> formato do ffmpeg antigo (6 algarismos significativos)."""
    return float('%.6g' % ((1 / sr) * round(float(v) * sr)))


def pausas(caminho, ruido_db=RITMO['ruido_db'], pausa_min=RITMO['pausa_min'], duracao=None):
    """Pausas [(início, fim)] em segundos, detectadas pelo silencedetect do ffmpeg.

    Ignora o silêncio do começo e do fim do arquivo (como na versão aprovada).

    O ffmpeg 7 imprime os tempos com 6 casas decimais; versões anteriores (a da versão aprovada)
    imprimiam 6 algarismos significativos. Para o resultado não depender da versão, cada tempo é
    alinhado à amostra de áudio e reescrito no formato antigo.
    """
    out = subprocess.run([ffmpeg(), '-hide_banner', '-i', str(caminho), '-af', f'silencedetect=noise={ruido_db}dB:d={pausa_min}',
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    sr = int(re.search(r'Audio: .*?(\d+) Hz', out).group(1))
    st = [tempo_padrao(x, sr) for x in re.findall(r'silence_start: ([0-9.]+)', out)]
    en = [tempo_padrao(x, sr) for x in re.findall(r'silence_end: ([0-9.]+)', out)]
    if duracao is None:
        duracao = len(decodificar(caminho)) / SR
    return [(s, e) for s, e in zip(st, en) if s > 0.05 and e < duracao - 0.05]


def inseridos(pausas_, alonga=RITMO['alonga'], acrescimo=RITMO['acrescimo']):
    """Silêncio acrescentado em cada pausa: [(meio da pausa, total acrescentado até ali)]."""
    acc, out = 0.0, []
    for s, e in pausas_:
        extra = alonga * (e - s) + acrescimo
        acc += extra
        out.append(((s + e) / 2, acc))
    return out


def ler_wav(caminho):
    with wave.open(str(caminho), 'rb') as w:
        n, sr, ch = w.getnframes(), w.getframerate(), w.getnchannels()
        dados = np.frombuffer(w.readframes(n), np.int16).reshape(-1, ch)
    return dados, sr


def gravar_wav(caminho, dados, sr=SR):
    dados = np.asarray(dados)
    ch = 1 if dados.ndim == 1 else dados.shape[1]
    with wave.open(str(caminho), 'wb') as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(np.clip(dados, -32768, 32767).astype(np.int16).tobytes())


def duracao_wav(caminho) -> float:
    with wave.open(str(caminho), 'rb') as w:
        return w.getnframes() / w.getframerate()


def desacelerar(origem, pausas_, saida, tempo=RITMO['tempo'], alonga=RITMO['alonga'], acrescimo=RITMO['acrescimo']) -> float:
    """Grava `saida` (wav) com as pausas alongadas e o andamento ajustado (tempo < 1 desacelera). Devolve a duração em segundos."""
    x = decodificar(origem)
    pieces, cur = [], 0
    for s, e in pausas_:
        mid = int((s + e) / 2 * SR)
        extra = alonga * (e - s) + acrescimo
        pieces.append(x[cur:mid])
        pieces.append(np.zeros(int(extra * SR), np.float32))
        cur = mid
    pieces.append(x[cur:])
    saida = Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    pad = saida.with_name(saida.stem + '-pausas.wav')
    gravar_wav(pad, np.concatenate(pieces))
    subprocess.run([ffmpeg(), '-y', '-v', 'error', '-i', str(pad), '-af', f'atempo={tempo}', str(saida)], check=True)
    pad.unlink()
    return round(duracao_wav(saida), 6)        # 6 casas, como o ffprobe media na versão aprovada


# O vento sai do gerador a ~-15,7 LUFS; o ganho em dB da mistura (GANHO_AMBIENTE_DB em ma.py) foi pensado para o
# ambiente antigo, a -12,3 LUFS. Esta diferença (medida em 40, 80 e 110 s) é somada na mistura, sem estourar o wav.
AJUSTE_AMBIENTE_DB = 3.4


def _suave(x, seg):
    """Média móvel de `seg` segundos (suaviza as rajadas)."""
    from scipy.signal import fftconvolve
    n = int(SR * seg)
    return fftconvolve(x, np.ones(n) / n, mode='same')


def _ruido_filtrado(semente, n, forma):
    """Ruído branco com o espectro moldado por `forma(f)` (amplitude), normalizado."""
    f = np.fft.rfftfreq(n, 1 / SR)
    x = np.fft.irfft(np.fft.rfft(np.random.default_rng(semente).standard_normal(n)) * forma(f), n)
    return x / (np.std(x) + 1e-12)


def _vento(n, semente):
    """Vento suave: ruído em faixa média cujo timbre vai e volta devagar, com rajadas leves. Sem tons."""
    t = np.arange(n) / SR
    rng = np.random.default_rng(70 + semente)
    sobe = lambda f: 1 / np.sqrt(1 + (60 / np.maximum(f, 1)) ** 4)                      # corta o grave (sem zumbido)
    a = _ruido_filtrado(4 + semente, n, lambda f: sobe(f) / np.sqrt(1 + ((f - 350) / 220) ** 2))
    b = _ruido_filtrado(5 + semente, n, lambda f: sobe(f) / np.sqrt(1 + ((f - 800) / 380) ** 2))
    centro = 450 + 250 * np.sin(2 * np.pi * 0.021 * t + semente) + 120 * np.sin(2 * np.pi * 0.057 * t + 2 * semente)
    mix = np.clip((centro - 300) / 500, 0, 1)
    rajada = _suave(0.6 + 0.4 * np.clip(np.sin(2 * np.pi * 0.07 * t + rng.uniform(0, 6)) + 0.3 * np.sin(2 * np.pi * 0.19 * t), -1, 1), 0.8)
    return (a * (1 - mix) + b * mix) * rajada


def ambiente(duracao, saida, semente=0):
    """Som ambiente original (sem amostras de terceiros): vento suave, estéreo, sem tons (escolha do criador
    em 12/10/2026; o acorde grave anterior soava como um motor zumbindo)."""
    n = int(SR * duracao)
    t = np.arange(n) / SR
    sig = np.stack([_vento(n, semente), _vento(n, semente + 100)], 1)
    sig /= np.max(np.abs(sig))
    sig *= (np.minimum(1, np.minimum(t / 3.0, (duracao - t) / 3.0)) * 0.9)[:, None]
    gravar_wav(saida, np.clip(sig, -1, 1) * 32767)


def mixar(vozes, duracao, saida, ganho_ambiente_db=-20.0, lufs=-16.0):
    """Mixa narração + ambiente e normaliza para `lufs` (EBU R128, dois passos).

    vozes: [(wav, atraso em s)]; duracao: total em s; saida: .wav ou .m4a/.aac.
    """
    saida = Path(saida)
    amb = saida.with_name(saida.stem + '-ambiente.wav')
    ambiente(duracao, amb)
    entradas, filtros, rotulos = [], [], []
    for i, (wav, atraso) in enumerate(vozes):
        entradas += ['-i', str(wav)]
        ms = int(round(atraso * 1000))
        filtros.append(f'[{i}:a]aresample={SR},aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]')
        rotulos.append(f'[v{i}]')
    entradas += ['-i', str(amb)]
    na = len(vozes)
    filtros.append(f'[{na}:a]volume={ganho_ambiente_db + AJUSTE_AMBIENTE_DB}dB[amb]')
    if na:
        filtros.append(''.join(rotulos) + f'[amb]amix=inputs={na + 1}:duration=longest:normalize=0,atrim=0:{duracao:.3f}[mix]')
    else:
        filtros.append(f'[amb]atrim=0:{duracao:.3f}[mix]')
    grafo = ';'.join(filtros)
    # 1º passo: medir a loudness da mistura
    medida = subprocess.run([ffmpeg(), '-hide_banner', '-nostats', *entradas, '-filter_complex',
                             grafo + f';[mix]loudnorm=I={lufs}:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                            capture_output=True, text=True).stderr
    m = {k: re.search(rf'"{k}"\s*:\s*"([-0-9.inf]+)"', medida).group(1)
         for k in ('input_i', 'input_tp', 'input_lra', 'input_thresh', 'target_offset')}
    # 2º passo: normalização linear com os valores medidos
    ln = (f'loudnorm=I={lufs}:TP=-1.5:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:'
          f'measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')
    codec = ['-c:a', 'pcm_s16le'] if saida.suffix == '.wav' else ['-c:a', 'aac', '-b:a', '192k']
    subprocess.run([ffmpeg(), '-y', '-v', 'error', *entradas, '-filter_complex', grafo + f';[mix]{ln},aresample=48000[out]',
                    '-map', '[out]', *codec, str(saida)], check=True)
    amb.unlink()
    return saida


def loudness(caminho) -> float:
    """Loudness integrada (LUFS) de um arquivo de áudio ou vídeo."""
    out = subprocess.run([ffmpeg(), '-hide_banner', '-nostats', '-i', str(caminho), '-af', 'ebur128', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[0-9.]+) LUFS', out)[-1])

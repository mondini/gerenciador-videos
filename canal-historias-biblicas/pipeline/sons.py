"""Sons gerados por código (pedido do criador): ambiências e efeitos sem licença de terceiros.

Uso (na pasta do canal):
  .venv/bin/python -m pipeline.sons vento SEGUNDOS destino.wav
  .venv/bin/python -m pipeline.sons musica SEGUNDOS destino.wav
"""
from __future__ import annotations

import argparse
import wave

import numpy as np


def vento(dur: float, seed: int = 3, sr: int = 48000, dbfs: float = -24.0) -> np.ndarray:
    """Vento de inverno: ruído filtrado (chiado grave, sem ronco) com rajadas lentas, estéreo."""
    rng = np.random.default_rng(seed)
    n = int(dur * sr)
    f = np.fft.rfftfreq(n, 1 / sr)
    filtro = 1 / np.sqrt(1 + (f / 180.0) ** 2) * np.clip(f / 40.0, 0, 1)
    t = np.arange(n) / sr
    canais = []
    for c in range(2):
        y = np.fft.irfft(np.fft.rfft(rng.normal(0, 1, n)) * filtro, n)
        rajada = 0.55 + 0.45 * np.sin(2 * np.pi * (t / 6.5 + c * 0.13)) * np.sin(2 * np.pi * t / 11.0 + 1.0)
        canais.append(y * rajada)
    est = np.stack(canais, 1)
    est *= 10 ** (dbfs / 20) / (np.sqrt(np.mean(est ** 2)) + 1e-9)
    entra = np.clip(np.arange(n) / (1.5 * sr), 0, 1)
    sai = np.clip((n - np.arange(n)) / (2.0 * sr), 0, 1)
    return est * (entra * sai)[:, None]


ACORDES = [  # ré maior em cadência lenta: D, G, Bm, A (frequências em Hz, voz média)
    (146.83, 220.00, 293.66, 369.99),
    (146.83, 196.00, 246.94, 293.66),
    (123.47, 185.00, 246.94, 293.66),
    (110.00, 164.81, 220.00, 277.18),
]
SINOS = [587.33, 659.25, 739.99, 880.00, 987.77]  # pentatônica de ré, oitava acima


def musica(dur: float, seed: int = 5, sr: int = 48000, acorde_s: float = 9.0, dbfs: float = -22.0) -> np.ndarray:
    """Pad sacro e calmo: acordes sustentados que se cruzam devagar, nota grave de ré e sinos suaves espaçados."""
    rng = np.random.default_rng(seed)
    n = int(dur * sr)
    t = np.arange(n) / sr
    est = np.zeros((n, 2))
    # acordes: cada um entra e sai em rampas de cosseno, sobrepostos pela metade da rampa
    rampa = acorde_s * 0.45
    k = 0
    inicio = -rampa
    while inicio < dur:
        notas = ACORDES[k % len(ACORDES)]
        a, b = max(0, int(inicio * sr)), min(n, int((inicio + acorde_s + rampa) * sr))
        tt = t[a:b] - inicio
        env = np.clip(np.minimum(tt / rampa, (acorde_s + rampa - tt) / rampa), 0, 1)
        env = 0.5 - 0.5 * np.cos(np.pi * env)
        for i, f in enumerate(notas):
            for c, desv in enumerate((-0.12, 0.12)):  # leve coro entre esquerda e direita
                fase = rng.uniform(0, 2 * np.pi)
                onda = np.sin(2 * np.pi * (f + desv) * tt + fase) + 0.18 * np.sin(4 * np.pi * (f + desv) * tt + fase)
                est[a:b, c] += env * onda * (0.9 if i == 0 else 0.6)
        k += 1
        inicio += acorde_s
    # nota grave de ré, contínua
    est += (0.55 * np.sin(2 * np.pi * 73.42 * t))[:, None]
    # sinos: decaimento longo, volume baixo, a cada 5–9 s
    s = 3.0
    while s < dur - 4:
        f = rng.choice(SINOS)
        a = int(s * sr)
        b = min(n, a + int(5 * sr))
        tt = t[a:b] - s
        sino = np.exp(-tt / 1.4) * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt / 0.4))
        pan = rng.uniform(0.3, 0.7)
        est[a:b, 0] += 0.5 * sino * (1 - pan)
        est[a:b, 1] += 0.5 * sino * pan
        s += rng.uniform(5, 9)
    # tira o brilho: passa-baixa suave pelo espectro
    for c in range(2):
        espec = np.fft.rfft(est[:, c])
        f = np.fft.rfftfreq(n, 1 / sr)
        est[:, c] = np.fft.irfft(espec / np.sqrt(1 + (f / 2400.0) ** 4), n)
    est *= 10 ** (dbfs / 20) / (np.sqrt(np.mean(est ** 2)) + 1e-9)
    entra = np.clip(t / 3.0, 0, 1)
    sai = np.clip((dur - t) / 4.0, 0, 1)
    return est * (entra * sai)[:, None]


def gravar_wav(caminho, est: np.ndarray, sr: int = 48000) -> None:
    pcm = (np.clip(est, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(caminho), 'wb') as f:
        f.setnchannels(est.shape[1])
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('som', choices=['vento', 'musica'])
    ap.add_argument('segundos', type=float)
    ap.add_argument('destino')
    a = ap.parse_args()
    gravar_wav(a.destino, {'vento': vento, 'musica': musica}[a.som](a.segundos))
    print(a.destino)


if __name__ == '__main__':
    main()

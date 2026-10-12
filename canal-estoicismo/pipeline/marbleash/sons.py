"""Sons de transição (sem amostras de terceiros): sintetizados por código, como o vento do ambiente.

Cada som tem o "golpe" em GOLPE segundos do arquivo. Uma peça sem narração declara no script de cena
`SOM = '<nome>'` e `SOM_GOLPE = <segundo da peça>`; a montagem começa o arquivo antes da peça para o golpe
cair nesse segundo (a subida entra no escurecimento do bloco anterior, a cauda no começo do seguinte).
"""
from __future__ import annotations

import numpy as np

from .audio import SR, gravar_wav, loudness

GOLPE = 1.0          # segundo do golpe dentro do arquivo
DURACAO = 5.0        # subida (1 s) + golpe + cauda
ALVO_LUFS = -28.0    # loudness do arquivo: ~4 dB abaixo da narração bruta do ElevenLabs (~-24 LUFS)
PICO_DB = -3.0       # teto de pico
GANHO_DB = 0.0       # ajuste fino na mistura (a narração entra sem ganho)


def _t(n=None):
    return np.arange(n or int(SR * DURACAO)) / SR


def _env(t, ataque, queda, inicio=GOLPE):
    """Envoltória: sobe em `ataque` s até o golpe, cai exponencialmente (constante `queda` s)."""
    e = np.where(t < inicio, 0.0, np.exp(-(t - inicio) / queda))
    if ataque:
        sub = np.clip((t - (inicio - ataque)) / ataque, 0, 1)
        e = np.where(t < inicio, sub ** 2, e)
    return e


def _ruido(semente, n, forma):
    f = np.fft.rfftfreq(n, 1 / SR)
    x = np.fft.irfft(np.fft.rfft(np.random.default_rng(semente).standard_normal(n)) * forma(f), n)
    return x / (np.std(x) + 1e-12)


def _passa_banda(x, centro, largura):
    """Filtro passa-banda que varia no tempo (centro em Hz por amostra), em janelas curtas."""
    out = np.zeros_like(x)
    janela = 2048
    passo = janela // 4
    w = np.hanning(janela)
    f = np.fft.rfftfreq(janela, 1 / SR)
    for i in range(0, len(x) - janela, passo):
        c = centro[i + janela // 2]
        g = 1 / np.sqrt(1 + ((f - c) / largura) ** 2)
        out[i:i + janela] += np.fft.irfft(np.fft.rfft(x[i:i + janela] * w) * g, janela) * w
    return out / 1.5


def _sala(sinal, segundos, semente, brilho=3000):
    """Reverberação sintética: resposta de ruído com queda exponencial, estéreo descorrelacionado."""
    from scipy.signal import fftconvolve
    n = int(SR * segundos)
    t = _t(n)
    canais = []
    for k in range(2):
        ir = _ruido(semente + k, n, lambda f: 1 / np.sqrt(1 + (f / brilho) ** 2)) * np.exp(-t / (segundos / 6.9))
        ir[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
        canais.append(fftconvolve(sinal, ir)[:len(sinal)] / np.sqrt(n))
    return np.stack(canais, 1)


def _tom(t, freqs, quedas, amps, inicio=GOLPE, desafina=0.0):
    x = np.zeros_like(t)
    for f, q, a in zip(freqs, quedas, amps):
        x += a * np.sin(2 * np.pi * f * (1 + desafina * np.sin(2 * np.pi * 0.7 * t)) * t) * _env(t, 0.004, q, inicio)
    return x


def brasa(t):
    """1 · Brasa: um sopro sobe (como quem acende a lanterna), golpe grave e macio, faíscas na cauda."""
    n = len(t)
    sopro = _passa_banda(_ruido(11, n, lambda f: 1 / np.sqrt(1 + (f / 4000) ** 2)), 300 + 1500 * np.clip(t / GOLPE, 0, 1) ** 2, 350)
    sopro *= _env(t, 0.9, 0.12)
    queda = 70 + 40 * np.exp(-np.maximum(t - GOLPE, 0) / 0.05)
    grave = np.sin(2 * np.pi * np.cumsum(queda) / SR) * _env(t, 0.006, 0.45)
    rng = np.random.default_rng(12)
    faiscas = np.zeros(n)
    for s in rng.uniform(GOLPE + 0.05, GOLPE + 1.6, 26):
        i = int(s * SR)
        faiscas[i:i + 40] += rng.uniform(0.2, 1) * np.exp(-np.arange(40) / 6) * rng.choice([-1, 1])
    faiscas = _passa_banda(faiscas, np.full(n, 3500.0), 1500) * np.exp(-np.maximum(t - GOLPE, 0) / 0.8)
    seco = 0.55 * sopro + 1.0 * grave + 2.2 * faiscas
    return 0.8 * np.stack([seco, seco], 1) + 0.6 * _sala(seco, 2.2, 13)


def pedra(t):
    """2 · Tigela de pedra: um toque grave com parciais inarmônicos, longa ressonância."""
    f0 = 146.8      # ré grave
    razoes = [1, 2.71, 5.12, 8.25]
    x = _tom(t, [f0 * r for r in razoes], [1.5, 0.9, 0.5, 0.25], [1, 0.45, 0.22, 0.1], desafina=0.0015)
    toque = _ruido(21, len(t), lambda f: 1 / np.sqrt(1 + (f / 1500) ** 2)) * _env(t, 0, 0.012) * 0.25
    seco = x + toque
    return 0.85 * np.stack([seco, seco * 0.97], 1) + 0.45 * _sala(seco, 2.2, 22, brilho=2000)


def tambor(t):
    """3 · Tambor grave: um golpe de pele, corpo que desce de tom, sala grande."""
    queda = 52 + 38 * np.exp(-np.maximum(t - GOLPE, 0) / 0.08)
    corpo = np.sin(2 * np.pi * np.cumsum(queda) / SR) * _env(t, 0.003, 0.6)
    pele = _ruido(31, len(t), lambda f: 1 / np.sqrt(1 + ((f - 180) / 140) ** 2)) * _env(t, 0, 0.07)
    sopro = _ruido(32, len(t), lambda f: 1 / np.sqrt(1 + ((f - 500) / 400) ** 2)) * _env(t, 0.7, 0.05) * 0.18
    seco = corpo + 0.5 * pele + sopro
    return 0.8 * np.stack([seco, seco], 1) + 0.7 * _sala(seco, 2.8, 33, brilho=1200)


def vento_sino(t):
    """4 · Vento e sino: uma rajada sobe e se resolve num sino pequeno e distante."""
    n = len(t)
    centro = 250 + 2200 * np.clip(t / GOLPE, 0, 1) ** 2.5
    rajada = _passa_banda(_ruido(41, n, lambda f: 1.0 + 0 * f), centro, 300) * _env(t, 0.95, 0.18)
    f0 = 784.0      # sol agudo
    sino = _tom(t, [f0 * r for r in (0.5, 1, 1.19, 1.56, 2.0, 2.74)], [2.2, 1.6, 1.0, 0.8, 0.6, 0.35],
                [0.35, 1, 0.5, 0.35, 0.25, 0.15]) * 0.5
    seco = 0.6 * rajada + sino
    return 0.7 * np.stack([seco, seco], 1) + 0.7 * _sala(seco, 3.2, 43, brilho=5000)


def aurora(t):
    """5 · Aurora: um acorde aberto (quintas) que floresce quando o sol acende, sobre um grave suave."""
    notas = [55.0, 110.0, 164.8, 220.0, 329.6]          # lá e mi: quintas abertas, sem terça
    amps = [0.7, 0.6, 0.45, 0.35, 0.2]
    flor = np.clip((t - (GOLPE - 0.6)) / 0.9, 0, 1) ** 2 * np.exp(-np.maximum(t - (GOLPE + 0.3), 0) / 0.6)
    x = np.zeros_like(t)
    for k, (f, a) in enumerate(zip(notas, amps)):
        for d in (-0.6, 0.6):          # dois osciladores levemente desafinados: brilho sem zumbido
            x += a * (np.sin(2 * np.pi * (f + d * (k + 1) / 3) * t) + 0.2 * np.sin(4 * np.pi * (f + d) * t))
    x *= flor / 2
    sub = np.sin(2 * np.pi * 48 * t) * _env(t, 0.01, 0.5) * 0.6
    seco = x + sub
    return 0.75 * np.stack([seco, seco], 1) + 0.55 * _sala(seco, 2.6, 53, brilho=3500)


SONS = {'brasa': brasa, 'pedra': pedra, 'tambor': tambor, 'vento-sino': vento_sino, 'aurora': aurora}


def gerar(nome, saida):
    """Grava o som `nome` em wav estéreo, nivelado em ALVO_LUFS (pico até PICO_DB), com um fim suave."""
    t = _t()
    sig = SONS[nome](t)
    sig *= np.minimum(1, (DURACAO - t) / 0.6)[:, None]
    sig *= 0.5 / (np.max(np.abs(sig)) + 1e-12)
    gravar_wav(saida, sig * 32767)
    sig *= 10 ** ((ALVO_LUFS - loudness(saida)) / 20)
    sig *= min(1.0, 10 ** (PICO_DB / 20) / (np.max(np.abs(sig)) + 1e-12))
    gravar_wav(saida, np.clip(sig, -1, 1) * 32767)
    return saida

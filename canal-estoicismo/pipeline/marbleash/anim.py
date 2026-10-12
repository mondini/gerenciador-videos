"""Curvas de animação e o balanço das peças nas varetas.

Todas as funções recebem o tempo `t` em segundos. As fórmulas são as do bloco 1 aprovado; mudar a
ordem das contas muda o último bit dos números e, às vezes, um pixel do vídeo.
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np


def ss(t: float, t0: float, d: float) -> float:
    """Subida suave de 0 a 1 que começa em t0 e dura d segundos (smoothstep)."""
    if d <= 0:
        return 1.0 if t >= t0 else 0.0
    x = min(max((t - t0) / d, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def env(t: float, a: float, ai: float, b: float, bo: float) -> float:
    """Envelope: sobe em `a` (duração ai) e desce em `b` (duração bo)."""
    return ss(t, a, ai) * (1 - ss(t, b, bo))


def lin(t: float, t0: float, d: float) -> float:
    """Rampa linear de 0 a 1 entre t0 e t0 + d."""
    return min(max((t - t0) / d, 0.0), 1.0) if d > 0 else float(t >= t0)


def lerp(a, b, f):
    """Interpolação linear entre a e b."""
    return a + (b - a) * f


@lru_cache(maxsize=None)
def _wob_params(seed: int):
    r = np.random.default_rng(seed)
    return r.uniform(0, 6.3, 3), r.uniform(0.6, 1.1, 3)


def wob(t: float, seed: int, amp: float = 2.5, ramp: float = 0.35):
    """Balanço de uma peça segurada à mão na vareta: (dx, dy, rotação em graus).

    Cada semente dá um balanço independente; `amp` é a amplitude em pixels, `ramp` em graus.
    """
    p, f = _wob_params(seed)
    return (amp * math.sin(t * f[0] + p[0]) + 0.6 * amp * math.sin(t * 2.3 * f[0] + p[1]),
            0.7 * amp * math.sin(t * f[1] + p[2]), ramp * math.sin(t * f[2] * 0.8 + p[0]))


def tremor(t: float) -> float:
    """Tremulação leve da luz da lanterna atrás do lençol (fator perto de 1)."""
    return 1 + 0.012 * math.sin(t * 7.3) * math.sin(t * 3.1)

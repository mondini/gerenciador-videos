"""O lençol iluminado por trás: tudo o que não muda de um quadro para outro.

- dobras irradiando dos cantos de cima (sombreado e deformação das sombras);
- luz de lanterna: centro quente, bordas escuras (vinheta);
- pano amontoado e escuro na base, com borda iluminada;
- bokeh, poeirinhas e grão fotográfico FIXO;
- grade sépia (preto quente -> marrom -> bege -> creme);
- disco de lua, chamas coloridas, foco de luz e zoom.

As sementes aleatórias e a ordem dos sorteios são as da versão aprovada.
"""
from __future__ import annotations

import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

from .cache import em_disco
from .config import H, W
from .traco import comp

LUTN = 2048          # degraus da tabela de cor (luz 0..1.3 -> sépia)


def _malha():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return yy, xx


def _dobras(xx, yy, g):
    f = np.zeros((H, W), np.float32)
    for (px, py, sgn) in ((-60, -40, 1), (W + 60, -40, -1)):
        dx, dy = xx - px, yy - py
        r = np.sqrt(dx * dx + dy * dy) + 1
        th = np.arctan2(dy, dx * sgn)
        env = np.exp(-r / 900.0) * np.clip(r / 120, 0, 1)
        f += env * (np.cos(th * 38) * 0.6 + np.cos(th * 17 + 1.3) * 0.4)
    sag = np.cos((xx - W / 2) / W * math.pi) * np.exp(-yy / 260.0)
    f += 0.5 * np.sin(yy / 40.0 + xx / 300.0) * sag
    big = ndimage.gaussian_filter(g.standard_normal((H // 8, W // 8)).astype(np.float32), 6)
    big = np.asarray(Image.fromarray(big).resize((W, H), Image.BICUBIC))
    f += big * 6
    return ndimage.gaussian_filter(f, 3)


def _pano(xx, yy, g, top, vign):
    h = np.zeros((H, W), np.float32)
    for k in range(16):
        c = float(g.uniform(820, 1100))
        amp = float(g.uniform(10, 40))
        per = float(g.uniform(120, 420))
        ph = float(g.uniform(0, 6.3))
        tilt = float(g.uniform(-0.12, 0.12))
        w = float(g.uniform(14, 46))
        A = float(g.uniform(0.6, 1.4))
        x0, x1 = float(g.uniform(-400, 900)), float(g.uniform(1000, 2400))
        span = np.clip((xx - x0) / 200, 0, 1) * np.clip((x1 - xx) / 200, 0, 1)
        cy = c + amp * np.sin(xx / per + ph) + tilt * (xx - W / 2)
        h += A * np.exp(-((yy - cy) / w) ** 2) * span
    h = ndimage.gaussian_filter(h, 2)
    hy, hx = np.gradient(h)
    light = np.clip(0.5 - 9 * hy + 3 * hx, 0, 1.2)             # iluminado de cima e de trás
    depth = np.clip((yy - top[None, :]) / 220, 0, 1)
    lum = (0.20 - 0.16 * depth) * (0.35 + 1.1 * light) * (0.4 + 0.6 * vign)
    edge = np.exp(-np.clip(yy - top[None, :], 0, None) / 7) * 0.20
    a = np.clip((yy - top[None, :] + 5) / 10, 0, 1)
    return lum + edge * a, a


@em_disco
def dados():
    """Luz, dobras, pano, bokeh/poeira, grão e mapas de deformação (calculado uma vez, fica em cache)."""
    yy, xx = _malha()
    g = np.random.default_rng(31)
    F = _dobras(xx, yy, g)
    FN = F / (np.abs(F).max() + 1e-6)
    shade = 1 + 0.22 * FN - 0.10 * np.clip(FN, 0, 1) ** 2
    gy, gx = np.gradient(F)
    DX, DY = gx * 420, gy * 420                    # quanto as dobras entortam as sombras
    hot = np.exp(-(((xx - 900) / 760) ** 2 + ((yy - 430) / 520) ** 2))
    LIGHT = (0.10 + 0.95 * hot) * shade
    vign = np.clip(1 - 0.75 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.72)) ** 2), 0, 1) ** 1.3
    LIGHT *= 0.25 + 0.75 * vign
    top = 850 + 30 * np.sin(xx[0] / 170) + 16 * np.sin(xx[0] / 63 + 1) + 9 * np.sin(xx[0] / 23) + 5 * np.sin(xx[0] / 9)
    CLOTH, CLOTH_A = _pano(xx, yy, g, top, vign)

    # bokeh, poeirinhas e grão fixo (gerador próprio)
    g = np.random.default_rng(31)
    OVER = np.zeros((H, W), np.float32)
    for k in range(14):
        cx, cy, r = float(g.uniform(300, 1600)), float(g.uniform(80, 700)), float(g.uniform(18, 46))
        OVER += 0.035 * np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)) ** 3) * hot
    for k in range(90):
        cx, cy = float(g.uniform(0, W)), float(g.uniform(0, 820))
        x0, x1, y0, y1 = int(max(0, cx - 8)), int(min(W, cx + 8)), int(max(0, cy - 8)), int(min(H, cy + 8))
        OVER[y0:y1, x0:x1] -= 0.05 * np.exp(-((xx[y0:y1, x0:x1] - cx) ** 2 + (yy[y0:y1, x0:x1] - cy) ** 2) / 3.0) * hot[y0:y1, x0:x1]
    GRAIN = cv2.GaussianBlur(g.standard_normal((H, W)).astype(np.float32), (0, 0), 0.7) * 0.022

    CLOTH, CLOTH_A = CLOTH.astype(np.float32), CLOTH_A.astype(np.float32)
    linhas = np.nonzero(CLOTH_A.any(1))[0]
    y_pano = int(linhas.min()) if len(linhas) else H
    return {
        'LIGHT': LIGHT.astype(np.float32),
        'MAPX': (xx + DX).astype(np.float32), 'MAPY': (yy + DY).astype(np.float32),
        'DMAX': float(max(np.abs(DX).max(), np.abs(DY).max())),
        'hot': hot, 'vign': vign,
        'Y_PANO': y_pano,                                           # primeira linha com pano
        'PANO': CLOTH[y_pano:], 'PANO_A': CLOTH_A[y_pano:], 'PANO_1MA': (1 - CLOTH_A)[y_pano:],
        'OVER': OVER, 'GRAIN': GRAIN,
    }


@lru_cache(maxsize=None)
def grade():
    """Tabela da grade sépia: índice (luz * (LUTN-1) / 1.3) -> cor. Devolve (LUT uint8, LUT float 0..1)."""
    stops = np.array([0, 0.15, 0.45, 0.8, 1.05, 1.3])
    cols = np.array([(10, 7, 5), (52, 36, 24), (138, 104, 72), (226, 196, 156), (255, 240, 214), (255, 248, 232)], np.float32)
    lut = np.stack([np.interp(np.linspace(0, 1.3, LUTN), stops, cols[:, k]) for k in range(3)], -1).astype(np.uint8)
    return lut, lut.astype(np.float32) / 255


@em_disco
def lua(cx, cy, r, crescente=0.0):
    """Disco claro projetado: máscara de luz 0..1 com borda de 4 px.

    crescente = 0 dá lua cheia; entre 0 e 1 um segundo disco "corta" a lua (como um recorte de papel)
    e sobra um crescente voltado para a esquerda — quanto maior, mais fino.
    """
    yy, xx = _malha()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    m = np.clip((r - d) / 4 + 0.5, 0, 1).astype(np.float32)
    if crescente > 0:
        d2 = np.sqrt((xx - (cx + r * crescente)) ** 2 + (yy - (cy - r * 0.25 * crescente)) ** 2)
        m *= 1 - np.clip((r * 0.95 - d2) / 4 + 0.5, 0, 1).astype(np.float32)
    ys, xs = np.nonzero(m)
    return m, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


@lru_cache(maxsize=8)
def foco(cx, cy, r, suave=90):
    """Máscara do foco de luz: 0 dentro do círculo de raio r, sobe até 1 numa faixa de `suave` px."""
    yy, xx = _malha()
    dd = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    m = np.clip((dd - r) / suave, 0, 1)
    m = m * m * (3 - 2 * m)
    return m, 1 - m


@em_disco
def chama_rgba(arte, *args):
    """Chama colorida: (cor RGB do quadro inteiro, máscara 0/1). `arte` desenha o sprite da chama."""
    sp = arte(*args)
    fr = np.zeros((H, W, 3), np.float32)
    comp(fr, sp)
    a = (fr.mean(-1) > 0.02).astype(np.float32)
    ys, xs = np.nonzero(a)
    if len(ys) == 0:                     # chama vazia (ex.: rachadura ainda sem traço)
        return fr, a, None
    return fr, a, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def camera(img, cx, cy, z):
    """Zoom da câmera z vezes em torno de (cx, cy)."""
    if z <= 1.001:
        return img
    M = np.array([[z, 0, cx - z * cx], [0, z, cy - z * cy]], np.float32)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)

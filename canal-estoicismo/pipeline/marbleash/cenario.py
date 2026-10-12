"""Cenário romano em camadas de profundidade: fundo distante, meio e as laterais da tela.

Cada função desenha numa folha do tamanho do quadro (recebe o `d` do PIL) ou devolve o sprite pronto.
O desfoque de cada camada (distância do lençol) é decidido no script de cena, via `quadro.Camada`.
"""
from __future__ import annotations

import math

import numpy as np

from .config import H, W
from .traco import (BASE, HOLE, INK, NullDraw, ell, flower, ivy, layer, poly, serrated, shape, spiral, stroke,
                    toward, tuft)


# ---------------- FUNDO DISTANTE: colinas, aqueduto de dois andares, templo no morro, ciprestes ----------------
def _longe(d):
    hill = [(x, 640 - 70 * math.sin(x / 380 + 0.6) - 30 * math.sin(x / 140)) for x in range(-20, W + 21, 12)]
    poly(d, hill + [(W + 20, H), (-20, H)])
    # templo no alto do morro
    tx, ty = 520, 600 - 70 * math.sin(520 / 380 + 0.6) - 30 * math.sin(520 / 140)
    poly(d, [(tx - 70, ty), (tx + 70, ty), (tx + 70, ty - 10), (tx - 70, ty - 10)])
    for k in range(6):
        poly(d, [(tx - 60 + k * 23, ty - 10), (tx - 54 + k * 23, ty - 10), (tx - 54 + k * 23, ty - 62), (tx - 60 + k * 23, ty - 62)])
    poly(d, [(tx - 78, ty - 62), (tx + 78, ty - 62), (tx + 78, ty - 74), (tx - 78, ty - 74)])
    poly(d, [(tx - 82, ty - 74), (tx, ty - 104), (tx + 82, ty - 74)])
    # aqueduto: dois andares de arcos, diminuindo à medida que se afasta para a direita
    x = 760.0
    sc = 1.0
    while x < 1760:
        w = 86 * sc
        top = 690 - 200 * sc
        mid_ = 690 - 150 * sc
        poly(d, [(x, top), (x + w, top), (x + w, 692), (x, 692)])
        r = w * 0.34
        cx = x + w / 2
        ell(d, cx, mid_ + 20 * sc + r, r, r, HOLE)
        poly(d, [(cx - r, mid_ + 20 * sc + r), (cx + r, mid_ + 20 * sc + r), (cx + r, 694), (cx - r, 694)], HOLE)
        for j in (-1, 1):
            ex = cx + j * w * 0.24
            rr = w * 0.12
            ell(d, ex, top + 16 * sc + rr, rr, rr, HOLE)
            poly(d, [(ex - rr, top + 16 * sc + rr), (ex + rr, top + 16 * sc + rr), (ex + rr, top + 36 * sc + rr), (ex - rr, top + 36 * sc + rr)], HOLE)
        poly(d, [(x - 2, top - 6 * sc), (x + w + 2, top - 6 * sc), (x + w + 2, top), (x - 2, top)])
        x += w
        sc *= 0.965
    # fileiras de ciprestes
    for k, x in enumerate((180, 230, 300, 1240, 1290, 1600, 1660)):
        yb = 650 - 70 * math.sin(x / 380 + 0.6) - 30 * math.sin(x / 140) + 10
        h = 120 + (k % 3) * 30
        shape(d, [(x, yb), (x - 16, yb - h * 0.3), (x - 10, yb - h * 0.75), (x, yb - h), (x + 10, yb - h * 0.75), (x + 16, yb - h * 0.3)], n=8)
    # pinheiros-mansos ao longe
    for x, y, r in ((1020, 560, 70), (1420, 590, 60)):
        stroke(d, [(x, y + 80), (x + 6, y + 30), (x + 2, y)], 8, 4)
        for j in range(5):
            ell(d, x - r + j * r * 0.5, y - 6 + 8 * math.sin(j * 1.9), r * 0.42, r * 0.22)


def longe():
    """Fundo distante (colinas, aqueduto, templo no morro, ciprestes), já levemente desfocado em 2x."""
    return layer(_longe, blur=1.3)


# ---------------- MEIO: chão, muro com balaústres fugindo para o ponto de fuga, ciprestes ----------------
def _meio(d):
    ground = [(x, 790 - 20 * math.sin(x / 300)) for x in range(-20, W + 21, 12)]
    poly(d, ground + [(W + 20, H), (-20, H)])
    a, b = (120, 740), (120, 820)
    poly(d, [a, toward(a, 0.42), toward(b, 0.42), b])
    for k in range(18):
        f = 0.02 + k * 0.022
        p, q = toward(a, f), toward(b, f)
        w = (toward(a, f + 0.01)[0] - p[0]) * 0.8
        h = q[1] - p[1]
        shape(d, [(p[0], p[1] + h * 0.25), (p[0] + w, p[1] + h * 0.25), (p[0] + w * 0.8, p[1] + h * 0.55), (p[0] + w, p[1] + h * 0.85),
                  (p[0], p[1] + h * 0.85), (p[0] + w * 0.2, p[1] + h * 0.55)], HOLE, n=4)
    for x, h in ((1140, 250), (1180, 200), (1216, 230)):
        shape(d, [(x, 790), (x - 26, 790 - h * 0.3), (x - 18, 790 - h * 0.75), (x, 790 - h), (x + 18, 790 - h * 0.75), (x + 26, 790 - h * 0.3)], n=10)
        for k in range(5):
            stroke(d, [(x, 760 - k * h / 6), (x + 10, 748 - k * h / 6)], 2, 0.5, HOLE)


def meio():
    """Plano do meio (chão, muro com balaústres, ciprestes atrás do templo)."""
    return layer(_meio, blur=1.0)


# ---------------- LATERAIS: pinheiro-manso à esquerda, coluna jônica com galho à direita ----------------
def pinheiro(d, g):
    """Pinheiro-manso entrando pela esquerda: tronco retorcido, copa de tufos de agulhas, pinhas, hera."""
    stroke(d, [(-100, BASE + 10), (0, BASE - 130), (56, 640), (70, 500), (150, 360), (250, 250)], 78, 22, n=16)
    for k in range(9):
        y0 = 820 - k * 62
        x0 = 10 + k * 18
        stroke(d, [(x0 - 14, y0), (x0 - 4, y0 - 26), (x0 + 6, y0 - 40)], 2.4, 0.4, HOLE, n=5)
    spiral(d, 52, 600, 12, 1.2, 3, HOLE)
    spiral(d, 98, 470, 8, 1.1, 2.4, HOLE, sign=-1)
    branches = [[(250, 250), (200, 200), (120, 150), (30, 120)], [(250, 250), (300, 190), (360, 140), (430, 110)],
                [(250, 250), (330, 230), (450, 200), (580, 170)], [(200, 200), (170, 140), (150, 90)], [(360, 140), (400, 90), (430, 60)],
                [(450, 200), (520, 150), (600, 120)], [(120, 150), (60, 100), (0, 80)], [(150, 360), (110, 300), (60, 260)], [(200, 300), (300, 285), (430, 262)]]
    for b in branches:
        stroke(d, b, 16, 5, n=8)
    core = [(-60, 120), (-30, 70), (40, 40), (130, 20), (230, 8), (330, 12), (440, 30), (540, 60), (630, 100), (660, 140), (600, 168), (500, 182),
            (400, 196), (300, 204), (200, 200), (100, 196), (0, 180), (-60, 170)]
    shape(d, core, n=8)
    for k in range(30):
        x = float(g.uniform(0, 600))
        y = float(g.uniform(50, 170))
        shape(d, [(x, y), (x + float(g.uniform(8, 20)), y - float(g.uniform(2, 8))), (x + float(g.uniform(12, 26)), y + float(g.uniform(2, 10))),
                  (x + float(g.uniform(2, 10)), y + float(g.uniform(6, 12)))], HOLE, n=4)
    for k in range(70):
        f = k / 70
        i = int(f * (len(core) - 1))
        j = i + 1
        t = f * (len(core) - 1) - i
        x = core[i][0] + (core[j][0] - core[i][0]) * t
        y = core[i][1] + (core[j][1] - core[i][1]) * t
        ang = math.degrees(math.atan2(y - 120, x - 300))
        tuft(d, g, x, y, ang, float(g.uniform(30, 48)), n=11, spread=130)
    for k in range(26):
        x = float(g.uniform(-30, 640))
        y = float(g.uniform(150, 205))
        tuft(d, g, x, y, 90 + float(g.uniform(-30, 30)), float(g.uniform(22, 38)), n=9, spread=110, w=2.6)
    for (x, y) in ((140, 218), (330, 226), (470, 214)):                 # pinhas
        stroke(d, [(x, y - 14), (x, y)], 2, 1.6)
        shape(d, [(x - 9, y), (x - 11, y + 14), (x, y + 26), (x + 11, y + 14), (x + 9, y)], n=6)
        for k in range(3):
            stroke(d, [(x - 8, y + 6 + k * 6), (x + 8, y + 8 + k * 6)], 1.2, 1.2, HOLE, n=3)
    for k in range(5):                                                  # hera pendurada no galho de baixo
        x0 = 120 + k * 78
        y0 = 226 + (k % 2) * 10
        pts = [(x0 + 12 * math.sin(i / 3.4 + k), y0 + i * 9) for i in range(11 + 4 * (k % 3))]
        stroke(d, pts, 3, 1.2, n=6)
        xe, ye = pts[-1]
        spiral(d, xe + 6, ye + 4, 7, 1.2, 1.8, INK)
        for i in range(2, len(pts), 2):
            xx, yy = pts[i]
            ivy(d, xx, yy, 40 if i % 4 else 140, float(g.uniform(22, 32)))


def coluna_galho(d, g):
    """Coluna jônica entrando pela direita, com hera subindo e um galho de folhas serrilhadas e flores."""
    cx = W - 90
    shape(d, [(cx - 64, -30), (W + 30, -30), (W + 30, BASE + 30), (cx - 74, BASE + 30), (cx - 72, BASE - 300), (cx - 66, 200)], n=4)
    for k in range(5):
        x = cx - 46 + k * 22
        stroke(d, [(x, 140), (x + 3, 400), (x + 1, 700), (x, BASE - 40)], 4, 4, HOLE)
    # capitel jônico com óvalos e volutas
    shape(d, [(cx - 124, 66), (W + 30, 66), (W + 30, 118), (cx - 104, 118)], n=4)
    for k in range(6):
        ell(d, cx - 70 + k * 22, 108, 6, 8, HOLE)
        ell(d, cx - 70 + k * 22, 108, 3, 5)
    for k in range(2):
        ell(d, cx - 106 + k * 34, 90, 17, 17)
        spiral(d, cx - 106 + k * 34, 90, 12, 1.8, 2.4, HOLE)
    # base com molduras
    shape(d, [(cx - 98, BASE - 34), (W + 30, BASE - 34), (W + 30, BASE + 26), (cx - 108, BASE + 26)], n=4)
    stroke(d, [(cx - 96, BASE - 14), (W + 20, BASE - 14)], 3, 3, HOLE)
    # hera subindo pela coluna
    vine = [(cx - 62 + 24 * math.sin(i / 3.0), 130 + i * 17) for i in range(44)]
    stroke(d, vine, 5, 3, n=4)
    for i in range(1, 44, 2):
        x, y = vine[i]
        ivy(d, x, y, 160 + (i % 3) * 30, float(g.uniform(24, 36)))
    # galho entrando, folhas serrilhadas, flores e botões
    br = [(cx - 60, 330), (cx - 140, 296), (cx - 230, 312), (cx - 310, 282), (cx - 390, 300)]
    stroke(d, br, 11, 3, n=8)
    stroke(d, [(cx - 180, 304), (cx - 220, 360), (cx - 290, 412)], 7, 2, n=8)
    stroke(d, [(cx - 310, 282), (cx - 330, 240), (cx - 318, 206)], 5, 2, n=8)
    stroke(d, [(cx - 250, 312), (cx - 266, 350), (cx - 252, 380)], 4, 1.5, n=8)
    for (x, y, a, L) in ((cx - 150, 298, -100, 78), (cx - 120, 300, 70, 66), (cx - 240, 312, 70, 86), (cx - 330, 280, -140, 66), (cx - 392, 300, 175, 60),
                         (cx - 226, 364, 110, 70), (cx - 290, 412, 160, 66), (cx - 318, 206, -80, 52), (cx - 200, 300, -60, 58)):
        stroke(d, [(x, y), (x + 6 * math.cos(math.radians(a)), y + 6 * math.sin(math.radians(a)))], 2, 1.5)
        serrated(d, x, y, a, L)
    flower(d, cx - 300, 452, 11)
    flower(d, cx - 206, 410, 10)
    flower(d, cx - 252, 392, 8)
    for (x, y) in ((cx - 360, 270), (cx - 170, 330)):
        stroke(d, [(x, y), (x - 4, y - 14)], 2, 1.2)
        shape(d, [(x - 4, y - 14), (x - 10, y - 24), (x - 4, y - 34), (x + 2, y - 24)], n=4)


def capim(d, g):
    """Capim fino e flores pequenas ao longo do chão."""
    for k in range(70):
        x = float(g.uniform(20, W - 20))
        y = BASE + 10 * math.sin(x / 210) + 6 * math.sin(x / 57) + 4
        for j in range(int(g.integers(4, 8))):
            h = float(g.uniform(10, 30))
            lean = float(g.uniform(-10, 10))
            stroke(d, [(x + j * 3, y), (x + j * 3 + lean * 0.5, y - h * 0.6), (x + j * 3 + lean, y - h)], 2.6, 0.3, n=5)
    for k in range(6):
        x = float(g.uniform(120, W - 260))
        y = BASE + 10 * math.sin(x / 210) + 2
        stroke(d, [(x, y), (x + 2, y - 30), (x - 2, y - 46)], 2, 1.4)
        flower(d, x - 2, y - 52, 5)


def laterais():
    """As laterais da tela: pinheiro à esquerda e coluna com galho à direita (perto da lâmpada).

    Os detalhes aleatórios (furos da copa, tufos, tamanho das folhas de hera) seguem a sequência de
    sorteios da versão aprovada, na qual um desenho de teste (pinheiro + coluna + capim) consumia o
    gerador antes do desenho usado no filme. Essa primeira passada é refeita aqui sem desenhar.
    """
    g = np.random.default_rng(21)
    nada = NullDraw()
    pinheiro(nada, g)
    coluna_galho(nada, g)
    capim(nada, g)
    return layer(lambda d: (pinheiro(d, g), coluna_galho(d, g)))

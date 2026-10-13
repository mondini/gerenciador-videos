"""Cenário romano em camadas de profundidade: fundo distante, meio e as laterais da tela.

Cada função desenha numa folha do tamanho do quadro (recebe o `d` do PIL) ou devolve o sprite pronto.
O desfoque de cada camada (distância do lençol) é decidido no script de cena, via `quadro.Camada`.
"""
from __future__ import annotations

import math

import numpy as np

from .config import H, W
from .traco import (BASE, HOLE, INK, NullDraw, cr, ell, flower, ivy, layer, poly, serrated, shape, spiral, stroke,
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


# =====================================================================================================
# MOLDURA "OLIVEIRA" (MA-002 em diante; decisão de 13/10/2026: cada vídeo tem a sua moldura fixa).
# Mesmo mundo romano, silhuetas diferentes das do MA-001: oliveira à esquerda, muro em ruína com arco
# quebrado e loureiro à direita, lenha e pedras na base, cidade murada no fundo, vinhedo no meio.
# Use com PANO = 'pesado' no script de cena (borda do pano sem o serrilhado de capim).
# =====================================================================================================
def folha_estreita(d, x, y, ang, L, larg=0.13, col=INK):
    """Folha lanceolada (oliveira: estreita; loureiro: larg≈0.22), com nervura central vazada."""
    a = math.radians(ang)
    c, s_ = math.cos(a), math.sin(a)
    T = lambda u, v: (x + c * u - s_ * v, y + s_ * u + c * v)
    shape(d, [T(0, 0), T(L * 0.25, L * larg * 0.8), T(L * 0.6, L * larg), T(L, 0), T(L * 0.6, -L * larg), T(L * 0.25, -L * larg * 0.8)],
          col, n=5)
    if L > 30:
        stroke(d, [T(L * 0.08, 0), T(L * 0.5, 0), T(L * 0.85, 0)], 1.4, 0.3, HOLE, n=3)


def raminho(d, g, pts, n_folhas, L, larg=0.13, w=3.0, abre=38):
    """Raminho fino com folhas alternadas saindo dos dois lados, apontando para a ponta."""
    stroke(d, pts, w, 0.8, n=6)
    c = cr(pts, False, 6)
    for i in range(n_folhas):
        f = 0.15 + 0.85 * i / max(n_folhas - 1, 1)
        k = min(int(f * (len(c) - 1)), len(c) - 2)
        (x, y), (x2, y2) = c[k], c[k + 1]
        base = math.degrees(math.atan2(y2 - y, x2 - x))
        lado = 1 if i % 2 else -1
        folha_estreita(d, x, y, base + lado * (abre + float(g.uniform(-10, 10))), L * float(g.uniform(0.75, 1.1)), larg)
    folha_estreita(d, *c[-1], math.degrees(math.atan2(c[-1][1] - c[-2][1], c[-1][0] - c[-2][0])), L * 0.9, larg)


def _galho_caido(x, y, ang, comp_, g):
    """Pontos de um galho que sai em `ang` graus e vai pendendo para baixo (oliveira)."""
    pts = [(x, y)]
    a = math.radians(ang)
    for k in range(4):
        a += math.radians(16 + float(g.uniform(-6, 8)))          # pende
        x += math.cos(a) * comp_ / 4
        y += math.sin(a) * comp_ / 4
        pts.append((x, y))
    return pts


def oliveira(d, g):
    """Oliveira antiga entrando pela esquerda: tronco em dois feixes torcidos, oco, nós; copa rala de raminhos pendentes."""
    # dois feixes do tronco, torcidos um sobre o outro
    stroke(d, [(-90, BASE + 30), (-20, 830), (30, 720), (0, 600), (60, 480), (140, 390)], 120, 44, n=14)
    stroke(d, [(50, BASE + 30), (95, 820), (60, 700), (120, 590), (95, 490), (170, 410)], 78, 34, n=14)
    shape(d, [(38, 760), (58, 700), (52, 630), (34, 600), (22, 660), (26, 720)], HOLE, n=8)       # o oco
    spiral(d, 100, 560, 10, 1.2, 2.6, HOLE)
    spiral(d, 0, 820, 13, 1.1, 3, HOLE, sign=-1)
    for k in range(7):                                                                             # casca em sulcos
        y0 = 880 - k * 64
        stroke(d, [(-30 + k * 12, y0), (-12 + k * 14, y0 - 40), (4 + k * 14, y0 - 70)], 2.6, 0.4, HOLE, n=5)
    # pernadas principais
    limbs = [[(140, 390), (230, 300), (330, 240), (450, 205), (560, 190)],
             [(140, 390), (110, 290), (70, 200), (30, 120), (-20, 70)],
             [(170, 410), (280, 380), (380, 360), (470, 365)],
             [(330, 240), (360, 160), (420, 100), (470, 60)],
             [(230, 300), (210, 220), (240, 150)],
             [(70, 200), (150, 150), (210, 90)]]
    for i, b in enumerate(limbs):
        stroke(d, b, 30 if i < 3 else 16, 7, n=8)
    # raminhos pendentes (copa rala, cheia de buracos de luz)
    pontas = [(560, 190, 10), (520, 196, 60), (450, 205, 40), (470, 365, 20), (430, 362, 70), (470, 60, 0), (420, 100, 50),
              (240, 150, -20), (210, 90, -40), (-20, 70, 110), (30, 120, 120), (380, 360, 60), (330, 240, 30), (150, 150, 70),
              (280, 380, 80), (110, 290, 140)]
    for (x, y, a) in pontas:
        for j in range(2 + int(g.integers(0, 2))):
            ang = a + float(g.uniform(-35, 35))
            raminho(d, g, _galho_caido(x, y, ang, float(g.uniform(90, 150)), g), int(g.integers(7, 11)), float(g.uniform(26, 34)))


def ruina_loureiro(d, g):
    """Muro de pedra em ruína entrando pela direita: pilar alto com o arranque de um arco quebrado, muro baixo
    de degraus partidos e um loureiro nascendo de uma fenda."""
    # pilar alto junto à borda
    px = 1735
    poly(d, [(px, BASE + 40), (px, 300), (W + 30, 270), (W + 30, BASE + 40)])
    # arranque do arco: aduelas em leque, partido no alto
    cx, cy, r0, r1 = 1545, 420, 180, 238                                # centro do arco à esquerda do pilar
    for k in range(5):
        a0 = math.radians(-k * 16)
        a1 = math.radians(-(k + 1) * 16 + 1.8)                          # junta vazada entre aduelas
        q = [(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)), (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)),
             (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)), (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))]
        if k == 4:                                                      # última aduela partida
            q[2] = ((q[1][0] + q[2][0]) / 2, (q[1][1] + q[2][1]) / 2 + 8)
            q[3] = ((q[0][0] + q[3][0]) / 2 + 6, (q[0][1] + q[3][1]) / 2)
        poly(d, q)
    poly(d, [(px - 4, 300), (W + 30, 266), (W + 30, 250), (px - 10, 286)])          # cornija do pilar
    poly(d, [(1810, 252), (1838, 226), (1852, 240), (1880, 214), (1900, 236), (W + 30, 230), (W + 30, 258), (1810, 262)])  # topo partido
    # muro baixo, topo em degraus quebrados, descendo para a esquerda
    topo = [(1490, BASE + 40), (1490, 700), (1512, 694), (1520, 652), (1560, 646), (1572, 600), (1610, 596),
            (1622, 548), (1668, 540), (1676, 490), (px, 486), (px, BASE + 40)]
    poly(d, topo)
    # juntas das pedras (vazadas): fiadas horizontais e juntas alternadas
    for row, y in enumerate(range(380, BASE, 46)):
        x_ini = max(1500 if y > 700 else 1576 if y > 600 else 1626 if y > 548 else 1680 if y > 490 else px + 4, 1500)
        stroke(d, [(x_ini, y), (W + 20, y - 2)], 2.2, 2.2, HOLE, n=3)
        for x in range(x_ini + (30 if row % 2 else 70), W, 96):
            stroke(d, [(x, y + 3), (x + 1, y + 42)], 2.0, 2.0, HOLE, n=3)
    shape(d, [(1600, 640), (1612, 700), (1604, 760), (1596, 700)], HOLE, n=4)       # fenda
    # loureiro nascendo da fenda
    tronco = [(1604, 700), (1580, 640), (1540, 560), (1500, 470), (1470, 400)]
    stroke(d, tronco, 14, 5, n=8)
    ramos = [[(1540, 560), (1470, 540), (1400, 500)], [(1500, 470), (1440, 430), (1380, 420)],
             [(1470, 400), (1450, 330), (1420, 270)], [(1520, 520), (1500, 450), (1530, 380)],
             [(1580, 640), (1520, 620), (1450, 610)]]
    for rm in ramos:
        raminho(d, g, rm, 9, float(g.uniform(40, 50)), larg=0.22, w=5, abre=48)
    for (x, y) in ((1430, 512), (1405, 438), (1455, 330), (1462, 612)):              # bagas
        for j in range(3):
            ell(d, x + j * 9 - 9, y + (j % 2) * 8, 5, 5)
    # hera seca escorrendo do pilar
    for k in range(3):
        x0 = px + 30 + k * 50
        pts = [(x0 + 10 * math.sin(i / 2.5 + k), 340 + i * 14) for i in range(10 + 3 * k)]
        stroke(d, pts, 3, 1.2, n=6)
        for i in range(2, len(pts), 3):
            ivy(d, pts[i][0], pts[i][1], 120 if i % 2 else 60, float(g.uniform(18, 26)))


def lenha_pedras(d, g):
    """Base da moldura: pilha de lenha vista de topo (anéis da madeira vazados) no canto esquerdo e
    pedras soltas à direita. Ficam atrás da borda do pano."""
    # pilha de toras 4-3-2-1, vista de frente (as pontas das toras)
    r = 33
    for fila, n in enumerate((4, 3, 2, 1)):
        for i in range(n):
            x = 140 + i * 2 * r * 0.98 + fila * r * 0.98 + float(g.uniform(-3, 3))
            y = 878 - fila * 2 * r * 0.86 + float(g.uniform(-2, 2))
            rr = r * float(g.uniform(0.9, 1.06))
            ell(d, x, y, rr, rr * 0.96)
            spiral(d, x + float(g.uniform(-3, 3)), y, rr * 0.62, 2.2, 1.7, HOLE, sign=1 if (i + fila) % 2 else -1)
            stroke(d, [(x - rr * 0.1, y - rr * 0.15), (x + rr * 0.5, y - rr * 0.55)], 1.6, 0.6, HOLE, n=3)  # rachadura
    # duas toras deitadas em perspectiva, encostadas na pilha
    stroke(d, [(360, 900), (440, 868), (530, 846)], 46, 40, n=6)
    ell(d, 532, 846, 20, 23)
    spiral(d, 532, 846, 13, 2, 1.5, HOLE)
    stroke(d, [(400, 912), (490, 894), (580, 886)], 40, 36, n=6)
    ell(d, 582, 886, 18, 20)
    spiral(d, 582, 886, 11, 2, 1.4, HOLE, sign=-1)
    # pedras soltas à direita
    for (x, y, rx, ry) in ((1300, 856, 70, 48), (1388, 868, 52, 40), (1220, 878, 44, 30), (1452, 884, 36, 28)):
        pts = [(x + rx * math.cos(a) * float(g.uniform(0.85, 1.1)), y + ry * math.sin(a) * float(g.uniform(0.8, 1.05)))
               for a in [k * math.pi / 5 for k in range(10)]]
        shape(d, pts, n=6)
    stroke(d, [(1268, 842), (1306, 826), (1338, 838)], 2.2, 0.6, HOLE, n=4)


def _cidade(d):
    """Fundo distante: um morro largo com uma cidade murada no alto (muralha, torres, portão, telhados, templo)."""
    morro = lambda x: 720 - 230 * math.exp(-((x - 760) / 520) ** 2) - 18 * math.sin(x / 150)
    poly(d, [(x, morro(x)) for x in range(-20, W + 21, 12)] + [(W + 20, H), (-20, H)])
    poly(d, [(x, 760 - 60 * math.exp(-((x - 1600) / 260) ** 2)) for x in range(900, W + 21, 12)] + [(W + 20, H), (900, H)])
    x0, x1 = 430, 1110
    # casario e templo atrás da muralha
    for k, x in enumerate(range(x0 + 20, x1 - 40, 46)):
        yb = morro(x) - 40
        h = 26 + (k * 37 % 30)
        poly(d, [(x, yb), (x + 40, yb), (x + 40, yb - h), (x, yb - h)])
        poly(d, [(x - 4, yb - h), (x + 20, yb - h - 16), (x + 44, yb - h)])
    tx, ty = 760, morro(760) - 96
    poly(d, [(tx - 64, ty + 30), (tx + 64, ty + 30), (tx + 64, ty - 40), (tx - 64, ty - 40)])
    poly(d, [(tx - 74, ty - 40), (tx, ty - 74), (tx + 74, ty - 40)])
    for k in range(5):
        poly(d, [(tx - 50 + k * 24, ty + 26), (tx - 44 + k * 24, ty + 26), (tx - 44 + k * 24, ty - 34), (tx - 50 + k * 24, ty - 34)], HOLE)
    # muralha seguindo o morro, com ameias
    wall = [(x, morro(x) - 22) for x in range(x0, x1 + 1, 10)]
    poly(d, [(x0, morro(x0) + 30)] + wall + [(x1, morro(x1) + 30)])
    for x in range(x0, x1, 20):
        poly(d, [(x, morro(x) - 22), (x + 11, morro(x) - 22), (x + 11, morro(x) - 34), (x, morro(x) - 34)])
    for x in (x0, 560, 690, 840, 970, x1 - 24):                         # torres
        yb = morro(x) - 10
        poly(d, [(x - 2, yb + 20), (x + 26, yb + 20), (x + 26, yb - 70), (x - 2, yb - 70)])
        for j in range(3):
            poly(d, [(x - 4 + j * 11, yb - 70), (x + 4 + j * 11, yb - 70), (x + 4 + j * 11, yb - 80), (x - 4 + j * 11, yb - 80)])
        ell(d, x + 12, yb - 44, 3, 6, HOLE)
    gx = 760                                                            # portão
    ell(d, gx, morro(gx) - 4, 18, 18, HOLE)
    poly(d, [(gx - 18, morro(gx) - 4), (gx + 18, morro(gx) - 4), (gx + 18, morro(gx) + 24), (gx - 18, morro(gx) + 24)], HOLE)


def cidade():
    """Fundo distante da moldura oliveira (cidade murada no morro), levemente desfocado em 2x."""
    return layer(_cidade, blur=1.3)


def _vinhedo(d):
    """Plano do meio: chão, fileiras de vinha em estacas fugindo para o ponto de fuga e um pequeno santuário."""
    ground = [(x, 800 - 14 * math.sin(x / 260 + 1)) for x in range(-20, W + 21, 12)]
    poly(d, ground + [(W + 20, H), (-20, H)])
    for (ax, ay) in ((260, 790), (430, 806), (620, 820)):
        a = (ax, ay)
        prev = None
        for k in range(14):
            f = k * 0.032
            p = toward(a, f)
            h = 64 * (1 - f * 1.25)
            stroke(d, [p, (p[0] + 1, p[1] - h)], 5 * (1 - f), 4 * (1 - f))
            top = (p[0], p[1] - h)
            if prev is not None:                                        # a vinha pendendo entre estacas
                mid = ((prev[0] + top[0]) / 2, (prev[1] + top[1]) / 2 + 14 * (1 - f))
                stroke(d, [prev, mid, top], 4 * (1 - f), 3 * (1 - f), n=6)
                ell(d, mid[0], mid[1] + 6 * (1 - f), 9 * (1 - f), 7 * (1 - f))
            prev = top
    sx, sy = 1240, 792                                                  # santuário de beira de estrada
    poly(d, [(sx - 30, sy), (sx + 30, sy), (sx + 30, sy - 70), (sx - 30, sy - 70)])
    poly(d, [(sx - 40, sy - 70), (sx, sy - 100), (sx + 40, sy - 70)])
    ell(d, sx, sy - 40, 12, 16, HOLE)


def vinhedo():
    """Plano do meio da moldura oliveira."""
    return layer(_vinhedo, blur=1.0)


def laterais_oliveira():
    """Laterais da moldura oliveira: oliveira à esquerda, ruína com loureiro à direita."""
    g = np.random.default_rng(202)
    return layer(lambda d: (oliveira(d, g), ruina_loureiro(d, g)))


def base_lenha():
    """Base da moldura oliveira: lenha empilhada à esquerda e pedras à direita."""
    g = np.random.default_rng(203)
    return layer(lambda d: lenha_pedras(d, g))

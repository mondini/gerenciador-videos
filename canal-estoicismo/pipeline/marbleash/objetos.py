"""Objetos romanos recortados: cada função devolve um sprite (Static) do tamanho do quadro, na posição
em que o objeto fica em cena. Para virar sombra, use `quadro.Camada(objetos.templo, ...)`.

Objetos em três quartos (templo, mesa) fogem para o ponto de fuga `traco.VP`, à direita fora da tela.
"""
from __future__ import annotations

import math

import numpy as np

from PIL import ImageFont

from . import config
from .config import H, S, W
from .traco import (BASE, FLOOR, HOLE, INK, ROD, P, Static, canvas, cr, down, ell, full, holes_row, layer, leaf, ln, serrated,
                    poly, shape, spiral, stroke, toward)


# ---------------- templo em três quartos (sobe do chão no gancho) ----------------
def _templo(d):
    x0, x1 = 600, 900                     # fachada da frente

    def side_quad(y_top, y_bot, f):
        return [(x1, y_top), toward((x1, y_top), f), toward((x1, y_bot), f), (x1, y_bot)]
    F = 0.085
    poly(d, side_quad(BASE - 26, BASE + 4, F))
    poly(d, side_quad(BASE - 262, BASE - 236, F))
    poly(d, side_quad(BASE - 236, BASE - 26, F))
    for k in range(5):                    # colunata lateral em escorço
        f0, f1 = 0.008 + k * 0.016, 0.016 + k * 0.016
        p0, p1 = toward((x1, BASE - 228), f0), toward((x1, BASE - 228), f1)
        q0, q1 = toward((x1, BASE - 32), f0), toward((x1, BASE - 32), f1)
        poly(d, [p0, p1, q1, q0], HOLE)
    # telhado lateral com linhas das telhas
    ridge0, ridgeF = (750, BASE - 350), toward((750, BASE - 350), F)
    eave0, eaveF = (x1 + 40, BASE - 258), toward((x1 + 40, BASE - 258), F)
    poly(d, [ridge0, ridgeF, eaveF, eave0])
    for k in range(9):
        f = 0.008 + k * 0.009
        stroke(d, [toward(ridge0, f), toward(eave0, f)], 1.6, 1.2, HOLE)
    # fachada: degraus, parede, colunas jônicas com caneluras, friso com gregas, frontão
    shape(d, [(x0 - 30, BASE + 4), (x1 + 30, BASE + 4), (x1 + 24, BASE - 14), (x0 - 24, BASE - 14)], n=4)
    poly(d, [(x0 - 10, BASE - 12), (x1 + 10, BASE - 12), (x1 + 10, BASE - 26), (x0 - 10, BASE - 26)])
    poly(d, [(x0 + 6, BASE - 24), (x1 - 6, BASE - 24), (x1 - 6, BASE - 236), (x0 + 6, BASE - 236)])
    for k in range(4):
        cx = x0 + 34 + k * 77
        if k < 3:
            gl, gr = cx + 22, cx + 54
            shape(d, [(gl, BASE - 30), (gr, BASE - 30), (gr - 2, BASE - 120), (gr, BASE - 200), (gl, BASE - 200), (gl + 2, BASE - 120)], HOLE, n=6)
        spiral(d, cx - 12, BASE - 214, 7, 1.4, 2, HOLE)
        spiral(d, cx + 12, BASE - 214, 7, 1.4, 2, HOLE, sign=-1)
        for j in range(3):
            stroke(d, [(cx - 7 + j * 7, BASE - 196), (cx - 6 + j * 7, BASE - 110), (cx - 7 + j * 7, BASE - 40)], 1.6, 1.6, HOLE)
    poly(d, [(x0 - 16, BASE - 236), (x1 + 16, BASE - 236), (x1 + 16, BASE - 262), (x0 - 16, BASE - 262)])
    for k in range(11):
        x = x0 + 4 + k * 27
        poly(d, [(x, BASE - 254), (x + 14, BASE - 254), (x + 14, BASE - 244), (x + 4, BASE - 244), (x + 4, BASE - 249), (x + 9, BASE - 249)], HOLE)
    roof = [(x0 - 40, BASE - 258)] + cr([(x0 - 40, BASE - 258), (x0 + 50, BASE - 288), (750, BASE - 350), (x1 - 50, BASE - 288), (x1 + 40, BASE - 258)], False, 14) + [(x1 + 40, BASE - 258)]
    poly(d, roof)
    shape(d, [(700, BASE - 266), (750, BASE - 300), (800, BASE - 266)], HOLE, n=6)          # relevo do tímpano
    ell(d, 750, BASE - 280, 9, 9)
    spiral(d, 750, BASE - 280, 6, 1.2, 1.4, HOLE)
    for k in range(10):
        x = x0 - 22 + k * 38
        shape(d, [(x - 7, BASE - 262), (x, BASE - 278), (x + 7, BASE - 262)], n=5)
    shape(d, [(740, BASE - 346), (750, BASE - 388), (760, BASE - 346)], n=6)
    for s_, x in ((-1, x0 - 40), (1, x1 + 40)):
        stroke(d, [(x, BASE - 260), (x + s_ * 10, BASE - 286), (x + s_ * 24, BASE - 296)], 7, 2)


def templo():
    """Templo/casa em três quartos, de pé no chão do palco (x 570–1000)."""
    return layer(_templo)


# ---------------- mesa em três quartos com tigela, pão, ânfora e vapor ----------------
def _mesa(d):
    top = 770
    fx0, fx1 = 1300, 1580                     # borda da frente
    back = lambda p: toward(p, 0.05)
    a, b = (fx0, top), (fx1, top)
    poly(d, [a, b, back(b), back(a)])           # tampo visto levemente de cima
    poly(d, [(fx0 - 8, top), (fx1 + 8, top), (fx1 + 4, top + 14), (fx0 - 4, top + 14)])
    stroke(d, [(fx0, top + 18), (fx1, top + 18)], 2.6, 2.6, HOLE)
    for x, s_, sc in ((fx0 + 26, -1, 1.0), (fx1 - 26, 1, 1.0)):
        stroke(d, [(x, top + 12), (x - s_ * 14, top + 56), (x + s_ * 6, top + 110), (x - s_ * 4, BASE - 18)], 16, 10)
        shape(d, [(x - 14, BASE - 22), (x + 18 * s_ + 4, BASE - 18), (x + 22 * s_, BASE - 4), (x - 16, BASE - 2)], n=6)
        spiral(d, x - s_ * 2, top + 40, 7, 1.3, 1.8, HOLE, sign=s_)
    for x in (fx0 + 26, fx1 - 26):              # pernas de trás: menores e mais altas
        bx, by = back((x, top))
        stroke(d, [(bx, by + 10), (bx + 6, by + 60), (bx + 2, BASE - 40)], 10, 6)
    shape(d, [(1370, 730), (1510, 730), (1502, 750), (1480, 764), (1440, 770), (1400, 764), (1378, 750)], n=8)
    for k in range(6):
        x = 1392 + k * 18
        d.arc([*P(x - 6, 740), *P(x + 6, 752)], 180, 360, fill=HOLE, width=3)
    shape(d, [(1400, 732), (1408, 710), (1440, 700), (1474, 708), (1482, 732)], n=10)
    for k in range(3):
        stroke(d, [(1418 + k * 16, 722), (1426 + k * 16, 710)], 2.4, 1.0, HOLE)
    shape(d, [(1546, top - 2), (1534, top - 28), (1530, top - 60), (1542, top - 88), (1550, top - 100), (1546, top - 110), (1564, top - 110),
              (1560, top - 100), (1568, top - 88), (1580, top - 60), (1576, top - 28), (1564, top - 2)], n=8)
    for s_ in (-1, 1):
        stroke(d, [(1555 + s_ * 6, top - 100), (1555 + s_ * 22, top - 96), (1555 + s_ * 20, top - 76)], 3, 3)
    stroke(d, [(1536, top - 52), (1574, top - 52)], 2, 2, HOLE)
    for i in range(3):                          # vapor
        x0 = 1418 + i * 22
        pts = [(x0 + 10 * math.sin(k / 3.0 + i), 694 - k * 9) for k in range(14)]
        stroke(d, pts, 4, 0.8, (24, 18, 13, 200))
        x, y = pts[-1]
        spiral(d, x, y, 6, 1.0, 1.6, (24, 18, 13, 200))


def mesa():
    """Mesa com pés de leão, tigela, pão, ânfora e vapor (x 1290–1600)."""
    return layer(_mesa)


# ---------------- lamparina a óleo pendurada e sua chama ----------------
def _lamparina(d):
    cx, cy = 1190, 370
    for k, ex in enumerate((-58, 0, 58)):
        stroke(d, [(cx, cy - 110), (cx + ex * 0.45, cy - 56 + abs(ex) * 0.12), (cx + ex * 0.85, cy - 6)], 2.4, 2.0)
    stroke(d, [(cx, -10), (cx + 2, 120), (cx, cy - 110)], 2.6, 2.4)
    ell(d, cx, cy - 112, 7, 7)
    ell(d, cx, cy - 112, 3, 3, HOLE)
    shape(d, [(cx - 70, cy + 6), (cx - 50, cy - 10), (cx, cy - 16), (cx + 46, cy - 10), (cx + 76, cy - 4), (cx + 92, cy + 4), (cx + 80, cy + 12),
              (cx + 46, cy + 22), (cx, cy + 30), (cx - 48, cy + 26), (cx - 78, cy + 16)], n=10)
    stroke(d, [(cx - 70, cy + 6), (cx - 96, cy - 8), (cx - 92, cy - 30), (cx - 74, cy - 24)], 6, 4)          # alça
    ell(d, cx, cy + 6, 16, 9, HOLE)
    ell(d, cx, cy + 6, 10, 5, INK)
    for k in range(8):
        a = k * math.pi / 4
        ell(d, cx + 13 * math.cos(a), cy + 6 + 7 * math.sin(a), 1.8, 1.8, HOLE)
    for k in range(6):
        ell(d, cx - 52 + k * 20, cy + 20, 2, 2, HOLE)


def lamparina():
    """Lucerna romana pendurada do teto por três correntes (corpo em x≈1190, y≈370)."""
    return full(_lamparina)


def chama(k=1):
    """Chama colorida da lamparina (bico em x≈1278, y≈368). k escolhe uma de quatro formas."""
    im, d = canvas(W, H)
    cx, cy = 1190 + 88, 370 - 2
    h = 46 + [0, 6, -4, 3][k]
    s = [0, 5, -4, 2][k]
    shape(d, [(cx - 9, cy), (cx - 8, cy - h * 0.4), (cx + s - 2, cy - h * 0.8), (cx + s, cy - h), (cx + s + 6, cy - h * 0.6), (cx + 9, cy - h * 0.25), (cx + 8, cy)],
          (255, 236, 186, 255), n=8)
    shape(d, [(cx - 4, cy), (cx + s * 0.5, cy - h * 0.5), (cx + 4, cy)], (255, 252, 240, 255), n=6)
    return Static(down(im))


# ---------------- glória: arco triunfal com portas, pedestal, soldados, moedas ----------------
def _arco(d):
    cx, base = 960, FLOOR + 30
    poly(d, [(cx - 260, base), (cx - 170, base), (cx - 170, base - 380), (cx + 170, base - 380), (cx + 170, base), (cx + 260, base), (cx + 260, base - 560), (cx - 260, base - 560)])
    d.pieslice([*P(cx - 170, base - 550), *P(cx + 170, base - 210)], 180, 360, fill=HOLE)
    poly(d, [(cx - 170, base - 380), (cx + 170, base - 380), (cx + 170, base - 381), (cx - 170, base - 381)], HOLE)
    for k in range(9):
        poly(d, [(cx - 240 + k * 60, base - 540), (cx - 220 + k * 60, base - 540), (cx - 220 + k * 60, base - 516), (cx - 240 + k * 60, base - 516)], HOLE)
    for side in (-1, 1):
        for k in range(5):
            ell(d, cx + side * 215, base - 340 + k * 60, 7, 7, HOLE)


def arco():
    """Arco triunfal no centro do palco (x 700–1220, até y≈370)."""
    return full(_arco)


def portas(q):
    """As duas folhas da porta do arco; q = 0 fechadas, 1 abertas."""
    im, d = canvas(W, H)
    cx, base = 960, FLOOR + 30
    w = 170 * (1 - 0.88 * q)
    for side in (-1, 1):
        xa = cx + side * 170
        xb = xa - side * w
        poly(d, [(xa, base), (xb, base + 24 * q), (xb, base - 380 - 24 * q), (xa, base - 380)])
        if w > 30:
            for k in range(3):
                ell(d, (xa + xb) / 2, base - 300 + k * 110, 9 * (w / 170) + 1, 9, HOLE)
    return Static(down(im))


def _pedestal(d):
    poly(d, [(880, FLOOR + 30), (1040, FLOOR + 30), (1024, FLOOR - 60), (896, FLOOR - 60)])
    poly(d, [(870, FLOOR - 60), (1050, FLOOR - 60), (1050, FLOOR - 74), (870, FLOOR - 74)])
    for k in range(5):
        ell(d, 912 + k * 24, FLOOR - 20, 4, 4, HOLE)


def pedestal():
    """Pedestal no centro (topo em y≈826), onde o imperador sobe."""
    return full(_pedestal)


def soldado():
    """Legionário de perfil com escudo, elmo de crista e lança. Âncora (0, 0) = pés."""
    im, d = canvas(140, 360)
    ox, oy = 70, 330
    poly(d, [(-16, -200), (16, -200), (24, -60), (30, 0), (-28, 0), (-22, -60)], INK, ox, oy)
    ell(d, 0, -226, 17, 20, INK, ox, oy)
    poly(d, [(-18, -236), (18, -240), (14, -262), (-6, -270), (-20, -250)], INK, ox, oy)   # elmo
    for k in range(5):
        ln(d, [(-8 + k * 4, -270), (-12 + k * 6, -290)], 2, INK, ox, oy)                   # crista
    ell(d, 6, -228, 2.4, 1.6, HOLE, ox, oy)
    poly(d, [(-34, -170), (14, -170), (14, -60), (-34, -60)], INK, ox, oy)                # escudo (scutum)
    ell(d, -10, -115, 9, 9, HOLE, ox, oy)
    ell(d, -10, -115, 5, 5, INK, ox, oy)
    holes_row(d, -30, -164, 10, -164, 6, 2, ox, oy)
    holes_row(d, -30, -66, 10, -66, 6, 2, ox, oy)
    ln(d, [(24, 30), (34, -320)], 3, INK, ox, oy)
    poly(d, [(30, -320), (35, -346), (40, -320)], INK, ox, oy)
    poly(d, [(-10, 0), (2, 0), (0, 30), (-12, 30)], INK, ox, oy)
    poly(d, [(8, 0), (20, 0), (22, 30), (10, 30)], INK, ox, oy)
    for k in range(4):
        poly(d, [(-18 + k * 10, -40), (-12 + k * 10, -40), (-14 + k * 10, -10), (-20 + k * 10, -10)], HOLE, ox, oy)
    ln(d, [(0, -80), (20, 360)], 2.6, ROD, ox, oy)
    return Static(down(im), -70, -330)


def moeda():
    """Moeda com furo central e oito furinhos. Âncora (0, 0) = centro."""
    im, d = canvas(40, 40)
    ell(d, 20, 20, 13, 13)
    ell(d, 20, 20, 6, 6, HOLE)
    for k in range(8):
        a = k * math.pi / 4
        ell(d, 20 + 9.5 * math.cos(a), 20 + 9.5 * math.sin(a), 1.4, 1.4, HOLE)
    return Static(down(im), -20, -20)


# ---------------- a beira do mundo: penhasco, ciprestes, tenda, mesa de campanha ----------------
def _penhasco(d):
    base = FLOOR + 30
    pts = [(0, base), (1380, base - 6), (1420, base + 20), (1404, base + 70), (1440, H), (0, H)]
    poly(d, pts)
    for x, h in ((260, 420), (330, 340)):                     # ciprestes
        poly(d, [(x - 4, base), (x + 4, base), (x + 3, base - 40)])
        poly(d, [(x, base - h), (x + 30, base - h * 0.55), (x + 26, base - 40), (x - 26, base - 40), (x - 30, base - h * 0.55)])
        for k in range(6):
            leaf(d, x - 10 + (k % 2) * 20, base - 80 - k * h / 7, -90 + (k % 2) * 40, 16, HOLE)
    poly(d, [(560, base), (720, base - 240), (880, base)])    # tenda, com aba vazada
    for k in range(5):
        ell(d, 720, base - 200 + k * 36, 5, 5, HOLE)
    ln(d, [(720, base - 240), (726, base - 276)], 4)
    poly(d, [(975, FLOOR - 40), (1035, FLOOR - 40), (1035, FLOOR - 30), (975, FLOOR - 30)])    # banco
    for x in (982, 1028):
        poly(d, [(x - 4, FLOOR - 30), (x + 4, FLOOR - 30), (x + 6, base), (x - 6, base)])
    poly(d, [(1040, 760), (1260, 760), (1260, 772), (1040, 772)])                            # mesa de campanha
    for x in (1060, 1240):
        poly(d, [(x - 5, 772), (x + 5, 772), (x + 8, base + 2), (x - 8, base + 2)])
    poly(d, [(1110, 760), (1230, 760), (1236, 744), (1104, 744)])                            # pergaminho
    holes_row(d, 1112, 752, 1228, 752, 12, 1.6)
    poly(d, [(1180, 744), (1220, 736), (1236, 744), (1220, 752)])                            # lucerna sobre a mesa


def penhasco():
    """A beira do mundo: chão que termina num penhasco (x≈1400), ciprestes, tenda, banco e mesa."""
    return full(_penhasco)


def chama_noite(k=1):
    """Chama da lucerna sobre a mesa de campanha (x≈1238, y≈738)."""
    im, d = canvas(W, H)
    cx, cy = 1238, 738
    h = 30 + [0, 4, -3, 2][k]
    s = [0, 3, -2, 1][k]
    poly(d, [(cx - 7, cy), (cx + s - 3, cy - h * 0.6), (cx + s, cy - h), (cx + s + 5, cy - h * 0.5), (cx + 7, cy)], (255, 230, 168, 255))
    return Static(down(im))


def _gavinha():
    pts = []
    a = 0
    for k in range(140):
        a += 0.07 + 0.04 * math.sin(k / 11)
        r = 10 + k * 0.8
        pts.append((r * math.cos(a * 2.6) * 0.8, -k * 2.0 + r * 0.35 * math.sin(a * 2.6)))
    return pts


def fumaca(i, q):
    """Fio de fumaça i (0, 1 ou 2) subindo da lucerna da mesa de campanha; q = quanto já subiu (0 a 1)."""
    im, d = canvas(W, H)
    pts = [(1240 + 0.7 * x + 50 * i, 700 + 0.7 * y - 30 * i) for x, y in _gavinha()]
    n = max(2, int(len(pts) * q))
    for j in range(1, n):
        ln(d, [pts[j - 1], pts[j]], 3 * (1 - j / len(pts)) + 1, (40, 28, 18, 170))
    return Static(down(im))


# ---------------- letreiro: texto projetado como sombra ----------------
def letreiro(texto, fonte='CormorantGaramond-MediumItalic.ttf', tamanho=52, cx=960, y=150, cor=(60, 34, 16, 255), tracking=0.0):
    """Texto centrado em cx, com o topo em y (ex.: o sussurro "not yet... not enough.").

    Padrão do canal: Cormorant Garamond itálico (citações), Cinzel (nomes), Inter (créditos).
    """
    f = ImageFont.truetype(config.fonte(fonte), int(tamanho * S))

    def desenho(d):
        if tracking:                                    # espaçamento entre letras (ex.: Cinzel do Design System)
            _, pos = _nome_layout(texto, fonte, tamanho, cx, tracking)
            for ch, x in zip(texto, pos):
                d.text((x, y * S), ch, font=f, fill=cor)
        else:
            wdt = f.getlength(texto)
            d.text((cx * S - wdt / 2, y * S), texto, font=f, fill=cor)
    return full(desenho)


# ---------------- logo A — Horizonte (abertura de todos os vídeos) ----------------
# Geometria do Design System (caixa 200 x 200, ver docs/identidade-visual.md): meio-sol de centro (100, 110)
# e raio 56, dois cortes em y 80 e 94, cinco linhas de horizonte em degraus; nome em Cinzel 600, tracking
# 0.06em, com o "&" em âmbar. No lençol, o logo é RECORTADO num painel de papel: a luz passa pelos vazados.
_HZ_LINHAS = ((24, 176, 110), (44, 156, 124), (60, 140, 138), (76, 124, 152), (90, 110, 166))
AMBAR = (232, 163, 61, 255)                    # amber-500


def _hz(x, y, cx, cy, s):
    return cx + (x - 100) * s, cy + (y - 110) * s


def _nome_layout(texto, fonte, tamanho, cx, tracking):
    """Posição x (em 2x) de cada letra do nome, centrado em cx, com o espaçamento do Design System."""
    f = ImageFont.truetype(config.fonte(fonte), int(tamanho * S))
    gap = tracking * tamanho * S
    larg = [f.getlength(ch) for ch in texto]
    x = cx * S - (sum(larg) + gap * (len(texto) - 1)) / 2
    pos = []
    for w in larg:
        pos.append(x)
        x += w + gap
    return f, pos


def horizonte_painel(cx=960, cy=455, escala=1.6, nome_y=625, tamanho=64, texto='MARBLE & ASH',
                     fonte='Cinzel-SemiBold.ttf', tracking=0.06):
    """Painel de papel preto do tamanho da tela com o logo Horizonte e o nome vazados."""
    im, d = canvas(W, H)
    d.rectangle([0, 0, W * S, H * S], fill=INK)
    d.pieslice([*P(*_hz(44, 54, cx, cy, escala)), *P(*_hz(156, 166, cx, cy, escala))], 180, 360, fill=HOLE)
    for y in (80, 94):                                      # os dois cortes atravessam o sol (papel que fica)
        d.line([P(*_hz(40, y, cx, cy, escala)), P(*_hz(160, y, cx, cy, escala))], fill=INK, width=int(4 * escala * S))
    for a, b, y in _HZ_LINHAS:
        d.line([P(*_hz(a, y, cx, cy, escala)), P(*_hz(b, y, cx, cy, escala))], fill=HOLE, width=int(3 * escala * S))
    f, pos = _nome_layout(texto, fonte, tamanho, cx, tracking)
    for ch, x in zip(texto, pos):
        if ch != ' ':
            d.text((x, nome_y * S), ch, font=f, fill=HOLE)
    return Static(down(im))


def horizonte_sol(cx=960, cy=455, escala=1.6):
    """Gelatina âmbar no recorte do sol (mesma geometria do painel)."""
    im, d = canvas(W, H)
    d.pieslice([*P(*_hz(44, 54, cx, cy, escala)), *P(*_hz(156, 166, cx, cy, escala))], 180, 360, fill=AMBAR)
    for y in (80, 94):
        d.line([P(*_hz(40, y, cx, cy, escala)), P(*_hz(160, y, cx, cy, escala))], fill=HOLE, width=int(4 * escala * S))
    return Static(down(im))


def horizonte_e(cx=960, nome_y=625, tamanho=64, texto='MARBLE & ASH', fonte='Cinzel-SemiBold.ttf', tracking=0.06):
    """Gelatina âmbar no "&" do nome (mesmo layout do painel)."""
    im, d = canvas(W, H)
    f, pos = _nome_layout(texto, fonte, tamanho, cx, tracking)
    d.text((pos[texto.index('&')], nome_y * S), '&', font=f, fill=AMBAR)
    return Static(down(im))


# =====================================================================================================
# Vídeo 1 · bloco 2 (O homem) — peças reaproveitáveis
# =====================================================================================================
def coroa_louros(cx=960, cy=250, r=110):
    """Coroa de louros: dois ramos de folhas serrilhadas em arco, com bagas e fita na base."""
    def desenho(d):
        for side in (-1, 1):
            pts = [(cx + r * math.cos(math.radians(90 + side * (22 + 148 * k / 14))),
                    cy + r * math.sin(math.radians(90 + side * (22 + 148 * k / 14)))) for k in range(15)]
            stroke(d, pts, 7, 2)
            for k in range(1, 14):
                x, y = pts[k]
                tx, ty = pts[k + 1][0] - pts[k - 1][0], pts[k + 1][1] - pts[k - 1][1]
                ang = math.degrees(math.atan2(ty, tx))
                L = 40 - 1.6 * k
                fora = math.degrees(math.atan2(y - cy, x - cx))
                for desvio in (-38, 38):
                    a_ = ang + desvio
                    if math.cos(math.radians(a_ - fora)) < -0.2:     # folha de dentro: menor
                        serrated(d, x, y, a_, L * 0.75, 0.3)
                    else:
                        serrated(d, x, y, a_, L, 0.32)
                if k % 3 == 1:
                    ell(d, x + 10 * math.cos(math.radians(fora)), y + 10 * math.sin(math.radians(fora)), 4, 4)
                    ell(d, x + 10 * math.cos(math.radians(fora)), y + 10 * math.sin(math.radians(fora)), 1.4, 1.4, HOLE)
        for side in (-1, 1):                                          # fita
            stroke(d, [(cx, cy + r + 2), (cx + side * 24, cy + r + 26), (cx + side * 30, cy + r + 58)], 9, 4)
        ell(d, cx, cy + r + 2, 9, 7)
    return full(desenho)


_RACHA = [(750, BASE - 352), (741, BASE - 322), (757, BASE - 296), (744, BASE - 266), (763, BASE - 240), (747, BASE - 196),
          (769, BASE - 148), (756, BASE - 104)]          # termina acima do pano da base


def _parcial(pts, q):
    """Os primeiros `q` (0..1) do comprimento de uma linha quebrada (rachadura crescendo)."""
    segs = list(zip(pts[:-1], pts[1:]))
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    resto, out = q * total, [pts[0]]
    for a, b in segs:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if resto >= L:
            out.append(b)
            resto -= L
        else:
            out.append((a[0] + (b[0] - a[0]) * resto / L, a[1] + (b[1] - a[1]) * resto / L))
            break
    return out


def _racha_pts(q):
    return _parcial(_RACHA, q)


def templo_rachado(q):
    """O templo de três quartos com uma rachadura vazada que desce do frontão (q = 0..1 do comprimento)."""
    def desenho(d):
        _templo(d)
        if q > 0:
            ln(d, _racha_pts(q), 5, HOLE)
    return layer(desenho)


def racha_brasa(q):
    """Gelatina âmbar da rachadura (mesmo traço de `templo_rachado`)."""
    def desenho(d):
        if q > 0:
            ln(d, _racha_pts(q), 5, AMBAR)
    return full(desenho)


def cidades(apagadas=0, n=6):
    """Fileira de cidades romanas ao longe (casas, cúpulas, torres) com janelas acesas (vazadas).

    As `apagadas` primeiras cidades (da esquerda) ficam com as janelas fechadas: a peste passando.
    """
    rr = np.random.default_rng(7)
    def desenho(d):
        base = 770
        poly(d, [(220, base + 6)] + [(x, base - 6 * math.sin(x / 70)) for x in range(220, 1720, 20)] + [(1720, base + 6), (1720, base + 40), (220, base + 40)])
        for i in range(n):
            x = 260 + i * 240
            for k in range(4):
                w, h = float(rr.uniform(34, 62)), float(rr.uniform(60, 150))
                tipo = int(rr.integers(0, 3))
                poly(d, [(x, base), (x, base - h), (x + w, base - h), (x + w, base)])
                if tipo == 0:
                    poly(d, [(x - 4, base - h), (x + w / 2, base - h - 22), (x + w + 4, base - h)])
                elif tipo == 1:
                    d.pieslice([*P(x + 2, base - h - w / 2 + 2), *P(x + w - 2, base - h + w / 2 - 2)], 180, 360, fill=INK)
                else:
                    poly(d, [(x + w * 0.3, base - h), (x + w * 0.3, base - h - 26), (x + w * 0.7, base - h - 26), (x + w * 0.7, base - h)])
                if i >= apagadas:
                    for j in range(int(h // 28)):
                        for c in range(max(1, int(w // 22))):
                            if rr.uniform() < 0.7:
                                wx, wy = x + 8 + c * 20, base - 20 - j * 26
                                d.rounded_rectangle([*P(wx, wy - 12), *P(wx + 8, wy)], radius=4 * S, fill=HOLE)
                else:
                    for j in range(int(h // 28)):
                        for c in range(max(1, int(w // 22))):
                            rr.uniform()
                x += w + float(rr.uniform(4, 14))
    return full(desenho)


def rio(fase):
    """O Danúbio: três faixas de onda recortadas correndo (fase 0..1 dá um ciclo)."""
    def desenho(d):
        for j, (y0, amp, esp, per) in enumerate(((772, 5, 9, 70), (800, 7, 12, 95), (832, 9, 16, 120))):
            ph = fase * 2 * math.pi + j * 1.7
            topo = [(x, y0 + amp * math.sin(x / per + ph)) for x in range(-20, W + 21, 10)]
            fundo = [(x, y + esp * (0.7 + 0.3 * math.sin(x / 37 + ph * 2))) for x, y in topo]
            poly(d, topo + fundo[::-1])
            for k in range(16):
                x = (k * 127 + fase * 380 * (j + 1)) % (W + 80) - 40
                y = y0 + amp * math.sin(x / per + ph) + esp * 0.35
                stroke(d, [(x, y), (x + 22, y - 1), (x + 40, y)], 2.4, 0.6, HOLE, n=4)
    return full(desenho)


def escudo_lancas(cx=960, cy=560):
    """Escudo de legionário (scutum) com umbo, raios e rebites vazados, e duas lanças cruzadas atrás."""
    def desenho(d):
        for side in (-1, 1):
            a0, a1 = (cx - side * 230, cy + 260), (cx + side * 230, cy - 300)
            stroke(d, [a0, ((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2), a1], 7, 6)
            ux, uy = (a1[0] - a0[0]) / 600, (a1[1] - a0[1]) / 600
            ponta = (a1[0] + ux * 70, a1[1] + uy * 70)
            shape(d, [a1, (a1[0] + ux * 30 - uy * 16, a1[1] + uy * 30 + ux * 16), ponta, (a1[0] + ux * 30 + uy * 16, a1[1] + uy * 30 - ux * 16)], n=5)
        w, h = 130, 190
        shape(d, [(cx - w, cy - h + 30), (cx - w + 18, cy - h), (cx + w - 18, cy - h), (cx + w, cy - h + 30),
                  (cx + w + 8, cy), (cx + w, cy + h - 30), (cx + w - 18, cy + h), (cx - w + 18, cy + h), (cx - w, cy + h - 30), (cx - w - 8, cy)], n=6)
        ell(d, cx, cy, 34, 34, HOLE)
        ell(d, cx, cy, 24, 24)
        spiral(d, cx, cy, 14, 1.4, 2.4, HOLE)
        for k in range(8):
            a = k * math.pi / 4
            stroke(d, [(cx + 44 * math.cos(a), cy + 44 * math.sin(a)), (cx + 110 * math.cos(a) * 0.9, cy + 170 * math.sin(a) * 0.9)], 3.2, 0.8, HOLE)
        holes_row(d, cx - w + 16, cy - h + 16, cx + w - 16, cy - h + 16, 11, 3)
        holes_row(d, cx - w + 16, cy + h - 16, cx + w - 16, cy + h - 16, 11, 3)
    return full(desenho)


def acampamento():
    """Acampamento militar à noite: tendas com abas e cordas, estacas, estandarte, toras e um tronco-banco."""
    def desenho(d):
        for x, w, h in ((300, 300, 230), (1340, 340, 250), (1660, 220, 160)):
            poly(d, [(x - w / 2, BASE), (x, BASE - h), (x + w / 2, BASE)])
            shape(d, [(x - 6, BASE - h + 30), (x + 16, BASE - 60), (x + 44, BASE), (x + 4, BASE)], HOLE, n=5)
            for side in (-1, 1):
                stroke(d, [(x + side * w * 0.25, BASE - h * 0.5), (x + side * (w * 0.5 + 40), BASE - 4)], 1.8, 1.2)
                poly(d, [(x + side * (w * 0.5 + 40) - 3, BASE - 6), (x + side * (w * 0.5 + 40) + 3, BASE - 6), (x + side * (w * 0.5 + 40), BASE + 6)])
            ln(d, [(x, BASE - h), (x + 4, BASE - h - 30)], 4)
            holes_row(d, x - w * 0.38, BASE - 20, x + w * 0.38, BASE - 20, 9, 2.2)
        ln(d, [(560, BASE), (562, BASE - 330)], 5)                    # estandarte
        shape(d, [(540, BASE - 330), (586, BASE - 330), (590, BASE - 270), (563, BASE - 252), (536, BASE - 270)], n=4)
        holes_row(d, 546, BASE - 300, 580, BASE - 300, 4, 3, shape='diamond')
        shape(d, [(548, BASE - 342), (563, BASE - 372), (578, BASE - 342)], n=4)
        for a, b in (((900, BASE - 6), (1020, BASE - 24)), ((900, BASE - 24), (1020, BASE - 6))):   # toras da fogueira
            stroke(d, [a, b], 14, 12)
        shape(d, [(690, BASE), (700, BASE - 34), (820, BASE - 38), (830, BASE)], n=6)               # tronco-banco
        spiral(d, 700, BASE - 18, 9, 1.2, 1.6, HOLE)
    return full(desenho)


def fogueira(k=0):
    """Chamas da fogueira do acampamento (4 formas para alternar): línguas assimétricas de pontas curvas."""
    im, d = canvas(W, H)
    r = np.random.default_rng(40 + k)
    for dx, h, w in ((0, 118, 24), (-30, 70, 17), (27, 86, 18), (-12, 50, 12), (14, 40, 10)):
        h *= float(r.uniform(0.8, 1.15))
        sw = float(r.uniform(-14, 14))
        cx, cy = 960 + dx, BASE - 22
        shape(d, [(cx - w, cy), (cx - w * 1.1, cy - h * 0.3), (cx - w * 0.4 + sw * 0.3, cy - h * 0.62), (cx + sw * 0.8 - 4, cy - h * 0.86),
                  (cx + sw, cy - h), (cx + sw * 0.5 + 6, cy - h * 0.72), (cx + w * 0.7, cy - h * 0.42), (cx + w, cy - h * 0.12), (cx + w * 0.8, cy)],
              (255, 226, 160, 255), n=10)
    return Static(down(im))


def floco():
    """Floco de neve: pontinho de papel recortado (desenhado em (100, 100))."""
    def desenho(d):
        ell(d, 100, 100, 3.6, 3.6)
        for k in range(6):
            a = k * math.pi / 3
            ln(d, [(100, 100), (100 + 6 * math.cos(a), 100 + 6 * math.sin(a))], 1.2)
    return full(desenho)


_CABECA = [(-10, 4), (-12, -16), (-22, -30), (-26, -50), (-20, -70), (-4, -82), (14, -80), (24, -68), (26, -56), (36, -44), (28, -40),
           (27, -32), (32, -27), (26, -24), (24, -16), (16, -6), (8, 0), (10, 6)]


def _racha_busto(cx):
    b = BASE
    return [(cx + 8, b - 372), (cx - 2, b - 342), (cx + 14, b - 312), (cx + 2, b - 284), (cx + 16, b - 254), (cx + 4, b - 218),
            (cx + 18, b - 186), (cx + 6, b - 160)]                   # da cabeça ao peito, acima da coluna


def busto(cx, mulher=False, semente=0, racha=0.0):
    """Busto romano sobre um pedestal (herma), de perfil. `mulher` troca barba e cachos por coque e tiara.

    `racha` 0..1: uma rachadura vazada desce da cabeça ao peito (ver `busto_brasa` para a gelatina âmbar).
    """
    rr = np.random.default_rng(semente)
    def desenho(d):
        b = BASE
        shape(d, [(cx - 66, b), (cx + 66, b), (cx + 60, b - 22), (cx - 60, b - 22)], n=4)              # base com moldura
        stroke(d, [(cx - 58, b - 12), (cx + 58, b - 12)], 2.4, 2.4, HOLE)
        poly(d, [(cx - 40, b - 22), (cx + 40, b - 22), (cx + 34, b - 150), (cx - 34, b - 150)])        # coluna da herma
        for k in range(3):
            stroke(d, [(cx - 18 + k * 18, b - 34), (cx - 16 + k * 18, b - 140)], 2.2, 2.2, HOLE)
        shape(d, [(cx - 54, b - 150), (cx + 54, b - 150), (cx + 48, b - 162), (cx - 48, b - 162)], n=4)
        shape(d, [(cx - 70, b - 166), (cx - 62, b - 214), (cx - 26, b - 236), (cx + 30, b - 236), (cx + 64, b - 212), (cx + 72, b - 166)], n=8)  # ombros
        for k in range(4):
            stroke(d, [(cx - 40 + k * 22, b - 226), (cx - 30 + k * 22, b - 196), (cx - 36 + k * 24, b - 170)], 2.6, 0.6, HOLE)
        s, ox, oy = 1.7, cx + 2, b - 236
        poly(d, cr([(ox + x * s, oy + y * s) for x, y in _CABECA], True, 12))
        shape(d, [(ox + 12 * s, oy - 58 * s), (ox + 20 * s, oy - 61 * s), (ox + 16 * s, oy - 55 * s)], HOLE, n=6)        # olho
        stroke(d, [(ox + 6 * s, oy - 66 * s), (ox + 14 * s, oy - 68 * s), (ox + 22 * s, oy - 65 * s)], 2.4, 0.6, HOLE)
        if mulher:
            ell(d, ox - 30 * s, oy - 56 * s, 13 * s, 12 * s)                                              # coque
            spiral(d, ox - 30 * s, oy - 56 * s, 9 * s, 1.6, 2.2, HOLE)
            for k in range(5):                                                                           # ondas do cabelo
                stroke(d, [(ox + (14 - k * 7) * s, oy - 78 * s), (ox + (6 - k * 7) * s, oy - 66 * s), (ox + (10 - k * 7) * s, oy - 54 * s)], 2.6, 0.8, HOLE)
            stroke(d, [(ox - 18 * s, oy - 80 * s), (ox + 4 * s, oy - 88 * s), (ox + 22 * s, oy - 80 * s)], 5, 3)    # tiara
            holes_row(d, ox - 12 * s, oy - 84 * s, ox + 16 * s, oy - 83 * s, 5, 1.6)
            ell(d, ox - 4 * s, oy - 38 * s, 2.6, 2.6, HOLE)                                              # brinco
        else:
            for k in range(7):                                                                           # cachos
                x, y = (-22 + k * 7 + float(rr.uniform(-2, 2))) * s, (-74 - 6 * math.sin(k / 2) + float(rr.uniform(-2, 2))) * s
                ell(d, ox + x, oy + y, 8 * s, 8 * s)
                spiral(d, ox + x, oy + y, 5 * s, 1.2, 1.6, HOLE, sign=1 if k % 2 else -1)
            if rr.uniform() < 0.75:                                                                      # barba
                for x, y in ((14, -10), (6, -6), (20, -16), (-2, -10)):
                    ell(d, ox + x * s, oy + y * s, 6 * s, 7 * s)
                    spiral(d, ox + x * s, oy + y * s, 3.6 * s, 1, 1.4, HOLE)
            spiral(d, ox - 6 * s, oy - 46 * s, 5 * s, 1.3, 1.8, HOLE)                                    # orelha
        if racha > 0:
            ln(d, _parcial(_racha_busto(cx), racha), 5, HOLE)
    return full(desenho)


def busto_brasa(q, cx=960):
    """Gelatina âmbar da rachadura do busto (mesmo traço de `busto(..., racha=q)`)."""
    def desenho(d):
        if q > 0:
            ln(d, _parcial(_racha_busto(cx), q), 5, AMBAR)
    return full(desenho)


def pergaminho(q, cx=960, y0=200, y1=440):
    """Rolo de pergaminho se abrindo entre dois cilindros (q = 0 fechado .. 1 aberto), com escrita vazada."""
    def desenho(d):
        w = 26 + 400 * q
        if q > 0.02:
            topo = [(x, y0 + 3 * math.sin(x / 40)) for x in range(int(cx - w), int(cx + w) + 1, 12)]
            fundo = [(x, y1 + 3 * math.sin(x / 40 + 1)) for x, _ in topo]
            poly(d, topo + fundo[::-1])
            rr = np.random.default_rng(3)
            for j in range(7):
                y = y0 + 34 + j * 30
                x = cx - 390
                while x < cx + 370:
                    L = float(rr.uniform(26, 70))
                    if cx - w + 18 < x and x + L < cx + w - 18:
                        stroke(d, [(x, y), (x + L * 0.5, y - 2), (x + L, y)], 3.2, 2.2, HOLE, n=4)
                    x += L + float(rr.uniform(10, 18))
        for x in (cx - w, cx + w):                                       # os dois cilindros
            shape(d, [(x - 13, y0 - 14), (x + 13, y0 - 14), (x + 15, y1 + 14), (x - 15, y1 + 14)], n=4)
            for y in (y0 - 26, y1 + 26):
                ell(d, x, y, 9, 13)
                ell(d, x, y, 3.5, 5, HOLE)
            stroke(d, [(x, y0 + 4), (x, y1 - 4)], 2, 2, HOLE)
    return full(desenho)


def bau(aberto=0.0, cx=960):
    """Baú de tesouro com reforços e fechadura vazada; `aberto` 0..1 gira a tampa para trás."""
    def desenho(d):
        b, w, h = BASE, 110, 120
        poly(d, [(cx - w, b - 6), (cx + w, b - 6), (cx + w, b - h), (cx - w, b - h)])
        for x in (cx - w + 8, cx + w - 22):
            poly(d, [(x, b), (x + 14, b), (x + 14, b - 8), (x, b - 8)])
        for x in (cx - 60, cx + 60):
            stroke(d, [(x, b - h + 4), (x, b - 10)], 4, 4, HOLE)
        holes_row(d, cx - w + 12, b - h + 14, cx + w - 12, b - h + 14, 12, 2.4)
        ell(d, cx, b - h + 46, 14, 16, HOLE)
        ell(d, cx, b - h + 46, 8, 10)
        poly(d, [(cx - 3, b - h + 50), (cx + 3, b - h + 50), (cx + 2, b - h + 60), (cx - 2, b - h + 60)], HOLE)
        a = math.radians(32 * aberto)                                   # a tampa sobe presa na dobradiça de trás (direita)
        hx, hy = cx + w + 6, b - h
        def T(x, y):
            return (hx + (x - hx) * math.cos(a) - (y - hy) * math.sin(a), hy + (x - hx) * math.sin(a) + (y - hy) * math.cos(a) - 10 * aberto)
        tampa = [T(cx - w - 6, b - h)] + [T(cx + w * math.cos(math.radians(t)), b - h - 46 * math.sin(math.radians(t))) for t in range(180, -1, -10)] + [T(cx + w + 6, b - h)]
        poly(d, tampa)
        for x in (cx - 60, cx + 60):
            ln(d, [T(x, b - h - 2), T(x, b - h - 40)], 4, HOLE)
        holes_row(d, *T(cx - w + 14, b - h - 8), *T(cx + w - 14, b - h - 8), 10, 2.2)
    return full(desenho)


def tesouro(i, cx=960, cy=BASE - 150):
    """Um dos tesouros do palácio, desenhado sobre a boca do baú: 0 cálice, 1 colar, 2 anel, 3 jarra, 4 moedas."""
    def desenho(d):
        if i == 0:
            shape(d, [(cx - 34, cy - 70), (cx + 34, cy - 70), (cx + 26, cy - 30), (cx + 6, cy - 14), (cx + 6, cy + 16), (cx + 26, cy + 26),
                      (cx - 26, cy + 26), (cx - 6, cy + 16), (cx - 6, cy - 14), (cx - 26, cy - 30)], n=4)
            holes_row(d, cx - 24, cy - 52, cx + 24, cy - 52, 6, 3, shape='diamond')
        elif i == 1:
            pts = [(cx + 60 * math.cos(math.radians(a)), cy - 40 + 52 * math.sin(math.radians(a))) for a in range(10, 171, 16)]
            stroke(d, pts, 3, 3)
            for x, y in pts:
                ell(d, x, y, 7, 7)
                ell(d, x, y, 2.4, 2.4, HOLE)
            shape(d, [(cx - 12, cy + 12), (cx, cy - 4), (cx + 12, cy + 12), (cx, cy + 34)], n=4)
            ell(d, cx, cy + 14, 4, 6, HOLE)
        elif i == 2:
            ell(d, cx, cy, 30, 30)
            ell(d, cx, cy, 20, 20, HOLE)
            shape(d, [(cx - 16, cy - 26), (cx, cy - 52), (cx + 16, cy - 26), (cx, cy - 18)], n=4)
            ell(d, cx, cy - 32, 5, 7, HOLE)
        elif i == 3:
            shape(d, [(cx - 10, cy - 70), (cx + 10, cy - 70), (cx + 8, cy - 54), (cx + 30, cy - 20), (cx + 26, cy + 20), (cx + 10, cy + 30),
                      (cx - 10, cy + 30), (cx - 26, cy + 20), (cx - 30, cy - 20), (cx - 8, cy - 54)], n=6)
            stroke(d, [(cx + 10, cy - 60), (cx + 40, cy - 52), (cx + 30, cy - 18)], 4, 3)
            holes_row(d, cx - 22, cy - 6, cx + 22, cy - 6, 6, 2.4)
            stroke(d, [(cx - 24, cy + 6), (cx + 24, cy + 6)], 2, 2, HOLE)
        else:
            for k in range(5):
                y = cy + 20 - k * 12
                ell(d, cx + (k % 2) * 6, y, 34, 9)
                stroke(d, [(cx - 26 + (k % 2) * 6, y), (cx + 26 + (k % 2) * 6, y)], 1.6, 1.6, HOLE)
    return full(desenho)


# ---------------- vídeo 1 · bloco 3 (o diário) ----------------
def risco(q, x0, x1, y):
    """Traço de tinta que risca uma palavra da esquerda para a direita (q = 0..1 do comprimento)."""
    def desenho(d):
        if q > 0:
            x = x0 + (x1 - x0) * q
            stroke(d, [(x0, y + 4), ((x0 + x) / 2, y - 2), (x, y - 6)], 7, 5)
    return full(desenho)


def anfiteatro():
    """O anfiteatro visto de fora: fachada curva com três ordens de arcos vazados e o ático com janelas.

    Os arcos estreitam perto das pontas (a fachada é uma elipse em perspectiva). Nenhuma pessoa: vazio.
    """
    def desenho(d):
        b, R = BASE, 720
        cotas = (0, 150, 280, 400, 470)                                 # base, ordens 1-3, topo do ático
        def x_de(t):
            return 960 + R * math.sin(t)
        def topo(x):
            return b - cotas[-1] + 26 * ((x - 960) / R) ** 2               # a borda de cima "dobra" na curva
        bordas = [(x_de(math.radians(a)), topo(x_de(math.radians(a)))) for a in range(-72, 73, 4)]
        poly(d, [(x_de(math.radians(-72)), b)] + bordas + [(x_de(math.radians(72)), b)])
        for k in (1, 2, 3):                                             # cornijas entre as ordens
            y = b - cotas[k]
            pts = [(x_de(math.radians(a)), y + 18 * ((x_de(math.radians(a)) - 960) / R) ** 2) for a in range(-70, 71, 5)]
            ln(d, pts, 3.4, HOLE)
        for k in (0, 1, 2):                                             # arcos
            y0, y1 = b - cotas[k] - 14, b - cotas[k + 1] + 16
            for a in range(-66, 67, 8):
                t = math.radians(a)
                x, w = x_de(t), 30 * math.cos(t)
                curva = 18 * ((x - 960) / R) ** 2
                r = w
                poly(d, [(x - w, y0 + curva), (x + w, y0 + curva), (x + w, y1 + r + curva), (x - w, y1 + r + curva)], HOLE)
                d.pieslice([*P(x - w, y1 + curva), *P(x + w, y1 + 2 * r + curva)], 180, 360, fill=HOLE)
        y0 = b - cotas[3] - 22                                          # ático: janelinhas alternadas
        for a in range(-62, 63, 16):
            t = math.radians(a)
            x, w = x_de(t), 12 * math.cos(t)
            curva = 22 * ((x - 960) / R) ** 2
            poly(d, [(x - w, y0 + curva), (x + w, y0 + curva), (x + w, y0 - 30 + curva), (x - w, y0 - 30 + curva)], HOLE)
    return full(desenho)


def linha_escrita(j, x0=600, x1=1320, y0=250, passo=78):
    """A mesma linha manuscrita (sempre a mesma: semente fixa), na linha `j` da página.

    Cursiva inclinada: letras com laço (e, l) e com arco (n, m), hastes altas de vez em quando.
    """
    rr = np.random.default_rng(77)
    y = y0 + j * passo
    def desenho(d):
        x = x0
        while x < x1 - 60:
            pts = []
            for _ in range(int(rr.integers(2, 7))):                    # letras da palavra
                tipo, w = int(rr.integers(0, 3)), float(rr.uniform(11, 17))
                h = float(rr.uniform(26, 36)) if tipo == 2 else float(rr.uniform(11, 16))
                for k in range(9):
                    t = k / 8
                    if tipo == 1:                                       # arco (n, m)
                        px, py = x + w * t, y - h * math.sin(math.pi * t)
                    else:                                               # laço (e) ou haste alta (l)
                        px, py = x + w * t - 0.45 * w * math.sin(2 * math.pi * t), y - h * (0.5 - 0.5 * math.cos(2 * math.pi * t))
                    pts.append((px + 0.3 * (y - py), py))               # inclinação da escrita
                x += w
            ln(d, pts, 3.2)
            x += float(rr.uniform(18, 28))
    return full(desenho)


# o imperador de toga em tamanho grande, parado (para o manto que tinge): mesmas formas do boneco
_TOGA = [(0, -188), (20, -184), (34, -150), (38, -100), (36, -40), (48, 30), (62, 110), (70, 160), (40, 172), (0, 168), (-40, 174),
         (-70, 166), (-60, 100), (-44, 20), (-38, -60), (-40, -130), (-28, -170)]
_PALLA = [(-26, -176), (-56, -150), (-70, -80), (-78, 0), (-74, 80), (-56, 40), (-44, -40), (-30, -120), (-6, -160)]
_DOBRAS = [[(30, -176), (6, -120), (-24, -60), (-48, 20), (-60, 120)]] + \
          [[(10 + k * 9, -60 + k * 6), (16 + k * 10, 40), (24 + k * 10, 140)] for k in range(4)]
_BRACO = [(-10, -4), (8, -6), (12, 20), (9, 52), (7, 80), (-6, 80), (-10, 50), (-13, 20)]
_MAO = [(-7, -2), (7, -2), (8, 30), (6, 62), (12, 70), (16, 78), (24, 82), (20, 88), (8, 92), (-2, 90), (-8, 78), (-6, 62), (-8, 30)]


def _figura_toga(d, cx, s, cor_manto, cor_resto, cor_furo):
    oy = BASE - 174 * s
    def Q(pts, dx=0, dy=0):
        return [(cx + (x + dx) * s, oy + (y + dy) * s) for x, y in pts]
    if cor_resto is not None:
        for x in (-14, 12):                                                         # pés
            shape(d, Q([(x - 10, 160), (x + 26, 160), (x + 40, 172), (x - 10, 174)]), cor_resto, n=4)
    shape(d, Q(_TOGA), cor_manto)
    shape(d, Q(_PALLA), cor_manto)
    for pts in _DOBRAS:
        stroke(d, Q(pts), 3.2 * s * 0.8, 0.6 * s, cor_furo)
    if cor_resto is not None:
        ox, oy2 = cx + 2 * s, oy - 184 * s                                           # cabeça e coroa de louros
        shape(d, [(ox + x * s, oy2 + y * s) for x, y in _CABECA], cor_resto, n=12)
        shape(d, [(ox + 12 * s, oy2 - 58 * s), (ox + 20 * s, oy2 - 61 * s), (ox + 16 * s, oy2 - 55 * s)], cor_furo, n=6)
        for k in range(9):
            a = math.radians(200 + k * 17)
            serrated(d, ox + (-2 + 26 * math.cos(a)) * s, oy2 + (-54 + 28 * math.sin(a)) * s,
                     math.degrees(a) + 70 * (1 if k < 5 else -1) - 90, 18 * s, 0.32)
    braco = Q(_BRACO, 10, -162)
    mao = Q(_MAO, 10, -162 + 78)
    shape(d, braco, cor_resto if cor_resto is not None else cor_furo)              # braço da frente, solto ao lado
    shape(d, mao, cor_resto if cor_resto is not None else cor_furo)


def figura_toga(cx=960, s=2.0):
    """O imperador grande, de pé e parado: toga, palla, braço solto e coroa de louros (formas do boneco)."""
    return full(lambda d: _figura_toga(d, cx, s, INK, INK, HOLE))


def toga_tinta(q, cx=960, s=2.0, chao=835):
    """Gelatina do manto tingido de cima para baixo (q = 0..1 da altura); o braço fica de fora e a tinta
    para em `chao` (o monte de capim da frente cobre os pés)."""
    def desenho(d):
        if q <= 0:
            return
        _figura_toga(d, cx, s, (255, 255, 255, 255), None, (0, 0, 0, 0))     # a cor vem da gelatina
        oy = BASE - 174 * s
        y = oy - 188 * s + q * 362 * s
        d.rectangle([*P(0, min(y, chao)), *P(W, H)], fill=(0, 0, 0, 0))
    return full(desenho)


# ---------------- vídeo 1 · bloco 4 (a lição) ----------------
def _celular_pts(cx, cy, e, inset=0.0):
    w, h, c = 110 * e - inset, 220 * e - inset, 16 * e                  # cantos chanfrados (pedra cortada)
    return [(cx - w + c, cy - h), (cx + w - c, cy - h), (cx + w, cy - h + c), (cx + w, cy + h - c), (cx + w - c, cy + h),
            (cx - w + c, cy + h), (cx - w, cy + h - c), (cx - w, cy - h + c)]


def celular(cx=1150, cy=540, e=1.0):
    """Celular recortado: corpo de cantos chanfrados, tela vazada, alto-falante e câmera."""
    def desenho(d):
        poly(d, _celular_pts(cx, cy, e))
        w, h = 110 * e - 12 * e, 220 * e - 40 * e
        poly(d, [(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)], HOLE)
        stroke(d, [(cx - 22 * e, cy - 202 * e), (cx + 22 * e, cy - 202 * e)], 4 * e, 4 * e, HOLE)
        ell(d, cx + 40 * e, cy - 202 * e, 4 * e, 4 * e, HOLE)
        ell(d, cx, cy + 202 * e, 9 * e, 9 * e, HOLE)
        ell(d, cx, cy + 202 * e, 5 * e, 5 * e)
    return full(desenho)


def celular_tela(cx=1150, cy=540, e=1.0):
    """A tela do celular (para a gelatina âmbar: o brilho de coisa nova)."""
    def desenho(d):
        w, h = 110 * e - 12 * e, 220 * e - 40 * e
        poly(d, [(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)], (255, 255, 255, 255))
    return full(desenho)


def redemoinho(fase, cx=540, cy=250, r=62):
    """Redemoinho de pensamentos sobre a cabeça: duas espirais girando (fase 0..1 dá uma volta)."""
    def desenho(d):
        for k in (0, 1):
            a0 = 2 * math.pi * fase + k * math.pi
            pts = [(cx + r * (0.12 + 0.88 * t) * math.cos(a0 + 3.2 * math.pi * t), cy + 0.55 * r * (0.12 + 0.88 * t) * math.sin(a0 + 3.2 * math.pi * t))
                   for t in [j / 30 for j in range(31)]]
            stroke(d, pts, 1.5, 6.5)
        for k in range(3):
            a = 2 * math.pi * (fase * 1.5 + k / 3)
            ell(d, cx + 1.15 * r * math.cos(a), cy + 0.62 * r * math.sin(a), 4, 4)
    return full(desenho)


def conta(q, cx=1280, y0=300, altura=420):
    """A conta a pagar: papel que desenrola para baixo de um rolinho (q = 0..1), com linhas, total e carimbo."""
    def desenho(d):
        w, y1 = 92, y0 + altura * q
        if q > 0.02:
            poly(d, [(cx - w, y0), (cx + w, y0), (cx + w, y1 - 8), (cx + w - 10, y1), (cx + w - 22, y1 - 8), (cx + w - 34, y1),
                     (cx - w + 34, y1), (cx - w + 22, y1 - 8), (cx - w + 10, y1), (cx - w, y1 - 8)])
            for j in range(12):
                y = y0 + 40 + j * 28
                if y > y1 - 30:
                    break
                L = 70 if j % 3 else 120
                stroke(d, [(cx - w + 18, y), (cx - w + 18 + L, y)], 3, 3, HOLE)
                stroke(d, [(cx + w - 48, y), (cx + w - 18, y)], 3, 3, HOLE)
            if q > 0.85:                                                    # total e carimbo
                yt = y0 + altura - 70
                stroke(d, [(cx - w + 14, yt - 18), (cx + w - 14, yt - 18)], 2, 2, HOLE)
                ell(d, cx + 30, yt + 18, 30, 30, HOLE)
                ell(d, cx + 30, yt + 18, 23, 23)
                stroke(d, [(cx + 12, yt + 4), (cx + 48, yt + 32)], 4, 4, HOLE)
        shape(d, [(cx - w - 14, y0 - 16), (cx + w + 14, y0 - 16), (cx + w + 14, y0 + 6), (cx - w - 14, y0 + 6)], n=4)   # rolinho
        for x in (cx - w - 22, cx + w + 22):
            ell(d, x, y0 - 5, 9, 13)
    return full(desenho)


def banquinho(cx=540, altura=92):
    """Banquinho de três pés (para o homem sentado na insônia)."""
    def desenho(d):
        b, h = BASE, altura
        shape(d, [(cx - 70, b - h), (cx + 70, b - h), (cx + 64, b - h + 14), (cx - 64, b - h + 14)], n=4)
        for x0, x1 in ((cx - 54, cx - 70), (cx + 54, cx + 70), (cx, cx + 4)):
            stroke(d, [(x0, b - h + 12), (x1, b)], 9, 7)
        stroke(d, [(cx - 62, b - h * 0.4), (cx + 62, b - h * 0.4)], 4, 4)
    return full(desenho)


_FENDA = [(940, 60), (956, 140), (930, 230), (962, 330), (938, 430), (970, 530), (944, 640), (966, 760), (948, BASE)]


def fenda(q):
    """Rachadura que desce pelo lençol e separa a família (q = 0..1 do comprimento)."""
    def desenho(d):
        if q > 0:
            pts = _parcial(_FENDA, q)
            ln(d, pts, 7)
            for (x, y), s in zip(pts[1:-1], (1, -1, 1, -1, 1, -1, 1)):         # galhinhos da rachadura
                ln(d, [(x, y), (x + s * 34, y + 30)], 3)
    return full(desenho)


def vaso(cx=960):
    """O vaso furado: grande pithos sobre um tripé, faixa de meandro vazada e uma fresta no fundo."""
    def desenho(d):
        corpo = [(cx - 64, 330), (cx + 64, 330), (cx + 58, 362), (cx + 150, 410), (cx + 236, 480), (cx + 250, 540), (cx + 226, 620),
                 (cx + 150, 700), (cx + 90, 738), (cx - 90, 738), (cx - 150, 700), (cx - 226, 620), (cx - 250, 540), (cx - 236, 480),
                 (cx - 150, 410), (cx - 58, 362)]
        shape(d, corpo, n=8)
        ell(d, cx, 330, 80, 14)                                               # boca
        ell(d, cx, 330, 58, 8, HOLE)
        stroke(d, [(cx - 200, 462), (cx + 200, 462)], 3, 3, HOLE)
        stroke(d, [(cx - 236, 532), (cx + 236, 532)], 3, 3, HOLE)
        for k in range(12):                                                   # meandro (gregas)
            x = cx - 198 + k * 34
            poly(d, [(x, 520), (x, 476), (x + 24, 476), (x + 24, 500), (x + 12, 500), (x + 12, 488), (x + 6, 488), (x + 6, 520)], HOLE)
        holes_row(d, cx - 200, 600, cx + 200, 600, 14, 4)
        shape(d, [(cx + 22, 712), (cx + 36, 700), (cx + 44, 724), (cx + 38, 738), (cx + 28, 738)], HOLE, n=4)   # a fresta
        for x0, x1 in ((cx - 70, cx - 120), (cx + 70, cx + 120), (cx - 10, cx - 8)):                         # tripé
            stroke(d, [(x0, 730), (x1, BASE)], 12, 9)
        stroke(d, [(cx - 100, 840), (cx + 100, 840)], 5, 5)
    return full(desenho)


def balanca(ang, cx=960, topo=360):
    """Balança de pratos: coluna, travessão inclinado `ang` graus (positivo = direita desce),
    moedas no prato da esquerda e um pão no da direita."""
    def desenho(d):
        b = BASE
        shape(d, [(cx - 110, b), (cx + 110, b), (cx + 90, b - 30), (cx - 90, b - 30)], n=4)
        poly(d, [(cx - 18, b - 30), (cx + 18, b - 30), (cx + 12, topo + 10), (cx - 12, topo + 10)])
        for k in range(4):
            stroke(d, [(cx - 6 + k * 4, b - 50), (cx - 4 + k * 4, topo + 40)], 1.6, 1.6, HOLE)
        ell(d, cx, topo, 16, 16)
        ell(d, cx, topo, 6, 6, HOLE)
        shape(d, [(cx - 6, topo - 10), (cx, topo - 60), (cx + 6, topo - 10)], n=4)          # fiel
        a = math.radians(ang)
        ca, sa = math.cos(a), math.sin(a)
        L = 300
        ln(d, [(cx - L * ca, topo - L * sa), (cx + L * ca, topo + L * sa)], 10)
        for s in (-1, 1):
            hx, hy = cx + s * L * ca, topo + s * L * sa
            ell(d, hx, hy, 9, 9)
            py = hy + 250
            for dx in (-80, 0, 80):
                ln(d, [(hx, hy), (hx + dx, py)], 2.4)
            shape(d, [(hx - 92, py), (hx + 92, py), (hx + 70, py + 24), (hx, py + 34), (hx - 70, py + 24)], n=6)
            if s < 0:                                                            # moedas
                for k in range(5):
                    ell(d, hx + (k % 2) * 8 - 4, py - 8 - k * 11, 40, 8)
                    stroke(d, [(hx - 30 + (k % 2) * 8, py - 8 - k * 11), (hx + 22 + (k % 2) * 8, py - 8 - k * 11)], 1.6, 1.6, HOLE)
            else:                                                                # pão
                shape(d, [(hx - 66, py - 2), (hx - 58, py - 40), (hx - 20, py - 62), (hx + 20, py - 62), (hx + 58, py - 40), (hx + 66, py - 2)], n=8)
                for k in range(3):
                    stroke(d, [(hx - 34 + k * 30, py - 50), (hx - 22 + k * 30, py - 30)], 4, 2, HOLE)
    return full(desenho)

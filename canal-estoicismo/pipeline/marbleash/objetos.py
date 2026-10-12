"""Objetos romanos recortados: cada função devolve um sprite (Static) do tamanho do quadro, na posição
em que o objeto fica em cena. Para virar sombra, use `quadro.Camada(objetos.templo, ...)`.

Objetos em três quartos (templo, mesa) fogem para o ponto de fuga `traco.VP`, à direita fora da tela.
"""
from __future__ import annotations

import math

from PIL import ImageFont

from . import config
from .config import H, S, W
from .traco import (BASE, FLOOR, HOLE, INK, ROD, P, Static, canvas, cr, down, ell, full, holes_row, layer, leaf, ln,
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
def letreiro(texto, fonte='CormorantGaramond-MediumItalic.ttf', tamanho=52, cx=960, y=150, cor=(60, 34, 16, 255)):
    """Texto centrado em cx, com o topo em y (ex.: o sussurro "not yet... not enough.").

    Padrão do canal: Cormorant Garamond itálico (citações), Cinzel (nomes), Inter (créditos).
    """
    f = ImageFont.truetype(config.fonte(fonte), int(tamanho * S))

    def desenho(d):
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

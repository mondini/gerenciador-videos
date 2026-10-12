"""Kit de recorte: o "papel" e a "tesoura" dos bonecos e do cenário.

Tudo é desenhado em 2x (config.S) com PIL e reduzido, para bordas suaves. Coordenadas sempre na
escala do vídeo (1920x1080). Cores: INK é o papel preto; HOLE é um furo (transparente), por onde a luz
passa. Um desenho vira:
  - um sprite (Static): imagem RGBa pré-multiplicada + posição;
  - depois uma máscara de sombra (0 = luz livre, ~1 = sombra), via `mascara()`.

As funções aqui são as do padrão aprovado (curvas Catmull-Rom, cortes que afinam como tesoura).
Não mude as fórmulas sem conferir os stills de referência: o desenho depende de cada conta.
"""
from __future__ import annotations

import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .cache import em_disco
from .config import H, S, W

INK = (14, 10, 7, 255)          # papel preto do recorte
HOLE = (0, 0, 0, 0)             # furo (a luz passa)
BRASS = (182, 142, 76, 255)     # rebite de latão
ROD = (34, 22, 12, 230)         # vareta
FLOOR = 900                     # linha dos pés dos bonecos
BASE = FLOOR + 30               # chão do palco
VP = (2600, 600)                # ponto de fuga fora da tela, à direita (câmera levemente à esquerda)


# ---------------- desenho básico (em 2x) ----------------
def canvas(w, h):
    """Folha transparente w x h (em pixels do vídeo), já em 2x."""
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def P(x, y, ox=0, oy=0):
    return ((x + ox) * S, (y + oy) * S)


def poly(d, pts, col=INK, ox=0, oy=0):
    d.polygon([P(x, y, ox, oy) for x, y in pts], fill=col)


def ell(d, cx, cy, rx, ry, col=INK, ox=0, oy=0):
    d.ellipse([*P(cx - rx, cy - ry, ox, oy), *P(cx + rx, cy + ry, ox, oy)], fill=col)


def ln(d, pts, w, col=INK, ox=0, oy=0):
    d.line([P(x, y, ox, oy) for x, y in pts], fill=col, width=max(1, int(w * S)), joint='curve')


def holes_row(d, x0, y0, x1, y1, n, r, ox=0, oy=0, shape='dot'):
    """Fileira de n furos (bolinhas ou losangos) entre (x0, y0) e (x1, y1)."""
    for i in range(n):
        f = (i + 0.5) / n
        x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        if shape == 'dot':
            ell(d, x, y, r, r, HOLE, ox, oy)
        else:
            poly(d, [(x, y - r * 1.6), (x + r, y), (x, y + r * 1.6), (x - r, y)], HOLE, ox, oy)


def leaf(d, x, y, ang, L, col, ox=0, oy=0):
    """Folha simples em losango (usada nos furos dos ciprestes)."""
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    pts = [(x, y), (x + c * L * 0.5 - s * L * 0.22, y + s * L * 0.5 + c * L * 0.22), (x + c * L, y + s * L),
           (x + c * L * 0.5 + s * L * 0.22, y + s * L * 0.5 - c * L * 0.22)]
    poly(d, pts, col, ox, oy)


def rivet(d, x, y, ox, oy):
    """Rebite de latão nas articulações."""
    ell(d, x, y, 4.2, 4.2, BRASS, ox, oy)
    ell(d, x, y, 1.6, 1.6, (90, 64, 30, 255), ox, oy)


# ---------------- curvas ----------------
def cr(pts, closed=True, n=10):
    """Curva Catmull-Rom passando pelos pontos."""
    P_ = list(pts)
    out = []
    m = len(P_)
    rng_ = range(m) if closed else range(m - 1)
    for i in rng_:
        p0 = P_[(i - 1) % m] if closed else P_[max(i - 1, 0)]
        p1, p2 = P_[i], P_[(i + 1) % m]
        p3 = P_[(i + 2) % m] if closed else P_[min(i + 2, m - 1)]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not closed:
        out.append(P_[-1])
    return out


def shape(d, pts, col=INK, ox=0, oy=0, n=10):
    """Forma fechada de contorno curvo (pontos de controle Catmull-Rom)."""
    poly(d, cr(pts, True, n), col, ox, oy)


def stroke(d, pts, w0, w1, col=INK, ox=0, oy=0, n=10):
    """Traço curvo que afina de w0 para w1 (corte de tesoura)."""
    c = cr(pts, False, n)
    L, R = [], []
    for i, (x, y) in enumerate(c):
        a, b = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        mm = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / max(len(c) - 1, 1)) / 2
        L.append((x - dy / mm * w, y + dx / mm * w))
        R.append((x + dy / mm * w, y - dx / mm * w))
    poly(d, L + R[::-1], col, ox, oy)


def spiral(d, cx, cy, r0, turns, w, col=HOLE, ox=0, oy=0, sign=1):
    """Espiral (cachos, volutas, nós da madeira)."""
    pts = [(cx + (r0 * (1 - k / 60)) * math.cos(sign * k / 60 * turns * 6.283),
            cy + (r0 * (1 - k / 60)) * math.sin(sign * k / 60 * turns * 6.283)) for k in range(61)]
    ln(d, pts, w, col, ox, oy)


def toward(p, f):
    """Move o ponto p uma fração f em direção ao ponto de fuga (perspectiva de três quartos)."""
    return (p[0] + (VP[0] - p[0]) * f, p[1] + (VP[1] - p[1]) * f)


# ---------------- vegetação ----------------
def tuft(d, g, x, y, ang, L, n=13, spread=120, w=3.2):
    """Tufo de agulhas de pinheiro saindo de (x, y). `g` é o gerador aleatório (numpy)."""
    for i in range(n):
        a = math.radians(ang + spread * (i / (n - 1) - 0.5) + float(g.uniform(-6, 6)))
        l = L * float(g.uniform(0.65, 1.0))
        bend = float(g.uniform(-0.12, 0.12))
        mx, my = x + math.cos(a + bend) * l * 0.5, y + math.sin(a + bend) * l * 0.5
        stroke(d, [(x, y), (mx, my), (x + math.cos(a) * l, y + math.sin(a) * l)], w, 0.4, n=6)


def ivy(d, x, y, ang, L):
    """Folha de hera de cinco pontas, com nervuras vazadas."""
    a = math.radians(ang)
    c, s_ = math.cos(a), math.sin(a)
    T = lambda u, v: (x + c * u - s_ * v, y + s_ * u + c * v)
    pts = [T(0, 0), T(L * 0.15, L * 0.18), T(L * 0.22, L * 0.52), T(L * 0.4, L * 0.32), T(L * 0.6, L * 0.48), T(L * 0.62, L * 0.2),
           T(L * 1.0, 0), T(L * 0.62, -L * 0.2), T(L * 0.6, -L * 0.48), T(L * 0.4, -L * 0.32), T(L * 0.22, -L * 0.52), T(L * 0.15, -L * 0.18)]
    poly(d, pts)
    for v in ((L * 0.85, 0), (L * 0.5, L * 0.36), (L * 0.5, -L * 0.36), (L * 0.2, L * 0.4), (L * 0.2, -L * 0.4)):
        stroke(d, [T(L * 0.08, 0), T(v[0] * 0.6, v[1] * 0.6), T(*v)], 1.6, 0.3, HOLE, n=4)


def serrated(d, x, y, ang, L, wid=0.36):
    """Folha serrilhada com nervura central e laterais vazadas."""
    a = math.radians(ang)
    c, s_ = math.cos(a), math.sin(a)
    T = lambda u, v: (x + c * u - s_ * v, y + s_ * u + c * v)
    up, dn = [], []
    for k in range(13):
        u = k / 12
        half = math.sin(math.pi * u) ** 0.8 * L * wid
        tooth = (L * 0.035 if k % 2 else 0)
        up.append(T(u * L, half + tooth))
        dn.append(T(u * L, -half - tooth))
    poly(d, up + dn[::-1])
    stroke(d, [T(L * 0.05, 0), T(L * 0.5, L * 0.015), T(L * 0.92, 0)], 2.2, 0.5, HOLE, n=5)
    for u in (0.25, 0.4, 0.55, 0.7, 0.82):
        for sg in (1, -1):
            stroke(d, [T(L * u, 0), T(L * (u + 0.1), sg * L * wid * 0.45), T(L * (u + 0.16), sg * L * wid * 0.7)], 1.4, 0.3, HOLE, n=4)


def flower(d, x, y, r):
    """Flor de oito pétalas com miolo vazado."""
    for k in range(8):
        a = k * math.pi / 4
        tip = (x + r * 1.9 * math.cos(a), y + r * 1.9 * math.sin(a))
        shape(d, [(x + r * 0.6 * math.cos(a - 0.35), y + r * 0.6 * math.sin(a - 0.35)), (x + r * 1.3 * math.cos(a - 0.22), y + r * 1.3 * math.sin(a - 0.22)), tip,
                  (x + r * 1.3 * math.cos(a + 0.22), y + r * 1.3 * math.sin(a + 0.22)), (x + r * 0.6 * math.cos(a + 0.35), y + r * 0.6 * math.sin(a + 0.35))], n=3)
        stroke(d, [(x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a)), (x + r * 1.5 * math.cos(a), y + r * 1.5 * math.sin(a))], 1.4, 0.4, HOLE, n=3)
    ell(d, x, y, r * 0.75, r * 0.75)
    ell(d, x, y, r * 0.4, r * 0.4, HOLE)
    for k in range(6):
        a = k * math.pi / 3
        ell(d, x + r * 0.4 * math.cos(a), y + r * 0.4 * math.sin(a), 1.4, 1.4)


# ---------------- sprites ----------------
def down(im):
    """Reduz o desenho de 2x para 1x (RGBa pré-multiplicado, LANCZOS)."""
    return im.convert('RGBa').resize((im.size[0] // S, im.size[1] // S), Image.LANCZOS)


def to_arr(im_small):
    return np.asarray(im_small).astype(np.float32) / 255.0     # RGBa pré-multiplicado


class Static:
    """Sprite: array RGBa pré-multiplicado recortado ao conteúdo + canto superior esquerdo (x0, y0)."""

    def __init__(self, im_small, x0=0, y0=0):
        a = to_arr(im_small)
        ys, xs = np.nonzero(a[..., 3] > 0.002)
        if len(ys):
            y0_, y1_, x0_, x1_ = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            a = np.ascontiguousarray(a[y0_:y1_, x0_:x1_])
            x0 += x0_
            y0 += y0_
        self.a = a
        self.x0, self.y0 = x0, y0
        self.h, self.w = self.a.shape[:2]


def comp(fr, sp, alpha=1.0, dx=0, dy=0, ymax=None):
    """Compõe o sprite sobre o quadro RGB `fr` (float32, H x W x 3), na posição (x0 + dx, y0 + dy)."""
    if alpha <= 0.003:
        return
    x0, y0 = int(round(sp.x0 + dx)), int(round(sp.y0 + dy))
    fx0, fy0 = max(0, x0), max(0, y0)
    fx1, fy1 = min(W, x0 + sp.w), min(H if ymax is None else ymax, y0 + sp.h)
    if fx1 <= fx0 or fy1 <= fy0:
        return
    src = sp.a[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
    reg = fr[fy0:fy1, fx0:fx1]
    a = src[..., 3:4] * alpha
    reg *= (1 - a)
    reg += src[..., :3] * alpha


def full(draw_fn):
    """Desenha numa folha do tamanho do quadro e devolve o sprite."""
    im, d = canvas(W, H)
    draw_fn(d)
    return Static(down(im))


def layer(draw_fn, blur=0.0):
    """Como `full`, com desfoque opcional aplicado ainda em 2x (usado no fundo distante)."""
    im, d = canvas(W, H)
    draw_fn(d)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur * 2))
    return Static(down(im))


# ---------------- máscaras de sombra ----------------
def mascara(*sprites, dx=0, dy=0):
    """Máscara de sombra do tamanho do quadro (0 = luz livre) a partir de sprites."""
    fr = np.ones((H, W, 3), np.float32)
    for sp in sprites:
        comp(fr, sp, 1.0, dx, dy)
    return np.ascontiguousarray(np.clip(1 - fr.mean(-1), 0, 1))


def borrar(m, s):
    """Desfoque gaussiano (sigma s, em pixels). s = 0 devolve a própria máscara."""
    return cv2.GaussianBlur(m, (0, 0), s) if s > 0 else m


def raio_borrao(s: float) -> int:
    """Raio do núcleo que o OpenCV usa para o sigma s (float32): além dele o desfoque é exatamente zero."""
    return (int(round(s * 8 + 1)) | 1) // 2 if s > 0 else 0


def retangulo(m):
    """Retângulo (x0, y0, x1, y1) onde a máscara não é zero, ou None."""
    ys = np.nonzero(m.any(1))[0]
    if len(ys) == 0:
        return None
    xs = np.nonzero(m.any(0))[0]
    return int(xs[0]), int(ys[0]), int(xs[-1]) + 1, int(ys[-1]) + 1


@em_disco
def mascara_camada(arte, args, desfoque, posicao):
    """Máscara de sombra já desfocada de uma peça do elenco + o retângulo onde ela existe."""
    sp = arte(*args)
    sps = sp if isinstance(sp, (tuple, list)) else (sp,)
    m = borrar(mascara(*sps, dx=posicao[0], dy=posicao[1]), desfoque)
    return m, retangulo(m)


class NullDraw:
    """Folha "de mentira": aceita os comandos de desenho e não desenha nada.

    Serve para reproduzir a sequência de sorteios aleatórios de um desenho sem gastar tempo desenhando.
    """

    def polygon(self, *a, **k):
        pass

    def ellipse(self, *a, **k):
        pass

    def line(self, *a, **k):
        pass

    def arc(self, *a, **k):
        pass

    def chord(self, *a, **k):
        pass

    def text(self, *a, **k):
        pass

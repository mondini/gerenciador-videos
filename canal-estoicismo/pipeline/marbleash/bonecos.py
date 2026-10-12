"""Bonecos articulados de perfil (cabeça, braços, antebraços, pernas), com rebites e vareta.

Cada peça (Part) é desenhada uma vez em volta do seu pivô; o boneco (Puppet) monta as peças a cada
quadro conforme a pose: um dicionário {peça: ângulo em graus}, somado ao ângulo da peça-mãe.

Peças: torso, head, uarmB/farmB (braço e antebraço de trás), uarmF/farmF (da frente), legB, legF.
"""
from __future__ import annotations

import math
from collections import OrderedDict
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw

from .config import H, W
from .traco import (HOLE, INK, ROD, P, Static, canvas, comp, down, ell, rivet, serrated, shape, spiral,
                    stroke)


class _Pos:
    """Sprite já girado/escalado, reaproveitado entre quadros (mesma imagem, outra posição)."""
    __slots__ = ('a', 'x0', 'y0', 'h', 'w')

    def __init__(self, a, x0, y0):
        self.a, self.x0, self.y0 = a, x0, y0
        self.h, self.w = a.shape[:2]


class Part:
    """Uma peça do boneco, desenhada com o pivô no centro de uma folha 2r x 2r."""

    def __init__(self, name, r, draw_fn, parent=None, attach=(0, 0)):
        im, d = canvas(2 * r, 2 * r)
        draw_fn(d, r, r)            # pivô em (r, r)
        self.img = down(im)
        self.r = r
        self.name = name
        self.parent = parent
        self.attach = attach
        self._giros = OrderedDict()

    def __getstate__(self):
        st = self.__dict__.copy()
        st['_giros'] = OrderedDict()
        return st

    def sprite(self, ang, scale, x, y):
        """Sprite da peça girada `ang` graus e escalada, com o canto da folha em (x, y)."""
        chave = (ang, scale)
        g = self._giros.get(chave)
        if g is None:
            im = self.img.rotate(-ang, resample=Image.BICUBIC, center=(self.r, self.r))
            if scale != 1.0:
                im = im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.BICUBIC)
            st = Static(im, 0, 0)
            g = (st.a, st.x0, st.y0)        # deslocamentos do recorte (inteiros numpy)
            self._giros[chave] = g
            if len(self._giros) > 64:
                self._giros.popitem(last=False)
        else:
            self._giros.move_to_end(chave)
        a, ox, oy = g
        return _Pos(a, x + ox, y + oy)


class Puppet:
    """Boneco articulado: peças, ordem de desenho (de trás para a frente) e pontos das varetas."""

    def __init__(self, parts, order, rods):
        self.parts = {p.name: p for p in parts}
        self.order = order
        self.rods = rods

    def pose(self, x, y, angles, scale=1.0):
        """Posição e ângulo de cada peça no quadro, com o pivô do torso em (x, y)."""
        world = {}

        def wp(name):
            if name in world:
                return world[name]
            p = self.parts[name]
            a = angles.get(name, 0.0)
            if p.parent is None:
                world[name] = ((x, y), a)
            else:
                (px, py), pa = wp(p.parent)
                r = math.radians(pa)
                ax, ay = p.attach[0] * scale, p.attach[1] * scale
                world[name] = ((px + ax * math.cos(r) - ay * math.sin(r), py + ax * math.sin(r) + ay * math.cos(r)), pa + a)
            return world[name]

        for n in self.parts:
            wp(n)
        return world

    def _vareta(self, world, x, scale):
        segs = []
        for name, (lx, ly) in self.rods:
            (px, py), pa = world[name]
            r = math.radians(pa)
            hx, hy = px + (lx * math.cos(r) - ly * math.sin(r)) * scale, py + (lx * math.sin(r) + ly * math.cos(r)) * scale
            segs.append(((hx, hy), (hx + (hx - x) * 0.25 + 30, H + 20)))
        bx0 = int(min(min(a[0], b[0]) for a, b in segs)) - 6
        bx1 = int(max(max(a[0], b[0]) for a, b in segs)) + 6
        by0 = int(min(a[1] for a, b in segs)) - 6
        im = Image.new('RGBA', (bx1 - bx0, H + 30 - by0), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for a, b in segs:
            d.line([(a[0] - bx0, a[1] - by0), (b[0] - bx0, b[1] - by0)], fill=ROD, width=3)
        return Static(im.convert('RGBa'), bx0, by0)

    def sprites(self, x, y, angles, scale=1.0, rods=True):
        """Sprites (vareta + peças, de trás para a frente) do boneco nesta pose."""
        world = self.pose(x, y, angles, scale)
        out = [self._vareta(world, x, scale)] if rods else []
        for name in self.order:
            p = self.parts[name]
            (px, py), pa = world[name]
            out.append(p.sprite(pa, scale, px - p.r * scale, py - p.r * scale))
        return out

    def draw(self, fr, x, y, angles, alpha=1.0, scale=1.0, rods=True):
        """Desenha o boneco sobre um quadro RGB inteiro (H x W x 3)."""
        for sp in self.sprites(x, y, angles, scale, rods):
            comp(fr, sp, alpha)

    def mascara(self, x, y, angles, scale=1.0, rods=True):
        """Máscara de sombra só na região que o boneco ocupa: (m, x0, y0), ou None se fora do quadro.

        Dá exatamente o mesmo resultado que desenhar num quadro inteiro e recortar (cada pixel é
        calculado igual), mas muito mais rápido.
        """
        sps = self.sprites(x, y, angles, scale, rods)
        rx0, ry0, rx1, ry1 = W, H, 0, 0
        for sp in sps:
            x0, y0 = int(round(sp.x0)), int(round(sp.y0))
            fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + sp.w), min(H, y0 + sp.h)
            if fx1 > fx0 and fy1 > fy0:
                rx0, ry0, rx1, ry1 = min(rx0, fx0), min(ry0, fy0), max(rx1, fx1), max(ry1, fy1)
        if rx1 <= rx0:
            return None
        fr = np.ones((ry1 - ry0, rx1 - rx0, 3), np.float32)
        for sp in sps:
            x0, y0 = int(round(sp.x0)), int(round(sp.y0))
            fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + sp.w), min(H, y0 + sp.h)
            if fx1 <= fx0 or fy1 <= fy0:
                continue
            src = sp.a[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
            reg = fr[fy0 - ry0:fy1 - ry0, fx0 - rx0:fx1 - rx0]
            reg *= (1 - src[..., 3:4])
            reg += src[..., :3]
        return np.clip(1 - fr.mean(-1), 0, 1), rx0, ry0


# ---------------- o homem (túnica, cabelo em cachos, barba) ----------------
@lru_cache(maxsize=None)
def homem() -> Puppet:
    """O homem comum do gancho: túnica com dobras vazadas, cinto de corda, barra bordada."""
    def torso(d, ox, oy):
        shape(d, [(0, -184), (18, -180), (30, -150), (33, -110), (30, -66), (36, -24), (44, 20), (56, 62), (40, 74), (22, 66),
                  (2, 78), (-18, 68), (-40, 80), (-60, 70), (-44, 24), (-36, -24), (-32, -70), (-34, -120), (-26, -164)], ox=ox, oy=oy)
        # palla sobre o ombro de trás
        shape(d, [(-24, -170), (-46, -150), (-56, -96), (-62, -30), (-54, 6), (-40, -30), (-30, -96), (-10, -150)], ox=ox, oy=oy)
        # dobras (cortes que afinam)
        stroke(d, [(-6, -150), (-12, -100), (-8, -50), (-16, 20), (-22, 60)], 3.2, 0.6, HOLE, ox, oy)
        stroke(d, [(10, -120), (6, -70), (12, -20), (16, 40)], 2.6, 0.6, HOLE, ox, oy)
        stroke(d, [(-44, -120), (-48, -60), (-50, 0)], 2.4, 0.5, HOLE, ox, oy)
        # cinto de corda com nó e borlas
        stroke(d, [(-34, -54), (-10, -48), (14, -50), (34, -56)], 4.5, 4.5, HOLE, ox, oy)
        ell(d, 18, -46, 5, 4, INK, ox, oy)
        for k in range(3):
            stroke(d, [(18 + k * 3, -44), (20 + k * 4, -30), (18 + k * 5, -16)], 2, 1, INK, ox, oy)
        # barra bordada: arcos e pontos
        for k in range(7):
            x = -46 + k * 15
            y = 56 + 4 * math.sin(k)
            d.arc([*P(x - 6, y - 6, ox, oy), *P(x + 6, y + 6, ox, oy)], 0, 180, fill=HOLE, width=3)
            ell(d, x, y - 9, 1.8, 1.8, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)

    def head(d, ox, oy):
        # pescoço e cabeça de perfil, virada para a direita: nariz, barba, cachos
        shape(d, [(-10, 4), (-12, -16), (-22, -30), (-26, -50), (-20, -70), (-4, -82), (14, -80), (24, -68), (26, -56), (36, -44), (28, -40),
                  (27, -32), (32, -27), (26, -24), (24, -16), (16, -6), (8, 0), (10, 6)], ox=ox, oy=oy, n=12)
        for k, (x, y, r) in enumerate([(-22, -66, 9), (-14, -78, 9), (-2, -84, 9), (10, -84, 8), (20, -78, 7), (-26, -54, 8), (-26, -42, 7)]):
            ell(d, x, y, r, r, INK, ox, oy)
            spiral(d, x, y, r * 0.6, 1.2, 1.4, HOLE, ox, oy, 1 if k % 2 else -1)
        for k, (x, y) in enumerate([(14, -10), (6, -6), (20, -16), (-2, -10)]):
            ell(d, x, y, 6, 7, INK, ox, oy)
            spiral(d, x, y, 3.6, 1, 1.2, HOLE, ox, oy)
        shape(d, [(12, -58), (20, -61), (16, -55)], HOLE, ox, oy, n=6)               # olho amendoado
        stroke(d, [(6, -66), (14, -68), (22, -65)], 2.2, 0.6, HOLE, ox, oy)          # sobrancelha
        spiral(d, -6, -46, 5, 1.3, 1.5, HOLE, ox, oy)                                  # orelha
        rivet(d, 0, 0, ox, oy)

    def uarm(d, ox, oy):
        shape(d, [(-10, -4), (8, -6), (12, 20), (9, 52), (7, 80), (-6, 80), (-10, 50), (-13, 20)], ox=ox, oy=oy)
        stroke(d, [(-2, 14), (0, 40), (-1, 66)], 2, 0.5, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)

    def farm(d, ox, oy):
        shape(d, [(-7, -2), (7, -2), (8, 30), (6, 62), (12, 70), (16, 78), (24, 82), (20, 88), (8, 92), (-2, 90), (-8, 78), (-6, 62), (-8, 30)], ox=ox, oy=oy)
        stroke(d, [(4, 70), (10, 74)], 1.4, 0.6, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)

    def leg(d, ox, oy):
        shape(d, [(-10, -2), (10, -2), (12, 30), (8, 60), (12, 84), (9, 110), (12, 118), (34, 122), (40, 128), (30, 132), (-8, 132), (-10, 116),
                  (-8, 92), (-14, 62), (-12, 30)], ox=ox, oy=oy)
        for k in range(4):
            stroke(d, [(-8, 98 + k * 7), (2, 101 + k * 7), (10, 99 + k * 7)], 1.6, 1.0, HOLE, ox, oy)
        stroke(d, [(-2, 20), (0, 50)], 1.8, 0.4, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)

    parts = [Part('torso', 200, torso), Part('head', 100, head, 'torso', (2, -180)),
             Part('legB', 150, leg, 'torso', (-10, 40)), Part('legF', 150, leg, 'torso', (10, 40)),
             Part('uarmB', 100, uarm, 'torso', (-8, -162)), Part('farmB', 110, farm, 'uarmB', (0, 78)),
             Part('uarmF', 100, uarm, 'torso', (10, -162)), Part('farmF', 110, farm, 'uarmF', (0, 78))]
    return Puppet(parts, ['uarmB', 'farmB', 'legB', 'legF', 'torso', 'head', 'uarmF', 'farmF'], rods=[('farmF', (8, 86)), ('torso', (0, 0))])


# ---------------- o imperador (toga até os pés, coroa de louros) ----------------
@lru_cache(maxsize=None)
def imperador() -> Puppet:
    """Marco Aurélio: toga longa com bordados vazados e coroa de louros; braços e pernas do homem."""
    def torso(d, ox, oy):
        shape(d, [(0, -188), (20, -184), (34, -150), (38, -100), (36, -40), (48, 30), (62, 110), (70, 160), (40, 172), (0, 168), (-40, 174), (-70, 166),
                  (-60, 100), (-44, 20), (-38, -60), (-40, -130), (-28, -170)], ox=ox, oy=oy)
        shape(d, [(-26, -176), (-56, -150), (-70, -80), (-78, 0), (-74, 80), (-56, 40), (-44, -40), (-30, -120), (-6, -160)], ox=ox, oy=oy)
        stroke(d, [(30, -176), (6, -120), (-24, -60), (-48, 20), (-60, 120)], 3.2, 1.0, HOLE, ox, oy)
        for k in range(4):
            stroke(d, [(10 + k * 9, -60 + k * 6), (16 + k * 10, 40), (24 + k * 10, 140)], 2.4, 0.5, HOLE, ox, oy)
        for k in range(9):
            x = -56 + k * 14
            y = 152 + 3 * math.sin(k)
            ell(d, x, y, 2.4, 2.4, HOLE, ox, oy)
        for k in range(8):
            ell(d, 22 - k * 7, -160 + k * 12, 2.2, 2.2, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)

    def head(d, ox, oy):
        shape(d, [(-10, 4), (-12, -16), (-22, -30), (-26, -50), (-20, -70), (-4, -82), (14, -80), (24, -68), (26, -56), (34, -44), (27, -40),
                  (27, -32), (31, -27), (25, -24), (22, -14), (14, -6), (8, 0), (10, 6)], ox=ox, oy=oy, n=12)
        for k in range(9):                                  # coroa de louros: folhas serrilhadas
            a = math.radians(200 + k * 17)
            x, y = -2 + 26 * math.cos(a), -54 + 28 * math.sin(a)
            serrated(d, x + ox, y + oy, math.degrees(a) + 70 * (1 if k < 5 else -1) - 90, 18, 0.32)
        for k, (x, y) in enumerate([(14, -10), (6, -6), (20, -16), (-2, -10)]):
            ell(d, x, y, 6, 7, INK, ox, oy)
            spiral(d, x, y, 3.6, 1, 1.2, HOLE, ox, oy)
        shape(d, [(12, -58), (20, -61), (16, -55)], HOLE, ox, oy, n=6)
        stroke(d, [(6, -66), (14, -68), (22, -65)], 2.2, 0.6, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)

    base = homem().parts
    T = Part('torso', 220, torso)
    Hd = Part('head', 100, head, 'torso', (2, -184))
    newp = [T, Hd, base['uarmB'], base['farmB'], base['uarmF'], base['farmF'], base['legB'], base['legF']]
    return Puppet(newp, ['uarmB', 'farmB', 'legB', 'legF', 'torso', 'head', 'uarmF', 'farmF'], rods=[('farmF', (8, 86)), ('torso', (0, 0))])

"""Compositor: o elenco de um bloco e a montagem de cada quadro no lençol.

O ELENCO (criado no topo do script de cena; nada é desenhado até ser usado):
  Camada(arte, *args, desfoque, opacidade, semente, pivo, balanco, dobra, posicao)
      uma peça recortada (cenário, objeto, texto). `desfoque` = distância do lençol (px);
      `semente` liga o balanço na vareta (wob); `dobra=False` não entorta a sombra nas dobras.
  Boneco(fabrica, escala, desfoque, opacidade)     boneco articulado (bonecos.homem, bonecos.imperador)
  Chama(arte, *args, brilho, cor, forca)           chama colorida com brilho em volta

O QUADRO (função `quadro(q, c)` do script de cena, chamada a cada quadro):
  q.u, q.t                 tempo desde o início da narração / tempo no vídeo do bloco
  q.ss / q.env / q.lin     curvas de animação já no tempo q.u
  q.luz(nivel)             luz da lanterna (1 = dia; chame primeiro)
  q.lua(alpha)             disco de lua projetado
  q.sombra(camada, *fatores, dx, dy)        sombra de uma peça (opacidade = da camada x fatores)
  q.multidao(camada, deslocamentos, *fatores, pesos)   várias cópias (soldados, moedas)
  q.boneco(boneco, x, y, pose, *fatores, desfoque)      boneco articulado na pose
  q.foco(forca, cx, cy, raio)              círculo de luz isolando um elemento
  q.chama(chama, *fatores, cintila, camada, dx, dy)    chama colorida (segue a camada, se dada)
  q.camera(cx, cy, zoom)                   aproximação da câmera

A ordem final é sempre a mesma, não importa a ordem das chamadas de foco/chama/câmera:
luz -> lua -> sombras (na ordem chamada) -> foco -> pano na base -> poeira e grão -> grade sépia
-> chamas -> câmera -> escurecimento final do bloco.
"""
from __future__ import annotations

import math

import cv2
import numpy as np

from . import lencol
from .anim import env, lin, ss, wob
from .config import H, W
from .traco import borrar, mascara_camada, raio_borrao


class Camada:
    """Uma peça do elenco projetada no lençol (ver docstring do módulo)."""

    def __init__(self, arte, *args, desfoque=0.0, opacidade=1.0, semente=None, pivo=(960, 1080),
                 balanco=(2.5, 0.35), dobra=True, posicao=(0, 0)):
        self.arte, self.args = arte, args
        self.desfoque, self.opacidade = desfoque, opacidade
        self.semente, self.pivo, self.balanco = semente, pivo, balanco
        self.dobra, self.posicao = dobra, posicao

    def mascara(self):
        return mascara_camada(self.arte, self.args, self.desfoque, self.posicao)

    def preparar(self):
        self.mascara()

    def __repr__(self):
        return f'Camada({self.arte.__name__}{self.args})'


class Boneco:
    """Boneco articulado do elenco: `fabrica` devolve o Puppet (ex.: bonecos.homem)."""

    def __init__(self, fabrica, escala=1.0, desfoque=1.1, opacidade=0.9, dobra=True):
        self.fabrica, self.escala, self.desfoque = fabrica, escala, desfoque
        self.opacidade, self.dobra = opacidade, dobra

    def preparar(self):
        self.fabrica()


class Chama:
    """Chama colorida (a única cor saturada do padrão), com brilho em volta de raio `brilho`."""

    def __init__(self, arte, *args, brilho=22, cor=(0.6, 0.38, 0.12), forca=1.3):
        self.arte, self.args = arte, args
        self.brilho, self.cor, self.forca = brilho, cor, forca

    def dados(self):
        return lencol.chama_rgba(self.arte, *self.args)

    def preparar(self):
        self.dados()


# ---------------- operações em região (resultado idêntico ao quadro inteiro, mais rápido) ----------------
def _cortar(r):
    x0, y0, x1, y1 = r
    return slice(y0, y1), slice(x0, x1)


def _ampliar(r, m):
    x0, y0, x1, y1 = r
    r = (max(0, int(math.floor(x0 - m))), max(0, int(math.floor(y0 - m))), min(W, int(math.ceil(x1 + m))), min(H, int(math.ceil(y1 + m))))
    return r if r[2] > r[0] and r[3] > r[1] else None


def _unir(a, b):
    if a is None:
        return b
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def mover(m, ret, dx=0.0, dy=0.0, rot=0.0, piv=(960, 1080)):
    """Desloca/gira a máscara inteira (como a vareta move a peça). Devolve (máscara, retângulo novo).

    Usa o quadro inteiro de propósito: no OpenCV 5 o warpAffine em recorte não dá o mesmo resultado.
    """
    if abs(dx) < 0.05 and abs(dy) < 0.05 and abs(rot) < 0.01:
        return m, ret
    M = cv2.getRotationMatrix2D(piv, rot, 1.0)
    M[0, 2] += dx
    M[1, 2] += dy
    out = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
    x0, y0, x1, y1 = ret
    cantos = np.array([[x0, y0, 1], [x1, y0, 1], [x0, y1, 1], [x1, y1, 1]], np.float64) @ M.T
    novo = (cantos[:, 0].min(), cantos[:, 1].min(), cantos[:, 0].max(), cantos[:, 1].max())
    return out, _ampliar(novo, 3)


class Quadro:
    """Um quadro em construção (ver docstring do módulo)."""

    def __init__(self, t, u, fim=None, fade=(1.0, 0.9)):
        self.t, self.u, self.fim, self._fade = t, u, fim, fade
        self.D = lencol.dados()
        self.nivel = 1.0
        self.L = None
        self._foco = None
        self._chamas = []
        self._camera = None

    # ---- tempo (no relógio da narração, q.u) ----
    def ss(self, t0, d):
        return ss(self.u, t0, d)

    def env(self, a, ai, b, bo):
        return env(self.u, a, ai, b, bo)

    def lin(self, t0, d):
        return lin(self.u, t0, d)

    # ---- luz ----
    def luz(self, nivel=1.0):
        """Acende a lanterna atrás do lençol com o nível dado (dia = 1; noite < 1; glória > 1)."""
        self.nivel = nivel
        self.L = self.D['LIGHT'] * nivel

    def _luz(self):
        if self.L is None:
            self.luz(1.0)
        return self.L

    def lua(self, alpha, cx=1520, cy=210, raio=78, brilho=0.9, crescente=0.0):
        """Lua projetada como disco claro (crescente > 0 recorta um crescente)."""
        if alpha > 0:
            L = self._luz()
            m, r = lencol.lua(cx, cy, raio, crescente) if crescente else lencol.lua(cx, cy, raio)
            sl = _cortar(r)
            L[sl] = L[sl] + m[sl] * brilho * alpha * self.D['vign'][sl]

    def _escurecer(self, m, r, op):
        L = self._luz()
        sl = _cortar(r)
        L[sl] *= 1 - op * m

    def _dobrar(self, m, r):
        """Entorta a sombra nas dobras do lençol (só na região onde ela pode aparecer)."""
        r = _ampliar(r, self.D['DMAX'] + 3)
        if r is None:
            return None, None
        sl = _cortar(r)
        return cv2.remap(m, self.D['MAPX'][sl], self.D['MAPY'][sl], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE), r

    # ---- sombras ----
    def sombra(self, camada, *fatores, dx=0, dy=0):
        """Projeta a camada. Opacidade = camada.opacidade x fatores (na ordem dada)."""
        op = camada.opacidade
        for f in fatores:
            op = op * f
        if op <= 0.003:
            return
        m, r = camada.mascara()
        if r is None:
            return
        if camada.semente is not None:
            wx, wy, wr = wob(self.u, camada.semente, *camada.balanco)
            m, r = mover(m, r, dx + wx, dy + wy, wr, camada.pivo)
        elif dx or dy:
            m, r = mover(m, r, dx, dy)
        if r is None:
            return
        if camada.dobra:
            m, r = self._dobrar(m, r)
        else:
            m = m[_cortar(r)]
        if r is not None:
            self._escurecer(m, r, op)

    def multidao(self, camada, deslocamentos, *fatores, pesos=None):
        """Várias cópias da camada (soldados, moedas), cada uma deslocada (dx, dy) do lugar onde foi desenhada.

        `pesos` (opcional) multiplica cada cópia (ex.: moeda sumindo). A sombra é o máximo das cópias.
        """
        op = camada.opacidade
        for f in fatores:
            op = op * f
        if op <= 0.003:
            return
        m, r0 = camada.mascara()
        acc, uni = None, None
        for i, (dx, dy) in enumerate(deslocamentos):
            w, r = mover(m, r0, dx, dy)
            if r is None:
                continue
            if acc is None:
                acc = np.zeros((H, W), np.float32)
            sl = _cortar(r)
            peca = w[sl] if pesos is None else w[sl] * pesos[i]
            acc[sl] = np.maximum(acc[sl], peca)
            uni = _unir(uni, r)
        if acc is None or not acc[_cortar(uni)].max() > 0:
            return
        if camada.dobra:
            mm, r = self._dobrar(acc, uni)
        else:
            mm, r = acc[_cortar(uni)], uni
        if r is not None:
            self._escurecer(mm, r, op)

    def boneco(self, boneco, x, y, pose, *fatores, desfoque=None):
        """Boneco articulado com o pivô do torso em (x, y) e a pose {peça: graus}."""
        op = boneco.opacidade
        for f in fatores:
            op = op * f
        if op <= 0.003:
            return
        res = boneco.fabrica().mascara(x, y, pose, boneco.escala)
        if res is None:
            return
        m, rx0, ry0 = res
        s = boneco.desfoque if desfoque is None else desfoque
        r = _ampliar((rx0, ry0, rx0 + m.shape[1], ry0 + m.shape[0]), raio_borrao(s) + 2)
        cheio = np.zeros((H, W), np.float32)
        cheio[ry0:ry0 + m.shape[0], rx0:rx0 + m.shape[1]] = m
        sl = _cortar(r)
        cheio[sl] = borrar(np.ascontiguousarray(cheio[sl]), s)
        if boneco.dobra:
            mm, r = self._dobrar(cheio, r)
        else:
            mm = cheio[sl]
        if r is not None:
            self._escurecer(mm, r, op)

    # ---- luz de cena, chamas e câmera (aplicados no fim, sempre na mesma ordem) ----
    def foco(self, forca, cx, cy, raio):
        """Foco de luz: o círculo fica claro e o resto cai na penumbra (forca 0..1)."""
        if forca > 0:
            self._foco = (forca, cx, cy, raio)

    def chama(self, chama, *fatores, cintila=(1.0, 0.0, 0.0), camada=None, dx=0, dy=0):
        """Chama colorida. Se `camada` for dada, a chama balança junto com ela (mesmo dx, dy).

        cintila = (base, amplitude, frequência): fator base + amplitude * sin(u * frequência).
        """
        mov = None
        if camada is not None:
            wx, wy, wr = wob(self.u, camada.semente, *camada.balanco)
            mov = (dx + wx, dy + wy, wr, camada.pivo)
        elif dx or dy:
            mov = (dx, dy, 0.0, (960, 1080))
        self._chamas.append((chama, fatores, cintila, mov))

    def camera(self, cx, cy, zoom):
        """Aproxima a câmera `zoom` vezes em torno de (cx, cy)."""
        self._camera = (cx, cy, zoom)

    def _aplicar_chama(self, img, chama, fatores, cintila, mov):
        frgb, fa, r = chama.dados()
        if mov is not None:
            dx, dy, rot, piv = mov
            if not (abs(dx) < 0.05 and abs(dy) < 0.05 and abs(rot) < 0.01):
                M = cv2.getRotationMatrix2D(piv, rot, 1.0)
                M[0, 2] += dx
                M[1, 2] += dy
                fa, r = mover(fa, r, dx, dy, rot, piv)
                frgb = np.stack([cv2.warpAffine(frgb[..., k], M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0) for k in range(3)], -1)
        if r is None:
            return img
        g = _ampliar(r, raio_borrao(chama.brilho) + 2)
        sl = _cortar(g)
        a = fa[sl]
        for f in fatores:
            a = a * f
        base, amp, freq = cintila
        a = a * (base + amp * math.sin(self.u * freq))
        brilho = borrar(np.ascontiguousarray(a), chama.brilho)[..., None]
        if img.dtype != np.float64:
            img = img.astype(np.float64)
        img[sl] = np.clip(img[sl] + brilho * np.array(chama.cor) * chama.forca, 0, 1)
        img[sl] = img[sl] * (1 - a[..., None]) + frgb[sl] * a[..., None]
        return img

    def finalizar(self):
        """Fecha o quadro e devolve a imagem RGB uint8 (H x W x 3)."""
        D = self.D
        L = self._luz()
        if self._foco is not None:
            spot, scx, scy, sr = self._foco
            m, um = lencol.foco(scx, scy, sr)
            L = L * (1 - 0.78 * spot * m) + 0.12 * spot * um * D['hot']
        y = D['Y_PANO']
        L[y:] = L[y:] * D['PANO_1MA'] + D['PANO'] * self.nivel ** 0.5 * D['PANO_A']
        L = np.clip(L + D['OVER'] * self.nivel + D['GRAIN'], 0, 1.299)
        lut, lutf = lencol.grade()
        idx = (L * (lencol.LUTN - 1) / 1.3).astype(np.int32)
        fade = 1 - ss(self.t, self.fim - self._fade[0], self._fade[1]) if self.fim is not None else 1.0
        if not self._chamas and self._camera is None and fade == 1.0:
            return lut[idx]                     # idêntico ao caminho em ponto flutuante (ver testes)
        img = lutf[idx]
        for ch in self._chamas:
            img = self._aplicar_chama(img, *ch)
        if self._camera is not None:
            img = lencol.camera(img, *self._camera)
        if fade != 1.0:
            img *= fade
        return (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)

"""Compositor: os atalhos de desempenho dão exatamente o mesmo resultado que o caminho completo."""
import cv2
import numpy as np

from marbleash import bonecos, lencol, quadro, traco
from marbleash.config import H, W


def test_atalho_da_grade_sepia_e_exato():
    lut, lutf = lencol.grade()
    assert np.array_equal((np.clip(lutf, 0, 1) * 255 + 0.5).astype(np.uint8), lut)


def test_raio_do_desfoque():
    m = np.zeros((200, 200), np.float32)
    m[100, 100] = 1
    for s in (0.7, 1.1, 2.6, 22.0):
        r = traco.raio_borrao(s)
        if 100 + r + 1 >= 200:
            continue
        b = cv2.GaussianBlur(m, (0, 0), s)
        ys, xs = np.nonzero(b)
        assert xs.max() - 100 <= r and 100 - xs.min() <= r


def test_mover_nao_deixa_nada_fora_do_retangulo():
    rng = np.random.default_rng(0)
    m = np.zeros((H, W), np.float32)
    m[400:520, 700:800] = cv2.GaussianBlur((rng.random((120, 100)) > 0.5).astype(np.float32), (0, 0), 2)
    ret = traco.retangulo(m)
    for _ in range(20):
        dx, dy, rot = rng.uniform(-300, 300), rng.uniform(-200, 200), rng.uniform(-1, 1)
        w, r = quadro.mover(m, ret, dx, dy, rot, (960, 1080))
        fora = w.copy()
        fora[r[1]:r[3], r[0]:r[2]] = 0
        assert not fora.any()


def test_mascara_do_boneco_igual_ao_quadro_inteiro():
    b = bonecos.homem()
    pose = {'legF': 12.3, 'legB': -9.1, 'uarmF': -20, 'farmF': -35, 'head': 7, 'torso': 4}
    fr = np.ones((H, W, 3), np.float32)
    b.draw(fr, 430, 700, pose, scale=1.35)
    cheia = np.clip(1 - fr.mean(-1), 0, 1)
    m, x0, y0 = b.mascara(430, 700, pose, 1.35)
    recorte = np.zeros((H, W), np.float32)
    recorte[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] = m
    assert np.array_equal(cheia, recorte)

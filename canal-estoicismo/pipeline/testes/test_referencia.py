"""Regressão visual: os stills do bloco 1 do vídeo 1 continuam idênticos à referência aprovada.

A referência (PNG) fica fora do git em videos/MA-001-…/trabalho/referencia/stills/. Sem ela, o teste é
pulado. Ela só vale no mesmo ambiente (mesmas versões de numpy/scipy/opencv/pillow): em outro
computador, gere a referência de novo antes de mexer no código (ver pipeline/LEIA-ME.md).
"""
import numpy as np
import pytest
from PIL import Image

from marbleash import config, render
from marbleash.projeto import Bloco, nome_video

VIDEO = nome_video(1)
REF = config.VIDEOS / VIDEO / 'trabalho' / 'referencia' / 'stills'


@pytest.mark.skipif(not REF.is_dir(), reason='sem stills de referência neste computador')
def test_stills_do_bloco1_identicos_a_referencia():
    b = Bloco(VIDEO, 1)
    refs = sorted(REF.glob('bloco1_*.png'))
    assert refs
    for p in refs:
        t = float(p.stem.split('_')[1])
        novo = render.quadro(b, t)
        velho = np.asarray(Image.open(p).convert('RGB'))
        assert np.array_equal(novo, velho), f'{p.name} mudou (ma stills 1 1 --referencia {REF})'

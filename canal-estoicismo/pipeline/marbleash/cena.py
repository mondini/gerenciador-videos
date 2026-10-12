"""Tudo o que um script de cena precisa, num import só:

    from marbleash.cena import *

Traz: math; os catálogos `cenario`, `objetos`, `bonecos`; o elenco (Camada, Boneco, Chama, Credito);
as curvas (ss, env, lin, lerp, tremor, wob); e as medidas do palco (W, H, FPS, FLOOR, BASE).
Modelo comentado: videos/video-01/bloco1/cena.py.
"""
import math

from . import bonecos, cenario, objetos
from .anim import env, lerp, lin, ss, tremor, wob
from .config import FPS, H, W
from .quadro import Boneco, Camada, Chama, Credito
from .traco import BASE, FLOOR

__all__ = ['math', 'bonecos', 'cenario', 'objetos', 'env', 'lerp', 'lin', 'ss', 'tremor', 'wob',
           'FPS', 'H', 'W', 'BASE', 'FLOOR', 'Boneco', 'Camada', 'Chama', 'Credito']

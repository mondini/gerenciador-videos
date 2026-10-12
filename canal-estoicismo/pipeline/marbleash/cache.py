"""Cache da arte e das máscaras: na memória do processo e em disco (pipeline/.cache).

Gerar a arte (desenho a 2x, desfoques, o lençol) leva dezenas de segundos; um quadro leva décimos.
Por isso tudo o que é caro passa por `@em_disco`: a primeira chamada calcula e grava; as próximas
(inclusive em outros processos do render paralelo) só leem o arquivo.

O cache é invalidado sozinho: a pasta leva a "impressão digital" do código que gera a arte e das versões
de numpy/scipy/opencv/pillow. Mudou o código, muda a pasta; pastas antigas são apagadas.
"""
from __future__ import annotations

import functools
import hashlib
import os
import pickle
import shutil
import tempfile
from collections import OrderedDict
from pathlib import Path

import numpy as np

from . import config

# módulos cujo código entra na impressão digital (os que desenham ou calculam arte)
_MODULOS_DE_ARTE = ('config', 'cache', 'traco', 'bonecos', 'cenario', 'objetos', 'lencol')
_LIMITE_MEMORIA = 700_000_000            # bytes guardados na memória de cada processo (o render usa vários)


@functools.lru_cache(maxsize=None)
def impressao() -> str:
    """Impressão digital do código de arte + versões das bibliotecas numéricas."""
    import cv2
    import PIL
    import scipy
    h = hashlib.sha1()
    pasta_pkg = Path(__file__).parent
    for nome in _MODULOS_DE_ARTE:
        h.update(nome.encode())
        h.update((pasta_pkg / f'{nome}.py').read_bytes())
    h.update(f'{np.__version__} {scipy.__version__} {cv2.__version__} {PIL.__version__}'.encode())
    return h.hexdigest()[:16]


def pasta() -> Path:
    """Pasta do cache para o código atual (cria e remove as de versões antigas)."""
    d = config.CACHE / impressao()
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)
        for velha in config.CACHE.iterdir():
            if velha.is_dir() and velha.name != d.name:
                shutil.rmtree(velha, ignore_errors=True)
    return d


def limpar() -> None:
    """Apaga todo o cache em disco (ele é refeito sob demanda)."""
    shutil.rmtree(config.CACHE, ignore_errors=True)


def esquecer() -> None:
    """Libera o que está guardado na memória deste processo (o disco continua)."""
    global _bytes
    _memoria.clear()
    _bytes = 0


def _estavel(obj) -> str:
    """repr estável entre execuções (funções viram 'modulo.nome')."""
    if callable(obj) and hasattr(obj, '__qualname__'):
        return f'{obj.__module__}.{obj.__qualname__}'
    if isinstance(obj, (tuple, list)):
        return '(' + ','.join(_estavel(o) for o in obj) + ')'
    if isinstance(obj, dict):
        return '{' + ','.join(f'{k}:{_estavel(v)}' for k, v in sorted(obj.items())) + '}'
    return repr(obj)


# ---------- gravação compacta: arrays do tamanho do quadro são guardados só no retângulo não nulo ----------
class _Recorte:
    def __init__(self, a: np.ndarray):
        nz = np.nonzero(a.reshape(a.shape[0], a.shape[1], -1).any(-1))
        self.shape, self.dtype = a.shape, a.dtype
        if len(nz[0]) == 0:
            self.y0 = self.x0 = 0
            self.a = a[:0, :0].copy()
        else:
            self.y0, self.x0 = int(nz[0].min()), int(nz[1].min())
            self.a = a[self.y0:nz[0].max() + 1, self.x0:nz[1].max() + 1].copy()

    def inteiro(self) -> np.ndarray:
        out = np.zeros(self.shape, self.dtype)
        out[self.y0:self.y0 + self.a.shape[0], self.x0:self.x0 + self.a.shape[1]] = self.a
        return out


def _compactar(v):
    if isinstance(v, np.ndarray) and v.ndim >= 2 and v.shape[:2] == (config.H, config.W):
        return _Recorte(v)
    if isinstance(v, tuple):
        return tuple(_compactar(x) for x in v)
    if isinstance(v, list):
        return [_compactar(x) for x in v]
    if isinstance(v, dict):
        return {k: _compactar(x) for k, x in v.items()}
    return v


def _expandir(v):
    if isinstance(v, _Recorte):
        return v.inteiro()
    if isinstance(v, tuple):
        return tuple(_expandir(x) for x in v)
    if isinstance(v, list):
        return [_expandir(x) for x in v]
    if isinstance(v, dict):
        return {k: _expandir(x) for k, x in v.items()}
    return v


def _tamanho(v) -> int:
    if isinstance(v, np.ndarray):
        return v.nbytes
    if isinstance(v, (tuple, list)):
        return sum(_tamanho(x) for x in v)
    if isinstance(v, dict):
        return sum(_tamanho(x) for x in v.values())
    return 1000


_memoria: OrderedDict = OrderedDict()
_bytes = 0


def _lembrar(chave, valor):
    global _bytes
    _memoria[chave] = valor
    _bytes += _tamanho(valor)
    while _bytes > _LIMITE_MEMORIA and len(_memoria) > 1:
        _, velho = _memoria.popitem(last=False)
        _bytes -= _tamanho(velho)


def em_disco(func):
    """Decorador: guarda o resultado em disco e na memória, pela função e seus argumentos."""
    nome = f'{func.__module__.split(".")[-1]}.{func.__qualname__}'

    @functools.wraps(func)
    def envolvida(*args, **kw):
        chave = nome + _estavel(args) + _estavel(kw)
        if chave in _memoria:
            _memoria.move_to_end(chave)
            return _memoria[chave]
        arq = pasta() / f'{nome}-{hashlib.sha1(chave.encode()).hexdigest()[:16]}.pkl'
        valor = None
        if arq.exists():
            try:
                with open(arq, 'rb') as f:
                    valor = _expandir(pickle.load(f))
            except Exception:           # arquivo corrompido (ex.: render interrompido): refaz
                valor = None
        if valor is None:
            valor = func(*args, **kw)
            fd, tmp = tempfile.mkstemp(dir=arq.parent, suffix='.tmp')
            with os.fdopen(fd, 'wb') as f:
                pickle.dump(_compactar(valor), f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, arq)        # gravação atômica: processos paralelos não se atrapalham
        _lembrar(chave, valor)
        return valor

    envolvida.sem_cache = func
    return envolvida

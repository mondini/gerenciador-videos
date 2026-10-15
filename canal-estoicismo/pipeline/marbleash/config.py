"""Caminhos, constantes do vídeo e ferramentas externas (ffmpeg, fontes)."""
from __future__ import annotations

import json
import os
import shutil
from functools import lru_cache
from pathlib import Path

W, H, FPS = 1920, 1080, 30      # vídeo final: 1920x1080, 30 quadros por segundo
S = 2                           # os recortes são desenhados em 2x e reduzidos (bordas suaves)

PIPELINE = Path(__file__).resolve().parents[1]                      # .../canal-estoicismo/pipeline
CANAL = Path(os.environ.get('MA_CANAL', PIPELINE.parent))             # .../canal-estoicismo
FONTES = CANAL / 'fontes-tipograficas'
VIDEOS = CANAL / 'videos'
CACHE = Path(os.environ.get('MA_CACHE', PIPELINE / '.cache'))
MODELOS = Path(os.environ.get('MA_MODELOS', PIPELINE / '.modelos'))
REPO = CANAL.parent                                                   # repositório (o .env da raiz fica aqui)

# Dados do canal (nome, prefixo do código dos vídeos, pasta no Drive): canal.json.
_CANAL_JSON = CANAL / 'canal.json'
CANAL_INFO = json.loads(_CANAL_JSON.read_text(encoding='utf-8')) if _CANAL_JSON.exists() else {}
PREFIXO = CANAL_INFO.get('prefixo', 'MA')


def env_repo(chave: str, padrao: str | None = None) -> str | None:
    """Valor do ambiente ou, se faltar, do .env da raiz do repositório (DRIVE_ROOT, ELEVENLABS_API_KEY)."""
    if os.environ.get(chave):
        return os.environ[chave]
    arq = REPO / '.env'
    if arq.exists():
        for linha in arq.read_text(encoding='utf-8').splitlines():
            k, sep, v = linha.strip().partition('=')
            if sep and k.strip() == chave and not k.startswith('#'):
                return v.strip().strip('"').strip("'")
    return padrao

# Onde mais procurar fontes que não estão em fontes-tipograficas/ (ex.: Inter no ambiente do Claude.ai).
_PASTAS_FONTES_SISTEMA = [
    Path('/usr/share/fonts/opentype/inter'),
    Path('/usr/share/fonts/truetype/inter'),
    Path('/usr/share/fonts/truetype/gfs'),
    Path('/usr/share/fonts'),
    Path.home() / 'Library/Fonts',
    Path('/Library/Fonts'),
]


@lru_cache(maxsize=None)
def ffmpeg() -> str:
    """Caminho do ffmpeg: $MA_FFMPEG, depois o PATH, depois o binário do pacote imageio-ffmpeg."""
    if os.environ.get('MA_FFMPEG'):
        return os.environ['MA_FFMPEG']
    achado = shutil.which('ffmpeg')
    if achado:
        return achado
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit('ffmpeg não encontrado. Instale (ver pipeline/LEIA-ME.md) ou defina MA_FFMPEG.')


@lru_cache(maxsize=None)
def fonte(nome: str) -> str:
    """Caminho de um arquivo de fonte (ex.: 'Cormorant-MediumItalic.ttf').

    Procura primeiro em fontes-tipograficas/ e depois em pastas comuns do sistema.
    """
    candidatos = [FONTES / nome] + [p / nome for p in _PASTAS_FONTES_SISTEMA]
    for c in candidatos:
        if c.exists():
            return str(c)
    for pasta in _PASTAS_FONTES_SISTEMA:            # última tentativa: busca recursiva pelo nome
        if pasta.is_dir():
            for c in pasta.rglob(nome):
                return str(c)
    raise FileNotFoundError(f'Fonte {nome!r} não encontrada em {FONTES}/ (confira o nome do arquivo; '
                            'fonte nova: baixe do Google Fonts, licença OFL, com o OFL-*.txt).')

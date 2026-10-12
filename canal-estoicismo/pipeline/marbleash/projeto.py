"""Pastas e dados de um vídeo e de um bloco; carregamento do script de cena.

Estrutura de um vídeo (videos/video-NN/):
  roteiro.md               roteiro e status
  audio/                   mp3 do ElevenLabs (fora do git)
  blocoN/cena.py           script de cena do bloco N (elenco + função quadro)
  blocoN/tempos.txt        deixas: nome, segundo no áudio original, frase
  blocoN/audio.json        qual mp3 foi usado, pausas detectadas e parâmetros de ritmo (gerado)
  trabalho/                intermediários: áudio desacelerado, vídeo sem som (fora do git)
  previas/                 prévias e stills de conferência (fora do git)
  final/                   vídeo final (fora do git)
"""
from __future__ import annotations

import importlib.util
import re
import sys
from functools import cached_property
from pathlib import Path

from . import audio, config, tempos


def nome_video(v) -> str:
    """Aceita '1', '01', 'video-01' -> 'video-01'."""
    v = str(v)
    m = re.fullmatch(r'(?:video-?)?(\d+)', v)
    return f'video-{int(m.group(1)):02d}' if m else v


class Bloco:
    """Um bloco de um vídeo: caminhos, script de cena, deixas e duração."""

    def __init__(self, video, numero):
        self.video = nome_video(video)
        self.numero = int(numero)
        self.nome = f'bloco{self.numero}'
        self.pasta_video = config.VIDEOS / self.video
        self.pasta = self.pasta_video / self.nome
        self.trabalho = self.pasta_video / 'trabalho'
        self.previas = self.pasta_video / 'previas'
        self.final = self.pasta_video / 'final'
        if not self.pasta_video.is_dir():
            raise SystemExit(f'Pasta do vídeo não encontrada: {self.pasta_video}')

    def __repr__(self):
        return f'Bloco({self.video}, {self.numero})'

    # ---- arquivos ----
    @property
    def arquivo_cena(self) -> Path:
        return self.pasta / 'cena.py'

    @property
    def arquivo_tempos(self) -> Path:
        return self.pasta / 'tempos.txt'

    @property
    def arquivo_audio_json(self) -> Path:
        return self.pasta / 'audio.json'

    @property
    def audio_lento(self) -> Path:
        return self.trabalho / f'{self.nome}-lento.wav'

    @property
    def roteiro(self) -> Path:
        return self.pasta_video / 'roteiro.md'

    def procurar_mp3(self):
        """O mp3 mais recente de videos/video-NN/audio/ com 'blocoN' no nome."""
        cands = [p for p in (self.pasta_video / 'audio').glob('*.mp3')
                 if re.search(rf'bloco0*{self.numero}(?!\d)', p.name, re.I)]
        if not cands:
            raise SystemExit(f'Nenhum mp3 com "{self.nome}" no nome em {self.pasta_video / "audio"}')
        return max(cands, key=lambda p: p.stat().st_mtime)

    # ---- dados ----
    @cached_property
    def audio_info(self) -> dict:
        if not self.arquivo_audio_json.exists():
            raise SystemExit(f'Falta {self.arquivo_audio_json}. Rode antes: ma audio {self.video} {self.numero}')
        return tempos.ler_audio_json(self.arquivo_audio_json)

    @cached_property
    def mapa(self) -> tempos.MapaRitmo:
        a = self.audio_info
        r = a['ritmo']
        return tempos.MapaRitmo(audio.inseridos(a['pausas'], r['alonga'], r['acrescimo']), r['tempo'])

    @property
    def duracao(self) -> float:
        """Duração da narração desacelerada (s)."""
        return self.audio_info['duracao_lenta']

    @cached_property
    def deixas(self) -> tempos.Deixas:
        if not self.arquivo_tempos.exists():
            raise SystemExit(f'Falta {self.arquivo_tempos}. Rode antes: ma tempos {self.video} {self.numero}')
        return tempos.Deixas(tempos.ler(self.arquivo_tempos), self.mapa, self.duracao)

    # ---- script de cena ----
    @cached_property
    def cena(self):
        if not self.arquivo_cena.exists():
            raise SystemExit(f'Falta o script de cena {self.arquivo_cena} (modelo: videos/video-01/bloco1/cena.py)')
        nome = f'cena_{self.video}_{self.nome}'.replace('-', '_')
        spec = importlib.util.spec_from_file_location(nome, self.arquivo_cena)
        mod = importlib.util.module_from_spec(spec)
        antes, sys.dont_write_bytecode = sys.dont_write_bytecode, True      # não sujar a pasta do bloco
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.dont_write_bytecode = antes
        return mod

    @property
    def entrada(self) -> float:
        """Segundos de vídeo antes da narração começar."""
        return getattr(self.cena, 'ENTRADA', 0.4)

    @property
    def saida(self) -> float:
        """Segundos de vídeo depois do fim da narração (o último segundo escurece)."""
        return getattr(self.cena, 'SAIDA', 1.0)

    @property
    def fim(self) -> float:
        return self.entrada + self.duracao + self.saida

    @property
    def n_quadros(self) -> int:
        return int(self.fim * config.FPS)

    def elenco(self):
        """Tudo o que o script de cena declarou (camadas, bonecos, chamas), inclusive dentro de listas/dicionários."""
        vistos, out = set(), []

        def visitar(v):
            if hasattr(v, 'preparar') and not isinstance(v, type):
                if id(v) not in vistos:
                    vistos.add(id(v))
                    out.append(v)
            elif isinstance(v, (list, tuple)):
                for x in v:
                    visitar(x)
            elif isinstance(v, dict):
                for x in v.values():
                    visitar(x)
        for nome, v in vars(self.cena).items():
            if not nome.startswith('_'):
                visitar(v)
        return out

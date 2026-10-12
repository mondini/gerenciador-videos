"""Pastas e dados de um vídeo e de um bloco; carregamento do script de cena.

Estrutura de um vídeo (videos/MA-NNN-slug/, ex.: videos/MA-001-the-man-who-had-everything/):
  roteiro.md               roteiro e status
  audio/                   mp3 do ElevenLabs (fora do git)
  blocoN/cena.py           script de cena do bloco N (elenco + função quadro)
  blocoN/tempos.txt        deixas: nome, segundo no áudio original, frase
  blocoN/audio.json        qual mp3 foi usado, pausas detectadas e parâmetros de ritmo (gerado)
Peças sem narração, iguais em todos os vídeos, ficam em videos/comum/<nome>/cena.py (ex.: abertura),
com DURACAO no script de cena.
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

# Transições na montagem (decisão de 12/10/2026; ver `ma juntar`):
#   bloco -> bloco (e a Pausa): dissolve de DISSOLVE s, sem escuro; os blocos do meio não escurecem no fim;
#   peça comum -> bloco: o bloco nasce do escuro em DISSOLVE s; bloco -> peça comum: o bloco escurece e corta.
DISSOLVE = 1.5
ENTRADA_BLOCO = 0.4 + DISSOLVE      # a voz entra depois do dissolve (o intervalo entre as falas fica ~1,4 s)
# The Pause: escurece devagar e o próximo bloco só começa a aparecer 3 s depois da última frase.
SAIDA_PAUSA = 3.0 + DISSOLVE
FADE_PAUSA = (SAIDA_PAUSA - 0.4, 2.4)


def nome_video(v) -> str:
    """Nome da pasta do vídeo. Aceita '1', '01', 'video-01', 'MA-001' ou o slug inteiro -> 'MA-001-the-man-who-had-everything'.

    A pasta é achada pelo código (`MA-001`), então o slug pode mudar sem quebrar os comandos.
    """
    v = str(v)
    m = re.fullmatch(rf'(?:video-?|{config.PREFIXO}-)?(\d+)', v, re.I)
    if not m:
        return v
    codigo = f'{config.PREFIXO}-{int(m.group(1)):03d}'
    achadas = sorted(p.name for p in config.VIDEOS.glob(f'{codigo}*')
                     if p.is_dir() and (p.name == codigo or p.name.startswith(f'{codigo}-')))
    if len(achadas) > 1:
        raise SystemExit(f'Mais de uma pasta para {codigo}: {", ".join(achadas)}')
    return achadas[0] if achadas else codigo


class Bloco:
    """Um bloco de um vídeo: caminhos, script de cena, deixas e duração."""

    def __init__(self, video, numero):
        self.video = nome_video(video)
        n = str(numero)
        self.numero = int(n) if n.isdigit() else n          # número do bloco ou nome de uma peça ('abertura')
        self.nome = f'bloco{self.numero}' if n.isdigit() else n
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
        """O mp3 mais recente de videos/<vídeo>/audio/ com 'blocoN' (ou o nome da peça, ex.: 'pausa') no nome."""
        padrao = rf'bloco0*{self.numero}(?!\d)' if isinstance(self.numero, int) else rf'\b{self.nome}\b'
        cands = [p for p in (self.pasta_video / 'audio').glob('*.mp3') if re.search(padrao, p.name, re.I)]
        if not cands:
            raise SystemExit(f'Nenhum mp3 com "{self.nome}" no nome em {self.pasta_video / "audio"}')
        return max(cands, key=lambda p: p.stat().st_mtime)

    # ---- dados ----
    @property
    def sem_narracao(self) -> bool:
        """Peça sem narração (abertura, vinheta): a duração vem de DURACAO no script de cena."""
        return self.arquivo_cena.exists() and hasattr(self.cena, 'DURACAO')

    @cached_property
    def audio_info(self) -> dict:
        if not self.arquivo_audio_json.exists():
            raise SystemExit(f'Falta {self.arquivo_audio_json}. Rode antes: ma audio {self.video} {self.numero}')
        return tempos.ler_audio_json(self.arquivo_audio_json)

    @cached_property
    def mapa(self) -> tempos.MapaRitmo:
        if self.sem_narracao:
            return tempos.MapaRitmo([], 1.0)
        a = self.audio_info
        r = a['ritmo']
        return tempos.MapaRitmo(audio.inseridos(a['pausas'], r['alonga'], r['acrescimo'], a.get('minimos')), r['tempo'])

    @property
    def duracao(self) -> float:
        """Duração da narração já no ritmo do canal (s); numa peça sem narração, DURACAO."""
        return self.cena.DURACAO if self.sem_narracao else self.audio_info['duracao_lenta']

    @cached_property
    def deixas(self) -> tempos.Deixas:
        if self.sem_narracao and not self.arquivo_tempos.exists():
            return tempos.Deixas([], self.mapa, self.duracao)
        if not self.arquivo_tempos.exists():
            raise SystemExit(f'Falta {self.arquivo_tempos}. Rode antes: ma tempos {self.video} {self.numero}')
        return tempos.Deixas(tempos.ler(self.arquivo_tempos), self.mapa, self.duracao)

    # ---- script de cena ----
    @cached_property
    def cena(self):
        if not self.arquivo_cena.exists():
            raise SystemExit(f'Falta o script de cena {self.arquivo_cena} (modelo: videos/MA-001-the-man-who-had-everything/bloco1/cena.py)')
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
    def cena_ou_nada(self):
        """O script de cena, ou um objeto vazio se ele ainda não existe (valem os padrões)."""
        return self.cena if self.arquivo_cena.exists() else object()

    @property
    def entrada(self) -> float:
        """Segundos de vídeo antes da narração começar."""
        padrao = 0.0 if self.sem_narracao else 0.4 if self.numero == 1 else ENTRADA_BLOCO
        return getattr(self.cena_ou_nada, 'ENTRADA', padrao)

    @property
    def saida(self) -> float:
        """Segundos de vídeo depois do fim da narração (o último segundo escurece)."""
        padrao = 0.0 if self.sem_narracao else SAIDA_PAUSA if self.nome == 'pausa' else 1.0
        return getattr(self.cena_ou_nada, 'SAIDA', padrao)

    @property
    def fade(self):
        """(segundos antes do fim em que o escurecimento final começa, duração do escurecimento), ou None.

        Escurecem: o gancho (bloco 1, antes da abertura), a Pausa e as peças sem narração. Os outros blocos
        terminam acesos (dissolve na montagem); o último bloco, antes do encerramento, declara FADE na cena."""
        if self.nome == 'pausa':
            padrao = FADE_PAUSA
        elif self.sem_narracao or self.numero == 1:
            padrao = (1.0, 0.9)
        else:
            padrao = None
        return getattr(self.cena_ou_nada, 'FADE', padrao)

    @property
    def acende(self):
        """(segundos no escuro, segundos para a luz subir, 'suave' | 'lanterna') no começo da peça."""
        return getattr(self.cena_ou_nada, 'ACENDE', (0.0, 0.0, 'suave'))

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

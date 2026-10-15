#!/usr/bin/env python3
"""Painel de todos os canais do repositório. Só lê: nunca altera nada nos canais.

  ./canais                    vídeos por etapa, próximas publicações e créditos do ElevenLabs
  ./canais calendario [-d N]  publicações de todos os canais nos próximos N dias (padrão: 30)
  ./canais creditos           gasto de créditos por canal e saldo da conta do ElevenLabs

O que cada canal oferece ao painel (contrato no CLAUDE.md da raiz):
  canal.json               nome, prefixo, pasta_drive e, opcional, "status": comando que imprime {"videos": [...]}
  calendario.json          publicações (fuso + itens)
  creditos-elevenlabs.csv  um registro por geração de narração
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shlex
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parent.parent
BRASILIA = ZoneInfo('America/Sao_Paulo')
ETAPAS = ['Ideia', 'Pesquisa', 'Roteiro', 'Narração', 'Imagens', 'Edição', 'Thumbnail', 'Pronto', 'Agendado', 'Publicado']
DIAS = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']


@dataclass
class Canal:
    pasta: Path
    nome: str
    prefixo: str
    comando_status: str = ''
    tem_canal_json: bool = True
    videos: list[dict] = field(default_factory=list)
    aviso: str = ''                     # status estimado ou comando com erro


def ler_canais(raiz: Path = RAIZ) -> list[Canal]:
    out = []
    for pasta in sorted(p for p in raiz.glob('canal-*') if p.is_dir()):
        arq = pasta / 'canal.json'
        cfg = json.loads(arq.read_text(encoding='utf-8')) if arq.exists() else {}
        out.append(Canal(pasta=pasta, nome=cfg.get('nome') or pasta.name, prefixo=cfg.get('prefixo') or '?',
                         comando_status=cfg.get('status', ''), tem_canal_json=arq.exists()))
    return out


# ---------------------------------------------------------------- status dos vídeos

def carregar_videos(canal: Canal) -> None:
    if canal.comando_status:
        r = None
        try:
            # sem shell: o comando do canal.json roda como programa + argumentos, sem interpretação do shell
            r = subprocess.run(shlex.split(canal.comando_status), cwd=canal.pasta, capture_output=True, text=True, timeout=180)
            videos = json.loads(r.stdout)['videos']
            if not isinstance(videos, list):
                raise TypeError('"videos" não é uma lista')
            canal.videos = videos
            return
        except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, TypeError, ValueError, OSError) as e:
            erro = (r.stderr.strip().splitlines() or [''])[-1] if r is not None and r.stderr else ''
            canal.aviso = (f'o comando de status falhou ({canal.comando_status}): {type(e).__name__}'
                           + (f' — {erro}' if erro else '') + '; status estimado pelas pastas')
    elif not canal.tem_canal_json:
        canal.aviso = 'sem canal.json; status estimado pelas pastas'
    else:
        canal.aviso = 'sem comando de status no canal.json; status estimado pelas pastas'
    canal.videos = estimar_videos(canal.pasta)


def estimar_videos(pasta_canal: Path) -> list[dict]:
    """Status aproximado pela estrutura padrão de pastas, para canais sem comando de status."""
    out = []
    for p in sorted((pasta_canal / 'videos').glob('*')):
        m = re.match(r'([A-Z]+-\d+)(?:-(.*))?$', p.name)
        if not (p.is_dir() and m):
            continue
        tem = lambda padrao: any(p.glob(padrao))
        roteiro, audio, final, pacote = (p / 'roteiro.md').exists(), tem('audio/*.mp3'), tem('final/*.mp4'), (p / 'pacote-de-publicacao.md').exists()
        etapa = ('Pronto' if final and pacote else 'Thumbnail' if final else 'Imagens' if audio
                 else 'Roteiro' if roteiro else 'Ideia')
        out.append({'codigo': m.group(1), 'titulo': (m.group(2) or '').replace('-', ' '), 'etapa': etapa,
                    'concluido': etapa == 'Pronto', 'pendencias': [], 'creditos_pendentes': 0})
    return out


def etapa_do_video(video: dict, calendario: list[dict], agora: datetime) -> str:
    """A etapa do canal, promovida pelo calendário: Pronto (concluído), Agendado, Publicado."""
    item = next((i for i in calendario if i['tipo'] == 'video' and i['codigo'] == video['codigo']), None)
    if item and (item['situacao'] == 'publicado' or (item['situacao'] == 'agendado' and item['quando'] <= agora)):
        return 'Publicado'
    if item and item['situacao'] == 'agendado':
        return 'Agendado'
    return 'Pronto' if video.get('concluido') else video['etapa']


# ---------------------------------------------------------------- calendário

def ler_calendario(canal: Canal) -> list[dict]:
    arq = canal.pasta / 'calendario.json'
    if not arq.exists():
        return []
    cal = json.loads(arq.read_text(encoding='utf-8'))
    fuso = ZoneInfo(cal['fuso'])
    out = []
    for i in cal['itens']:
        quando = datetime.combine(date.fromisoformat(i['data']), time.fromisoformat(i['hora']), tzinfo=fuso)
        out.append({**i, 'quando': quando, 'canal': canal})
    return out


def fmt_quando(dt: datetime) -> str:
    """'qui 15/10 15:00 BRT (14:00 ET)'."""
    br = dt.astimezone(BRASILIA)
    texto = f'{DIAS[br.weekday()]} {br:%d/%m %H:%M} BRT'
    if dt.tzinfo != BRASILIA:
        texto += f' ({dt:%H:%M} {_sigla(dt)})'
    return texto


def _sigla(dt: datetime) -> str:
    nome = dt.tzname() or ''
    return {'EDT': 'ET', 'EST': 'ET'}.get(nome, nome)


# ---------------------------------------------------------------- créditos

def ler_creditos(canal: Canal) -> list[dict]:
    arq = canal.pasta / 'creditos-elevenlabs.csv'
    if not arq.exists():
        return []
    with arq.open(encoding='utf-8', newline='') as f:
        return [{**r, 'creditos': _inteiro(r.get('creditos'))} for r in csv.DictReader(f)]


def _inteiro(v) -> int:
    """Créditos de uma linha do CSV; célula vazia ou inválida conta 0 (não derruba o painel)."""
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def env_raiz(chave: str, raiz: Path = RAIZ) -> str:
    if os.environ.get(chave):
        return os.environ[chave]
    arq = raiz / '.env'
    if arq.exists():
        for linha in arq.read_text(encoding='utf-8').splitlines():
            m = re.match(rf'\s*{re.escape(chave)}\s*=\s*(.*)$', linha)
            if m:
                return m.group(1).strip().strip('"').strip("'").strip()
    return ''


def saldo_elevenlabs() -> str:
    """Saldo da conta (consulta grátis, não gasta créditos)."""
    chave = env_raiz('ELEVENLABS_API_KEY')
    if not chave:
        return 'chave não configurada (ELEVENLABS_API_KEY no .env da raiz)'
    req = urllib.request.Request('https://api.elevenlabs.io/v1/user/subscription', headers={'xi-api-key': chave})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            s = json.loads(r.read())
    except (urllib.error.URLError, TimeoutError) as e:
        return f'não foi possível consultar ({e})'
    usados, limite = s.get('character_count', 0), s.get('character_limit', 0)
    texto = f'{_n(limite - usados)} de {_n(limite)} créditos (plano {s.get("tier", "?")})'
    if s.get('next_character_count_reset_unix'):
        texto += f'; renova em {datetime.fromtimestamp(s["next_character_count_reset_unix"], BRASILIA):%d/%m/%Y}'
    return texto


def _n(x: float) -> str:
    return f'{x:,.0f}'.replace(',', '.')


# ---------------------------------------------------------------- saída

def _titulo(t: str, n: int = 48) -> str:
    return t if len(t) <= n else t[:n - 1] + '…'


def cmd_painel(a, raiz: Path = RAIZ, agora: datetime | None = None) -> str:
    agora = agora or datetime.now(BRASILIA)
    canais = ler_canais(raiz)
    linhas = [f'Painel dos canais · {DIAS[agora.weekday()]} {agora:%d/%m/%Y %H:%M} (Brasília)', '']
    agenda = []
    for c in canais:
        carregar_videos(c)
        cal = ler_calendario(c)
        agenda += cal
        linhas.append(f'{c.nome} · {c.prefixo} · {c.pasta.name}/' if c.tem_canal_json else f'{c.pasta.name}/')
        if c.aviso:
            linhas.append(f'  ({c.aviso})')
        etapas = {v['codigo']: etapa_do_video(v, cal, agora) for v in c.videos}
        contagem = [f'{e} {list(etapas.values()).count(e)}' for e in ETAPAS if e in etapas.values()]
        linhas.append('  ' + (' · '.join(contagem) if contagem else 'nenhum vídeo'))
        ideias = [v['codigo'] for v in c.videos if etapas[v['codigo']] == 'Ideia']
        for v in c.videos:
            etapa = etapas[v['codigo']]
            if etapa == 'Ideia':
                continue
            extra = ''
            pub = next((i for i in cal if i['tipo'] == 'video' and i['codigo'] == v['codigo']), None)
            if pub and etapa in ('Pronto', 'Agendado', 'Publicado'):
                extra = ('planejado ' if pub['situacao'] == 'planejado' else '') + fmt_quando(pub['quando'])
            elif v.get('pendencias'):
                extra = f'falta {len(v["pendencias"])} item(ns)'
            if v.get('creditos_pendentes'):
                extra += f' · ~{_n(v["creditos_pendentes"])} créditos a gastar'
            linhas.append(f'  {v["codigo"]:<9} {etapa:<10} {_titulo(v["titulo"]):<48}  {extra}'.rstrip())
        if ideias:
            linhas.append(f'  Ideia: {", ".join(ideias)}')
        linhas.append('')

    proximas = sorted((i for i in agenda if agora <= i['quando'] <= agora + timedelta(days=14)), key=lambda i: i['quando'])
    linhas.append('Próximas publicações (14 dias)')
    linhas += [_linha_agenda(i) for i in proximas] or ['  nenhuma']
    linhas.append('')
    linhas += _bloco_creditos(canais, agora)
    return '\n'.join(linhas)


def _linha_agenda(i: dict) -> str:
    return (f'  {fmt_quando(i["quando"]):<30} {i["canal"].prefixo:<4} {i["tipo"]:<6} {i["codigo"]:<8} '
            f'{_titulo(i["titulo"], 44):<44}  [{i["situacao"]}]')


def _bloco_creditos(canais: list[Canal], agora: datetime) -> list[str]:
    mes = f'{agora:%Y-%m}'
    linhas = ['ElevenLabs', f'  saldo: {saldo_elevenlabs()}']
    for c in canais:
        regs = ler_creditos(c)
        a_gastar = sum(v.get('creditos_pendentes', 0) for v in c.videos)
        if not regs and not a_gastar:
            continue
        no_mes = sum(r['creditos'] for r in regs if r['data'].startswith(mes))
        estimados = sum(1 for r in regs if r['origem'] != 'medido')
        texto = f'  {c.prefixo:<4} gasto em {agora:%m/%Y}: {_n(no_mes)} · total: {_n(sum(r["creditos"] for r in regs))}'
        if estimados:
            texto += f' ({estimados} registro(s) estimado(s))'
        if a_gastar:
            texto += f' · a gastar nos roteiros abertos: ~{_n(a_gastar)}'
        linhas.append(texto)
    return linhas


def cmd_calendario(a, raiz: Path = RAIZ, agora: datetime | None = None) -> str:
    agora = agora or datetime.now(BRASILIA)
    desde = agora - timedelta(days=1)                       # inclui as de ontem, para conferir o que acabou de sair
    itens = sorted((i for c in ler_canais(raiz) for i in ler_calendario(c)
                    if desde <= i['quando'] <= agora + timedelta(days=a.dias)), key=lambda i: i['quando'])
    return '\n'.join([f'Publicações de {desde:%d/%m} a {agora + timedelta(days=a.dias):%d/%m/%Y}'] +
                     ([_linha_agenda(i) for i in itens] or ['  nenhuma']))


def cmd_creditos(a, raiz: Path = RAIZ, agora: datetime | None = None) -> str:
    agora = agora or datetime.now(BRASILIA)
    canais = ler_canais(raiz)
    linhas = [f'ElevenLabs · saldo: {saldo_elevenlabs()}', '']
    for c in canais:
        regs = ler_creditos(c)
        linhas.append(f'{c.nome} ({c.prefixo})')
        if not regs:
            linhas += ['  nenhum gasto registrado (creditos-elevenlabs.csv)', '']
            continue
        for r in regs:
            linhas.append(f'  {r["data"]}  {r["video"]:<9} {_n(r["creditos"]):>7}  {r["origem"]:<9} {r["o_que"]}')
        linhas += [f'  total: {_n(sum(r["creditos"] for r in regs))}', '']
    return '\n'.join(linhas).rstrip()


def main(argv=None):
    ap = argparse.ArgumentParser(prog='canais', description='Painel de todos os canais (só leitura).')
    sub = ap.add_subparsers(dest='cmd')
    sp = sub.add_parser('calendario', help='publicações de todos os canais')
    sp.add_argument('-d', '--dias', type=int, default=30, help='quantos dias à frente (padrão: 30)')
    sub.add_parser('creditos', help='gastos do ElevenLabs por canal e saldo')
    a = ap.parse_args(argv)
    print({'calendario': cmd_calendario, 'creditos': cmd_creditos}.get(a.cmd, cmd_painel)(a))


if __name__ == '__main__':
    main()

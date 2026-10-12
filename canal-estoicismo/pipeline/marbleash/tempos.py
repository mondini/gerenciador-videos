"""Tempos da narração: o arquivo de deixas (tempos.txt), o mapa de ritmo e a sugestão automática.

Fluxo de um bloco:
  1. `ma audio`  detecta as pausas do áudio original e grava bloco/audio.json (+ áudio desacelerado);
  2. `ma tempos` sugere bloco/tempos.txt: o início de cada frase do roteiro no áudio ORIGINAL,
     cruzando as pausas com o transcritor (faster-whisper) ou, sem ele, só com as pausas;
  3. você confere/renomeia as deixas usadas no script de cena e ajusta à mão se preciso;
  4. o pipeline converte cada segundo original para o tempo do vídeo desacelerado (MapaRitmo).
"""
from __future__ import annotations

import difflib
import json
import math
import re
import unicodedata
from pathlib import Path


# ---------------- mapa de ritmo: tempo original -> tempo desacelerado ----------------
class MapaRitmo:
    """Converte um segundo do áudio original no segundo do áudio desacelerado."""

    def __init__(self, inseridos, tempo):
        self.inseridos = [tuple(x) for x in inseridos]
        self.tempo = tempo

    def __call__(self, t):
        extra = 0.0
        for mid, acc in self.inseridos:
            if mid < t:
                extra = acc
            else:
                break
        return (t + extra) / self.tempo

    def inverso(self, v):
        """Segundo no áudio original correspondente ao segundo v do áudio desacelerado (aproximado)."""
        lo, hi = 0.0, v * self.tempo + 1
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if self(mid) < v else (lo, mid)
        return lo


# ---------------- arquivo de tempos ----------------
_NOME = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$|^-$')


def ler(caminho):
    """Lê tempos.txt: [(nome, segundo_original, frase)]."""
    linhas = []
    for n, linha in enumerate(Path(caminho).read_text(encoding='utf-8').splitlines(), 1):
        s = linha.split('  #')[0].strip() if not linha.lstrip().startswith('#') else ''
        if not s:
            continue
        partes = s.split(None, 2)
        if len(partes) < 2 or not _NOME.match(partes[0]):
            raise ValueError(f'{caminho}:{n}: esperado "NOME SEGUNDO FRASE", veio {linha!r}')
        try:
            seg = float(partes[1])
        except ValueError:
            raise ValueError(f'{caminho}:{n}: o segundo {partes[1]!r} não é um número')
        linhas.append((partes[0], seg, partes[2] if len(partes) > 2 else ''))
    return linhas


def escrever(caminho, linhas, cabecalho=()):
    """Grava tempos.txt alinhado em colunas. linhas: [(nome, segundo, frase, origem)]."""
    w = max([len(l[0]) for l in linhas] + [4])
    out = [f'# {c}' if c else '#' for c in cabecalho]
    for nome, seg, frase, origem in linhas:
        corpo = f'{nome:<{w}}  {seg:6.2f}  {frase}'
        out.append(f'{corpo:<{w + 76}}  # {origem}' if origem else corpo)
    Path(caminho).write_text('\n'.join(out) + '\n', encoding='utf-8')


class Deixas:
    """As deixas de um bloco no tempo do vídeo (segundos desde o início da narração): c.nome."""

    def __init__(self, linhas, mapa, fim):
        self._t = {}
        for nome, seg, _ in linhas:
            if nome != '-':
                if nome in self._t:
                    raise ValueError(f'deixa repetida em tempos.txt: {nome}')
                self._t[nome] = mapa(seg)
        self._t.setdefault('fim', fim)

    def __getattr__(self, nome):
        if nome.startswith('_'):
            raise AttributeError(nome)
        try:
            return self._t[nome]
        except KeyError:
            raise AttributeError(f'deixa {nome!r} não existe em tempos.txt (há: {", ".join(sorted(self._t))})') from None

    def __getitem__(self, nome):
        return self._t[nome]

    def nomes(self):
        return dict(self._t)


# ---------------- texto do roteiro ----------------
# Peças narradas que não são "Bloco N": nome usado no comando -> título da seção no roteiro.md.
TITULOS = {'pausa': 'The Pause'}


def texto_do_bloco(roteiro_md, numero):
    """O texto pronto para o ElevenLabs do "## Bloco N" do roteiro.md (bloco de código).
    `numero` também pode ser o nome de uma peça narrada de TITULOS (ex.: 'pausa' -> "## The Pause")."""
    txt = Path(roteiro_md).read_text(encoding='utf-8')
    titulo = TITULOS.get(str(numero), f'Bloco {numero}')
    m = re.search(rf'^## {re.escape(titulo)}\b.*?\n```[^\n]*\n(.*?)```', txt, re.S | re.M)
    if not m:
        raise ValueError(f'não achei "## {titulo}" seguido de um bloco ``` em {roteiro_md}')
    return m.group(1)


_TAG = re.compile(r'\[[a-z ]+\]')


def palavras_do_texto(texto):
    """Palavras do roteiro (sem as audio tags), cada uma com a força da pausa escrita depois dela.

    força: 3 = fim de linha, 2 = ponto/reticências/interrogação/exclamação, 1 = vírgula/dois-pontos, 0 = nada.
    """
    out = []
    for linha in texto.splitlines():
        linha = _TAG.sub(' ', linha)
        toks = re.findall(r"[A-Za-zÀ-ÿ0-9'’\-]+[^\sA-Za-zÀ-ÿ0-9'’\-]*", linha)
        for i, tok in enumerate(toks):
            m = re.match(r"([A-Za-zÀ-ÿ0-9'’\-]+)(.*)", tok)
            palavra, pont = m.group(1), m.group(2)
            forca = 2 if re.search(r'[.?!…]', pont) else (1 if re.search(r'[,;:]', pont) else 0)
            if i == len(toks) - 1:
                forca = 3
            out.append({'palavra': palavra, 'texto': tok, 'forca': forca})
    return out


def _sem_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def _norm(p):
    return re.sub(r"[^a-z0-9]", '', _sem_acento(p.lower()))


def _silabas(p):
    p = _norm(p)
    if not p:
        return 1
    if p.isdigit():
        return 2 * len(p)
    grupos = re.findall(r'[aeiouy]+', p)
    n = len(grupos) - (1 if p.endswith('e') and len(grupos) > 1 and not p.endswith(('le', 'ee'))  else 0)
    return max(1, n)


def frases(palavras, forca_min=1):
    """Agrupa as palavras em frases, quebrando onde a força da pontuação é >= forca_min."""
    out, atual = [], []
    for i, w in enumerate(palavras):
        atual.append(i)
        if w['forca'] >= forca_min:
            out.append(atual)
            atual = []
    if atual:
        out.append(atual)
    return out


def nome_automatico(palavras, idx, usados):
    base = '_'.join(_norm(palavras[i]['palavra']) for i in idx[:2]) or 'frase'
    if not re.match(r'^[a-z_]', base):
        base = 'f_' + base
    nome, k = base, 2
    while nome in usados:
        nome, k = f'{base}{k}', k + 1
    usados.add(nome)
    return nome


# ---------------- sugestão de tempos ----------------
def transcrever(caminho_audio, modelo='small.en', pasta_modelos=None):
    """Palavras com tempo [(palavra, início, fim)] pelo faster-whisper (None se não estiver instalado)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    import os
    if pasta_modelos:
        os.environ.setdefault('HF_HOME', str(Path(pasta_modelos) / 'hf'))
        os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
    m = WhisperModel(modelo, device='cpu', compute_type='int8', download_root=str(pasta_modelos) if pasta_modelos else None)
    segs, _ = m.transcribe(str(caminho_audio), language='en', word_timestamps=True, beam_size=5, vad_filter=False)
    return [(w.word.strip(), float(w.start), float(w.end)) for s in segs for w in s.words]


def _inicios_pelas_palavras(palavras, transcritas):
    """Tempo de início de cada palavra do roteiro, casando com as palavras transcritas."""
    a = [_norm(w['palavra']) for w in palavras]
    b = [_norm(w[0]) for w in transcritas]
    t = [None] * len(a)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            t[blk.a + k] = transcritas[blk.b + k][1]
    for op, i1, i2, j1, j2 in sm.get_opcodes():          # trocas 1 para 1 (palavra transcrita diferente)
        if op == 'replace':
            for k in range(min(i2 - i1, j2 - j1)):
                if t[i1 + k] is None:
                    t[i1 + k] = transcritas[j1 + k][1]
    conhecidos = [i for i, v in enumerate(t) if v is not None]
    for i in range(len(t)):                               # o que sobrou: interpola pelas sílabas
        if t[i] is None and conhecidos:
            ant = max([k for k in conhecidos if k < i], default=None)
            pos = min([k for k in conhecidos if k > i], default=None)
            if ant is not None and pos is not None:
                s_tot = sum(_silabas(palavras[k]['palavra']) for k in range(ant, pos))
                s_ate = sum(_silabas(palavras[k]['palavra']) for k in range(ant, i))
                t[i] = t[ant] + (t[pos] - t[ant]) * s_ate / max(s_tot, 1)
            else:
                t[i] = t[ant] if ant is not None else t[pos]
    return t


def _inicios_pelas_pausas(palavras, falas):
    """Sem transcritor: distribui as palavras nos trechos de fala entre pausas (programação dinâmica)."""
    n, m = len(palavras), len(falas)
    sil = [_silabas(w['palavra']) for w in palavras]
    pref = [0]
    for s in sil:
        pref.append(pref[-1] + s)
    taxa = sum(e - s for s, e in falas) / max(pref[-1], 1)          # segundos por sílaba
    custo_quebra = {3: 0.0, 2: 0.0, 1: 0.4, 0: 3.0}
    custo_dentro = {3: 0.6, 2: 0.3, 1: 0.0, 0: 0.0}
    dentro = [0.0]                       # soma acumulada do custo de pontuação "engolida" dentro de um trecho
    for w in palavras:
        dentro.append(dentro[-1] + custo_dentro[w['forca']])
    INF = float('inf')
    best = [[INF] * (n + 1) for _ in range(m + 1)]
    back = [[0] * (n + 1) for _ in range(m + 1)]
    best[0][0] = 0.0
    for j in range(1, m + 1):
        d = falas[j - 1][1] - falas[j - 1][0]
        for i in range(1, n + 1):
            for k in range(j - 1, i):
                if best[j - 1][k] == INF:
                    continue
                syl = pref[i] - pref[k]
                c = math.log(max(d, 0.05) / (taxa * syl)) ** 2
                c += custo_quebra[palavras[i - 1]['forca']] if i < n else 0.0
                c += dentro[i - 1] - dentro[k]
                if best[j - 1][k] + c < best[j][i]:
                    best[j][i], back[j][i] = best[j - 1][k] + c, k
    t = [0.0] * n
    i = n
    for j in range(m, 0, -1):
        k = back[j][i]
        s, e = falas[j - 1]
        syl = pref[i] - pref[k]
        for q in range(k, i):
            t[q] = s + (e - s) * (pref[q] - pref[k]) / max(syl, 1)
        i = k
    return t


def _casar_pausas(inicios, pausas_, alcance=0.6, sem_pausa=0.6, pausa_sobrando=0.6):
    """Casa, em ordem, cada início aproximado de frase com no máximo uma pausa. Devolve {frase: pausa}.

    O transcritor costuma marcar a palavra seguinte dentro da pausa (ou um pouco antes); por isso a
    distância é medida até o intervalo inteiro da pausa. Frase sem pausa (vírgula falada de corrido) e
    pausa sem frase (respiração no meio da frase) custam `sem_pausa` e `pausa_sobrando`.
    """
    M, N = len(inicios), len(pausas_)
    INF = float('inf')
    D = [[INF] * (N + 1) for _ in range(M + 1)]
    B = [[None] * (N + 1) for _ in range(M + 1)]
    D[0][0] = 0.0
    for k in range(M + 1):
        for j in range(N + 1):
            d0 = D[k][j]
            if d0 == INF:
                continue
            if k < M and d0 + sem_pausa < D[k + 1][j]:
                D[k + 1][j], B[k + 1][j] = d0 + sem_pausa, (k, j, False)
            if j < N and d0 + pausa_sobrando < D[k][j + 1]:
                D[k][j + 1], B[k][j + 1] = d0 + pausa_sobrando, (k, j, False)
            if k < M and j < N:
                s, e = pausas_[j]
                dist = max(0.0, s - inicios[k], inicios[k] - e)
                if dist <= alcance and d0 + 2 * dist < D[k + 1][j + 1]:
                    D[k + 1][j + 1], B[k + 1][j + 1] = d0 + 2 * dist, (k, j, True)
    casados, k, j = {}, M, N
    while (k, j) != (0, 0):
        pk, pj, casou = B[k][j]
        if casou:
            casados[pk] = pj
        k, j = pk, pj
    return casados


def sugerir(texto, pausas_, duracao, transcritas=None):
    """Sugere [(nome, segundo, frase, origem)] para cada frase do texto.

    Com `transcritas` (faster-whisper), usa o tempo das palavras; sem, distribui pelas pausas.
    Frases casadas com uma pausa recebem o fim exato da pausa (origem "pausa").
    """
    palavras = palavras_do_texto(texto)
    if transcritas:
        t = _inicios_pelas_palavras(palavras, transcritas)
        origem_base = 'voz'
    else:
        inicio = 0.0
        falas, a = [], inicio
        for s, e in pausas_:
            falas.append((a, s))
            a = e
        falas.append((a, duracao))
        t = _inicios_pelas_pausas(palavras, falas)
        origem_base = 'estimado'
    grupos = frases(palavras)
    casados = _casar_pausas([t[g[0]] for g in grupos[1:]], pausas_)
    linhas, usados = [], set()
    for n, idx in enumerate(grupos):
        t0 = t[idx[0]]
        if n == 0 and t0 < 0.5:
            t0, origem = 0.0, 'início'
        elif n - 1 in casados:
            t0, origem = pausas_[casados[n - 1]][1], 'pausa'
        else:
            origem = origem_base
        texto_frase = ' '.join(palavras[i]['texto'] for i in idx)
        linhas.append((nome_automatico(palavras, idx, usados), round(t0, 2), texto_frase, origem))
    return linhas


# ---------------- audio.json ----------------
def ler_audio_json(caminho):
    return json.loads(Path(caminho).read_text(encoding='utf-8'))


def gravar_audio_json(caminho, dados):
    Path(caminho).write_text(json.dumps(dados, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')

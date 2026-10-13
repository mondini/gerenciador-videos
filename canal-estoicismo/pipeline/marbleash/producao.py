"""Status de um vídeo (o que já existe e o que falta), backup no Google Drive e limpeza ao concluir.

O status é lido dos arquivos da pasta do vídeo e dos títulos do roteiro.md; não há status escrito à mão.
  - Texto aprovado: o título da seção no roteiro.md tem "aprovado" (ex.: "## Bloco 2 — O homem (aprovado)").
  - Narração: um mp3 em audio/ com o nome da peça (bloco2, pausa).
  - Animação: blocoN/tempos.txt, blocoN/cena.py e a prévia previas/blocoN.mp4.
  - Entrega: final/*.mp4, thumbnails/ (2 imagens: A e C), shorts/ (5+ mp4) e pacote-de-publicacao.md.

Backup: copia para DRIVE_ROOT/<pasta do canal>/VIDEOS/<pasta do vídeo>/, nas subpastas do sistema de gestão.
Nunca apaga nada no Drive. Texto e projeto (roteiro, cena.py, tempos) que mudaram guardam a versão anterior
em _versoes/; mídia que dá para gerar de novo (prévias, final) é só atualizada.
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from . import config, tempos

ETAPAS = ['Roteiro', 'Narração', 'Imagens', 'Edição', 'Thumbnail']   # as do sistema de gestão que o pipeline sabe medir
CREDITOS_POR_CARACTERE = 1                                            # ElevenLabs: ~1 crédito por caractere
SHORTS_MIN = 5
THUMBS_MIN = 2           # A (Palavra) e C (Gancho), para o teste A/B do YouTube (decisão de 12/10/2026)
_IMAGEM = {'.png', '.jpg', '.jpeg', '.webp'}
_SIMULACAO = ('-youtube4mbps', '-4k')                                 # arquivos de conferência, não de entrega


@dataclass
class Peca:
    nome: str                 # bloco2, pausa
    titulo: str               # título da seção no roteiro
    texto_aprovado: bool
    caracteres: int
    mp3: Path | None
    tempos: bool
    cena: bool
    previa: bool

    def faltas(self) -> list[str]:
        f = []
        if not self.texto_aprovado:
            f.append('texto')
        if not self.mp3:
            f.append('narração')
        if not self.tempos:
            f.append('tempos')
        if not self.cena:
            f.append('cena')
        if not self.previa:
            f.append('prévia')
        return f


@dataclass
class Status:
    pasta: Path
    codigo: str
    slug: str
    titulo: str               # título de publicação
    nome_interno: str
    pecas: list[Peca] = field(default_factory=list)
    final: Path | None = None
    duracao_final: float | None = None
    thumbnails: int = 0
    shorts: int = 0
    pacote: bool = False

    @property
    def etapa(self) -> str:
        """Etapa do kanban do sistema em que o vídeo está, pelo que já existe."""
        if not self.pecas or any(not p.texto_aprovado for p in self.pecas):
            return 'Roteiro'
        if any(not p.mp3 for p in self.pecas):
            return 'Narração'
        if any(not (p.tempos and p.cena and p.previa) for p in self.pecas):
            return 'Imagens'
        if not self.final:
            return 'Edição'
        return 'Thumbnail'

    @property
    def concluido(self) -> bool:
        return not self.pendencias()

    @property
    def creditos_pendentes(self) -> int:
        """Créditos do ElevenLabs para narrar as peças que ainda não têm mp3."""
        return sum(p.caracteres for p in self.pecas if not p.mp3) * CREDITOS_POR_CARACTERE

    def pendencias(self) -> list[str]:
        """O que falta, em frases curtas (é isto que vai para o sistema de gestão)."""
        out = []
        if not self.pecas:
            out.append('roteiro: nenhuma seção "## Bloco N" no roteiro.md')
        for p in self.pecas:
            if p.faltas():
                out.append(f'{p.nome}: falta {", ".join(p.faltas())}')
        if not self.final:
            out.append('vídeo final (ma juntar)')
        if self.thumbnails < THUMBS_MIN:
            out.append(f'thumbnails: {self.thumbnails}/{THUMBS_MIN} em thumbnails/')
        if self.shorts < SHORTS_MIN:
            out.append(f'shorts: {self.shorts}/{SHORTS_MIN} em shorts/')
        if not self.pacote:
            out.append('pacote-de-publicacao.md')
        return out


def _campo(md: str, rotulo: str) -> str:
    m = re.search(rf'^\s*-\s*\*\*{re.escape(rotulo)}:\*\*\s*(.+)$', md, re.M)
    return m.group(1).strip() if m else ''


def _secoes(md: str) -> list[tuple[str, str, str]]:
    """(nome da peça, título da seção, linha do título) das seções narradas do roteiro, na ordem."""
    inversos = {v: k for k, v in tempos.TITULOS.items()}
    out = []
    for m in re.finditer(r'^## (.+)$', md, re.M):
        linha = m.group(1)
        b = re.match(r'Bloco (\d+)\b', linha)
        if b:
            out.append((f'bloco{b.group(1)}', f'Bloco {b.group(1)}', linha))
            continue
        for titulo, nome in inversos.items():
            if linha.startswith(titulo):
                out.append((nome, titulo, linha))
    return out


def _mp3(pasta: Path, nome: str) -> Path | None:
    num = re.fullmatch(r'bloco(\d+)', nome)
    padrao = rf'bloco0*{num.group(1)}(?!\d)' if num else rf'\b{nome}\b'
    cands = [p for p in (pasta / 'audio').glob('*.mp3') if re.search(padrao, p.name, re.I)]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def _final(pasta: Path) -> Path | None:
    cands = [p for p in (pasta / 'final').glob('*.mp4') if not any(s in p.stem for s in _SIMULACAO)]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def _previa(pasta: Path, nome: str) -> bool:
    """A prévia do bloco no Mac ou, depois do `ma limpar`, a cópia no Drive (04_video/)."""
    if (pasta / 'previas' / f'{nome}.mp4').exists():
        return True
    try:
        return (pasta_drive_do_video(pasta) / '04_video' / f'{nome}.mp4').exists()
    except SystemExit:              # Drive indisponível: só vale o que está no Mac
        return False


def ler_status(pasta_video: Path) -> Status:
    pasta = Path(pasta_video)
    m = re.match(rf'({re.escape(config.PREFIXO)}-\d{{3}})(?:-(.*))?$', pasta.name)
    codigo, slug = (m.group(1), m.group(2) or '') if m else (pasta.name, '')
    roteiro = pasta / 'roteiro.md'
    md = roteiro.read_text(encoding='utf-8') if roteiro.exists() else ''
    titulo_h1 = re.search(r'^# (?:.*?—\s*)?(.+)$', md, re.M)
    st = Status(pasta=pasta, codigo=codigo, slug=slug,
                titulo=_campo(md, 'Título de publicação'),
                nome_interno=_campo(md, 'Nome interno') or (titulo_h1.group(1).strip() if titulo_h1 else ''))
    for nome, titulo, linha in _secoes(md):
        try:
            texto = tempos.texto_do_bloco(roteiro, nome.removeprefix('bloco') if nome.startswith('bloco') else nome)
        except ValueError:
            texto = ''
        texto_falado = re.sub(r'\[[a-z ]+\]', '', texto)          # audio tags não contam como fala, mas custam crédito
        sub = pasta / nome
        st.pecas.append(Peca(
            nome=nome, titulo=titulo,
            texto_aprovado=bool(re.search(r'\baprovad[oa]\b', linha, re.I)) and not re.search(r'\bnão aprovad', linha, re.I),
            caracteres=len(texto.strip()) if texto_falado.strip() else 0,
            mp3=_mp3(pasta, nome),
            tempos=(sub / 'tempos.txt').exists(),
            cena=(sub / 'cena.py').exists(),
            previa=_previa(pasta, nome),
        ))
    st.final = _final(pasta)
    st.thumbnails = sum(1 for p in (pasta / 'thumbnails').glob('*') if p.suffix.lower() in _IMAGEM)
    st.shorts = len(list((pasta / 'shorts').glob('*.mp4')))
    st.pacote = (pasta / 'pacote-de-publicacao.md').exists()
    return st


# ---------------------------------------------------------------- backup no Drive

def pasta_drive_do_video(pasta_video: Path, drive_root: Path | None = None) -> Path:
    raiz = Path(drive_root) if drive_root else _drive_root()
    return raiz / config.CANAL_INFO.get('pasta_drive', 'Marble & Ash') / 'VIDEOS' / Path(pasta_video).name


def _drive_root() -> Path:
    v = config.env_repo('DRIVE_ROOT')
    if not v:
        raise SystemExit('DRIVE_ROOT não definido (no .env da raiz do repositório, o mesmo do sistema de gestão).')
    raiz = Path(v).expanduser()
    if not raiz.is_dir():
        raise SystemExit(f'DRIVE_ROOT não existe: {raiz}\nO Google Drive for Desktop está aberto e logado?')
    return raiz


def _mapa_backup(pasta: Path) -> list[tuple[Path, str, bool]]:
    """(arquivo local, destino relativo à pasta do vídeo no Drive, guardar versão anterior se mudar)."""
    itens: list[tuple[Path, str, bool]] = []
    for nome in ('roteiro.md', 'pacote-de-publicacao.md'):
        if (pasta / nome).exists():
            itens.append((pasta / nome, f'01_roteiro/{nome}', True))
    for p in sorted((pasta / 'audio').glob('*.mp3')):
        itens.append((p, f'02_audio/{p.name}', True))
    for p in sorted((pasta / 'previas').glob('*')):
        if p.is_file() and (p.suffix == '.mp4' or p.suffix.lower() in _IMAGEM) and not any(s in p.stem for s in _SIMULACAO):
            itens.append((p, f'04_video/{p.name}', False))
    for sub in sorted(x for x in pasta.iterdir() if x.is_dir() and (x / 'cena.py').exists()):
        for nome in ('cena.py', 'tempos.txt', 'audio.json'):
            if (sub / nome).exists():
                itens.append((sub / nome, f'05_projeto/{sub.name}/{nome}', True))
    for p in sorted((pasta / 'thumbnails').glob('*')):
        if p.suffix.lower() in _IMAGEM:
            itens.append((p, f'06_thumbnail/{p.name}', True))
    for p in sorted((pasta / 'final').glob('*.mp4')):
        if not any(s in p.stem for s in _SIMULACAO):
            itens.append((p, f'07_export/{p.name}', False))
    for p in sorted((pasta / 'shorts').glob('*.mp4')):
        itens.append((p, f'07_export/shorts/{p.name}', False))
    return itens


def _igual(a: Path, b: Path) -> bool:
    if not b.exists() or a.stat().st_size != b.stat().st_size:
        return False
    if a.stat().st_size < 5_000_000:                          # texto e arquivos pequenos: compara o conteúdo
        return a.read_bytes() == b.read_bytes()
    return int(b.stat().st_mtime) >= int(a.stat().st_mtime)   # mídia grande: tamanho + data (não baixa do Drive)


def _copiar(origem: Path, destino: Path) -> None:
    """Copia por um arquivo temporário e renomeia no fim: o Drive nunca vê um arquivo pela metade."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_name(f'.{destino.name}.parcial')
    shutil.copy2(origem, tmp)
    tmp.replace(destino)


def backup(pasta_video: Path, drive_root: Path | None = None, agora: datetime | None = None, avisar=print) -> dict:
    """Copia o vídeo para o Drive. Devolve contagens {novos, atualizados, iguais, versoes, bytes}."""
    pasta = Path(pasta_video)
    destino = pasta_drive_do_video(pasta, drive_root)
    carimbo = (agora or datetime.now()).strftime('%Y-%m-%d_%H%M%S')
    res = {'novos': 0, 'atualizados': 0, 'iguais': 0, 'versoes': 0, 'bytes': 0, 'destino': destino}
    for origem, rel, versionar in _mapa_backup(pasta):
        alvo = destino / rel
        if _igual(origem, alvo):
            res['iguais'] += 1
            continue
        if alvo.exists():
            if versionar:
                _copiar(alvo, destino / '_versoes' / carimbo / rel)
                res['versoes'] += 1
            res['atualizados'] += 1
        else:
            res['novos'] += 1
        _copiar(origem, alvo)
        res['bytes'] += origem.stat().st_size
        avisar(f'  -> {rel}')
    return res


# ---------------------------------------------------------------- limpeza ao concluir

def _tamanho(p: Path) -> int:
    return p.stat().st_size if p.is_file() else sum(f.stat().st_size for f in p.rglob('*') if f.is_file())


def plano_limpeza(pasta_video: Path, drive_root: Path | None = None) -> list[Path]:
    """O que pode sair do Mac quando o vídeo está concluído e com backup.

    Sai: trabalho/ (intermediários, refeitos pelo pipeline; menos trabalho/referencia/, usada no teste visual),
    previas/stills/ (conferência), as simulações do YouTube e as prévias (vídeos e imagens) que já estão no Drive
    com o mesmo tamanho. Fica: roteiro, áudios, scripts de cena, final, thumbnails, shorts e pacote.
    """
    pasta = Path(pasta_video)
    destino = pasta_drive_do_video(pasta, drive_root)
    sai: list[Path] = []
    trabalho = pasta / 'trabalho'
    if trabalho.is_dir():
        sai += [p for p in sorted(trabalho.iterdir()) if p.name != 'referencia']
    previas = pasta / 'previas'
    if previas.is_dir():
        for p in sorted(previas.iterdir()):
            if p.is_dir() or any(s in p.stem for s in _SIMULACAO):
                sai.append(p)
            elif p.suffix == '.mp4' or p.suffix.lower() in _IMAGEM:
                no_drive = destino / '04_video' / p.name
                if no_drive.exists() and no_drive.stat().st_size == p.stat().st_size:
                    sai.append(p)
    sai += [p for p in sorted((pasta / 'final').glob('*.mp4')) if any(s in p.stem for s in _SIMULACAO)]
    return sai


def limpar(itens: list[Path]) -> int:
    """Apaga os itens (só na pasta local do canal, nunca no Drive). Devolve os bytes liberados."""
    total = 0
    for p in itens:
        if not p.resolve().is_relative_to(config.VIDEOS.resolve()):
            raise SystemExit(f'Recusado: {p} está fora de {config.VIDEOS}')
        total += _tamanho(p)
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    return total


# ---------------------------------------------------------------- sincronização com o sistema de gestão

def dados_sincronizar(st: Status) -> dict:
    """Corpo do POST /api/sincronizar do sistema de gestão (ver src/server/servicos/sincronizar.ts)."""
    return {
        'prefixo': config.PREFIXO,
        'codigo': st.codigo,
        'pasta': st.pasta.name,
        'nomeInterno': st.nome_interno or st.slug or st.codigo,
        'tituloFinal': st.titulo or None,
        'etapa': st.etapa,
        'roteiro': (st.pasta / 'roteiro.md').read_text(encoding='utf-8') if (st.pasta / 'roteiro.md').exists() else '',
        'duracaoFinalSeg': round(st.duracao_final) if st.duracao_final else None,
        'pendencias': st.pendencias(),
    }


def sincronizar(st: Status, url: str | None = None) -> dict:
    import json
    import urllib.error
    import urllib.request
    base = url or f'http://localhost:{config.env_repo("PORT", "4321")}'
    req = urllib.request.Request(f'{base}/api/sincronizar', data=json.dumps(dados_sincronizar(st)).encode(),
                                 headers={'content-type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f'O sistema recusou: {json.loads(e.read()).get("erro", e)}')
    except urllib.error.URLError:
        raise SystemExit(f'O sistema de gestão não está rodando em {base}. Na raiz do repositório: npm run dev')

"""Status, backup e limpeza de um vídeo. Tudo em pasta temporária: nunca o Drive real."""
import os
from datetime import datetime

import pytest

from marbleash import config, producao

ROTEIRO = '''# Vídeo 1 — The Man Who Had Everything

- **Título de publicação:** The Richest Man in Rome
- **Nome interno:** The Man Who Had Everything

## Bloco 1 — Gancho (aprovado)

```
He had everything. [pause] Not yet.
```

## The Pause (aprovado)

```
Breathe in.
```

## Bloco 2 — O homem

```
A man in Rome.
```
'''


def _video(tmp_path, nome='MA-001-the-man-who-had-everything'):
    pasta = tmp_path / 'videos' / nome
    pasta.mkdir(parents=True)
    (pasta / 'roteiro.md').write_text(ROTEIRO, encoding='utf-8')
    return pasta


def _arq(p, conteudo=b'x'):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(conteudo)
    return p


def _peca_pronta(pasta, nome):
    _arq(pasta / 'audio' / f'video01-{nome}-starter.mp3')
    _arq(pasta / nome / 'tempos.txt')
    _arq(pasta / nome / 'cena.py')
    _arq(pasta / 'previas' / f'{nome}.mp4')


def test_status_le_codigo_titulos_e_pecas(tmp_path):
    st = producao.ler_status(_video(tmp_path))
    assert (st.codigo, st.slug) == ('MA-001', 'the-man-who-had-everything')
    assert st.titulo == 'The Richest Man in Rome'
    assert st.nome_interno == 'The Man Who Had Everything'
    assert [(p.nome, p.texto_aprovado) for p in st.pecas] == [('bloco1', True), ('pausa', True), ('bloco2', False)]
    assert st.etapa == 'Roteiro'
    assert st.creditos_pendentes == len('He had everything. [pause] Not yet.') + len('Breathe in.') + len('A man in Rome.')


def test_etapa_avanca_com_os_arquivos(tmp_path):
    pasta = _video(tmp_path)
    (pasta / 'roteiro.md').write_text(ROTEIRO.replace('## Bloco 2 — O homem', '## Bloco 2 — O homem (aprovado)'))
    assert producao.ler_status(pasta).etapa == 'Narração'
    for nome in ('bloco1', 'pausa', 'bloco2'):
        _arq(pasta / 'audio' / f'video01-{nome}-starter.mp3')
    st = producao.ler_status(pasta)
    assert (st.etapa, st.creditos_pendentes) == ('Imagens', 0)
    for nome in ('bloco1', 'pausa', 'bloco2'):
        _peca_pronta(pasta, nome)
    assert producao.ler_status(pasta).etapa == 'Edição'
    _arq(pasta / 'final' / 'MA-001-youtube4mbps.mp4')            # simulação não conta como final
    assert producao.ler_status(pasta).etapa == 'Edição'
    _arq(pasta / 'final' / 'MA-001.mp4')
    st = producao.ler_status(pasta)
    assert st.etapa == 'Thumbnail' and not st.concluido
    assert st.pendencias() == ['thumbnails: 0/3 em thumbnails/', 'shorts: 0/5 em shorts/', 'pacote-de-publicacao.md']
    for letra in 'ABC':
        _arq(pasta / 'thumbnails' / f'MA-001_thumb_{letra}.png')
    for i in range(5):
        _arq(pasta / 'shorts' / f'short{i}.mp4')
    _arq(pasta / 'pacote-de-publicacao.md')
    assert producao.ler_status(pasta).concluido


def test_bloco10_nao_confunde_com_bloco1(tmp_path):
    pasta = _video(tmp_path)
    _arq(pasta / 'audio' / 'video01-bloco10-starter.mp3')
    assert producao.ler_status(pasta).pecas[0].mp3 is None


def test_backup_copia_nas_subpastas_e_nunca_apaga(tmp_path):
    pasta = _video(tmp_path)
    _peca_pronta(pasta, 'bloco1')
    drive = tmp_path / 'drive'
    drive.mkdir()
    res = producao.backup(pasta, drive, avisar=lambda *_: None)
    dest = producao.pasta_drive_do_video(pasta, drive)
    assert dest.name == 'MA-001-the-man-who-had-everything'
    for rel in ('01_roteiro/roteiro.md', '02_audio/video01-bloco1-starter.mp3', '04_video/bloco1.mp4',
                '05_projeto/bloco1/cena.py', '05_projeto/bloco1/tempos.txt'):
        assert (dest / rel).exists(), rel
    assert res['novos'] == 5
    extra = _arq(dest / '02_audio' / 'take-antigo.mp3')         # o que só existe no Drive fica lá
    assert producao.backup(pasta, drive, avisar=lambda *_: None)['iguais'] == 5
    assert extra.exists()


def test_backup_guarda_versao_anterior_do_roteiro(tmp_path):
    pasta = _video(tmp_path)
    drive = tmp_path / 'drive'
    drive.mkdir()
    producao.backup(pasta, drive, avisar=lambda *_: None)
    (pasta / 'roteiro.md').write_text(ROTEIRO + '\nmais texto\n', encoding='utf-8')
    res = producao.backup(pasta, drive, agora=datetime(2026, 10, 12, 9, 30), avisar=lambda *_: None)
    dest = producao.pasta_drive_do_video(pasta, drive)
    assert res['atualizados'] == 1 and res['versoes'] == 1
    assert (dest / '01_roteiro/roteiro.md').read_text().endswith('mais texto\n')
    assert (dest / '_versoes/2026-10-12_093000/01_roteiro/roteiro.md').read_text() == ROTEIRO


def test_limpeza_so_tira_o_que_tem_backup_ou_e_refeito(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'VIDEOS', tmp_path / 'videos')
    pasta = _video(tmp_path)
    drive = tmp_path / 'drive'
    drive.mkdir()
    _arq(pasta / 'trabalho' / 'bloco1-video.mp4')
    ref = _arq(pasta / 'trabalho' / 'referencia' / 'stills' / 'bloco1_1.0.png')
    _arq(pasta / 'previas' / 'stills' / 'a.png')
    com_backup = _arq(pasta / 'previas' / 'bloco1.mp4')
    producao.backup(pasta, drive, avisar=lambda *_: None)
    sem_backup = _arq(pasta / 'previas' / 'bloco2.mp4')
    simulacao = _arq(pasta / 'final' / 'MA-001-youtube4mbps.mp4')
    final = _arq(pasta / 'final' / 'MA-001.mp4')
    audio = _arq(pasta / 'audio' / 'video01-bloco1-starter.mp3')
    itens = producao.plano_limpeza(pasta, drive)
    assert com_backup in itens and simulacao in itens and pasta / 'trabalho' / 'bloco1-video.mp4' in itens
    assert sem_backup not in itens and final not in itens and audio not in itens
    producao.limpar(itens)
    assert ref.exists() and final.exists() and audio.exists() and sem_backup.exists()
    assert not com_backup.exists() and not (pasta / 'previas' / 'stills').exists()


def test_le_drive_root_do_env_do_repositorio(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'REPO', tmp_path)
    monkeypatch.delenv('DRIVE_ROOT', raising=False)
    (tmp_path / '.env').write_text('# comentário\nDRIVE_ROOT="/x/Meu Drive/Canais"\nOUTRA=1\n')
    assert config.env_repo('DRIVE_ROOT') == '/x/Meu Drive/Canais'
    assert config.env_repo('OUTRA') == '1'
    monkeypatch.setenv('OUTRA', '2')
    assert config.env_repo('OUTRA') == '2'
    assert os.environ['OUTRA'] == '2'


def test_novo_video_a_partir_do_plano(tmp_path, monkeypatch):
    from marbleash import config, producao
    plano = tmp_path / 'plano.md'
    plano.write_text('| # | Nome interno | Título | Tema | Provérbio |\n|---|---|---|---|---|\n'
                     '| 3 | The Last Hour | Memento Mori for Busy Minds | Memento mori | 27:1 |\n\n'
                     '| Formato | O que promete | Vídeos |\n|---|---|---|\n| Conceito estoico | uma ideia | 3, 7 |\n\n'
                     '- **Vídeo 3 — The Last Hour:** memento mori para viver melhor.\n', encoding='utf-8')
    monkeypatch.setattr(config, 'VIDEOS', tmp_path / 'videos')
    pasta = producao.novo_video(3, plano)
    assert pasta.name == f'{config.PREFIXO}-003-the-last-hour'
    txt = (pasta / 'roteiro.md').read_text(encoding='utf-8')
    assert '# Vídeo 3 — The Last Hour' in txt and 'Conceito estoico (uma ideia)' in txt and 'memento mori para viver melhor' in txt
    with pytest.raises(SystemExit):
        producao.novo_video(3, plano)


def test_painel_junta_plano_e_pastas(tmp_path, monkeypatch):
    plano = tmp_path / 'plano.md'
    plano.write_text('| # | Nome interno | Título | Tema | Provérbio |\n|---|---|---|---|---|\n'
                     '| 1 | The Man Who Had Everything | The Richest Man in Rome | Riqueza | 16:18 |\n'
                     '| 2 | On Anger | How to Stay Calm | Raiva | 15:1 |\n', encoding='utf-8')
    monkeypatch.setattr(config, 'VIDEOS', tmp_path / 'videos')
    _video(tmp_path)
    _video(tmp_path, 'MA-007-extra')
    v = {x['codigo']: x for x in producao.painel(plano)}
    assert list(v) == ['MA-001', 'MA-002', 'MA-007']
    assert v['MA-001']['etapa'] == 'Roteiro' and v['MA-001']['titulo'] == 'The Richest Man in Rome'
    assert v['MA-001']['creditos_pendentes'] > 0 and not v['MA-001']['concluido']
    assert v['MA-002'] == {'codigo': 'MA-002', 'titulo': 'How to Stay Calm', 'etapa': 'Ideia', 'concluido': False,
                           'pendencias': [], 'creditos_pendentes': 0}

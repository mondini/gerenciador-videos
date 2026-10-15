"""Painel da raiz, com canais de mentira em pasta temporária."""
import json
import sys
from argparse import Namespace
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import canais  # noqa: E402

AGORA = datetime(2026, 10, 14, 21, 0, tzinfo=canais.BRASILIA)


def _repo(tmp_path):
    a = tmp_path / 'canal-a'
    (a / 'videos').mkdir(parents=True)
    videos = {'videos': [
        {'codigo': 'AA-001', 'titulo': 'Primeiro', 'etapa': 'Thumbnail', 'concluido': True, 'pendencias': [], 'creditos_pendentes': 0},
        {'codigo': 'AA-002', 'titulo': 'Segundo', 'etapa': 'Thumbnail', 'concluido': True, 'pendencias': [], 'creditos_pendentes': 0},
        {'codigo': 'AA-003', 'titulo': 'Terceiro', 'etapa': 'Narração', 'concluido': False, 'pendencias': ['x'], 'creditos_pendentes': 1200},
        {'codigo': 'AA-004', 'titulo': 'Quarto', 'etapa': 'Ideia', 'concluido': False, 'pendencias': [], 'creditos_pendentes': 0}]}
    (a / 'status.json').write_text(json.dumps(videos))
    (a / 'canal.json').write_text(json.dumps({'nome': 'Canal A', 'prefixo': 'AA', 'status': 'cat status.json'}))
    (a / 'calendario.json').write_text(json.dumps({'fuso': 'America/New_York', 'itens': [
        {'data': '2026-10-15', 'hora': '14:00', 'tipo': 'video', 'codigo': 'AA-001', 'titulo': 'Primeiro', 'situacao': 'agendado'},
        {'data': '2026-11-05', 'hora': '14:00', 'tipo': 'video', 'codigo': 'AA-002', 'titulo': 'Segundo', 'situacao': 'planejado'}]}))
    (a / 'creditos-elevenlabs.csv').write_text('data,video,o_que,caracteres,creditos,origem,nota\n'
                                               '2026-09-30,AA-000,teste,100,100,medido,\n'
                                               '2026-10-12,AA-001,blocos,6700,6638,medido,\n')
    b = tmp_path / 'canal-b' / 'videos'
    (b / 'BB-001-piloto').mkdir(parents=True)
    (b / 'BB-001-piloto' / 'roteiro.md').write_text('# piloto')
    (b / 'comum').mkdir()
    return tmp_path


def test_painel_junta_status_calendario_e_creditos(tmp_path, monkeypatch):
    monkeypatch.setattr(canais, 'saldo_elevenlabs', lambda: 'teste')
    txt = canais.cmd_painel(Namespace(), _repo(tmp_path), AGORA)
    assert 'Thumbnail' not in txt                                   # concluído vira Pronto, agendado vira Agendado
    assert 'Narração 1 · Pronto 1 · Agendado 1' in txt
    assert 'AA-001    Agendado' in txt and 'qui 15/10 15:00 BRT (14:00 ET)' in txt
    assert 'Ideia: AA-004' in txt and '~1.200 créditos a gastar' in txt
    assert 'canal-b/\n  (sem canal.json; status estimado pelas pastas)' in txt
    assert 'BB-001    Roteiro' in txt
    assert 'gasto em 10/2026: 6.638 · total: 6.738 · a gastar nos roteiros abertos: ~1.200' in txt


def test_publicado_quando_a_data_agendada_passou(tmp_path):
    item = {'tipo': 'video', 'codigo': 'X-1', 'situacao': 'agendado', 'quando': AGORA}
    assert canais.etapa_do_video({'codigo': 'X-1', 'etapa': 'Thumbnail', 'concluido': True}, [item], AGORA) == 'Publicado'


def test_calendario_converte_para_brasilia_com_horario_de_verao_americano(tmp_path):
    txt = canais.cmd_calendario(Namespace(dias=30), _repo(tmp_path), AGORA)
    assert 'qui 15/10 15:00 BRT (14:00 ET)' in txt                  # EDT: 1 h de diferença
    assert 'qui 05/11 16:00 BRT (14:00 ET)' in txt                  # EST, depois de 1º/11: 2 h


def test_env_da_raiz(tmp_path, monkeypatch):
    monkeypatch.delenv('ELEVENLABS_API_KEY', raising=False)
    (tmp_path / '.env').write_text('DRIVE_ROOT="/x"\nELEVENLABS_API_KEY=abc\n')
    assert canais.env_raiz('ELEVENLABS_API_KEY', tmp_path) == 'abc'
    (tmp_path / '.env').write_text('ELEVENLABS_API_KEY=\n')
    assert canais.env_raiz('ELEVENLABS_API_KEY', tmp_path) == ''

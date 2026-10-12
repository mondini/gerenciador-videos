"""Tempos: mapa de ritmo, arquivo tempos.txt, texto do roteiro e sugestão de deixas."""
import pytest

from marbleash import audio, tempos


def mapa_antigo(ins, tempo):
    """Fórmula da versão aprovada (render2.mapper), para comparar."""
    def m(t):
        extra = 0.0
        for mid, acc in ins:
            if mid < t:
                extra = acc
            else:
                break
        return (t + extra) / tempo
    return m


PAUSAS = [(2.99918, 3.87776), (5.04925, 5.73265), (7.43358, 8.13402)]


def test_mapa_igual_ao_aprovado():
    ins = audio.inseridos(PAUSAS)
    novo, velho = tempos.MapaRitmo(ins, 0.92), mapa_antigo(ins, 0.92)
    for t in (0, 1.5, 3.88, 5.73, 8.14, 20):
        assert novo(t) == velho(t)


def test_inverso_do_mapa():
    m = tempos.MapaRitmo(audio.inseridos(PAUSAS), 0.92)
    for t in (0.5, 4.2, 9.0):
        assert abs(m.inverso(m(t)) - t) < 1e-6


def test_tempo_padrao_igual_ao_ffmpeg_antigo():
    # ffmpeg 7 imprime 3.877755; o ffmpeg da versão aprovada imprimia 3.87776 (6 algarismos)
    assert audio.tempo_padrao('3.877755', 44100) == 3.87776
    assert audio.tempo_padrao('2.999184', 44100) == 2.99918


def test_arquivo_de_tempos_ida_e_volta(tmp_path):
    p = tmp_path / 'tempos.txt'
    tempos.escrever(p, [('roof', 3.88, 'A roof over your head.', 'pausa'), ('-', 5.0, 'sem nome', '')], ['cabeçalho'])
    assert tempos.ler(p) == [('roof', 3.88, 'A roof over your head.'), ('-', 5.0, 'sem nome')]


def test_tempos_com_nome_invalido(tmp_path):
    p = tmp_path / 'tempos.txt'
    p.write_text('nome-com-hifen 3.0 frase\n')
    with pytest.raises(ValueError):
        tempos.ler(p)


def test_deixas_no_tempo_do_video():
    m = tempos.MapaRitmo(audio.inseridos(PAUSAS), 0.92)
    c = tempos.Deixas([('roof', 3.88, 'x'), ('-', 4.0, 'y')], m, fim=10.0)
    assert c.roof == m(3.88)
    assert c.fim == 10.0
    with pytest.raises(AttributeError):
        c.nao_existe


def test_texto_do_bloco(tmp_path):
    md = tmp_path / 'roteiro.md'
    md.write_text('## Bloco 1 — Gancho\n\n```\n[softly] Hello there.\nSecond line...\n```\n\n## Bloco 2\n\n```\nOther.\n```\n')
    assert tempos.texto_do_bloco(md, 1) == '[softly] Hello there.\nSecond line...\n'
    assert tempos.texto_do_bloco(md, 2) == 'Other.\n'


def test_texto_da_pausa(tmp_path):
    md = tmp_path / 'roteiro.md'
    md.write_text('## The Pause (aprovado)\n\n```\nBreathe in...\n```\n')
    assert tempos.texto_do_bloco(md, 'pausa') == 'Breathe in...\n'


def test_palavras_e_forca_da_pontuacao():
    ws = tempos.palavras_do_texto('[softly] Every door... open.\nAnd yet, night')
    assert [w['palavra'] for w in ws] == ['Every', 'door', 'open', 'And', 'yet', 'night']
    assert [w['forca'] for w in ws] == [0, 2, 3, 0, 1, 3]


TEXTO = 'A roof over your head.\nLight at the touch of a finger.\nFood you never had to hunt.'
PAUSAS_TEXTO = [(1.6, 2.4), (4.3, 5.0)]


def test_sugestao_so_com_pausas():
    linhas = tempos.sugerir(TEXTO, PAUSAS_TEXTO, 7.0)
    assert [(n, s, o) for n, s, _, o in linhas] == [('a_roof', 0.0, 'início'), ('light_at', 2.4, 'pausa'), ('food_you', 5.0, 'pausa')]


def test_sugestao_com_transcritor_encaixa_na_pausa():
    # o transcritor marca a palavra seguinte dentro da pausa (ou um pouco antes): deve encaixar no fim da pausa
    palavras = [(w, t, t + 0.2) for w, t in zip('A roof over your head Light at the touch of a finger Food you never had to hunt'.split(),
                                                [0.0, 0.2, 0.4, 0.6, 0.9, 2.1, 2.6, 2.8, 3.0, 3.3, 3.5, 3.7, 4.2, 5.2, 5.4, 5.7, 5.9, 6.2])]
    linhas = tempos.sugerir(TEXTO, PAUSAS_TEXTO, 7.0, palavras)
    assert [s for _, s, _, _ in linhas] == [0.0, 2.4, 5.0]

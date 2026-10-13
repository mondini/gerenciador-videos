"""Vídeo 2 · The Pause. Script de cena (moldura "oliveira", à meia-luz).

Mesmo formato da Pausa do canal, outra imagem: no lugar do sol do logo, uma brasa que respira.
  1. "Seneca wrote that the greatest remedy for anger... is delay": a luz acende devagar sobre um carvão no chão
     do palco, com as rachaduras ainda apagadas; o homem do gancho, de pé à esquerda, olha para ele.
  2. "Unclench your jaw. Let your hands fall open": o homem solta os braços e abre as mãos.
  3. Duas respirações guiadas pela contagem falada: na inspiração a brasa acende nas rachaduras, a luz cresce
     e o homem ergue um pouco a cabeça; na expiração a brasa esfria e a luz baixa.
  4. A pergunta aparece na tela (Cormorant Garamond) quando é lida; "Just notice... how heavy it is": a câmera
     aproxima bem devagar da brasa.
"""
from marbleash.cena import *

PANO = 'pesado'
STILLS = (1.5, 8.0, 12.0, 16.0, 26.0, 33.0)

AMBAR = (1.0, 0.62, 0.22)
CHAO = BASE - 172 * 1.35
CX, CY = 1080, 790                                            # o carvão no chão do palco

# ================= ELENCO =================
LONGE = Camada(cenario.cidade, desfoque=9, opacidade=0.30, semente=11, pivo=(760, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.vinhedo, desfoque=6, opacidade=0.42, semente=12, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais_oliveira, desfoque=4.5, opacidade=0.86, semente=13, pivo=(200, 1080), balanco=(3.0, 0.45))
BASE_LENHA = Camada(cenario.base_lenha, desfoque=3.5, opacidade=0.88, semente=14, pivo=(400, 1080), balanco=(1.6, 0.2))
CARVAO = Camada(objetos.carvao, CX, CY, 1.3, desfoque=1.8, opacidade=0.92)
BRASA = Chama(objetos.brasa, CX, CY, 1.3, brilho=46, cor=(0.8, 0.45, 0.12), forca=1.6, gelatina=AMBAR, desfoque=1.8)
HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
CRED = Credito('Seneca, Of Anger II.29 · trans. Aubrey Stewart')


def _texto(texto, y):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', 46, 960, y, desfoque=1.4, opacidade=0.8,
                  semente=17, pivo=(960, 170), balanco=(1.2, 0.15))


PERGUNTA = [_texto('What are you still carrying…', 150), _texto('that happened days ago?', 212)]


# ================= LINHA DO TEMPO =================
def _respira(q, inspira, expira, fim):
    """0 = brasa fria (descanso); 1 = brasa acesa (pulmões cheios)."""
    return q.ss(inspira, expira - inspira) * (1 - q.ss(expira, fim - expira))


def quadro(q, c):
    u = q.u
    h = _respira(q, c.breathe_in, c.let_go, c.one_more - 0.2) + _respira(q, c.breathe_in2, c.and_out, c.now - 0.2)
    q.luz((0.3 + 0.7 * q.ss(0.0, 2.2)) * (0.5 + 0.3 * h) * tremor(u))

    q.sombra(LONGE, 0.8)
    q.sombra(MEIO, 0.8)
    q.sombra(CARVAO, q.ss(0.2, 1.4))
    q.chama(BRASA, q.ss(0.6, 1.6), 0.25 + 0.75 * h, cintila=(0.94, 0.06, 2.3))

    solta = q.ss(c.jaw, 1.8)                                   # "unclench your jaw... hands fall open"
    q.boneco(HOMEM, 560, CHAO, {'uarmF': 4 - 14 * (1 - solta), 'farmF': -6 - 30 * (1 - solta), 'uarmB': -4 + 14 * (1 - solta),
                                'farmB': -6 - 30 * (1 - solta), 'torso': 3 * solta - 2 * h, 'head': 14 * solta - 9 * h})

    for linha, deixa in zip(PERGUNTA, (c.what, c.what + 1.2)):
        q.sombra(linha, q.ss(deixa - 0.2, 0.9))
    q.credito(CRED, q.env(c.seneca, 0.8, c.jaw, 0.8))

    q.sombra(BASE_LENHA)
    q.sombra(LATERAIS)
    q.camera(CX - 60, CY - 60, 1 + 0.06 * q.ss(c.put, c.fim - c.put))

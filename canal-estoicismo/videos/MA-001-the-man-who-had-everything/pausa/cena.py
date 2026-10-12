"""Vídeo 1 · The Pause. Script de cena (padrão Teatro de Sombras Projetadas).

O logo Horizonte vira paisagem: o mar de papel com o reflexo vazado e o sol âmbar, cortado pelas duas tiras
do logo, de pé no horizonte. O homem do gancho olha o mar, de costas para nós (perfil, à esquerda).
  1. "Wherever you are... let your shoulders drop": a luz acende devagar; o homem baixa os ombros e a cabeça.
  2. Duas respirações guiadas pela contagem falada: na inspiração o sol sobe inteiro acima do horizonte, a luz
     cresce e o reflexo acende; na expiração ele volta a ser o meio-sol do logo e a luz baixa. O homem ergue
     um pouco a cabeça ao inspirar.
  3. A pergunta: aparece na tela (Cormorant Garamond) quando é lida e fica até o fim ("Stay with that");
     a câmera aproxima bem devagar.
"""
from marbleash.cena import *

STILLS = (1.5, 10.5, 18.0, 25.0, 37.0)

HZ, R = objetos.PAUSA_HZ, objetos.PAUSA_R
SOBE = 1.25 * R                                               # quanto o centro do sol sobe na inspiração
AMBAR = (0.91, 0.64, 0.24)                                    # amber-500
CHAO = BASE - 172 * 1.35                                      # pivô do torso do homem de pé (escala 1.35)

# ================= ELENCO =================
LATERAIS = Camada(cenario.laterais, desfoque=4.5, opacidade=0.86, semente=3, pivo=(200, 1080), balanco=(3.0, 0.45))
MAR = Camada(objetos.pausa_mar, desfoque=2.4, opacidade=0.72)
FAIXAS = Camada(objetos.pausa_faixas, desfoque=2.4, opacidade=0.86)
SOL = Chama(objetos.pausa_sol, brilho=34, cor=(0.6, 0.38, 0.12), forca=0.9, gelatina=AMBAR, desfoque=2.4)
REFLEXO = Chama(objetos.pausa_reflexo, brilho=12, cor=(0.6, 0.38, 0.12), forca=0.5, gelatina=AMBAR, desfoque=2.4)
HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)


def _texto(texto, y):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', 46, 960, y,
                  desfoque=1.4, opacidade=0.8, semente=17, pivo=(960, 170), balanco=(1.2, 0.15))


PERGUNTA = [_texto('What do you have today…', 150), _texto('that you once prayed for?', 212)]


# ================= LINHA DO TEMPO =================
def _respira(q, inspira, expira, fim):
    """0 = meio-sol do logo (descanso); 1 = sol inteiro acima do horizonte (pulmões cheios)."""
    return q.ss(inspira, expira - inspira) * (1 - q.ss(expira, fim - expira))


def quadro(q, c):
    u = q.u
    h = _respira(q, c.breathe_in, c.and_let, c.one_more - 0.2) + _respira(q, c.breathe_in2, c.and_out, c.now - 0.2)
    q.luz((0.3 + 0.7 * q.ss(0.0, 2.2)) * (0.6 + 0.32 * h) * tremor(u))

    # ---- o sol (atrás do mar) e as tiras do logo ----
    dy = -SOBE * h
    q.chama(SOL, q.ss(0.2, 1.6), 0.8 + 0.15 * h, cintila=(0.97, 0.03, 4), dy=dy, recorte=(0, 0, W, HZ))
    q.sombra(FAIXAS, dy=dy)

    # ---- o mar e o reflexo ----
    q.sombra(MAR)
    q.chama(REFLEXO, q.ss(0.6, 1.6), 0.2 + 0.6 * h, cintila=(0.9, 0.1, 3))

    # ---- o homem olha o mar ----
    solta = q.ss(c.let_your, 1.6)                              # "let your shoulders drop"
    q.boneco(HOMEM, 380, CHAO, {'uarmF': 4 - 10 * (1 - solta), 'farmF': -6 - 14 * (1 - solta), 'uarmB': -4 + 10 * (1 - solta),
                                'farmB': -6 - 14 * (1 - solta), 'torso': 2 * solta - 2 * h, 'head': 10 * solta - 9 * h})

    # ---- a pergunta ----
    for linha, deixa in zip(PERGUNTA, (c.what_do, c.that_you)):
        q.sombra(linha, q.ss(deixa - 0.2, 0.9))

    q.sombra(LATERAIS)
    q.camera(960, 520, 1 + 0.05 * q.ss(c.now, c.fim - c.now))

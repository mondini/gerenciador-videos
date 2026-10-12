"""Vídeo 1 · Bloco 6 — Fechamento. Script de cena (padrão Teatro de Sombras Projetadas).

Volta ao gancho e fecha o círculo, em calma (o público ouve para dormir):
  1. A casa à noite: o homem do gancho diante da casa, da lamparina e da mesa, com a lua crescente; o
     sussurro "not yet... not enough." volta no mesmo lugar do bloco 1; "never go completely quiet": ele
     enfraquece, mas não some.
  2. A tenda: "It didn't for Marcus either": o imperador escreve à noite; Roma aparece ao longe em "the
     whole empire" e se apaga; "what was already in his hands": foco nas mãos dele.
  3. De volta à casa: o sussurro reaparece fraco; em "answer it" o homem ergue a cabeça e o sussurro se desfaz
     (sobe e some).
  4. "Look around you": a casa, a lamparina e a mesa ganham âmbar uma a uma (roof, light, something to eat);
     "a few people who know your name": um adulto e uma criança chegam pela direita. "Once... enough":
     a luz esquenta; leve aproximação.
  5. A tenda de novo: o imperador pousa a pena ("sets down his pen") e olha a lamparina; tudo escurece
     devagar e só a chama fica ("the lamp... is still burning"). "Old wisdom... for quiet hours": escurece
     até o encerramento padrão.
"""
from marbleash.cena import *

SAIDA = 1.6                   # o último segundo e meio escurece (entra o encerramento padrão)
FADE = (1.5, 1.4)
STILLS = (4.0, 8.0, 13.5, 19.5, 23.0, 26.5, 30.5, 33.5, 37.0, 43.0, 47.0, 51.0)

AMBAR = (0.91, 0.64, 0.24)                                    # amber-500
CHAO = BASE - 172 * 1.35                                      # pivô do torso do homem de pé (escala 1.35)

# ================= ELENCO =================
LONGE = Camada(cenario.longe, desfoque=9, opacidade=0.30, semente=1, pivo=(1200, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.meio, desfoque=6, opacidade=0.42, semente=2, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais, desfoque=4.5, opacidade=0.86, semente=3, pivo=(200, 1080), balanco=(3.0, 0.45))
PENHASCO = Camada(objetos.penhasco, desfoque=3.0, opacidade=0.86, semente=10, pivo=(900, BASE), balanco=(2.0, 0.2))

TEMPLO = Camada(objetos.templo, desfoque=2.4, opacidade=0.82, semente=4, pivo=(800, BASE), balanco=(2.2, 0.3))
MESA = Camada(objetos.mesa, desfoque=2.4, opacidade=0.82, semente=5, pivo=(1450, BASE), balanco=(2.2, 0.3))
LAMPARINA = Camada(objetos.lamparina, desfoque=1.8, opacidade=0.84, semente=6, pivo=(1190, 0), balanco=(3.0, 0.6))
CHAMA = Chama(objetos.chama, 1, brilho=22, cor=(0.6, 0.38, 0.12), forca=1.3)
OURO = [Chama(cam.arte, brilho=10, cor=(0.6, 0.38, 0.12), forca=0.3, gelatina=AMBAR, desfoque=cam.desfoque) for cam in (TEMPLO, LAMPARINA, MESA)]
SUSSURRO = Camada(objetos.letreiro, 'not yet...   not enough.', 'Cormorant-MediumItalic.ttf', desfoque=1.5, opacidade=0.75, semente=7, pivo=(960, 200),
                  balanco=(1.5, 0.2))                         # o mesmo sussurro do bloco 1

HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
ADULTO = Boneco(bonecos.homem, escala=1.25, desfoque=1.1, opacidade=0.9)
CRIANCA = Boneco(bonecos.homem, escala=0.82, desfoque=1.1, opacidade=0.9)
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)
CHAMA_NOITE = Chama(objetos.chama_noite, 1, brilho=26, cor=(0.7, 0.42, 0.12), forca=1.5)


# ================= LINHA DO TEMPO =================
def _anda(q, i=0):
    """Pernas de quem caminha."""
    return 26 * math.sin(q.u * 7 + i)


def _escreve(q, pousa):
    """Pose do imperador sentado escrevendo; `pousa` 0..1 abaixa a pena e ergue a cabeça para a lamparina."""
    u = q.u
    osc = math.sin(u * 9) * (1 - pousa)
    return {'uarmF': -62 + 6 * osc + 40 * pousa, 'farmF': -58 + 10 * math.sin(u * 13) * (1 - pousa) + 36 * pousa,
            'legF': -70, 'legB': -60, 'uarmB': -20, 'farmB': -30, 'head': 10 - 16 * pousa}


def quadro(q, c):
    u = q.u
    casa1 = q.env(0.0, 0.8, c.it_didnt - 0.3, 1.0)
    tenda1 = q.env(c.it_didnt - 0.3, 1.0, c.so_tonight - 0.3, 1.0)
    casa2 = q.env(c.so_tonight - 0.3, 1.0, c.far_away - 0.3, 1.2)
    tenda2 = q.ss(c.far_away - 0.3, 1.2)
    casa = max(casa1, casa2)
    tenda = max(tenda1, tenda2)
    quente = q.ss(c.once - 0.2, 2.0) * casa2                         # "you would have called this enough"
    apaga = q.ss(c.and_the - 0.3, c.old_wisdom - c.and_the + 1.5)     # tudo escurece, só a chama fica
    q.luz((0.5 + 0.14 * quente) * (1 - 0.6 * apaga) * tremor(u))
    q.lua(casa, cx=960, cy=130, raio=58, crescente=0.45)
    q.lua(tenda * (1 - apaga))

    # ---- fundo ----
    q.sombra(LONGE, max(casa, tenda1 * q.env(c.he_had - 0.2, 1.0, c.and_still, 1.4)))   # Roma ao longe em "the whole empire"
    q.sombra(MEIO, casa)
    q.sombra(PENHASCO, tenda)

    # ---- a casa ----
    if casa > 0.002:
        for camada in (TEMPLO, LAMPARINA, MESA):
            q.sombra(camada, casa)
        q.chama(CHAMA, casa, cintila=(0.9, 0.1, 11), camada=LAMPARINA)
        ouro = [q.ss(d - 0.2, 1.4) for d in (c.a_roof, c.a_little, c.something_to)]
        for gel, camada, o in zip(OURO, (TEMPLO, LAMPARINA, MESA), ouro):
            q.chama(gel, casa2, o * (0.3 + 0.2 * quente), camada=camada)
        # o homem: curvado no sussurro; ergue a cabeça para responder; olha em volta
        curva = q.env(c.not_yet - 0.2, 1.2, c.answer - 0.2, 1.2)
        olha = q.env(c.look_around - 0.2, 1.4, c.a_few, 1.2)
        q.boneco(HOMEM, 430, CHAO, {'uarmF': 4 + 10 * curva, 'farmF': -6 - 20 * curva, 'uarmB': -4, 'farmB': -8,
                                    'head': 24 * curva - 4 - 14 * olha * (0.5 + 0.5 * math.sin(u * 0.8)), 'torso': 6 * curva + 3}, casa)
        # o sussurro: volta, enfraquece ("never go completely quiet"), reaparece fraco e se desfaz em "answer it"
        s1 = q.env(c.not_yet - 0.2, 1.0, c.it_didnt - 0.3, 1.0) * (1 - 0.55 * q.ss(c.quiet - 0.3, 1.2))
        desfaz = q.ss(c.answer - 0.1, 1.6)
        s2 = q.ss(c.you_dont - 0.2, 1.2) * 0.45 * (1 - desfaz)
        q.sombra(SUSSURRO, max(s1, s2) * casa, dx=-360, dy=90 - 70 * desfaz)
        # "a few people who know your name": um adulto e uma criança chegam pela direita
        chega = q.ss(c.a_few - 0.6, 2.4)
        if chega > 0:
            passo = _anda(q) * (1 - q.ss(c.a_few + 1.4, 0.5))
            q.boneco(ADULTO, lerp(2080, 1110, chega), BASE - 172 * 1.25, {'legF': passo, 'legB': -passo, 'uarmF': 4, 'farmF': -6, 'head': 4},
                     casa2, espelho=True)
            q.boneco(CRIANCA, lerp(2200, 1220, chega), BASE - 172 * 0.82, {'legF': -passo, 'legB': passo, 'uarmF': -30, 'farmF': -10, 'head': -6},
                     casa2, espelho=True)

    # ---- a tenda ----
    if tenda > 0.002:
        pousa = q.ss(c.pen - 0.5, 1.4) * tenda2
        q.boneco(IMPERADOR, 990, BASE - 110, _escreve(q, pousa), tenda, 1 - 0.8 * apaga)
        q.chama(CHAMA_NOITE, tenda, cintila=(0.85, 0.15, 13))

    q.sombra(LATERAIS, 1 - 0.5 * apaga)

    # ---- foco e câmera ----
    q.foco(0.45 * q.env(c.not_yet - 0.3, 1.4, c.maybe_it, 1.2), 520, 560, 320)                    # o homem e o sussurro
    q.foco(0.45 * tenda1 * q.ss(c.he_had2, 1.4), 1040, 650, 330)                                   # as mãos do imperador
    q.foco(0.35 * q.env(c.once - 0.2, 1.6, c.far_away - 0.3, 1.0), 900, 620, 520)                  # a casa inteira, em calma
    q.foco(0.6 * tenda2 * q.ss(c.and_the - 0.3, 1.6), lerp(1040, 1238, apaga), lerp(640, 800, apaga), 300 - 170 * apaga)   # fecha na chama
    z1 = q.env(c.not_yet - 0.6, 2.0, c.maybe_it, 1.4) * 0.16
    z2 = tenda1 * q.ss(c.he_had2 - 0.4, 2.0) * 0.2
    z3 = q.env(c.once - 0.4, 3.0, c.far_away - 0.3, 1.0) * 0.06
    z4 = tenda2 * q.ss(c.an_old - 0.4, c.fim - c.an_old) * 0.3
    if z1 > 0:
        q.camera(520, 560, 1 + z1)
    elif z2 > 0:
        q.camera(1040, 650, 1 + z2)
    elif z3 > 0:
        q.camera(900, 560, 1 + z3)
    elif z4 > 0:
        q.camera(1140, 680, 1 + z4)

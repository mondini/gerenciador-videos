"""Vídeo 2 · Bloco 6 — Fechamento. Script de cena (moldura "oliveira"). Termina em calma (o público ouve para dormir).

  1. "tonight, if that argument starts again in your head": noite, lua minguante; a sombra do outro volta, e o
     homem começa a erguer o braço, como no gancho; "the one you've already won a hundred times": a sombra pisca.
  2. ALÍVIO (pedido do criador) em "you don't have to win it one more time": o braço cai, os ombros descem,
     as mãos se abrem, a cabeça sobe um pouco; a sombra do outro se desfaz para cima, cada vez mais borrada;
     a luz em volta dele amolece e esquenta (foco largo e suave).
  3. "When the next replay begins... let it pass": um fio de fumaça sobe ao lado da cabeça e se dissipa;
     "leave the fire... unfed": a fogueira pequena ao lado, com a tora pousada no chão, sem ser jogada.
  4. "Almost two thousand years ago, an emperor let a box of letters burn": Marco ao lado da capsa no fogo;
     "He never had to carry them": o fogo baixa.
  5. "one small ember is still glowing... Only... with warmth": sobra uma brasa nas cinzas; a câmera se
     aproxima devagar; "Old wisdom... for quiet hours": escurece até o encerramento padrão.
"""
from marbleash.cena import *

PANO = 'pesado'
SAIDA = 1.6
FADE = (1.5, 1.4)
STILLS = (3.0, 8.0, 11.0, 14.0, 22.0, 30.0, 38.0, 44.0, 50.0, 55.0)

CHAO = BASE - 172 * 1.35
CHAO_IMP = BASE - 172 * 1.3
A = (500, 400)
AMBAR = (1.0, 0.62, 0.22)

# ================= ELENCO =================
LONGE = Camada(cenario.cidade, desfoque=9, opacidade=0.30, semente=11, pivo=(760, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.vinhedo, desfoque=6, opacidade=0.42, semente=12, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais_oliveira, desfoque=4.5, opacidade=0.86, semente=13, pivo=(200, 1080), balanco=(3.0, 0.45))
BASE_LENHA = Camada(cenario.base_lenha, desfoque=3.5, opacidade=0.88, semente=14, pivo=(400, 1080), balanco=(1.6, 0.2))

HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
OUTRO = Boneco(bonecos.homem, escala=1.35, desfoque=3.4, opacidade=0.5)
OUTRO_SOME = [Boneco(bonecos.homem, escala=1.35, desfoque=3.4 + 3 * k, opacidade=0.5) for k in range(6)]   # cada vez mais borrado
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)
FUMACA = {(i, k): Camada(objetos.fumaca, i, k / 20, desfoque=2.2, opacidade=0.5) for i in range(2) for k in range(2, 21, 2)}
FOGUEIRA = Camada(objetos.fogueira_toras, 2, 1240, desfoque=2.0, opacidade=0.86, semente=90, pivo=(1240, BASE), balanco=(1.2, 0.1))
FOGO = [[Chama(objetos.labareda, k, tam, 1240, brilho=26 + 10 * tam, cor=(0.7, 0.42, 0.12), forca=1.3) for k in range(4)]
        for tam in (0.2, 0.4, 0.65)]
TORA = Camada(objetos.tora, desfoque=1.4, opacidade=0.88, posicao=A)
CAPSA = Camada(objetos.capsa, 1240, 0.0, 0, desfoque=1.8, opacidade=0.88, semente=91, pivo=(1240, BASE), balanco=(1.2, 0.15))
CINZA = [Camada(objetos.cinza, k, desfoque=1.2, opacidade=0.55, posicao=A) for k in range(6)]
CARVAO = Camada(objetos.carvao, 1240, 820, 0.55, desfoque=1.6, opacidade=0.9)
BRASA = Chama(objetos.brasa, 1240, 820, 0.55, brilho=40, cor=(0.8, 0.45, 0.12), forca=1.5, gelatina=AMBAR, desfoque=1.6)


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    homem = 1 - q.ss(c.emperor - 0.4, 1.2)
    marco = q.env(c.emperor - 0.4, 1.2, c.ember - 0.4, 1.4)
    brasa = q.ss(c.ember - 0.6, 1.6)

    alivio = q.ss(c.win, 2.2)                                          # o momento de alívio
    q.luz((0.55 + 0.12 * alivio) * (1 - 0.3 * brasa) * tremor(u))
    q.lua(1.0, cx=1500, cy=160, raio=50, crescente=-0.5)

    q.sombra(LONGE, 0.85)
    q.sombra(MEIO, 0.85)

    # ---- 1 a 3. a discussão volta; o alívio; o replay que passa; o fogo sem lenha ----
    if homem > 0.002:
        tensao = q.ss(c.argument, 1.2) * (1 - alivio)
        g = tensao * (0.5 + 0.5 * math.sin(u * 5.5))
        q.boneco(HOMEM, 640, CHAO, {'uarmF': -40 * tensao - 50 * g + 6 * alivio, 'farmF': -40 * tensao + 20 * g - 6 * (1 - tensao),
                                    'uarmB': 8 * tensao - 4 * alivio, 'farmB': -12 * tensao - 6,
                                    'head': -4 * tensao - 8 * alivio, 'torso': 4 * tensao + 1 * alivio}, homem)
        piscar = 1.0
        if c.hundred <= u < c.win:
            piscar = 0.3 + 0.7 * (0.5 + 0.5 * math.cos((u - c.hundred) * 9))
        some = q.ss(c.win + 0.3, 2.4)                                   # a sombra do outro se desfaz para cima
        aparece = q.ss(c.argument - 0.2, 1.2)
        if some < 0.999:
            q.boneco(OUTRO_SOME[min(5, int(some * 6))], 940, CHAO - 120 * some, {'uarmF': -20, 'farmF': -30, 'head': 2},
                     homem, aparece * piscar * (1 - some), espelho=True)
        q.foco(0.55 * q.env(c.win + 0.4, 2.0, c.emperor - 0.6, 1.2), 640, 580, 420)
        fumaca = q.lin(c.replay, c.leave + 1.5 - c.replay)              # o próximo replay sobe como fumaça e passa
        if 0 < fumaca < 1:
            k = max(2, min(20, int(round(20 * fumaca / 2)) * 2))
            q.sombra(FUMACA[(0, k)], homem, 1 - q.ss(c.letpass + 0.8, 1.6), dx=-560, dy=-260)
        fogo = q.ss(c.leave - 0.6, 1.2)
        q.sombra(FOGUEIRA, homem, fogo)
        q.chama(FOGO[1][int(u * 8) % 4], homem, fogo, cintila=(0.85, 0.15, 9))
        q.sombra(TORA, homem, fogo, dx=900 - A[0], dy=objetos.CHAO2 - 70 - A[1])

    # ---- 4. o imperador e as cartas no fogo ----
    if marco > 0.002:
        q.boneco(IMPERADOR, 760, CHAO_IMP, {'uarmF': 6, 'farmF': -14, 'head': 12, 'torso': 2}, marco)
        q.sombra(CAPSA, marco, 1 - q.ss(c.carry, 2.0), dy=60 * q.ss(c.carry, 2.0))
        baixa = q.ss(c.carry, 2.0)
        q.chama(FOGO[2 - int(round(2 * baixa))][int(u * 8) % 4], marco, cintila=(0.85, 0.15, 9))
        pts, pesos = [], []
        for i in range(12):
            p = ((u - c.emperor) * 0.2 + i * 0.083) % 1.0
            pts.append((1240 - A[0] + 70 * math.sin(i * 1.3 + u * 0.6), objetos.CHAO2 - 120 - 460 * p - A[1]))
            pesos.append(math.sin(math.pi * p))
        for k in range(6):
            q.multidao(CINZA[k], pts[k::6], marco, pesos=pesos[k::6])

    # ---- 5. a última brasa ----
    if brasa > 0.002:
        q.sombra(CARVAO, brasa)
        quente = q.ss(c.ember + 0.6, 1.4) * (1 - 0.2 * q.ss(c.slogan, 2.0))
        q.chama(BRASA, brasa, quente, cintila=(0.92, 0.08, 1.8))
        q.foco(0.6 * brasa, 1240, 800, 260)
        q.camera(1240, 780, 1 + 0.18 * q.ss(c.ember, c.fim - c.ember))

    q.sombra(BASE_LENHA)
    q.sombra(LATERAIS)

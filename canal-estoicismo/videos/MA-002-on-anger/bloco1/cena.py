"""Vídeo 2 · Bloco 1 — Gancho. Script de cena (padrão Teatro de Sombras Projetadas, moldura "oliveira").

A discussão que não acaba:
  1. "You've already won this argument": o homem discute com a sombra do outro (um vulto espelhado e borrado);
     "a hundred times": a sombra some e volta, várias vezes, e o homem repete o gesto.
  2. Onde ela volta: a bica de parede ("In the shower"), o marco da estrada ("On the drive home") e a cama às
     três da manhã, de olho aberto, com a lua minguante ("staring at the ceiling"). A sombra do outro sempre ao lado.
  3. "To your boss. To your mother. To that person...": o chefe, a mãe e alguém de mão estendida surgem à direita,
     um a cada nome; "a little more": a mão avança. "you lose a little more of your peace": somem, a luz cai.
  4. "Your anger is not the problem": uma labareda sobe e baixa ("It comes... and it goes"); "the grudge":
     no lugar dela fica uma pedra, que cai e fica ("The part that stays").
  5. "The Stoics... Marcus Aurelius": o imperador entra; "the worst betrayal": a sombra de um general surge
     atrás dele; "the traitor's letters": a capsa de cartas aparece entre os dois; "We'll get there": escurece.
"""
from marbleash.cena import *

PANO = 'pesado'
ENTRADA = 0.4
SAIDA = 1.0
STILLS = (2.0, 5.0, 8.0, 11.0, 16.0, 20.0, 24.0, 30.0, 36.0, 42.0, 47.0, 51.0)

CHAO = BASE - 172 * 1.35                                      # pivô do torso do homem de pé (escala 1.35)
CHAO_IMP = BASE - 172 * 1.3

# ================= ELENCO =================
LONGE = Camada(cenario.cidade, desfoque=9, opacidade=0.30, semente=11, pivo=(760, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.vinhedo, desfoque=6, opacidade=0.42, semente=12, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais_oliveira, desfoque=4.5, opacidade=0.86, semente=13, pivo=(200, 1080), balanco=(3.0, 0.45))
BASE_LENHA = Camada(cenario.base_lenha, desfoque=3.5, opacidade=0.88, semente=14, pivo=(400, 1080), balanco=(1.6, 0.2))

BICA = Camada(objetos.bica, desfoque=2.4, opacidade=0.84, semente=20, pivo=(1460, BASE), balanco=(2.0, 0.25))
AGUA = [Camada(objetos.agua, k, desfoque=1.6, opacidade=0.7) for k in range(4)]
ESTRADA = Camada(objetos.estrada, desfoque=2.6, opacidade=0.84, semente=21, pivo=(1300, BASE), balanco=(1.6, 0.2))
CAMA = Camada(objetos.cama, desfoque=2.2, opacidade=0.84, semente=22, pivo=(1000, BASE), balanco=(1.6, 0.2))
DEITADO = Camada(objetos.homem_deitado, desfoque=1.4, opacidade=0.9, semente=22, pivo=(1000, BASE), balanco=(1.6, 0.2))
CHEFE = Camada(objetos.figura_chefe, 1060, desfoque=1.4, opacidade=0.86, semente=23, pivo=(1060, BASE), balanco=(2.0, 0.3))
MAE = Camada(objetos.figura_mulher, 1290, 1.9, 0.6, desfoque=1.4, opacidade=0.86, semente=24, pivo=(1290, BASE), balanco=(2.0, 0.3))
MAO = Camada(objetos.mao_estendida, 1640, 720, -140.0, desfoque=1.8, opacidade=0.86, semente=25, pivo=(1700, 900), balanco=(2.0, 0.4))
PEDRA = Camada(objetos.pedra_grande, 1.4, desfoque=1.4, opacidade=0.88, posicao=(820, 400))
CAPSA = Camada(objetos.capsa, 980, 0.0, desfoque=2.0, opacidade=0.84, semente=26, pivo=(1180, BASE), balanco=(1.6, 0.2))
GENERAL = Camada(objetos.general, 1380, 0.0, desfoque=2.6, opacidade=0.7, semente=27, pivo=(1380, BASE), balanco=(1.6, 0.2))

HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
OUTRO = Boneco(bonecos.homem, escala=1.35, desfoque=3.4, opacidade=0.5)      # a sombra do outro: borrada, meio apagada
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)
LABAREDA = [Chama(objetos.labareda, k, 1.0, 760, brilho=30, cor=(0.7, 0.42, 0.12), forca=1.4) for k in range(4)]


def _gesto(u, forca):
    """Braço da frente batendo no ar, como quem ganha uma discussão."""
    return forca * (0.5 + 0.5 * math.sin(u * 5.5))


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    # ---- trechos ----
    discute = 1 - q.ss(c.shower - 0.3, 0.8)
    banho = q.env(c.shower - 0.3, 0.8, c.drive - 0.3, 0.8)
    estrada = q.env(c.drive - 0.3, 0.8, c.three - 0.3, 0.8)
    cama = q.env(c.three - 0.3, 1.0, c.know - 0.3, 0.9)
    pessoas = q.env(c.know - 0.2, 0.8, c.strange - 0.4, 1.0)
    fogo = q.env(c.strange, 1.0, c.stoics - 0.3, 1.0)
    marco = q.ss(c.stoics - 0.2, 1.2)

    noite = cama
    q.luz((1 - 0.5 * noite) * (1 - 0.25 * q.env(c.lose, 1.5, c.strange, 1.2)) * (1 - 0.2 * marco) * tremor(u))
    q.lua(q.ss(c.three, 1.4) * cama, cx=1180, cy=150, raio=56, crescente=-0.45)        # minguante

    q.sombra(LONGE)
    q.sombra(MEIO)

    # ---- 1. a discussão com a sombra do outro ----
    vivo = discute + banho + estrada
    if vivo > 0.002:
        piscar = 1.0
        if c.hundred <= u < c.shower:                                       # "a hundred times": some e volta
            piscar = 0.25 + 0.75 * (0.5 + 0.5 * math.cos((u - c.hundred) * 9))
        g = _gesto(u, 1.0 if u < c.shower else 0.6)
        xh = lerp(700, 640, banho) if estrada < 0.5 else 760
        anda = estrada * math.sin(u * 4.2)
        q.boneco(HOMEM, xh, CHAO + 2 * abs(anda), {'uarmF': -40 - 50 * g, 'farmF': -40 + 20 * g, 'uarmB': 8, 'farmB': -12,
                                                   'head': -4, 'torso': 4, 'legF': 20 * anda, 'legB': -20 * anda}, vivo)
        q.boneco(OUTRO, xh + 300, CHAO, {'uarmF': -20, 'farmF': -30, 'head': 2}, vivo * piscar * (1 - 0.4 * estrada), espelho=True)
    if banho > 0.002:
        q.sombra(BICA, banho, dx=500 * (1 - q.ss(c.shower - 0.3, 0.9)))
        q.sombra(AGUA[int(u * 8) % 4], banho * q.ss(c.shower + 0.4, 0.5))
    if estrada > 0.002:
        q.sombra(ESTRADA, estrada, dx=-260 * q.lin(c.drive - 0.3, c.three - c.drive))   # o marco passa: ele caminha

    # ---- 2. três da manhã ----
    if cama > 0.002:
        q.sombra(CAMA, cama)
        q.sombra(DEITADO, cama)
        q.boneco(OUTRO, 1240, CHAO - 40, {'uarmF': -30, 'farmF': -20}, cama * 0.6 * (0.7 + 0.3 * math.sin(u * 1.3)), espelho=True)

    # ---- 3. o chefe, a mãe, a mão estendida ----
    if pessoas > 0.002:
        q.boneco(HOMEM, 520, CHAO, {'uarmF': 6, 'farmF': -10, 'uarmB': -4, 'farmB': -8,
                                    'head': 10 * q.ss(c.every, 1.5), 'torso': 2 + 6 * q.ss(c.lose, 1.5)}, pessoas)
        apaga = 1 - q.ss(c.lose, 1.4)
        q.sombra(CHEFE, pessoas, q.ss(c.boss - 0.2, 0.7), apaga)
        q.sombra(MAE, pessoas, q.ss(c.mother - 0.2, 0.7), apaga)

    # ---- 4. a raiva vem e vai; o rancor fica ----
    if fogo > 0.002:
        q.boneco(HOMEM, 520, CHAO, {'uarmF': 4, 'farmF': -10, 'head': 6, 'torso': 3}, fogo)
        chama = q.env(c.anger, 0.6, c.goes, 1.0)
        if chama > 0.01:
            q.chama(LABAREDA[int(u * 8) % 4], fogo, chama, cintila=(0.85, 0.15, 9))
        cai = q.ss(c.grudge + 0.2, 0.5)                                       # a pedra cai onde estava o fogo e fica
        if cai > 0:
            q.sombra(PEDRA, fogo, dy=lerp(-140, CHAO2_PEDRA - 400, cai))

    # ---- 5. Marco Aurélio, a traição e as cartas ----
    if marco > 0.002:
        entra = q.ss(c.marcus - 0.4, 1.8)
        q.boneco(IMPERADOR, lerp(-160, 560, entra), CHAO_IMP, {'uarmF': 4, 'farmF': -14, 'uarmB': -6, 'farmB': -10,
                                                              'head': 8 * q.ss(c.betrayal, 1.0), 'torso': 1.5 * math.sin(u * 0.8)}, marco)
        q.sombra(GENERAL, marco, q.ss(c.betrayal, 1.4))
        q.sombra(CAPSA, marco, q.ss(c.letters, 1.0), dy=-60 * (1 - q.ss(c.letters, 1.0)))
        q.foco(q.ss(c.letters + 0.4, 1.2), 980, 640, 260)

    q.sombra(BASE_LENHA)
    q.sombra(LATERAIS)
    if pessoas > 0.002:                                                     # a mão vem de fora, na frente da ruína
        avanca = q.ss(c.person + 0.6, 1.2)                                  # "a little more": a mão avança
        q.sombra(MAO, pessoas, q.ss(c.person - 0.2, 0.7), 1 - q.ss(c.lose, 1.4),
                 dx=160 * (1 - q.ss(c.person - 0.2, 0.8)) - 110 * avanca, dy=-30 * avanca)
    if cama > 0:
        q.camera(1000, 700, 1 + 0.12 * cama * q.ss(c.three, c.know - c.three))


CHAO2_PEDRA = objetos.CHAO2 - 130                                              # centro da pedra pousada acima do pano

"""Vídeo 1 · Bloco 5 — Provérbios 16:18. Script de cena (padrão Teatro de Sombras Projetadas).

Grupos de cenas guiados pela narração:
  1. Outra terra: o pergaminho romano à esquerda; o fundo romano dá lugar a outra terra (colinas secas,
     cidade murada, tamareiras); "a much older book": o rolo hebraico se abre do lado oposto.
  2. Salomão: o rei entra e para diante do rolo; SOLOMON no alto; "in one single line": uma só linha do rolo
     acende em âmbar e o rei ergue a mão para ela.
  3. Provérbios 16:18: a torre sobe do chão; um homem pequeno sobe a escada por fora, andar por andar, e
     despenca no "fall". "The higher you climb": a câmera olha o topo; "the harder the ground": o homem caído.
  4. Provérbios 16:19: à esquerda, gente simples em volta de uma fogueira; à direita, dois orgulhosos dividem
     o tesouro de um baú (as moedas voam para eles). "Lose it": os dois se apagam, o ouro fica; o foco vai
     para a fogueira.
  5. Dois homens: o rei à esquerda, o imperador à direita, olhando um para o outro; cada um ganha o foco no
     seu nome; "the same quiet truth": uma linha âmbar sai de cada um e se encontra no centro.
  6. "Power... whispers": o homem do gancho no centro; o redemoinho sobre a cabeça; "more than he is":
     a sombra dele cresce atrás, grande e borrada (como quem chega perto da lâmpada).
"""
from marbleash.cena import *

STILLS = (3.5, 7.5, 13.0, 16.5, 21.0, 23.9, 24.4, 27.0, 30.0, 36.0, 43.0, 46.0, 50.0, 60.0, 64.0, 68.6)   # um still por cena

TINTA = (60, 34, 16, 255)
AMBAR = (0.91, 0.64, 0.24)                                    # amber-500


def _chao(escala, pe=BASE):
    """Pivô do torso de um boneco de pé com os pés em `pe`."""
    return pe - 172 * escala


def _anda(q, i=0):
    """Pernas de quem caminha."""
    return 26 * math.sin(q.u * 7 + i)


def _citacao(texto, y, cx=1000, tamanho=42):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', tamanho, cx, y,
                  desfoque=1.4, opacidade=0.8, semente=17, pivo=(cx, 170), balanco=(1.2, 0.15))


# ================= ELENCO =================
LONGE = Camada(cenario.longe, desfoque=9, opacidade=0.30, semente=1, pivo=(1200, 700), balanco=(1.2, 0.08))
ORIENTE = Camada(objetos.oriente, desfoque=9, opacidade=0.30, semente=1, pivo=(1200, 700), balanco=(1.2, 0.08))
LATERAIS = Camada(cenario.laterais, desfoque=4.5, opacidade=0.86, semente=3, pivo=(200, 1080), balanco=(3.0, 0.45))
HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
REI = Boneco(bonecos.rei, escala=1.3, desfoque=1.1, opacidade=0.9)
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)

# 1–2. os dois livros e Salomão
PERGAMINHO = Camada(objetos.pergaminho, 0.55, 540, 250, 470, desfoque=1.6, opacidade=0.85, semente=12, pivo=(540, 360), balanco=(1.5, 0.15))
ROLO = [Camada(objetos.rolo, k / 12, desfoque=1.6, opacidade=0.86, semente=13, pivo=(1340, 370), balanco=(1.5, 0.15)) for k in range(13)]
LINHA = Chama(objetos.rolo_linha, brilho=14, cor=(0.6, 0.38, 0.12), forca=0.7, gelatina=AMBAR, desfoque=1.6)
SOLOMON = Camada(objetos.letreiro, 'SOLOMON', 'Cinzel-SemiBold.ttf', 60, 800, 225, TINTA, 0.08,
                 desfoque=1.2, opacidade=0.85, semente=14, pivo=(800, 260), balanco=(1.2, 0.1))

# 3. Provérbios 16:18: a torre
TX = 1150
TORRE = Camada(objetos.torre, TX, desfoque=2.2, opacidade=0.86, semente=16, pivo=(TX, BASE), balanco=(1.4, 0.12))
ALPINISTA = Boneco(bonecos.homem, escala=0.6, desfoque=1.3, opacidade=0.9)
Q1618 = [_citacao('Pride goes before destruction,', 330, 720), _citacao('and an arrogant spirit before a fall.', 388, 720)]   # abaixo da copa do pinheiro
CRED_1618 = Credito('Proverbs 16:18 · World English Bible')


def _caminho():
    """A escada por fora da torre: do chão, à esquerda, até o topo, andar por andar (lados alternados)."""
    andares = objetos.TORRE
    pts = [(TX - andares[0][0] / 2 - 60, BASE)]
    for i in range(5):
        lado = -1 if i % 2 == 0 else 1
        pts.append((TX + lado * (andares[i + 1][0] / 2 + 14), andares[i + 1][1]))
    pts.append((TX, andares[6][1]))
    return pts


CAMINHO = _caminho()

# 4. Provérbios 16:19: a fogueira dos simples e o baú dos orgulhosos
CRIANCA = Boneco(bonecos.homem, escala=0.82, desfoque=1.1, opacidade=0.9)
ADULTO = Boneco(bonecos.homem, escala=1.2, desfoque=1.1, opacidade=0.9)
FOGO = [Chama(objetos.fogueira, k, brilho=30, cor=(0.7, 0.42, 0.12), forca=1.4) for k in range(4)]
FOGO_DX = -330                                                # a fogueira fica em x = 630
BX = 1450
SOBE_BAU = -100                                               # o baú pousa sobre o monte de capim da base
BAU = Camada(objetos.bau, 1.0, BX, desfoque=2.0, opacidade=0.85, semente=31, pivo=(BX, BASE), balanco=(2.0, 0.2))
OURO = [Camada(objetos.tesouro, i, BX, BASE - 150, desfoque=1.8, opacidade=0.85, semente=40 + i, pivo=(BX, BASE - 150), balanco=(2.5, 0.4))
        for i in (0, 3, 4)]
MOEDA = Camada(objetos.moeda, desfoque=1.4, opacidade=0.82, posicao=(100, 100), dobra=False)     # centro em (100, 100)
Q1619 = [_citacao('It is better to be of a lowly spirit with the poor,', 92, 1060, 38),
         _citacao('than to divide the plunder with the proud.', 144, 1060, 38)]
CRED_1619 = Credito('Proverbs 16:19 · World English Bible')

# 5. os dois homens e a linha âmbar
FIO = Chama(objetos.fio, 380, 1540, 420, 80, brilho=16, cor=(0.6, 0.38, 0.12), forca=0.8, gelatina=AMBAR, desfoque=1.2)

# 6. a sombra que cresce
REDEMOINHO = [Camada(objetos.redemoinho, k / 12, desfoque=1.4, opacidade=0.8, dobra=True) for k in range(12)]
GRANDE = [Boneco(bonecos.homem, escala=1.8, desfoque=3.5, opacidade=0.62), Boneco(bonecos.homem, escala=2.2, desfoque=6.0, opacidade=0.58)]
HX = 820


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    livros = q.env(0.0, 0.8, c.tradition_says - 0.2, 1.0)            # o pergaminho romano
    rolo = q.env(c.a_much - 0.4, 0.8, c.pride_goes - 0.6, 0.9)
    rei = q.env(c.tradition_says - 0.4, 0.8, c.pride_goes - 0.6, 0.9)
    torre = q.env(c.pride_goes - 0.6, 1.0, c.and_the - 0.5, 1.0)
    simples = q.env(c.and_the - 0.5, 1.0, c.two_men - 0.5, 1.0)
    dois = q.env(c.two_men - 0.5, 1.0, c.power_does - 0.5, 1.0)
    poder = q.ss(c.power_does - 0.5, 1.0)
    topo = q.env(c.fall - 1.2, 0.8, c.fall, 0.4)                      # o homem no alto da torre
    q.luz((1 + 0.1 * topo - 0.2 * dois - 0.3 * poder) * tremor(u))

    # ---- fundo: Roma dá lugar a outra terra ----
    q.sombra(LONGE, 1 - q.ss(c.in_another - 0.2, 1.6))
    q.sombra(ORIENTE, q.env(c.in_another - 0.2, 1.6, c.and_the - 0.5, 1.0))

    # ---- 1. o pergaminho romano e o rolo hebraico ----
    if livros > 0.002:
        q.sombra(PERGAMINHO, livros, 1 - 0.35 * q.ss(c.in_another, 1.2))
    if rolo > 0.002:
        k = int(round(12 * q.ss(c.a_much - 0.2, 1.8)))
        q.sombra(ROLO[k], rolo)
        if k == 12:
            q.chama(LINHA, rolo, q.ss(c.line - 0.2, 1.0), cintila=(0.92, 0.08, 5), camada=ROLO[12])

    # ---- 2. Salomão ----
    if rei > 0.002:
        chega = q.ss(c.tradition_says - 0.4, 2.6)
        passo = _anda(q) * (1 - q.ss(c.tradition_says + 1.8, 0.6))
        ergue = q.ss(c.he_holds - 0.3, 1.2)
        q.boneco(REI, 80 + 560 * chega, _chao(1.3), {'legF': passo, 'legB': -passo, 'uarmF': 4 - 60 * ergue, 'farmF': -6 - 40 * ergue,
                                                     'uarmB': -4, 'farmB': -6, 'head': 4 - 6 * ergue}, rei)
        q.sombra(SOLOMON, rei, q.ss(c.solomon - 0.3, 1.0))
        q.foco(0.3 * q.env(c.line - 0.2, 1.0, c.pride_goes - 0.8, 0.6), 1340, 374, 300)

    # ---- 3. Provérbios 16:18: a torre e a queda ----
    if torre > 0.002:
        sobe = q.ss(c.pride_goes - 0.5, 1.6)
        q.sombra(TORRE, torre, dy=640 * (1 - sobe))
        texto = q.env(c.pride_goes - 0.2, 0.8, c.in_other, 1.0)
        for linha, deixa in zip(Q1618, (c.pride_goes, c.and_an)):
            q.sombra(linha, torre, texto, q.ss(deixa - 0.2, 0.8))
        q.credito(CRED_1618, torre * texto)

        s = 0.6
        cai = q.ss(c.fall, 0.9)
        if cai <= 0:                                                    # subindo
            p = q.ss(c.pride_goes + 0.6, c.fall - c.pride_goes - 1.3) * (len(CAMINHO) - 1)
            i = min(int(p), len(CAMINHO) - 2)
            f = p - i
            (x0, y0), (x1, y1) = CAMINHO[i], CAMINHO[i + 1]
            x, pe = lerp(x0, x1, f), lerp(y0, y1, min(1, f * 1.6))
            parado = q.ss(c.fall - 1.2, 0.4)
            passo = _anda(q) * (1 - parado)
            q.boneco(ALPINISTA, x, _chao(s, pe), {'legF': passo, 'legB': -passo, 'uarmF': 10 - 50 * parado, 'farmF': -10 - 30 * parado,
                                                  'uarmB': -10, 'farmB': -6, 'head': -4 - 10 * parado}, torre, q.ss(c.pride_goes + 0.4, 0.6))
        else:                                                           # a queda (para fora da torre, à direita)
            x0, pe0 = CAMINHO[-1]
            x = lerp(x0, TX + 340, cai)
            y = lerp(_chao(s, pe0), BASE - 74, cai ** 2)                # cai deitado, acima do capim
            q.boneco(ALPINISTA, x, y, {'torso': 90 * cai, 'legF': 30 * math.sin(u * 11) * (1 - cai), 'legB': -20 * (1 - cai),
                                       'uarmF': -120 * (1 - cai) - 10, 'farmF': -20, 'uarmB': 100 * (1 - cai), 'farmB': -10}, torre)
        q.foco(0.3 * q.env(c.ground - 0.3, 0.8, c.and_the - 0.6, 0.6), TX + 340, BASE - 80, 260)

    # ---- 4. Provérbios 16:19 ----
    if simples > 0.002:
        texto = q.env(c.it_is - 0.2, 0.8, c.in_simple, 1.0)
        for linha, deixa in zip(Q1619, (c.it_is, c.than_to)):
            q.sombra(linha, simples, texto, q.ss(deixa - 0.2, 0.8))
        q.credito(CRED_1619, simples * texto)
        # os simples, em volta do fogo
        q.boneco(ADULTO, 430, _chao(1.2), {'uarmF': -30, 'farmF': -40, 'head': 8}, simples)
        q.boneco(CRIANCA, 530, _chao(0.82), {'uarmF': -40, 'farmF': -30, 'head': 4}, simples)
        q.boneco(ADULTO, 830, _chao(1.2), {'uarmF': -30, 'farmF': -40, 'head': 8}, simples, espelho=True)
        q.chama(FOGO[int(u * 8) % 4], simples, 0.8 + 0.3 * q.ss(c.better_to, 1.0),
                cintila=(0.85, 0.15, 9), dx=FOGO_DX)
        # os orgulhosos e o baú
        alma = 1 - 0.75 * q.ss(c.more_lose, 1.6)
        q.sombra(BAU, simples, dy=SOBE_BAU)
        for i, t in enumerate(OURO):
            q.sombra(t, simples, dx=(i - 1) * 70, dy=SOBE_BAU - 40)
        orgulho = {'uarmF': -50, 'farmF': -50, 'uarmB': 10, 'head': -14, 'torso': -4}
        q.boneco(ADULTO, BX - 220, _chao(1.2), orgulho, simples, alma)
        q.boneco(ADULTO, BX + 220, _chao(1.2), orgulho, simples, alma, espelho=True)
        mais = 1 + 2 * q.ss(c.less, 2.0)                                # "more": as moedas voam mais rápido
        pos = []
        for i in range(6):
            p = (max(0.0, u - c.plunder + 0.4) * 0.6 * mais + i / 6) % 1
            if u < c.plunder - 0.4 + i * 0.25:
                continue
            lado = 1 if i % 2 else -1
            x = BX + lado * 190 * p
            y = BASE - 230 - 160 * math.sin(math.pi * p) + 40 * p
            pos.append((x - 100, y - 100))
        if pos:
            q.multidao(MOEDA, pos, simples)
        q.foco(0.3 * q.env(c.better_to - 0.2, 1.0, c.two_men - 0.6, 0.8), 630, 700, 340)

    # ---- 5. os dois homens e a mesma verdade ----
    if dois > 0.002:
        um = q.env(c.one - 0.2, 0.6, c.the_other - 0.1, 0.6)
        outro = q.env(c.the_other - 0.2, 0.6, c.different_faiths - 0.1, 0.6)
        q.boneco(REI, 330, _chao(1.3), {'uarmF': 4, 'farmF': -6, 'uarmB': -4, 'farmB': -6, 'head': 6}, dois, 1 - 0.4 * outro)
        q.boneco(IMPERADOR, 1590, _chao(1.3), {'uarmF': 4, 'farmF': -6, 'uarmB': -4, 'farmB': -6, 'head': 6}, dois, 1 - 0.4 * um, espelho=True)
        if um > 0:
            q.foco(0.3 * um, 330, 640, 300)
        elif outro > 0:
            q.foco(0.3 * outro, 1590, 640, 300)
        p = q.ss(c.both_of - 0.2, c.truth - c.both_of + 0.5)
        if p > 0:
            q.chama(FIO, dois, recorte=(0, 0, 380 + (960 - 380) * p + 2, H))
            q.chama(FIO, dois, recorte=(1540 - (1540 - 960) * p - 2, 0, W, H))

    # ---- 6. o poder sussurra ----
    if poder > 0.002:
        g1 = q.ss(c.more - 0.6, 1.4) * (1 - q.ss(c.more + 0.6, 1.4))
        g2 = q.ss(c.more + 0.2, 1.8)
        q.boneco(GRANDE[1], HX + 60, _chao(2.2, BASE + 80), {'head': -8, 'torso': -2}, poder, g2)
        q.boneco(GRANDE[0], HX + 30, _chao(1.8, BASE + 50), {'head': -8, 'torso': -2}, poder, g1)
        q.boneco(HOMEM, HX, _chao(1.35), {'uarmF': 4, 'farmF': -6, 'uarmB': -4, 'farmB': -6, 'head': 4 - 10 * q.ss(c.that_he, 1.5)}, poder)
        sussurro = q.env(c.it_whispers - 0.3, 1.0, c.that_he + 0.4, 1.2)
        if sussurro > 0:
            q.sombra(REDEMOINHO[int(u * 6) % 12], poder, 0.8 * sussurro, dx=HX - 540)

    q.sombra(LATERAIS)

    # ---- câmera ----
    z_linha = q.env(c.line - 0.2, 1.5, c.pride_goes - 0.8, 0.6) * 0.10
    z_alto = q.env(c.the_higher - 0.2, 1.2, c.the_harder - 0.1, 0.8) * 0.12
    z_chao = q.env(c.ground - 0.4, 1.0, c.and_the - 0.6, 0.8) * 0.14
    z_poder = q.ss(c.power_does, c.fim - c.power_does) * 0.06
    if z_linha > 0:
        q.camera(1340, 374, 1 + z_linha)
    elif z_alto > 0:
        q.camera(TX, 340, 1 + z_alto)
    elif z_chao > 0:
        q.camera(TX + 300, 820, 1 + z_chao)
    elif z_poder > 0:
        q.camera(HX + 60, 480, 1 + z_poder)

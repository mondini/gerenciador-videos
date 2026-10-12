"""Vídeo 1 · Bloco 4 — A lição. Script de cena (padrão Teatro de Sombras Projetadas).

Grupos de cenas guiados pela narração:
  1. O celular: o homem entra; o celular sobe com a tela acesa em âmbar (a coisa nova); o brilho apaga;
     um maior empurra o velho, outro maior ainda; os novos vão embora e o velho volta igual.
     "Something changed in you": redemoinho sobre a cabeça do homem.
  2. O dinheiro: moedas empilham no pedestal; somem, e a conta desenrola. Insônia (noite, lua, o homem
     sentado com a cabeça nas mãos); a família que racha e se afasta; as portas do arco se fecham.
  3. O vaso furado ("another kind of poverty"): moedas caem na boca do vaso e escorrem pela fresta do
     fundo; quanto mais entra (mais rápido), mais sai. O homem olha.
  4. Provérbios 30:8: a balança (moedas x pão) balança, pende para um lado e para o outro e se equilibra.
  5. Meditações 7.27: o imperador escreve na tenda; a casa, a mesa (tigela) e a lamparina do gancho voltam
     com gelatina âmbar; somem em "if they were gone" e reaparecem.
"""
from marbleash.cena import *

STILLS = (5.5, 12.0, 20.0, 27.0, 35.2, 36.8, 39.2, 42.5, 50.0, 64.0, 69.5, 82.5, 92.0, 99.6)   # um still por grupo/cena

TINTA = (60, 34, 16, 255)
AMBAR = (0.91, 0.64, 0.24)                                    # amber-500
CHAO = BASE - 172 * 1.35                                      # pivô do torso do homem de pé (escala 1.35)

# ================= ELENCO =================
LONGE = Camada(cenario.longe, desfoque=9, opacidade=0.30, semente=1, pivo=(1200, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.meio, desfoque=6, opacidade=0.42, semente=2, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais, desfoque=4.5, opacidade=0.86, semente=3, pivo=(200, 1080), balanco=(3.0, 0.45))
PENHASCO = Camada(objetos.penhasco, desfoque=3.0, opacidade=0.86, semente=10, pivo=(900, BASE), balanco=(2.0, 0.2))
HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
CRIANCA = Boneco(bonecos.homem, escala=0.82, desfoque=1.1, opacidade=0.9)
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)
CHAMA_NOITE = Chama(objetos.chama_noite, 1, brilho=26, cor=(0.7, 0.42, 0.12), forca=1.5)
MOEDA = Camada(objetos.moeda, desfoque=1.4, opacidade=0.82, posicao=(100, 100), dobra=False)     # centro em (100, 100)


def _citacao(texto, y, cx=1000):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', 42, cx, y,
                  desfoque=1.4, opacidade=0.8, semente=17, pivo=(cx, 170), balanco=(1.2, 0.15))


# 1. o celular
CEL = Camada(objetos.celular, 1150, 540, 1.0, desfoque=1.6, opacidade=0.88, semente=11, pivo=(1150, 760), balanco=(1.5, 0.15))
CEL2 = Camada(objetos.celular, 1250, 540, 1.2, desfoque=1.6, opacidade=0.88, semente=12, pivo=(1250, 800), balanco=(1.5, 0.15))
CEL3 = Camada(objetos.celular, 1330, 540, 1.45, desfoque=1.6, opacidade=0.88, semente=13, pivo=(1330, 860), balanco=(1.5, 0.15))
TELA = Chama(objetos.celular_tela, 1150, 540, 1.0, brilho=26, cor=(0.6, 0.38, 0.12), forca=0.8, gelatina=AMBAR, desfoque=1.6)
TELA2 = Chama(objetos.celular_tela, 1250, 540, 1.2, brilho=26, cor=(0.6, 0.38, 0.12), forca=0.8, gelatina=AMBAR, desfoque=1.6)
TELA3 = Chama(objetos.celular_tela, 1330, 540, 1.45, brilho=26, cor=(0.6, 0.38, 0.12), forca=0.8, gelatina=AMBAR, desfoque=1.6)
REDEMOINHO = [Camada(objetos.redemoinho, k / 12, desfoque=1.4, opacidade=0.8, dobra=True) for k in range(12)]

# 2. o dinheiro, a insônia, a família, as portas
PEDESTAL = Camada(objetos.pedestal, desfoque=2.0, opacidade=0.85, semente=9, pivo=(960, BASE), balanco=(2.0, 0.2))
SOBE_PEDESTAL = -90                                          # acima do monte de capim da frente
PILHA = [(960 + 30 * (c - (5 - r - 1) / 2), 798 + SOBE_PEDESTAL - 24 * r) for r in range(5) for c in range(5 - r)]   # pirâmide de 15 moedas
CONTA = [Camada(objetos.conta, k / 16, desfoque=1.5, opacidade=0.86, semente=14, pivo=(1280, 300), balanco=(2.0, 0.3)) for k in range(17)]
BANQUINHO = Camada(objetos.banquinho, 540, 150, desfoque=1.8, opacidade=0.86, semente=15, pivo=(540, BASE), balanco=(1.0, 0.1))
FENDA = [Camada(objetos.fenda, k / 12, desfoque=1.2, opacidade=0.85) for k in range(13)]
ARCO = Camada(objetos.arco, desfoque=3.2, opacidade=0.62, semente=8, pivo=(960, BASE), balanco=(2.5, 0.3))
PORTAS = [Camada(objetos.portas, k / 24, desfoque=3.2, opacidade=0.6, semente=8, pivo=(960, BASE), balanco=(2.5, 0.3))
          for k in range(25)]

# 3. o vaso furado
VASO = Camada(objetos.vaso, desfoque=2.0, opacidade=0.86, semente=16, pivo=(960, BASE), balanco=(1.2, 0.1))

# 4. Provérbios 30:8
BALANCA = [Camada(objetos.balanca, (k - 12) * 1.2, desfoque=1.8, opacidade=0.86, semente=18, pivo=(960, BASE), balanco=(1.2, 0.1))
           for k in range(25)]
Q308 = [_citacao('Give me neither poverty nor riches.', 105),
        _citacao('Feed me with the food that is needful for me.', 165)]
CRED_308 = Credito('Proverbs 30:8 · World English Bible')

# 5. Meditações 7.27 e a casa do gancho em âmbar
Q727 = [_citacao('Think not so much of what thou hast not', 105, 1070),
        _citacao('as of what thou hast…', 165, 1070)]
CRED_727 = Credito('Marcus Aurelius, Meditations 7.27 · trans. George Long')
TEMPLO = Camada(objetos.templo, desfoque=2.4, opacidade=0.82, semente=4, pivo=(800, BASE), balanco=(2.2, 0.3))
MESA = Camada(objetos.mesa, desfoque=2.4, opacidade=0.82, semente=5, pivo=(1450, BASE), balanco=(2.2, 0.3))
LAMPARINA = Camada(objetos.lamparina, desfoque=1.8, opacidade=0.84, semente=6, pivo=(1190, 0), balanco=(3.0, 0.6))
CHAMA = Chama(objetos.chama, 1, brilho=22, cor=(0.6, 0.38, 0.12), forca=1.3)
OURO = [(c, Chama(c.arte, brilho=10, cor=(0.6, 0.38, 0.12), forca=0.3, gelatina=AMBAR, desfoque=c.desfoque)) for c in (TEMPLO, MESA, LAMPARINA)]


# ================= LINHA DO TEMPO =================
def _anda(q, i=0):
    """Pernas de quem caminha."""
    return 26 * math.sin(q.u * 7 + i)


def quadro(q, c):
    u = q.u
    pe1 = 1 - q.ss(c.awake - 0.4, 0.6)                              # o homem de pé (celular, dinheiro)
    celular = q.env(c.phone - 0.5, 1.0, c.money - 0.6, 0.8)
    dinheiro = q.env(c.money - 0.6, 0.8, c.awake - 0.4, 0.6)
    sentado = q.env(c.awake - 0.4, 0.6, c.families - 0.4, 0.6)
    familia = q.env(c.families - 0.4, 0.6, c.choices - 0.4, 0.6)
    portas = q.env(c.choices - 0.5, 0.8, c.poverty - 0.6, 0.9)
    pe2 = q.env(c.choices - 0.4, 0.6, c.proverbs - 0.6, 0.9)        # o homem diante das portas e do vaso
    vaso = q.env(c.poverty - 0.6, 1.0, c.proverbs - 0.6, 0.9)
    balanca = q.env(c.proverbs - 0.6, 1.0, c.marcus - 0.6, 0.9)
    tenda = q.env(c.marcus - 0.6, 1.0, c.simple - 0.3, 1.0)
    casa = q.ss(c.stop - 0.3, 1.2)
    some = q.ss(c.gone, 0.7) * (1 - q.ss(c.gone + 1.3, 1.0))        # "if they were gone": somem e voltam
    noite = max(sentado, tenda)
    fechou = portas * q.ss(c.choices, 1.6)
    q.luz((1 - 0.5 * noite) * (1 - 0.15 * fechou) * (1 - 0.3 * casa * some) * tremor(u))
    q.lua(sentado, cx=1500, cy=190, raio=55, crescente=0.45)
    q.lua(tenda, cx=1610, cy=150, raio=50, crescente=0.45)

    # ---- fundo ----
    q.sombra(LONGE, max(celular, dinheiro, 0.7 * sentado, portas, vaso, balanca, 0.7 * tenda, casa))
    q.sombra(MEIO, max(celular, dinheiro, portas, vaso, balanca))

    # ---- o homem de pé (entra caminhando) ----
    if pe1 > 0.002:
        chega = q.ss(0.0, 3.0)
        passo = _anda(q) * (1 - q.ss(2.4, 0.6))
        mudou = q.ss(c.changed - 0.2, 1.2)
        q.boneco(HOMEM, -150 + 690 * chega, CHAO, {'legF': passo, 'legB': -passo, 'uarmF': 4, 'farmF': -6, 'uarmB': -4, 'farmB': -6,
                                                   'head': 4 + 12 * mudou, 'torso': 3 * mudou}, pe1)
        if mudou > 0:
            q.sombra(REDEMOINHO[int(u * 10) % 12], pe1, mudou * (1 - q.ss(c.now2, 1.0)))

    # ---- 1. o celular ----
    if celular > 0.002:
        sobe = q.ss(c.phone - 0.2, 1.4)
        empurra = q.ss(c.slower, 0.8)
        empurra2 = q.ss(c.older, 0.8)
        volta = q.ss(c.nothing - 0.2, 1.2)
        dx1 = -330 * empurra * (1 - volta) - 160 * empurra2 * (1 - volta)
        dy1 = 600 * (1 - sobe)
        q.sombra(CEL, celular, min(1, sobe * 3), dx=dx1, dy=dy1)
        brilho = q.ss(c.phone + 0.4, 1.2) * (1 - q.ss(c.andthen, c.justphone - c.andthen + 0.4))
        if brilho > 0:
            q.chama(TELA, celular, brilho, cintila=(0.92, 0.08 * q.env(c.thrill, 0.5, c.andthen, 0.5), 11), camada=CEL, dx=dx1, dy=dy1)
        sai = q.ss(c.nothing - 0.2, 1.2)
        dx2 = 900 * (1 - empurra) - 280 * empurra2 + 1100 * sai
        q.sombra(CEL2, celular, empurra, dx=dx2)
        q.chama(TELA2, celular, empurra * (1 - empurra2), camada=CEL2, dx=dx2)
        dx3 = 900 * (1 - empurra2) + 1100 * sai
        q.sombra(CEL3, celular, empurra2, dx=dx3)
        q.chama(TELA3, celular, empurra2 * (1 - sai), camada=CEL3, dx=dx3)
        q.foco(0.5 * celular * q.ss(c.changed, 1.2), 560, 520, 300)

    # ---- 2. o dinheiro ----
    if dinheiro > 0.002:
        q.sombra(PEDESTAL, dinheiro, dy=SOBE_PEDESTAL)
        pos, pesos = [], []
        for i, (x, y) in enumerate(PILHA):
            cai = q.ss(c.money - 0.2 + 0.11 * i, 0.5)
            if cai <= 0:
                continue
            pos.append((x - 100, -60 + (y + 60) * cai - 100))
            pesos.append(1 - q.ss(c.notenough + 0.6 - 0.07 * i, 0.4) if i >= 2 else 1.0)    # sobram duas
        if pos:
            q.multidao(MOEDA, pos, dinheiro, pesos=pesos)
        k = int(round(16 * q.ss(c.notenough + 0.4, 1.4)))
        if k:
            q.sombra(CONTA[k], dinheiro)

    # ---- 2b. a insônia ----
    if sentado > 0.002:
        q.sombra(BANQUINHO, sentado)
        q.boneco(HOMEM, 560, BASE - 206, {'legF': -80, 'legB': -70, 'uarmF': -30, 'farmF': -130, 'uarmB': -20, 'farmB': -120,
                                          'head': 26, 'torso': 12}, sentado)

    # ---- 2c. a família que racha ----
    if familia > 0.002:
        k = int(round(12 * q.ss(c.families + 0.2, 1.0)))
        afasta = q.ss(c.families + 0.9, 1.2)
        q.boneco(HOMEM, 760 - 140 * afasta, CHAO, {'uarmF': -24, 'farmF': -10, 'head': 4}, familia)
        q.boneco(CRIANCA, 880 - 140 * afasta, BASE - 172 * 0.82, {'uarmB': 24, 'farmB': -10, 'head': -10}, familia)
        q.boneco(HOMEM, 1120 + 160 * afasta, BASE - 172 * 1.3, {'uarmB': 20, 'farmB': -8, 'head': 8}, familia)
        if k:
            q.sombra(FENDA[k], familia)

    # ---- 2d. as portas se fecham; o homem diante delas (e do vaso) ----
    if portas > 0.002:
        q.sombra(ARCO, portas)
        q.sombra(PORTAS[int(round(24 * (1 - q.ss(c.choices, 1.6))))], portas)
    if pe2 > 0.002:
        q.boneco(HOMEM, 460, CHAO, {'uarmF': 4, 'farmF': -6, 'uarmB': -4, 'farmB': -6, 'head': 6 + 6 * q.ss(c.ahead, 1.0)}, pe2)

    # ---- 3. o vaso furado ----
    if vaso > 0.002:
        q.sombra(VASO, vaso)
        fase = 0.45 * max(0.0, u - c.poverty) + 0.75 * max(0.0, u - c.follows)    # quanto mais ganha, mais rápido
        entra, sai, pesos = [], [], []
        for i in range(6):
            p = (fase + i / 6) % 1
            y = -40 + 362 * p
            entra.append((960 + 26 * math.sin(i * 2.1) - 100, y - 100))
            p2 = (fase + i / 6 + 0.4) % 1
            sai.append((992 + 10 * p2 - 100, 748 + 110 * p2 - 100))
            pesos.append(min(1.0, (1 - p2) * 4))
        q.multidao(MOEDA, entra, vaso, q.ss(c.poverty + 0.3, 0.8))
        q.multidao(MOEDA, sai, vaso, q.ss(c.poverty + 0.9, 0.8), pesos=pesos)
        q.foco(0.5 * vaso * q.env(c.feeling, 1.0, c.proverbs - 0.8, 0.8), 990, 740, 230)

    # ---- 4. Provérbios 30:8: a balança ----
    if balanca > 0.002:
        t = u - c.proverbs
        a = 6 * math.sin(1.3 * t) * (1 - q.ss(c.poor - 0.5, 0.6)) \
            + 14 * q.env(c.poor, 0.8, c.rich, 0.8) - 14 * q.env(c.rich, 0.8, c.forget + 0.4, 1.4)
        k = max(0, min(24, int(round(a / 1.2)) + 12))
        q.sombra(BALANCA[k], balanca, q.ss(c.proverbs - 0.3, 1.0))
        texto = q.env(c.give - 0.2, 0.8, c.inother - 0.3, 1.0)
        for i, linha in enumerate(Q308):
            q.sombra(linha, balanca, texto, q.ss((c.give, c.feed)[i] - 0.2, 0.8))
        q.credito(CRED_308, balanca * texto)

    # ---- 5. Meditações 7.27: a tenda ----
    if tenda > 0.002:
        q.sombra(PENHASCO, tenda)
        osc = math.sin(u * 9)
        q.boneco(IMPERADOR, 990, BASE - 110, {'uarmF': -62 + 6 * osc, 'farmF': -58 + 10 * math.sin(u * 13), 'legF': -70, 'legB': -60,
                                              'uarmB': -20, 'farmB': -30, 'head': 10}, tenda)
        q.chama(CHAMA_NOITE, tenda, cintila=(0.85, 0.15, 13))
        texto = q.ss(c.q727 - 0.2, 0.8)
        for i, linha in enumerate(Q727):
            q.sombra(linha, tenda, texto, q.ss(c.q727 - 0.2 + 1.8 * i, 0.8))
        q.credito(CRED_727, tenda * texto)

    # ---- 5b. a casa, a tigela e a lamparina do gancho, em âmbar ----
    if casa > 0.002:
        vis = casa * (1 - some)
        for camada in (TEMPLO, MESA, LAMPARINA):
            q.sombra(camada, vis)
        q.chama(CHAMA, vis, cintila=(0.9, 0.1, 9), camada=LAMPARINA)
        ouro = q.ss(c.look - 0.2, 1.5) * (0.45 + 0.3 * q.ss(c.choose, 1.5))
        for camada, gel in OURO:
            q.chama(gel, vis, ouro, camada=camada)

    # ---- laterais sempre presentes ----
    q.sombra(LATERAIS)

    # ---- câmera ----
    z_homem = q.env(c.changed - 0.3, 2.0, c.now2 - 0.2, 0.8) * 0.12
    z_vaso = q.env(c.feeling - 0.3, 2.5, c.proverbs - 0.8, 0.8) * 0.10
    z_tenda = q.env(c.marcus - 0.4, 2.0, c.q727 - 0.8, 1.0) * 0.16
    z_casa = q.env(c.choose, 2.5, c.gone, 0.8) * 0.08
    if z_homem > 0:
        q.camera(620, 540, 1 + z_homem)
    elif z_vaso > 0:
        q.camera(960, 640, 1 + z_vaso)
    elif z_tenda > 0:
        q.camera(1060, 640, 1 + z_tenda)
    elif z_casa > 0:
        q.camera(1100, 600, 1 + z_casa)

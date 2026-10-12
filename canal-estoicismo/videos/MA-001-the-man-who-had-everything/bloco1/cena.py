"""Vídeo 1 · Bloco 1 — Gancho. Script de cena (padrão Teatro de Sombras Projetadas).

MODELO OFICIAL para os próximos blocos: copie este arquivo para videos/video-NN/blocoN/cena.py e
troque o elenco e a função quadro(). Os tempos vêm de tempos.txt (c.roof, c.light...), sempre em
segundos desde o início da narração, já no ritmo desacelerado.

Três cenas guiadas pela narração:
  1. A casa (dia -> noite): o homem entra caminhando; o templo sobe do chão; a lamparina desce do teto
     e acende; a mesa desliza da direita; "not yet... not enough" + noite + lua crescente + foco e zoom no homem.
  2. A glória (luz forte): o imperador sobe num pedestal e ergue o braço; moedas chovem; soldados
     marcham dos dois lados; o arco se abre.
  3. A beira do mundo (noite): penhasco, tenda, ciprestes; o imperador sentado escreve; fumaça da
     lamparina; foco de luz e zoom lento até o fim do bloco.
"""
from marbleash.cena import *

ENTRADA = 0.4          # segundos de vídeo antes da narração
SAIDA = 1.0            # segundos depois da narração (o último segundo escurece)
STILLS = (3, 8.5, 16.5, 23, 27, 31, 35.8)      # conferência: caminhada, lamparina, sussurro, moedas, portas, noite, escrita

# ================= ELENCO =================
# desfoque = distância do lençol (px): personagem ~1, objetos 1.5–3, laterais 4.5, fundo 6–9.
# semente/pivo/balanco = balanço independente de cada peça na vareta (amplitude px, rotação graus).
LONGE = Camada(cenario.longe, desfoque=9, opacidade=0.30, semente=1, pivo=(1200, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.meio, desfoque=6, opacidade=0.42, semente=2, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais, desfoque=4.5, opacidade=0.86, semente=3, pivo=(200, 1080), balanco=(3.0, 0.45))
PENHASCO = Camada(objetos.penhasco, desfoque=3.0, opacidade=0.86, semente=10, pivo=(900, BASE), balanco=(2.0, 0.2))

TEMPLO = Camada(objetos.templo, desfoque=2.4, opacidade=0.82, semente=4, pivo=(800, BASE), balanco=(2.2, 0.3))
MESA = Camada(objetos.mesa, desfoque=2.4, opacidade=0.82, semente=5, pivo=(1450, BASE), balanco=(2.2, 0.3))
LAMPARINA = Camada(objetos.lamparina, desfoque=1.8, opacidade=0.84, semente=6, pivo=(1190, 0), balanco=(3.0, 0.6))
SUSSURRO = Camada(objetos.letreiro, 'not yet...   not enough.', 'Cormorant-MediumItalic.ttf', desfoque=1.5, opacidade=0.75, semente=7, pivo=(960, 200),
                  balanco=(1.5, 0.2))

ARCO = Camada(objetos.arco, desfoque=3.2, opacidade=0.62, semente=8, pivo=(960, BASE), balanco=(2.5, 0.3))
PORTAS = [Camada(objetos.portas, k / 24, desfoque=3.2, opacidade=0.6, semente=8, pivo=(960, BASE), balanco=(2.5, 0.3))
          for k in range(25)]                                   # 25 passos da porta abrindo (balança junto com o arco)
PEDESTAL = Camada(objetos.pedestal, desfoque=2.0, opacidade=0.85, semente=9, pivo=(960, BASE), balanco=(2.0, 0.2))
SOLDADO = Camada(objetos.soldado, desfoque=2.6, opacidade=0.82, posicao=(200, 400))      # pés desenhados em (200, 400)
MOEDA = Camada(objetos.moeda, desfoque=1.4, opacidade=0.8, posicao=(100, 100), dobra=False)  # centro em (100, 100)
FUMACA = {(i, k): Camada(objetos.fumaca, i, k / 20, desfoque=2.2, opacidade=0.55)
          for i in range(3) for k in range(2, 21, 2)}           # 3 fios, cada um em 10 passos de subida

HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)

CHAMA = Chama(objetos.chama, 1, brilho=22, cor=(0.6, 0.38, 0.12), forca=1.3)
CHAMA_NOITE = Chama(objetos.chama_noite, 1, brilho=26, cor=(0.7, 0.42, 0.12), forca=1.5)


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    # ---- cenas e luz ----
    s1 = 1 - q.ss(c.imagine, 1.2)                                   # cena 1: a casa
    s2 = q.ss(c.imagine - 0.2, 1.2) * (1 - q.ss(c.andyet, 1.6))     # cena 2: a glória
    s3 = q.ss(c.andyet + 0.4, 1.6)                                  # cena 3: a beira do mundo
    noite1 = q.ss(c.still, 2.5) * (1 - q.ss(c.imagine, 1.6))
    gloria = q.ss(c.imagine, 3.0) * (1 - q.ss(c.andyet, 2.0))
    noite3 = q.ss(c.andyet, 2.5)
    q.luz((1 - 0.5 * noite1) * (1 + 0.15 * gloria) * (1 - 0.55 * noite3) * tremor(u))
    q.lua(q.ss(c.still + 0.6, 2.0) * s1, cx=960, cy=130, raio=58, crescente=0.45)   # crescente no céu livre, longe do galho
    q.lua(q.ss(c.night, 2.0) * s3)                                                 # lua cheia na beira do mundo

    # ---- fundo: Roma nas cenas 1 e 2; a beira do mundo na 3 ----
    roma = 1 - s3
    q.sombra(LONGE, roma)
    q.sombra(MEIO, roma)
    q.sombra(PENHASCO, s3)

    # ---- cena 1: a casa ----
    if s1 > 0.002:
        sobe = q.ss(c.roof, 1.6)                                    # templo sobe do chão
        q.sombra(TEMPLO, s1, min(1, sobe * 3), dy=420 * (1 - sobe))
        desce = q.ss(c.light, 1.8)                                  # lamparina desce do teto
        q.sombra(LAMPARINA, s1, dy=-460 * (1 - desce))
        desliza = q.ss(c.food, 1.6)                                 # mesa desliza da direita
        q.sombra(MESA, s1, dx=760 * (1 - desliza))
        anda = q.ss(0.3, 3.6)                                       # o homem entra caminhando...
        x = lerp(-180, 430, anda)
        andando = 0 < anda < 0.98
        sw = math.sin(u * 4.2) if andando else 0.25 * math.sin(u * 0.9)
        curva = q.ss(c.notyet, 1.4) * (1 - q.ss(c.imagine - 0.6, 0.8))   # ...e se curva no "not yet"
        y = BASE - 172 * 1.35 + (2 * abs(sw) if andando else 0)
        q.boneco(HOMEM, x, y, {'legF': 22 * sw, 'legB': -22 * sw, 'uarmF': -14 * sw + 10 * curva, 'uarmB': 14 * sw,
                               'farmF': -18 - 20 * curva, 'farmB': -10, 'head': 24 * curva - 4, 'torso': 6 * curva + 3}, s1)
        q.sombra(SUSSURRO, q.env(c.notyet, 1.2, c.imagine - 0.2, 1.0), dx=-360, dy=90)

    # ---- cena 2: a glória ----
    if s2 > 0.002:
        sobe = 360 * (1 - q.ss(c.imagine + 0.4, 1.6))               # pedestal sobe com o imperador
        porta = q.ss(c.door, 0.8)
        if porta > 0:
            q.sombra(PORTAS[int(round(24 * q.ss(c.open, 1.6)))], s2, porta)
            q.sombra(ARCO, s2, porta)
        soldados = []                                               # 6 de cada lado, marchando para o centro
        for i in range(12):
            lado = -1 if i < 6 else 1
            k = i % 6
            alvo = (720 - k * 95) if lado < 0 else (1200 + k * 95)
            p = q.ss(c.army + k * 0.12, 1.6)
            sx = lerp(alvo + lado * 1000, alvo, p)
            if -100 < sx < W + 100:
                soldados.append((sx - 200, -400 + BASE + 30 - 6 * abs(math.sin(u * 7 + i)) * (1 - p) + 4 * math.sin(u * 1.3 + i)))
        q.multidao(SOLDADO, soldados, s2)
        moedas, pesos = [], []                                      # chuva de moedas
        for i in range(36):
            p = q.lin(c.coin + (i * 0.37) % 2.0, 1.4)
            if 0 < p < 1:
                moedas.append((460 + (i * 173) % 800, -60 + (BASE - 90) * p * p))
                pesos.append(1 - ss(p, 0.9, 0.1))
        q.multidao(MOEDA, moedas, s2, pesos=pesos)
        q.sombra(PEDESTAL, s2, dy=sobe)
        braco = q.ss(c.imagine + 1.6, 1.4)
        q.boneco(IMPERADOR, 965, BASE - 104 - 184 * 1.3 + sobe, {'uarmF': -150 * braco, 'farmF': -20 * braco, 'head': -6 * braco,
                                                                 'uarmB': 8, 'farmB': -12, 'torso': 1.5 * math.sin(u * 0.8)},
                 s2, desfoque=1.2)

    # ---- cena 3: a beira do mundo ----
    if s3 > 0.002:
        escrevendo = u > c.wrote
        osc = math.sin(u * 9) if escrevendo else 0
        q.boneco(IMPERADOR, 990, BASE - 110, {'uarmF': -62 + 6 * osc, 'farmF': -58 + 10 * math.sin(u * 13) * (1 if escrevendo else 0),
                                              'legF': -70, 'legB': -60, 'uarmB': -20, 'farmB': -30,
                                              'head': 10 + 6 * q.ss(c.abouthow, 1.5)},
                 s3, q.ss(c.night + 0.4, 1.2))
        for i in range(3):                                          # fumaça da lamparina
            k = int(round(20 * q.lin(c.wrote + 0.8 + i * 1.9, 3.0)))
            k -= k % 2
            if k >= 2:
                q.sombra(FUMACA[i, k], s3, 1 - q.ss(c.abouthow + i * 0.6, 2.0))
        moedas, pesos = [], []                                      # moedas que sobem e somem ("not about how to get more")
        for i in range(10):
            p = q.lin(c.notabout + i * 0.18, 2.2)
            if 0 < p < 1:
                moedas.append((1200 + 120 * math.sin(i) - 200 * p, 500 - 220 * p))
                pesos.append(math.sin(math.pi * p))
        q.multidao(MOEDA, moedas, s3, pesos=pesos)

    # ---- laterais sempre presentes (moldura natural da tela) ----
    q.sombra(LATERAIS)

    # ---- foco de luz, chamas e câmera ----
    q.foco(q.env(c.notyet - 0.3, 1.6, c.imagine - 0.2, 1.4), 520, 560, 320)      # no homem curvado
    q.foco(q.env(c.wrote - 0.5, 2.0, c.inwhat + 1.5, 1.5), 1040, 650, 330)       # no imperador escrevendo
    if s1 > 0.01 and u > c.light + 1.0:
        q.chama(CHAMA, s1, cintila=(0.9, 0.1, 11), camada=LAMPARINA, dy=-460 * (1 - q.ss(c.light, 1.8)))
    if s3 > 0.01 and u > c.night + 1.0:
        q.chama(CHAMA_NOITE, s3, cintila=(0.85, 0.15, 13))
    z1 = q.env(c.notyet - 0.6, 2.4, c.imagine - 0.4, 1.8) * 0.38
    z2 = q.env(c.door - 0.2, 1.4, c.andyet - 0.4, 1.4) * 0.12
    z3 = q.env(c.wrote - 0.8, 3.0, c.inwhat + 2.0, 1.6) * (0.38 + 0.14 * q.ss(c.abouthow, 3.0))
    if z1 > 0:
        q.camera(520, 560, 1 + z1)
    elif z2 > 0:
        q.camera(960, 600, 1 + z2)
    elif z3 > 0:
        q.camera(1060, 640, 1 + z3)

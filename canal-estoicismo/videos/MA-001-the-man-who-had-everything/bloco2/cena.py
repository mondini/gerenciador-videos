"""Vídeo 1 · Bloco 2 — O homem. Script de cena (padrão Teatro de Sombras Projetadas).

Grupos de cenas guiados pela narração:
  1. O nome: coroa de louros + MARCUS AURELIUS em Cinzel; o templo sobe com Roma ao fundo ("the whole known world").
  2. Sem conforto: o templo racha (fresta em âmbar); a peste: cidades ao longe apagam as janelas, uma a uma.
  3. A fronteira: o Danúbio correndo, legionários marchando, escudo e lanças; o imperador aparece.
  4. O acampamento: noite, tendas, fogueira em âmbar, o imperador sentado; neve no "Cold".
  5. Escrevendo: na mesa de campanha (cenário do gancho), sob a lucerna, foco e zoom.
  6. As pessoas que o formaram: cinco bustos sobem; o da mãe em destaque; a citação de Meditações 1.3 com crédito.
  7. A lenda: o pergaminho se abre (Historia Augusta); o baú desliza, abre, e os tesouros sobem e vão embora;
     a dúvida escurece; "the story survived" traz a luz quente e o imperador de volta.
"""
from marbleash.cena import *

STILLS = (4.4, 13.9, 18.9, 24.0, 33.4, 36.9, 48.4, 67.4)      # um still por grupo

TINTA = (60, 34, 16, 255)
AMBAR = (0.91, 0.64, 0.24)                                    # amber-500

# ================= ELENCO =================
LONGE = Camada(cenario.longe, desfoque=9, opacidade=0.30, semente=1, pivo=(1200, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.meio, desfoque=6, opacidade=0.42, semente=2, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais, desfoque=4.5, opacidade=0.86, semente=3, pivo=(200, 1080), balanco=(3.0, 0.45))
PENHASCO = Camada(objetos.penhasco, desfoque=3.0, opacidade=0.86, semente=10, pivo=(900, BASE), balanco=(2.0, 0.2))

LOUROS = Camada(objetos.coroa_louros, desfoque=1.3, opacidade=0.85, semente=12, pivo=(960, 300), balanco=(1.5, 0.2))
NOME = Camada(objetos.letreiro, 'MARCUS AURELIUS', 'Cinzel-SemiBold.ttf', 84, 960, 460, TINTA, 0.04,
              desfoque=1.2, opacidade=0.85, semente=13, pivo=(960, 500), balanco=(1.2, 0.1))
SUBTITULO = Camada(objetos.letreiro, 'EMPEROR OF ROME  ·  AD 161 – 180', 'Cinzel-SemiBold.ttf', 30, 960, 580, TINTA, 0.2,
                   desfoque=1.2, opacidade=0.75, semente=13, pivo=(960, 500), balanco=(1.2, 0.1))
TEMPLO = [Camada(objetos.templo_rachado, k / 10, desfoque=2.4, opacidade=0.82, semente=4, pivo=(800, BASE), balanco=(2.2, 0.3))
          for k in range(11)]                                  # 11 passos da rachadura
RACHA = [Chama(objetos.racha_brasa, k / 10, brilho=10, forca=0.6, gelatina=AMBAR, desfoque=2.4) for k in range(11)]
CIDADES = [Camada(objetos.cidades, k, desfoque=2.2, opacidade=0.8, semente=14, pivo=(960, 800), balanco=(1.2, 0.08))
           for k in range(7)]                                  # k cidades já apagadas

RIO = [Camada(objetos.rio, k / 16, desfoque=1.8, opacidade=0.8) for k in range(16)]
SOLDADO = Camada(objetos.soldado, desfoque=2.6, opacidade=0.82, posicao=(200, 400))
ESCUDO = Camada(objetos.escudo_lancas, desfoque=2.2, opacidade=0.85, semente=15, pivo=(960, 700), balanco=(2.0, 0.25))
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)

ACAMPAMENTO = Camada(objetos.acampamento, desfoque=2.4, opacidade=0.84, semente=16, pivo=(960, BASE), balanco=(1.8, 0.15))
FOGO = [Chama(objetos.fogueira, k, brilho=30, cor=(0.7, 0.42, 0.12), forca=1.4) for k in range(4)]
FLOCO = Camada(objetos.floco, desfoque=1.0, opacidade=0.55, dobra=False)
CHAMA_NOITE = Chama(objetos.chama_noite, 1, brilho=26, cor=(0.7, 0.42, 0.12), forca=1.5)

BUSTOS = [Camada(objetos.busto, x, i == 2, i, desfoque=1.6, opacidade=0.86, semente=20 + i, pivo=(x, BASE), balanco=(1.5, 0.2))
          for i, x in enumerate((520, 740, 960, 1180, 1400))]  # o do meio (i = 2) é a mãe
CITACAO1 = Camada(objetos.letreiro, 'Simplicity in my way of living,', 'CormorantGaramond-MediumItalic.ttf', 58, 960, 140,
                  desfoque=1.4, opacidade=0.8, semente=17, pivo=(960, 200), balanco=(1.2, 0.15))
CITACAO2 = Camada(objetos.letreiro, 'far removed from the habits of the rich.', 'CormorantGaramond-MediumItalic.ttf', 58, 960, 222,
                  desfoque=1.4, opacidade=0.8, semente=17, pivo=(960, 200), balanco=(1.2, 0.15))
CRED_LONG = Credito('Marcus Aurelius, Meditations 1.3 · trans. George Long')

PERGAMINHO = [Camada(objetos.pergaminho, k / 20, desfoque=1.6, opacidade=0.85, semente=30, pivo=(960, 320), balanco=(2.0, 0.25))
              for k in range(21)]
CRED_HA = Credito('Historia Augusta, Life of Marcus 17')
BAU = [Camada(objetos.bau, k / 8, desfoque=2.0, opacidade=0.85, semente=31, pivo=(960, BASE), balanco=(2.0, 0.2)) for k in range(9)]
SOBE_BAU = -100              # o baú pousa sobre o monte de capim da base, em vez de ficar atrás dele
TESOUROS = [Camada(objetos.tesouro, i, desfoque=1.8, opacidade=0.85, semente=40 + i, pivo=(960, BASE - 150), balanco=(2.5, 0.4))
            for i in range(5)]


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    nome = 1 - q.ss(c.atime - 0.5, 1.0)
    roma = q.ss(c.atime - 0.6, 1.2) * (1 - q.ss(c.plague - 0.4, 1.2))
    peste = q.env(c.plague - 0.6, 1.0, c.northern - 0.4, 1.2)
    guerra = q.env(c.northern - 0.6, 1.2, c.camp - 0.8, 1.2)
    campo = q.env(c.camp - 0.8, 1.2, c.sat - 0.4, 1.0)
    escrita = q.env(c.sat - 0.6, 1.0, c.people - 0.5, 1.0)
    bustos = q.env(c.people - 0.6, 1.0, c.historians - 0.6, 1.2)
    lenda = q.ss(c.historians - 0.8, 1.2)
    noite = max(campo, escrita)
    gloria = q.ss(c.story, 2.5) * lenda
    duvida = q.env(c.whether, 1.0, c.story, 1.2)
    q.luz((1 - 0.35 * peste) * (1 - 0.5 * noite) * (1 - 0.12 * guerra) * (1 - 0.15 * duvida) * (1 + 0.12 * gloria) * tremor(u))
    q.lua(noite * q.ss(c.camp, 2.0), cx=960, cy=130, raio=58, crescente=0.45)

    # ---- fundo ----
    q.sombra(LONGE, max(roma, guerra, 0.8 * peste, 0.7 * campo))
    q.sombra(MEIO, max(roma, guerra, 0.7 * campo))
    q.sombra(PENHASCO, escrita)

    # ---- 1. o nome ----
    if nome > 0.002:
        q.sombra(LOUROS, nome, q.ss(0.2, 1.4))
        q.sombra(NOME, nome, q.ss(0.5, 1.0))
        q.sombra(SUBTITULO, nome, q.ss(c.nearly, 1.0))

    # ---- 2. o templo racha; a peste apaga as cidades ----
    if roma > 0.002:
        sobe = q.ss(c.atime, 1.6)
        k = int(round(10 * q.ss(c.years + 0.3, 2.0)))
        q.sombra(TEMPLO[k], roma, min(1, sobe * 3), dy=420 * (1 - sobe))
        if k > 0:
            q.chama(RACHA[k], roma, camada=TEMPLO[k], dy=420 * (1 - sobe))
    if peste > 0.002:
        q.sombra(CIDADES[min(6, int(7 * q.lin(c.city - 0.6, 3.2)))], peste)

    # ---- 3. a fronteira do Danúbio ----
    if guerra > 0.002:
        q.sombra(RIO[int(u * 6) % 16], guerra)
        marcha = []
        for i in range(7):
            x = -150 + ((u - c.northern) * 70 + i * 300) % 2300
            marcha.append((x - 200, -400 + BASE + 30 - 6 * abs(math.sin(u * 5 + i))))
        q.multidao(SOLDADO, marcha, guerra, q.ss(c.northern + 0.3, 1.5))
        escudo = q.env(c.warsend, 0.8, c.somost + 0.4, 1.0)
        q.sombra(ESCUDO, guerra, escudo, dy=300 * (1 - q.ss(c.warsend, 1.0)))
        q.boneco(IMPERADOR, 960, BASE - 172 * 1.3, {'uarmF': 8, 'farmF': -10, 'uarmB': -6, 'farmB': -8, 'torso': 1.2 * math.sin(u * 0.8)},
                 guerra, q.ss(c.somost + 0.3, 1.0))

    # ---- 4. o acampamento ----
    if campo > 0.002:
        q.sombra(ACAMPAMENTO, campo)
        frio = q.ss(c.cold, 1.5)
        q.boneco(IMPERADOR, 760, BASE - 76, {'legF': -70, 'legB': -60, 'uarmF': -50, 'farmF': -40, 'uarmB': -20, 'farmB': -30,
                                             'head': 10 + 12 * frio, 'torso': 4 + 3 * frio}, campo)
        if frio > 0:
            flocos = [((i * 137.3) % 1900 + 20 * math.sin(u * 0.7 + i) - 100, ((u - c.cold) * 60 + i * 53.7) % 900 - 100) for i in range(70)]
            q.multidao(FLOCO, flocos, campo, frio)
        q.chama(FOGO[int(u * 8) % 4], campo, cintila=(0.85, 0.15, 9))
        q.foco(0.8 * campo, 860, 760, 380)

    # ---- 5. escrevendo na mesa de campanha ----
    if escrita > 0.002:
        osc = math.sin(u * 9)
        q.boneco(IMPERADOR, 990, BASE - 110, {'uarmF': -62 + 6 * osc, 'farmF': -58 + 10 * math.sin(u * 13), 'legF': -70, 'legB': -60,
                                              'uarmB': -20, 'farmB': -30, 'head': 10 + 6 * q.ss(c.victories, 1.5)}, escrita)
        q.chama(CHAMA_NOITE, escrita, cintila=(0.85, 0.15, 13))
        q.foco(q.env(c.sat, 1.5, c.people - 0.6, 1.0), 1040, 650, 330)

    # ---- 6. as pessoas que o formaram; a mãe; a citação ----
    if bustos > 0.002:
        mae = q.ss(c.mother, 1.0)
        for i, b in enumerate(BUSTOS):
            p = q.ss(c.people + i * 0.35, 1.2)
            q.sombra(b, bustos, min(1, p * 3), 1 if i == 2 else 1 - 0.5 * mae, dy=380 * (1 - p))
        q.foco(q.env(c.mother, 1.0, c.simplicity - 0.3, 1.0), 960, 640, 240)
        cit = q.env(c.simplicity, 1.0, c.historians - 1.0, 1.2)
        q.sombra(CITACAO1, cit)
        q.sombra(CITACAO2, q.env(c.farremoved, 1.0, c.historians - 1.0, 1.2))
        q.credito(CRED_LONG, cit)

    # ---- 7. a lenda ----
    if lenda > 0.002:
        q.sombra(PERGAMINHO[int(round(20 * q.ss(c.historians + 0.2, 2.2)))], lenda, 1 - 0.35 * duvida)
        q.credito(CRED_HA, q.env(c.historians, 0.8, c.story - 0.5, 1.0))
        tampa = int(round(8 * q.ss(c.sold - 0.4, 0.8)))
        q.sombra(BAU[tampa], lenda, 1 - 0.35 * duvida, dx=760 * (1 - q.ss(c.whenwars, 1.6)), dy=SOBE_BAU)
        for i, t in enumerate(TESOUROS):
            t0 = c.sold + i * 0.45
            sobe, vai = q.ss(t0, 1.2), q.ss(t0 + 1.4, 2.2)
            lado = -1 if i % 2 else 1
            q.sombra(t, lenda, min(1, sobe * 2), 1 - vai, dx=(i - 2) * 90 * sobe + lado * (320 + i * 60) * vai, dy=SOBE_BAU - 120 * sobe - 30 * vai)
        q.boneco(IMPERADOR, 1380, BASE - 172 * 1.3, {'uarmF': 8, 'farmF': -10, 'uarmB': -6, 'farmB': -8, 'head': 4},
                 lenda, q.ss(c.sounds - 0.6, 1.2))

    # ---- laterais sempre presentes ----
    q.sombra(LATERAIS)

    # ---- câmera: aproximações nos momentos-chave ----
    z_mae = q.env(c.mother, 1.5, c.simplicity - 0.4, 1.2) * 0.18
    z_escrita = q.env(c.sat - 0.4, 2.0, c.people - 0.6, 1.0) * 0.22
    z_bau = q.env(c.sold - 0.5, 1.2, c.whether, 1.2) * 0.12
    if z_mae > 0:
        q.camera(960, 640, 1 + z_mae)
    elif z_escrita > 0:
        q.camera(1060, 640, 1 + z_escrita)
    elif z_bau > 0:
        q.camera(960, 720 + SOBE_BAU, 1 + z_bau)

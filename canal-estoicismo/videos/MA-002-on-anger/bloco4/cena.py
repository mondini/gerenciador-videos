"""Vídeo 2 · Bloco 4 — A traição de Avídio Cássio. Script de cena (moldura "oliveira"). A ideia mais forte do vídeo.

  1. "In the year 175": AD 175 em Cinzel; o general entra à esquerda (AVIDIUS CASSIUS) e Marco o encara da direita.
     "the entire East in his hands": o mapa do Oriente, e a hachura âmbar acende da fronteira para a costa.
  2. "a false rumor": o mensageiro atravessa a galope. "declared himself emperor": o general ergue a coroa de louros
     sobre a própria cabeça; os estandartes sobem atrás dele. "The man you raised up": foco nele, Marco olhando.
  3. "Rome began to prepare for civil war": duas legiões paradas, frente a frente, estandartes no alto.
     "Marcus gathered his soldiers": Marco fala às tropas; "to forgive him... a greater prize": a luz esquenta.
  4. "He never got that chance": escurece; o general afunda. "They brought his head": a caixa coberta chega
     pela direita; "would not look at it": Marco vira o rosto; "buried": a caixa desce para a terra.
  5. "And then... the letters": a capsa no centro; a tampa se abre, as cartas lacradas sobem; "Marcus burned
     them": o fogo acende e as cartas queimam fechadas, uma a uma; cinzas sobem. Foco no fogo.
  6. "He simply refused to feed it": o fogo baixa sozinho; Marco ao lado, uma tora no chão que ele não joga.
     A citação 11.18 em Cormorant. "some letters are better left unread": só a capsa fechada, com luz mansa.
     "Let's pause here": termina aceso (dissolve para a Pausa).
"""
from marbleash.cena import *

PANO = 'pesado'
STILLS = (2.0, 9.0, 14.0, 20.0, 26.0, 36.0, 50.0, 62.0, 72.0, 84.0, 100.0, 118.0)

CHAO = BASE - 172 * 1.35
CHAO_IMP = BASE - 172 * 1.3
TINTA = (60, 34, 16, 255)
A = (600, 520)                                                # âncora das peças de centro (0, 0)
AMBAR = (0.91, 0.64, 0.24)

# ================= ELENCO =================
LONGE = Camada(cenario.cidade, desfoque=9, opacidade=0.30, semente=11, pivo=(760, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.vinhedo, desfoque=6, opacidade=0.42, semente=12, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais_oliveira, desfoque=4.5, opacidade=0.86, semente=13, pivo=(200, 1080), balanco=(3.0, 0.45))
BASE_LENHA = Camada(cenario.base_lenha, desfoque=3.5, opacidade=0.88, semente=14, pivo=(400, 1080), balanco=(1.6, 0.2))


def _nome(texto, y, tam=64, tracking=0.06):
    return Camada(objetos.letreiro, texto, 'Cinzel-SemiBold.ttf', tam, 960, y, TINTA, tracking, desfoque=1.4, opacidade=0.8,
                  semente=60, pivo=(960, 180), balanco=(1.0, 0.1))


ANO = _nome('AD 175', 130, 54, 0.2)
NOME = _nome('AVIDIUS CASSIUS', 210)
GENERAL = [Camada(objetos.general, 560, k / 8, desfoque=1.4, opacidade=0.88, semente=61, pivo=(560, BASE), balanco=(1.4, 0.15))
           for k in range(9)]
MAPA = Camada(objetos.mapa_oriente, desfoque=1.3, opacidade=0.88, semente=62, pivo=(960, 460), balanco=(1.0, 0.12))
ORIENTE = [Chama(objetos.oriente_brasa, k / 10, brilho=10, cor=(0.6, 0.38, 0.12), forca=0.6, gelatina=AMBAR, desfoque=1.3)
           for k in range(11)]
CAVALO = [Camada(objetos.cavalo, k, desfoque=1.4, opacidade=0.9, posicao=A) for k in range(4)]
ESTANDARTE = [Camada(objetos.estandarte, x, 0.85, desfoque=2.2, opacidade=0.8, semente=63 + i, pivo=(x, BASE), balanco=(1.6, 0.25))
              for i, x in enumerate((300, 820, 1120, 1640))]
SOLDADO = Camada(objetos.soldado, desfoque=2.6, opacidade=0.82, posicao=(200, 400))
SOLDADO_E = Camada(objetos.espelhado, objetos.soldado, desfoque=2.6, opacidade=0.82, posicao=(200, 400))
CAIXA = Camada(objetos.caixa_coberta, 1300, desfoque=1.8, opacidade=0.88, semente=67, pivo=(1300, BASE), balanco=(1.4, 0.2))
CAPSA = [Camada(objetos.capsa, 960, k / 6, desfoque=1.8, opacidade=0.88, semente=68, pivo=(960, BASE), balanco=(1.2, 0.15))
         for k in range(7)]
CAPSA_FECHADA = Camada(objetos.capsa, 960, 0.0, 0, desfoque=1.8, opacidade=0.88, semente=68, pivo=(960, BASE), balanco=(1.2, 0.15))
CARTA = [Camada(objetos.carta, k / 10, 1.0, desfoque=1.3, opacidade=0.9, posicao=A) for k in range(11)]
CINZA = [Camada(objetos.cinza, k, desfoque=1.2, opacidade=0.6, posicao=A) for k in range(6)]
FOGUEIRA = [Camada(objetos.fogueira_toras, n, 1240, desfoque=2.0, opacidade=0.86, semente=69, pivo=(1240, BASE), balanco=(1.2, 0.1))
            for n in (3, 5)]
FOGO = [[Chama(objetos.labareda, k, tam, 1240, brilho=30 + 10 * tam, cor=(0.7, 0.42, 0.12), forca=1.4) for k in range(4)]
        for tam in (0.35, 0.6, 0.9, 1.2)]
TORA = Camada(objetos.tora, desfoque=1.4, opacidade=0.88, posicao=A)


def _texto(texto, y):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', 46, 960, y, desfoque=1.4, opacidade=0.8,
                  semente=70, pivo=(960, 170), balanco=(1.2, 0.15))


CITACAO = [_texto(t, 110 + 56 * k) for k, t in enumerate(('as the sense of pain', 'is a characteristic of weakness,', 'so also is anger.'))]

IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)

CRED_DIO = Credito('Cassius Dio, Roman History 72.26–29 · Loeb Classical Library')
CRED_MED = Credito('Marcus Aurelius, Meditations 11.18 · trans. George Long')


def _legiao(q, x0, passo, n, fator, espelho):
    """Fileira parada de n soldados a partir de x0 (respiram de leve na vareta)."""
    u = q.u
    pos = [(x0 + i * passo - 200, objetos.CHAO2 + 16 - 400 + 3 * math.sin(u * 1.1 + i)) for i in range(n)]
    q.multidao(SOLDADO_E if espelho else SOLDADO, pos, fator)


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    abertura = 1 - q.ss(c.hero - 0.3, 0.8)
    mapa = q.env(c.hero - 0.3, 0.8, c.rumor - 0.3, 0.8)
    revolta = q.env(c.rumor - 0.3, 0.8, c.war - 0.3, 0.9)
    guerra = q.env(c.war - 0.3, 0.9, c.chance - 0.3, 1.0)
    morte = q.env(c.chance - 0.3, 1.0, c.then - 0.3, 0.9)
    cartas = q.env(c.then - 0.3, 0.9, c.think - 0.3, 1.0)
    fim = q.ss(c.think - 0.3, 1.0)

    escuro = q.env(c.chance, 1.0, c.head, 1.2)
    calor = q.env(c.forgive, 1.2, c.chance, 0.8)
    q.luz((1 - 0.45 * escuro) * (1 + 0.15 * calor) * (1 - 0.3 * cartas * q.ss(c.burned, 1.0)) * (1 - 0.25 * fim) * tremor(u))

    q.sombra(LONGE, 1 - mapa)
    q.sombra(MEIO, 1 - mapa)

    # ---- 1. o general e o imperador ----
    if abertura > 0.002:
        q.sombra(ANO, abertura, q.ss(c.year - 0.2, 0.8))
        q.sombra(NOME, abertura, q.ss(c.cassius + 1.0, 0.8))
        entra = q.ss(c.cassius, 1.6)
        q.sombra(GENERAL[0], abertura, entra, dx=-500 * (1 - entra))
        q.boneco(IMPERADOR, 1360, CHAO_IMP, {'uarmF': 4, 'farmF': -14, 'head': 2}, abertura, espelho=True)
        q.credito(CRED_DIO, q.env(c.year, 0.8, c.rumor, 0.8))
    if mapa > 0.002:
        q.sombra(MAPA, mapa)
        acende = q.ss(c.east - 0.2, c.rumor - c.east)
        q.chama(ORIENTE[int(round(10 * acende))], mapa, cintila=(0.95, 0.05, 3))

    # ---- 2. o boato, a coroa ----
    if revolta > 0.002:
        corre = q.lin(c.rumor - 0.2, 3.2)
        if 0 < corre < 1:
            q.sombra(CAVALO[int(u * 10) % 4], revolta, dx=lerp(-300, 2200, corre) - A[0], dy=BASE + 30 - 40 - A[1])
        coroa = q.ss(c.declared, 1.6)
        sobe = q.ss(c.declared + 0.4, 1.4)
        for k, est in enumerate(ESTANDARTE[:1]):
            q.sombra(est, revolta, sobe, dy=500 * (1 - sobe))
        q.sombra(GENERAL[int(round(8 * coroa))], revolta)
        q.boneco(IMPERADOR, 1360, CHAO_IMP, {'uarmF': 4, 'farmF': -14, 'head': -4 + 10 * q.ss(c.imagine, 1.2)}, revolta, espelho=True)
        q.foco(q.env(c.raised - 0.3, 1.0, c.war - 0.2, 0.8), 560, 560, 300)

    # ---- 3. a guerra civil; Marco fala às tropas ----
    if guerra > 0.002:
        frente = q.ss(c.war - 0.2, 1.4)
        _legiao(q, 1880 - 150 * 4 * frente, 150, 4, guerra * frente, True)
        q.sombra(ESTANDARTE[3], guerra, frente)
        fala = q.ss(c.gathered - 0.2, 1.2)
        _legiao(q, 120 - 400 * (1 - fala), 130, 3, guerra * fala, False)
        q.sombra(ESTANDARTE[0], guerra, fala)
        gesto = q.env(c.afraid, 0.6, c.chance, 0.8) * (0.6 + 0.4 * math.sin(u * 2.2))
        q.boneco(IMPERADOR, 760, CHAO_IMP, {'uarmF': -40 - 50 * gesto, 'farmF': -30, 'uarmB': -6, 'farmB': -10, 'head': 2}, guerra, fala)
        q.credito(CRED_DIO, q.env(c.dio, 0.8, c.chance, 0.8))

    # ---- 4. a morte de Cássio e a caixa ----
    if morte > 0.002:
        afunda = q.ss(c.killed, 1.4)
        q.sombra(GENERAL[8], morte, 1 - afunda, dy=380 * afunda)
        chega = q.ss(c.head - 0.2, 1.8)
        enterra = q.ss(c.buried, 1.6)
        q.sombra(CAIXA, morte, chega, dx=600 * (1 - chega), dy=300 * enterra)
        vira = q.ss(c.look - 0.2, 0.8)
        q.boneco(IMPERADOR, 760, CHAO_IMP, {'uarmF': 6, 'farmF': -16, 'head': 14 * vira, 'torso': 4 * vira}, morte, espelho=vira > 0.5)
        q.credito(CRED_DIO, q.env(c.months, 0.8, c.then - 0.2, 0.8))

    # ---- 5. as cartas ----
    if cartas > 0.002:
        abre = q.ss(c.among - 0.2, 1.4)
        fogo = q.ss(c.burned - 0.6, 1.0)
        q.sombra(CAPSA[int(round(6 * abre))], cartas)
        q.boneco(IMPERADOR, 520, CHAO_IMP, {'uarmF': -30 * q.env(c.burned - 0.8, 0.6, c.without, 1.0), 'farmF': -20, 'head': 6}, cartas)
        if fogo > 0.002:
            q.sombra(FOGUEIRA[1], cartas, fogo)
            q.chama(FOGO[3][int(u * 8) % 4], cartas, fogo, cintila=(0.85, 0.15, 9))
        for i in range(6):                                                   # as cartas sobem da capsa e vão ao fogo
            t0 = c.names + i * 0.7
            sai = q.ss(t0, 0.9)
            if sai <= 0:
                continue
            voa = q.ss(c.burned + i * 0.6, 1.2)
            col, fila = i % 3, i // 3                                        # duas fileiras de três, longe do rosto de Marco
            x = lerp(1010 + (col - 1) * 260, 1240 + (i - 2.5) * 14, voa)
            y = lerp(objetos.CHAO2 - 360, objetos.CHAO2 - 380 - 60 * sai - 80 * fila, 1 - voa) + 220 * voa
            queima = q.ss(c.burned + i * 0.6 + 1.0, 2.0)
            if queima < 0.99:
                q.sombra(CARTA[int(round(10 * queima))], cartas, sai, dx=x - A[0], dy=y - A[1])
        if fogo > 0.01:
            cinzas, pesos = [], []
            for i in range(14):
                p = ((u - c.burned) * 0.22 + i * 0.071) % 1.0
                cinzas.append((1240 - A[0] + 60 * math.sin(i * 1.7 + u * 0.8) + 40 * p, objetos.CHAO2 - 120 - 520 * p - A[1]))
                pesos.append(math.sin(math.pi * p))
            for k in range(6):
                q.multidao(CINZA[k], cinzas[k::6], cartas, fogo, pesos=pesos[k::6])
        q.foco(q.env(c.burned + 0.4, 1.4, c.account, 1.0), 1240, 700, 330)
        q.credito(CRED_DIO, q.env(c.among, 0.8, c.think - 0.2, 0.8))

    # ---- 6. ele não alimentou; a citação; as cartas que ficam sem ler ----
    if fim > 0.002:
        baixa = q.ss(c.refused, c.journal - c.refused + 2.0)
        q.sombra(FOGUEIRA[0], fim)
        tam = FOGO[max(0, 2 - int(baixa * 3))]
        q.chama(tam[int(u * 8) % 4], fim, 1 - 0.6 * baixa, cintila=(0.85, 0.15, 9))
        q.boneco(IMPERADOR, 760, CHAO_IMP, {'uarmF': 8, 'farmF': -12, 'head': 10, 'torso': 2}, fim)
        q.sombra(TORA, fim, q.ss(c.refused - 0.4, 0.8), dx=980 - A[0], dy=objetos.CHAO2 - 70 - A[1])
        for k, linha in enumerate(CITACAO):
            q.sombra(linha, fim, q.env((c.pain - 0.2, c.pain + 0.9, c.so_also - 0.2)[k], 0.9, c.knew - 0.2, 0.9))
        q.credito(CRED_MED, q.env(c.pain - 0.2, 0.8, c.knew, 0.8))
        q.sombra(CAPSA_FECHADA, fim, q.ss(c.knew, 1.2), dx=500)
        q.foco(q.ss(c.unread - 0.4, 1.4) * 0.6, 1460, 700, 280)

    q.sombra(BASE_LENHA)
    q.sombra(LATERAIS)

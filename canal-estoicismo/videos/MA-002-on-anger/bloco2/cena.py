"""Vídeo 2 · Bloco 2 — A raiva e o rancor. Script de cena (moldura "oliveira").

  1. Sêneca: uma fogueira pequena no centro; o nome SENECA em Cinzel. "We don't just feel anger... we feed it":
     o homem joga uma tora, e outra, e outra (a cada frase), e o fogo cresce. A citação aparece em Cormorant.
     "we keep the fire burning, just to prove we were right to light it": o fogo no máximo.
  2. Marco: a tabuinha de cera dupla; as regras vão sendo riscadas (I a IX) em "a list of rules"; em "consider"
     a oitava regra ganha foco.
  3. "what they did to you happened once": um único clarão. "What you do with it... happens every day":
     a luz passa de dia para noite três vezes sobre o homem parado. "The insult took a few seconds": o chefe
     aparece e some num instante; "The grudge... can take years": cai neve em volta do homem, que continua ali.
  4. Provérbios (rolo pequeno no canto): "A stone is heavy": a pedra desce; "a fool's provocation": pousa
     nas costas do homem, que se curva.
  5. "everything you lift at the gym": o homem ergue os halteres com facilidade; "unlike the gym": a pedra
     volta às costas e ele se curva mais. "Home. To the dinner table. And into bed": a mesa de jantar e
     depois a cama, sempre com a pedra.
"""
from marbleash.cena import *

PANO = 'pesado'
STILLS = (2.0, 9.0, 16.0, 26.0, 36.0, 44.0, 52.0, 60.0, 66.0, 72.0, 78.0, 84.0)

CHAO = BASE - 172 * 1.35
TINTA = (60, 34, 16, 255)
AMBAR = (0.91, 0.64, 0.24)

# ================= ELENCO =================
LONGE = Camada(cenario.cidade, desfoque=9, opacidade=0.30, semente=11, pivo=(760, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.vinhedo, desfoque=6, opacidade=0.42, semente=12, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais_oliveira, desfoque=4.5, opacidade=0.86, semente=13, pivo=(200, 1080), balanco=(3.0, 0.45))
BASE_LENHA = Camada(cenario.base_lenha, desfoque=3.5, opacidade=0.88, semente=14, pivo=(400, 1080), balanco=(1.6, 0.2))

FOGUEIRA = [Camada(objetos.fogueira_toras, n, 1100, desfoque=2.0, opacidade=0.86, semente=30, pivo=(1100, BASE), balanco=(1.2, 0.1))
            for n in range(1, 8)]
FOGO = [[Chama(objetos.labareda, k, tam, 1100, brilho=30 + 10 * tam, cor=(0.7, 0.42, 0.12), forca=1.4) for k in range(4)]
        for tam in (0.5, 0.75, 1.0, 1.25, 1.5, 1.75)]
A = (500, 400)                                                # âncora: peças de centro (0, 0) desenhadas em A
TORA = Camada(objetos.tora, desfoque=1.4, opacidade=0.88, posicao=A)
NOME = Camada(objetos.letreiro, 'SENECA', 'Cinzel-SemiBold.ttf', 72, 960, 150, TINTA, 0.06, desfoque=1.4, opacidade=0.8,
              semente=31, pivo=(960, 180), balanco=(1.0, 0.1))


def _texto(texto, y, tam=44):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', tam, 960, y, desfoque=1.4, opacidade=0.8,
                  semente=32, pivo=(960, 170), balanco=(1.2, 0.15))


CITACAO = [_texto('we nurse it and inflame it,', 120), _texto('as though to be violently angry', 176),
           _texto('proved our anger to be just.', 232)]
TABUA = [Camada(objetos.tabuinha, n, 960, 470, desfoque=1.4, opacidade=0.86, semente=33, pivo=(960, 470), balanco=(1.2, 0.15))
         for n in range(10)]
REGRA8 = Chama(objetos.linha_chao, 1.0, 1150, brilho=0)          # (não usado: o foco marca a regra VIII)
PEDRA = Camada(objetos.pedra_grande, 1.4, desfoque=1.4, opacidade=0.9, posicao=A)
PEDRA_COSTAS = Camada(objetos.pedra_grande, 1.15, True, desfoque=1.4, opacidade=0.92, posicao=A)
HALTERES = Camada(objetos.halteres, desfoque=1.3, opacidade=0.9, posicao=A)
CHEFE = Camada(objetos.figura_chefe, 1300, desfoque=1.6, opacidade=0.8, semente=34, pivo=(1300, BASE), balanco=(1.6, 0.2))
FLOCO = Camada(objetos.floco, desfoque=1.0, opacidade=0.95, posicao=(-100, -100), dobra=False)
ROLO = Camada(objetos.rolo_icone, 1250, 120, desfoque=1.4, opacidade=0.8, semente=35, pivo=(1250, 120), balanco=(1.0, 0.2))
MESA = Camada(objetos.mesa_jantar, 1260, desfoque=2.2, opacidade=0.84, semente=36, pivo=(1260, BASE), balanco=(1.6, 0.2))
CAMA = Camada(objetos.cama, 1060, desfoque=2.2, opacidade=0.84, semente=37, pivo=(1060, BASE), balanco=(1.6, 0.2))
DEITADO = Camada(objetos.homem_deitado, 1060, desfoque=1.4, opacidade=0.9, semente=37, pivo=(1060, BASE), balanco=(1.6, 0.2))

HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)

CRED_SEN = Credito('Seneca, Of Anger III.29 · trans. Aubrey Stewart')
CRED_MED = Credito('Marcus Aurelius, Meditations 11.18 · trans. George Long')
CRED_PROV = Credito('Proverbs 27:3 · World English Bible')


def _ponto(x, y, pose, peca, local):
    """Onde fica, no quadro, um ponto `local` (coordenadas da peça) do homem nesta pose (ex.: a mão)."""
    (px, py), ang = bonecos.homem().pose(x, y, pose, 1.35)[peca]
    r = math.radians(ang)
    lx, ly = local[0] * 1.35, local[1] * 1.35
    return px + lx * math.cos(r) - ly * math.sin(r), py + lx * math.sin(r) + ly * math.cos(r)


def _arremesso(q, t0, de=(600, 520), para=(1100, 820)):
    """Posição da tora jogada em t0 (arco de 0,9 s) ou None fora do voo."""
    p = q.lin(t0, 0.9)
    if not 0 < p < 1:
        return None
    x = lerp(de[0], para[0], p)
    y = lerp(de[1], para[1], p) - 220 * math.sin(math.pi * p)
    return x, y


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    fogueira = 1 - q.ss(c.trap - 0.3, 1.0)
    tabua = q.env(c.trap - 0.3, 1.0, c.once - 0.3, 0.8)
    ciclo = q.env(c.once - 0.3, 0.8, c.proverbs - 0.3, 0.9)
    pedra = q.ss(c.proverbs - 0.3, 0.9)

    # luz: dia/noite três vezes em "happens every day"; neve em "years"
    dias = q.env(c.what, 0.4, c.insult, 0.6) * (0.5 - 0.5 * math.cos((u - c.what) * 2 * math.pi * 3 / max(c.insult - c.what, 0.1)))
    clarao = q.env(c.once, 0.15, c.once + 0.3, 0.5)
    noite_cama = q.ss(c.bed - 0.4, 1.4)
    q.luz((1 - 0.45 * dias) * (1 + 0.3 * clarao) * (1 - 0.4 * noite_cama) * (1 - 0.15 * fogueira) * tremor(u))
    q.lua(dias * 0.9 + noite_cama, cx=1300, cy=150, raio=50, crescente=0.5)

    q.sombra(LONGE, 1 - 0.6 * tabua)
    q.sombra(MEIO, 1 - 0.6 * tabua)

    # ---- 1. Sêneca: a fogueira alimentada ----
    if fogueira > 0.002:
        jogadas = [c.feed, c.suspect, c.because, c.nurse, c.keep]
        n = 1 + sum(1 for t in jogadas if u > t + 0.9)
        q.sombra(FOGUEIRA[min(n, 7) - 1], fogueira)
        tam = FOGO[min(n - 1, 5)]
        q.chama(tam[int(u * 8) % 4], fogueira, cintila=(0.85, 0.15, 9))
        # o homem joga as toras (braço sobe antes de cada arremesso)
        ergue = max([q.env(t - 0.5, 0.4, t + 0.1, 0.4) for t in jogadas] + [0])
        q.boneco(HOMEM, 560, CHAO, {'uarmF': -20 - 110 * ergue, 'farmF': -30 + 10 * ergue, 'uarmB': 6, 'farmB': -12,
                                    'head': 6, 'torso': 4 - 6 * ergue}, fogueira)
        for t in jogadas:
            pos = _arremesso(q, t)
            if pos:
                q.sombra(TORA, fogueira, dx=pos[0] - A[0], dy=pos[1] - A[1])
        q.sombra(NOME, fogueira, q.env(c.seneca - 0.2, 0.8, c.feed, 1.0))
        for k, linha in enumerate(CITACAO):
            q.sombra(linha, fogueira, q.env(c.nurse - 0.2 + 0.25 * k, 0.8, c.trap - 0.6, 0.8))
        q.credito(CRED_SEN, q.env(c.nurse - 0.2, 0.8, c.trap - 0.4, 0.8))

    # ---- 2. Marco: a lista de regras ----
    if tabua > 0.002:
        k = int(round(9 * q.ss(c.list - 0.2, max(c.consider - c.list, 0.5))))
        q.sombra(TABUA[k], tabua)
        q.foco(q.ss(c.consider, 1.0) * tabua, 1150, 545, 170)                 # a regra VIII
        q.credito(CRED_MED, q.env(c.consider - 0.2, 0.8, c.once - 0.4, 0.8))

    # ---- 3. aconteceu uma vez; acontece todo dia; o insulto e os anos ----
    if ciclo > 0.002:
        curva = q.ss(c.what, 1.5)
        q.boneco(HOMEM, 760, CHAO, {'uarmF': 4, 'farmF': -10, 'uarmB': -4, 'farmB': -8, 'head': 8 + 10 * curva, 'torso': 3 + 5 * curva}, ciclo)
        q.sombra(CHEFE, ciclo, q.env(c.insult, 0.3, c.insult + 1.2, 0.4))
        neve = q.env(c.grudge, 1.0, c.proverbs, 0.8)
        if neve > 0:
            flocos, pesos = [], []
            for i in range(40):
                p = ((u - c.grudge) * 0.12 + i * 0.137) % 1.0
                flocos.append(((i * 263) % 1500 + 200 + 30 * math.sin(u + i), -40 + 900 * p))
                pesos.append(math.sin(math.pi * p))
            q.multidao(FLOCO, flocos, ciclo, neve, pesos=pesos)

    # ---- 4 e 5. a pedra, a academia, o jantar e a cama ----
    if pedra > 0.002:
        q.sombra(ROLO, pedra, q.env(c.proverbs - 0.2, 0.8, c.words2, 1.0))
        q.credito(CRED_PROV, q.env(c.stone - 0.2, 0.8, c.words2 + 0.4, 0.8))
        academia = q.env(c.gym - 0.2, 0.6, c.unlike, 0.6)
        nas_costas = q.ss(c.fool, 0.8) * (1 - academia)
        cama = q.ss(c.bed - 0.3, 1.0)
        curva = nas_costas * (1 + 0.5 * q.ss(c.stronger, 1.2))
        x = lerp(700, 760, q.ss(c.home, 1.0))
        if cama < 0.98:
            if academia > 0.01:                                               # os halteres sobem e descem fácil
                sobe = 0.5 + 0.5 * math.sin(u * 4.0)
                pose = {'uarmF': -150 * sobe - 10, 'farmF': -10, 'uarmB': -140 * sobe - 10, 'farmB': -10, 'head': -6, 'torso': 1}
                q.boneco(HOMEM, x, CHAO, pose, pedra, 1 - cama)
                hx, hy = _ponto(x, CHAO, pose, 'farmF', (8, 86))
                q.sombra(HALTERES, academia, dx=hx - A[0], dy=hy - A[1])
            else:
                pose = {'uarmF': 20 * curva, 'farmF': -20 - 20 * curva, 'uarmB': 10, 'farmB': -12,
                        'head': 10 + 16 * curva, 'torso': 4 + 22 * curva}
                q.boneco(HOMEM, x, CHAO + 22 * curva, pose, pedra, 1 - cama)
            desce = q.ss(c.stone - 0.3, 1.0)
            if academia > 0.01:                                               # na academia a pedra fica no chão
                q.sombra(PEDRA, pedra, academia, dx=x + 300 - A[0], dy=objetos.CHAO2 - 90 - A[1])
            if nas_costas > 0.01:                                             # a pedra apoiada nas costas
                px, py = _ponto(x, CHAO + 22 * curva, {'torso': 4 + 22 * curva}, 'torso', (-80, -130))
                q.sombra(PEDRA_COSTAS, pedra, 1 - cama, nas_costas, dx=px - A[0], dy=py - A[1])
            elif academia <= 0.01:
                q.sombra(PEDRA, pedra, 1 - cama, desce, dx=760 - A[0], dy=lerp(-160, 300, desce) - A[1])
        q.sombra(MESA, pedra, q.env(c.dinner - 0.2, 0.7, c.bed, 0.8))
        if cama > 0.002:
            q.sombra(CAMA, cama)
            q.sombra(DEITADO, cama)
            q.sombra(PEDRA, cama, dx=1000 - A[0], dy=objetos.CHAO2 - 250 - A[1])            # a pedra no peito, na cama

    q.sombra(BASE_LENHA)
    q.sombra(LATERAIS)

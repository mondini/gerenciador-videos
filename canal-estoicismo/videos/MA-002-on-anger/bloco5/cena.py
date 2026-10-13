"""Vídeo 2 · Bloco 5 — Provérbio-ponte. Script de cena (moldura "oliveira").

  1. "Marcus took cities. He won wars": a cidade murada em primeiro plano e uma fileira de legionários diante dela.
     "a box of letters he never opened": a capsa fechada, pequena, sob um foco de luz.
  2. Provérbios (rolo pequeno no canto): "slow to anger... than he who takes a city": a citação em Cormorant.
     "Ruling your own spirit... you do alone. Every day. And usually at night": a cidade e os soldados se apagam;
     fica o homem sozinho; a noite cai, com a lua minguante.
  3. "Without wood... a fire goes out": uma fogueira pequena. "A grudge is a fire": a cada "every time..." o homem
     joga uma tora e o fogo sobe; "You only have to stop feeding it": ele segura a última tora e a pousa no chão.
  4. "It won't go out tonight... Slowly... it turns to ash": o fogo vai baixando até sobrar brasa e cinza.
"""
from marbleash.cena import *

PANO = 'pesado'
STILLS = (2.0, 8.0, 16.0, 26.0, 34.0, 42.0, 50.0, 58.0, 66.0, 72.0)

CHAO = BASE - 172 * 1.35
A = (500, 400)

# ================= ELENCO =================
LONGE = Camada(cenario.cidade, desfoque=9, opacidade=0.30, semente=11, pivo=(760, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.vinhedo, desfoque=6, opacidade=0.42, semente=12, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais_oliveira, desfoque=4.5, opacidade=0.86, semente=13, pivo=(200, 1080), balanco=(3.0, 0.45))
BASE_LENHA = Camada(cenario.base_lenha, desfoque=3.5, opacidade=0.88, semente=14, pivo=(400, 1080), balanco=(1.6, 0.2))

CIDADE = Camada(objetos.cidade_sitiada, 1250, desfoque=2.4, opacidade=0.86, semente=80, pivo=(1250, BASE), balanco=(1.4, 0.15))
SOLDADO = Camada(objetos.soldado, desfoque=2.6, opacidade=0.82, posicao=(200, 400))
CAPSA = Camada(objetos.capsa, 560, 0.0, 0, desfoque=1.8, opacidade=0.88, semente=81, pivo=(560, BASE), balanco=(1.2, 0.15))
ROLO = Camada(objetos.rolo_icone, 1250, 120, desfoque=1.4, opacidade=0.8, semente=82, pivo=(1250, 120), balanco=(1.0, 0.2))
FOGUEIRA = [Camada(objetos.fogueira_toras, n, 1150, desfoque=2.0, opacidade=0.86, semente=83, pivo=(1150, BASE), balanco=(1.2, 0.1))
            for n in range(1, 8)]
FOGO = [[Chama(objetos.labareda, k, tam, 1150, brilho=30 + 10 * tam, cor=(0.7, 0.42, 0.12), forca=1.4) for k in range(4)]
        for tam in (0.15, 0.3, 0.5, 0.75, 1.0, 1.3, 1.6)]
TORA = Camada(objetos.tora, desfoque=1.4, opacidade=0.88, posicao=A)
CINZA = [Camada(objetos.cinza, k, desfoque=1.2, opacidade=0.55, posicao=A) for k in range(6)]
HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)


def _texto(texto, y):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', 44, 960, y, desfoque=1.4, opacidade=0.8,
                  semente=84, pivo=(960, 170), balanco=(1.2, 0.15))


CITACAO = [_texto('One who is slow to anger is better than the mighty;', 200), _texto('one who rules his spirit, than he who takes a city.', 256)]
CRED_1632 = Credito('Proverbs 16:32 · World English Bible')
CRED_2620 = Credito('Proverbs 26:20 · World English Bible')


def _ponto(x, y, pose, peca, local):
    (px, py), ang = bonecos.homem().pose(x, y, pose, 1.35)[peca]
    r = math.radians(ang)
    lx, ly = local[0] * 1.35, local[1] * 1.35
    return px + lx * math.cos(r) - ly * math.sin(r), py + lx * math.sin(r) + ly * math.cos(r)


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    cidade = 1 - q.ss(c.alone - 0.3, 1.4)
    noite = q.ss(c.every - 0.4, 1.6)
    fogo_cena = q.ss(c.another - 0.4, 1.0)
    q.luz((1 - 0.45 * noite) * (1 - 0.15 * q.ss(c.slowly, 2.0)) * tremor(u))
    q.lua(noite, cx=1500, cy=160, raio=50, crescente=-0.5)

    q.sombra(LONGE)
    q.sombra(MEIO)

    # ---- 1. a cidade tomada e a capsa que ele não abriu ----
    if cidade > 0.002:
        q.sombra(CIDADE, cidade)
        tropa = q.ss(c.won - 0.2, 1.4)
        q.multidao(SOLDADO, [(760 + i * 110 - 200, objetos.CHAO2 + 16 - 400 + 3 * math.sin(u * 1.1 + i)) for i in range(4)], cidade, tropa)
        q.sombra(CAPSA, cidade, q.env(c.victory - 0.2, 0.8, c.proverbs + 1.0, 1.0))
        q.foco(q.env(c.victory, 0.9, c.proverbs + 0.6, 0.9), 560, 640, 240)
        q.sombra(ROLO, q.env(c.proverbs - 0.2, 0.8, c.another, 1.0))
        for k, linha in enumerate(CITACAO):
            q.sombra(linha, q.env(c.slow - 0.2 + 0.5 * k, 0.8, c.alone, 0.9))
        q.credito(CRED_1632, q.env(c.slow - 0.2, 0.8, c.alone, 0.8))

    # ---- 2. sozinho, à noite ----
    if fogo_cena < 0.998:
        sozinho = q.ss(c.army, 1.2) * (1 - fogo_cena)
        q.boneco(HOMEM, 620, CHAO, {'uarmF': 4, 'farmF': -10, 'uarmB': -4, 'farmB': -8, 'head': 6 + 6 * noite, 'torso': 3}, sozinho)

    # ---- 3 e 4. a fogueira do rancor ----
    if fogo_cena > 0.002:
        jogadas = [c.replay, c.story, c.rehearse]
        n = 1 + sum(1 for t in jogadas if u > t + 0.9)
        apaga = q.ss(c.tonight, c.fim - c.tonight)
        nivel = max(0, min(6, n + 1 - int(round(6 * apaga))))
        q.sombra(FOGUEIRA[n], fogo_cena)
        q.chama(FOGO[nivel][int(u * 8) % 4], fogo_cena, 1 - 0.5 * apaga, cintila=(0.85, 0.15, 9))
        q.credito(CRED_2620, q.env(c.wood - 0.2, 0.8, c.fire, 0.8))
        ergue = max([q.env(t - 0.5, 0.4, t + 0.1, 0.4) for t in jogadas] + [0])
        segura = q.env(c.feeding - 0.6, 0.8, c.tonight + 1.0, 1.0)               # segura a última tora... e a pousa
        pose = {'uarmF': -20 - 110 * ergue - 50 * segura, 'farmF': -30 + 10 * ergue - 30 * segura, 'uarmB': 6, 'farmB': -12,
                'head': 6 + 8 * segura, 'torso': 4 - 6 * ergue}
        q.boneco(HOMEM, 620, CHAO, pose, fogo_cena)
        for t in jogadas:                                                        # toras jogadas em arco
            p = q.lin(t, 0.9)
            if 0 < p < 1:
                x, y = lerp(700, 1150, p), lerp(520, 820, p) - 220 * math.sin(math.pi * p)
                q.sombra(TORA, fogo_cena, dx=x - A[0], dy=y - A[1])
        if segura > 0.01:
            mx, my = _ponto(620, CHAO, pose, 'farmF', (8, 86))
            q.sombra(TORA, fogo_cena, segura, dx=mx + 40 - A[0], dy=my - A[1])
        pousada = q.ss(c.tonight + 0.8, 1.0)
        q.sombra(TORA, fogo_cena, pousada, dx=760 - A[0], dy=objetos.CHAO2 - 70 - A[1])
        cinza = q.ss(c.nowood, 2.0)
        if cinza > 0.01:
            pts, pesos = [], []
            for i in range(12):
                p = ((u - c.nowood) * 0.18 + i * 0.083) % 1.0
                pts.append((1150 - A[0] + 70 * math.sin(i * 1.3 + u * 0.6), objetos.CHAO2 - 90 - 420 * p - A[1]))
                pesos.append(math.sin(math.pi * p))
            for k in range(6):
                q.multidao(CINZA[k], pts[k::6], fogo_cena, cinza, pesos=pesos[k::6])

    q.sombra(BASE_LENHA)
    q.sombra(LATERAIS)

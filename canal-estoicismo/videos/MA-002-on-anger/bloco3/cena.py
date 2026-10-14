"""Vídeo 2 · Bloco 3 — A pessoa que sempre quer mais. Script de cena (moldura "oliveira").

  1. A reunião: mesa comprida, dois ouvintes; o chefe ergue o rolo (o trabalho do homem) e eles aplaudem;
     "never once says your name": o homem, de lado, baixa a cabeça.
  2. "The relative... The friend...": a mãe de dedo em riste e uma mão estendida pela direita; "they want more":
     duas mãos avançam dos dois lados.
  3. Marco: o imperador cercado, ao fundo, pelas mesmas figuras; a pergunta aparece em Cormorant.
     "angry at winter for being cold": neve, e o homem de punho erguido para o céu (leve humor). "some peace":
     a neve para e a luz esquenta.
  4. "Anger is a signal... a line was crossed": a linha âmbar no chão; o chefe passa por cima dela.
     "So act. Say no.": o homem ergue a palma; "Draw the line... out loud": a linha brilha mais.
  5. Provérbios (rolo pequeno no canto): o homem fala baixo (ondas suaves) e a pedra teimosa vai sendo empurrada.
  6. "A grudge becomes nothing. It just sits there... every night": noite, a cama, e o rancor sentado à beira dela.
"""
from marbleash.cena import *

PANO = 'pesado'
STILLS = (4.0, 10.0, 16.0, 26.0, 36.0, 46.0, 56.0, 66.0, 76.0, 86.0, 94.0, 100.0)

CHAO = BASE - 172 * 1.35
CHAO_IMP = BASE - 172 * 1.3
TINTA = (60, 34, 16, 255)
A = (500, 400)                                                # âncora das peças de centro (0, 0)

# ================= ELENCO =================
LONGE = Camada(cenario.cidade, desfoque=9, opacidade=0.30, semente=11, pivo=(760, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.vinhedo, desfoque=6, opacidade=0.42, semente=12, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais_oliveira, desfoque=4.5, opacidade=0.86, semente=13, pivo=(200, 1080), balanco=(3.0, 0.45))
BASE_LENHA = Camada(cenario.base_lenha, desfoque=3.5, opacidade=0.88, semente=14, pivo=(400, 1080), balanco=(1.6, 0.2))

MESA = Camada(objetos.mesa_reuniao, 980, desfoque=2.2, opacidade=0.84, semente=40, pivo=(980, BASE), balanco=(1.4, 0.15))
OUVINTES = {(x, k): Camada(objetos.ouvinte, x, k / 4, desfoque=1.6, opacidade=0.86, semente=41 + i, pivo=(x, BASE), balanco=(1.2, 0.15))
            for i, x in enumerate((700, 900)) for k in range(5)}
CHEFE = [Camada(objetos.figura_chefe, 1330, 1.9, k / 6, desfoque=1.4, opacidade=0.88, semente=43, pivo=(1330, BASE), balanco=(1.6, 0.2))
         for k in range(7)]
CHEFE_LINHA = Camada(objetos.figura_chefe, 1330, desfoque=1.4, opacidade=0.88, semente=43, pivo=(1330, BASE), balanco=(1.6, 0.2))
MAE = Camada(objetos.figura_mulher, 1250, 1.9, 1.0, desfoque=1.4, opacidade=0.86, semente=44, pivo=(1250, BASE), balanco=(1.6, 0.2))
MAO_D = Camada(objetos.mao_estendida, 1640, 720, -140.0, desfoque=1.8, opacidade=0.86, semente=45, pivo=(1700, 900), balanco=(2.0, 0.4))
MAO_E = Camada(objetos.mao_estendida, 280, 760, -40.0, desfoque=1.8, opacidade=0.86, semente=46, pivo=(200, 900), balanco=(2.0, 0.4))
LINHA = [Chama(objetos.linha_chao, k / 10, 1000, brilho=18, cor=(0.7, 0.42, 0.12), forca=1.2) for k in range(11)]
ONDA = [Camada(objetos.onda_voz, k, 870, 470, desfoque=1.4, opacidade=0.7) for k in range(8)]
PEDRA = Camada(objetos.pedra_grande, 1.4, desfoque=1.4, opacidade=0.9, posicao=A)
FLOCO = Camada(objetos.floco, desfoque=1.0, opacidade=0.95, posicao=(-100, -100), dobra=False)
ROLO = Camada(objetos.rolo_icone, 1250, 120, desfoque=1.4, opacidade=0.8, semente=47, pivo=(1250, 120), balanco=(1.0, 0.2))
CAMA = Camada(objetos.cama, 1000, desfoque=2.2, opacidade=0.84, semente=48, pivo=(1000, BASE), balanco=(1.6, 0.2))
DEITADO = Camada(objetos.homem_deitado, 1000, desfoque=1.4, opacidade=0.9, semente=48, pivo=(1000, BASE), balanco=(1.6, 0.2))
VULTO = Camada(objetos.vulto_sentado, 1290, desfoque=2.0, opacidade=0.85, semente=49, pivo=(1290, BASE), balanco=(1.2, 0.15))


def _texto(texto, y):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', 46, 960, y, desfoque=1.4, opacidade=0.8,
                  semente=50, pivo=(960, 170), balanco=(1.2, 0.15))


PERGUNTA = [_texto('could the world exist', 130), _texto('without people like this?', 190)]

HOMEM = Boneco(bonecos.homem, escala=1.35, desfoque=1.1, opacidade=0.9)
AMIGO = Boneco(bonecos.homem, escala=1.3, desfoque=1.5, opacidade=0.8)
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)

CRED_942 = Credito('Marcus Aurelius, Meditations 9.42 · paraphrased')
CRED_847 = Credito('Marcus Aurelius, Meditations 8.47 · trans. George Long')
CRED_PROV = Credito('Proverbs 25:15 · World English Bible')


# ================= LINHA DO TEMPO =================
def quadro(q, c):
    u = q.u
    reuniao = 1 - q.ss(c.relative - 0.3, 0.9)
    pedidos = q.env(c.relative - 0.3, 0.9, c.marcus - 0.3, 0.9)
    marco = q.env(c.marcus - 0.3, 0.9, c.expecting - 0.3, 0.9)
    inverno = q.env(c.expecting - 0.3, 0.9, c.help - 0.3, 0.9)
    limite = q.env(c.help - 0.3, 0.9, c.proverbs - 0.3, 0.9)
    voz = q.env(c.proverbs - 0.3, 0.9, c.nothing - 0.3, 0.9)
    noite = q.ss(c.nothing - 0.3, 1.2)

    frio = inverno * (1 - q.ss(c.peace, 1.5))
    q.luz((1 - 0.25 * frio) * (1 + 0.12 * q.env(c.peace, 1.2, c.help, 1.0)) * (1 - 0.5 * noite) * tremor(u))
    q.lua(noite, cx=1500, cy=160, raio=50, crescente=-0.5)

    q.sombra(LONGE)
    q.sombra(MEIO)

    # ---- 1. a reunião ----
    if reuniao > 0.002:
        q.sombra(MESA, reuniao)
        palmas = q.env(c.boss + 1.2, 0.5, c.name + 0.6, 0.6)
        bate = int(round(4 * palmas * (0.5 + 0.5 * math.sin(u * 14))))
        for x in (700, 900):
            q.sombra(OUVINTES[(x, bate)], reuniao)
        ergue = q.ss(c.boss + 0.3, 1.0)
        q.sombra(CHEFE[int(round(6 * ergue))], reuniao)
        baixa = q.ss(c.name, 1.2)
        q.boneco(HOMEM, 330, CHAO, {'uarmF': 4, 'farmF': -10, 'uarmB': -4, 'farmB': -8, 'head': -4 + 22 * baixa, 'torso': 2 + 6 * baixa},
                 reuniao)

    # ---- 2. o parente, o amigo, as mãos ----
    if pedidos > 0.002:
        q.boneco(HOMEM, 620, CHAO, {'uarmF': 4, 'farmF': -10, 'head': 6, 'torso': 3}, pedidos)
        q.sombra(MAE, pedidos, q.env(c.relative - 0.2, 0.7, c.give, 0.8))
        amigo = q.env(c.friend - 0.2, 0.8, c.give + 0.4, 0.8)
        q.boneco(AMIGO, 1480, BASE - 172 * 1.3, {'uarmF': -70, 'farmF': -20, 'head': 4}, pedidos, amigo, espelho=True)

    # ---- 3. Marco, a pergunta ----
    if marco > 0.002:
        q.boneco(IMPERADOR, 560, CHAO_IMP, {'uarmF': 4, 'farmF': -14, 'uarmB': -6, 'farmB': -10, 'head': 4,
                                            'torso': 1.5 * math.sin(u * 0.8)}, marco)
        for k, linha in enumerate(PERGUNTA):
            q.sombra(linha, marco, q.ss(c.offends + 0.6 * k, 0.9))
        q.credito(CRED_942, q.env(c.offends - 0.2, 0.8, c.expecting - 0.4, 0.8))

    # ---- 3b. o inverno ----
    if inverno > 0.002:
        punho = q.env(c.winter, 0.5, c.right, 1.0)
        sacode = punho * math.sin(u * 10) * 8
        q.boneco(HOMEM, 820, CHAO, {'uarmF': -150 * punho - 4 + sacode, 'farmF': -30 * punho - 10, 'uarmB': -4, 'farmB': -8,
                                    'head': -14 * punho + 6 * (1 - punho), 'torso': 2}, inverno)
        if frio > 0.01:
            flocos, pesos = [], []
            for i in range(50):
                p = ((u - c.expecting) * 0.14 + i * 0.113) % 1.0
                flocos.append(((i * 271) % 1500 + 200 + 30 * math.sin(u + i), -40 + 900 * p))
                pesos.append(math.sin(math.pi * p))
            q.multidao(FLOCO, flocos, frio, pesos=pesos)

    # ---- 4. a linha ----
    if limite > 0.002:
        brilho = q.ss(c.crossed, 0.8) * (0.7 + 0.3 * q.ss(c.line, 0.8))
        q.chama(LINHA[int(round(10 * q.ss(c.crossed - 0.2, 1.0)))], limite, brilho, cintila=(0.95, 0.05, 3))
        passa = q.ss(c.crossed + 0.4, 1.6) * (1 - q.ss(c.soact, 1.0))       # o chefe pisa além da linha e recua
        q.sombra(CHEFE_LINHA, limite, dx=-260 * passa)
        palma = q.ss(c.no - 0.2, 0.6)
        q.boneco(HOMEM, 640, CHAO, {'uarmF': -80 * palma, 'farmF': -60 * palma - 10, 'uarmB': -4, 'farmB': -8,
                                    'head': 2, 'torso': 2 - 2 * palma}, limite)
        q.credito(CRED_847, q.env(c.act - 0.2, 0.8, c.soact + 0.6, 0.8))

    # ---- 5. a voz calma move a pedra teimosa ----
    if voz > 0.002:
        q.sombra(ROLO, voz, q.env(c.proverbs - 0.2, 0.8, c.difference, 1.0))
        q.credito(CRED_PROV, q.env(c.patience - 0.2, 0.8, c.calm + 0.4, 0.8))
        falando = q.env(c.patience, 0.4, c.difference, 0.6)
        q.boneco(HOMEM, 760, CHAO, {'uarmF': 10, 'farmF': -20, 'head': 4, 'torso': 2}, voz)
        if falando > 0.01:
            q.sombra(ONDA[int(u * 6) % 8], voz, falando)
        empurra = q.ss(c.tongue, c.difference - c.tongue)
        q.sombra(PEDRA, voz, dx=1180 + 220 * empurra - A[0], dy=objetos.CHAO2 - 90 - A[1])
        q.chama(LINHA[10], voz, q.env(c.boundary - 0.2, 0.6, c.nothing, 0.8), cintila=(0.95, 0.05, 3))

    # ---- 6. o rancor espera à beira da cama ----
    if noite > 0.002:
        q.sombra(CAMA, noite)
        q.sombra(DEITADO, noite)
        q.sombra(VULTO, noite, q.ss(c.sits - 0.2, 1.4))

    q.sombra(BASE_LENHA)
    q.sombra(LATERAIS)
    if pedidos > 0.002:                                                       # as mãos vêm de fora, na frente da moldura
        mais = q.ss(c.more - 0.2, 1.0)
        q.sombra(MAO_D, pedidos, q.env(c.friend + 0.6, 0.6, c.marcus - 0.4, 0.6), dx=160 * (1 - q.ss(c.friend + 0.6, 0.8)) - 110 * mais)
        q.sombra(MAO_E, pedidos, q.env(c.give - 0.2, 0.6, c.marcus - 0.4, 0.6), dx=-160 * (1 - q.ss(c.give, 0.8)) + 110 * mais)

"""Vídeo 1 · Bloco 3 — O diário. Script de cena (padrão Teatro de Sombras Projetadas).

Grupos de cenas guiados pela narração:
  1. A tenda: o imperador escreve à noite sob a lucerna (continua o fim do bloco 2).
  2. Latim riscado -> ΦΙΛΟΣΟΦΙΑ; três bustos de mestres sobem.
  3. O título: ΤΑ ΕΙΣ ΕΑΥΤΟΝ e, embaixo, "To Himself".
  4. Sem plateia: o anfiteatro vazio vai apagando; o imperador cansado no centro, no foco.
  5. A mesma linha escrita seis vezes; as mais antigas se apagam ("what you keep forgetting").
  6. Não era perfeito: o busto sobe inteiro e racha, com a fresta em âmbar ("a man fighting").
  7. A manhã: sol nascendo atrás do imperador; Meditações 2.1 na tela; seis pessoas difíceis aparecem,
     uma por palavra, e atravessam o caminho dele; ele fica parado, no foco ("steal his peace").
  8. A noite: de volta à tenda, lua; Meditações 6.30 na tela.
  9. A coroa: CAESAR no alto; a coroa de louros em âmbar em volta da cabeça; o homem some e a coroa fica.
 10. O manto: o imperador grande; a púrpura imperial (suave, translúcida) tinge o manto de cima para baixo;
     o homem some e só o manto fica. Única exceção ao âmbar no vídeo, aprovada pelo criador em 12/10/2026.
"""
from PIL import ImageFont

from marbleash import config
from marbleash.cena import *

STILLS = (2.0, 7.9, 11.8, 18.6, 25.2, 40.6, 47.6, 63.4, 69.0, 89.0, 98.4, 107.6)   # um still por grupo (+ a travessia)

TINTA = (60, 34, 16, 255)
AMBAR = (0.91, 0.64, 0.24)                                    # amber-500
CHAO = BASE - 172 * 1.3                                       # pivô do torso de um boneco de pé (escala 1.3)


def _largura(texto, fonte, tamanho, tracking=0.0):
    f = ImageFont.truetype(config.fonte(fonte), tamanho)
    return f.getlength(texto) + tracking * tamanho * (len(texto) - 1)


# ================= ELENCO =================
LONGE = Camada(cenario.longe, desfoque=9, opacidade=0.30, semente=1, pivo=(1200, 700), balanco=(1.2, 0.08))
MEIO = Camada(cenario.meio, desfoque=6, opacidade=0.42, semente=2, pivo=(700, 800), balanco=(1.6, 0.12))
LATERAIS = Camada(cenario.laterais, desfoque=4.5, opacidade=0.86, semente=3, pivo=(200, 1080), balanco=(3.0, 0.45))
PENHASCO = Camada(objetos.penhasco, desfoque=3.0, opacidade=0.86, semente=10, pivo=(900, BASE), balanco=(2.0, 0.2))
CHAMA_NOITE = Chama(objetos.chama_noite, 1, brilho=26, cor=(0.7, 0.42, 0.12), forca=1.5)
IMPERADOR = Boneco(bonecos.imperador, escala=1.3, desfoque=1.1, opacidade=0.9)
HOMEM = Boneco(bonecos.homem, escala=1.2, desfoque=1.1, opacidade=0.88)

# 2. latim riscado -> grego; os mestres
LATIM_TXT = 'LINGVA LATINA'
LATIM = Camada(objetos.letreiro, LATIM_TXT, 'Cinzel-SemiBold.ttf', 84, 960, 300, TINTA, 0.04,
               desfoque=1.2, opacidade=0.85, semente=13, pivo=(960, 360), balanco=(1.2, 0.1))
_L = _largura(LATIM_TXT, 'Cinzel-SemiBold.ttf', 84, 0.04) / 2 + 30
RISCO = [Camada(objetos.risco, k / 12, 960 - _L, 960 + _L, 352, desfoque=1.2, opacidade=0.9, semente=13, pivo=(960, 360), balanco=(1.2, 0.1))
         for k in range(13)]
FILO = Camada(objetos.letreiro, 'ΦΙΛΟΣΟΦΙΑ', 'GFSBaskerville.otf', 96, 960, 170, TINTA, 0.08,
              desfoque=1.2, opacidade=0.85, semente=14, pivo=(960, 230), balanco=(1.2, 0.1))
MESTRES = [Camada(objetos.busto, x, False, s, desfoque=1.6, opacidade=0.86, semente=20 + i, pivo=(x, BASE), balanco=(1.5, 0.2))
           for i, (x, s) in enumerate(((700, 20), (960, 21), (1220, 23)))]

# 3. o título
TITULO_GR = Camada(objetos.letreiro, 'ΤΑ ΕΙΣ ΕΑΥΤΟΝ', 'GFSBaskerville.otf', 104, 960, 330, TINTA, 0.08,
                   desfoque=1.2, opacidade=0.85, semente=15, pivo=(960, 420), balanco=(1.2, 0.1))
TITULO_EN = Camada(objetos.letreiro, 'To Himself', 'CormorantGaramond-MediumItalic.ttf', 64, 960, 490,
                   desfoque=1.4, opacidade=0.8, semente=15, pivo=(960, 420), balanco=(1.2, 0.1))

# 4. o anfiteatro vazio (longe: mais claro e borrado que o imperador na frente)
ANFITEATRO = Camada(objetos.anfiteatro, desfoque=3.6, opacidade=0.55, semente=16, pivo=(960, BASE), balanco=(1.2, 0.08))

# 5. a mesma linha, seis vezes
LINHAS = [Camada(objetos.linha_escrita, j, desfoque=1.2, opacidade=0.82, semente=30 + j, pivo=(960, 250 + 78 * j), balanco=(1.0, 0.1))
          for j in range(6)]

# 6. o busto que racha
BUSTO = [Camada(objetos.busto, 960, False, 3, k / 10, desfoque=1.6, opacidade=0.88, semente=40, pivo=(960, BASE), balanco=(1.5, 0.15))
         for k in range(11)]
BRASA = [Chama(objetos.busto_brasa, k / 10, brilho=10, forca=0.6, gelatina=AMBAR, desfoque=1.6) for k in range(11)]

# 7. a manhã: Meditações 2.1 e as pessoas difíceis
def _citacao(texto, y, cx=1000):
    return Camada(objetos.letreiro, texto, 'CormorantGaramond-MediumItalic.ttf', 42, cx, y,
                  desfoque=1.4, opacidade=0.8, semente=17, pivo=(cx, 170), balanco=(1.2, 0.15))


Q21 = [_citacao('Begin the morning by saying to thyself,', 105),
       _citacao('I shall meet with the busy-body, the ungrateful,', 165),
       _citacao('arrogant, deceitful, envious, unsocial.', 225)]
CRED_21 = Credito('Marcus Aurelius, Meditations 2.1 · trans. George Long')
PESSOAS_X = (300, 480, 660, 840, 1020, 1200)
POSES = (                                                     # uma postura por tipo de pessoa
    {'torso': 6, 'head': -6, 'uarmF': -80, 'farmF': -10, 'uarmB': 10, 'farmB': -10},       # intrometido: aponta
    {'torso': -2, 'head': -14, 'uarmF': 20, 'farmF': -70, 'uarmB': 24, 'farmB': -60},      # ingrato: queixo alto
    {'torso': -6, 'head': -20, 'uarmF': 30, 'farmF': -90, 'uarmB': 30, 'farmB': -90},      # arrogante: mãos na cintura
    {'torso': 10, 'head': 14, 'uarmF': -40, 'farmF': -100, 'uarmB': -10, 'farmB': -20},    # falso: mão na boca
    {'torso': 8, 'head': -4, 'uarmF': -100, 'farmF': -20, 'uarmB': 6, 'farmB': -10},       # invejoso: estende a mão
    {'torso': 4, 'head': 24, 'uarmF': -14, 'farmF': -104, 'uarmB': -12, 'farmB': -96},     # antissocial: braços fechados
)

# 8. a noite: Meditações 6.30
Q630 = [_citacao('Take care that thou art not made into a Cæsar,', 105, 1070),     # a copa da noite é maior
        _citacao('that thou art not dyed with this dye;', 165, 1070),
        _citacao('for such things happen.', 225, 1070)]
CRED_630 = Credito('Marcus Aurelius, Meditations 6.30 · trans. George Long')

# 9. a coroa sem o homem (a coroa em volta da cabeça do imperador de pé em x = 960)
CAESAR = Camada(objetos.letreiro, 'CAESAR', 'Cinzel-SemiBold.ttf', 96, 960, 110, TINTA, 0.2,
                desfoque=1.2, opacidade=0.85, semente=18, pivo=(960, 160), balanco=(1.2, 0.1))
COROA = Camada(objetos.coroa_louros, 966, 400, 96, desfoque=1.3, opacidade=0.85, semente=19, pivo=(966, 400), balanco=(1.0, 0.1))
COROA_OURO = Chama(objetos.coroa_louros, 966, 400, 96, brilho=16, cor=(0.6, 0.38, 0.12), forca=0.6, gelatina=AMBAR, desfoque=1.3)

# 10. o manto que tinge
FIGURA = Camada(objetos.figura_toga, desfoque=1.4, opacidade=0.9, semente=50, pivo=(960, BASE), balanco=(1.0, 0.08))
PURPURA = (0.40, 0.20, 0.34)                                  # púrpura imperial, apagada (exceção pedida pelo criador)
MANTO = [Chama(objetos.toga_tinta, k / 24, brilho=8, cor=(0.30, 0.12, 0.26), forca=0.25, gelatina=PURPURA, desfoque=1.4) for k in range(25)]


# ================= LINHA DO TEMPO =================
def _escrevendo(q, alpha):
    """O imperador sentado à mesa de campanha, escrevendo sob a lucerna (mesma cena do bloco 2)."""
    u = q.u
    q.sombra(PENHASCO, alpha)
    osc = math.sin(u * 9)
    q.boneco(IMPERADOR, 990, BASE - 110, {'uarmF': -62 + 6 * osc, 'farmF': -58 + 10 * math.sin(u * 13), 'legF': -70, 'legB': -60,
                                          'uarmB': -20, 'farmB': -30, 'head': 10}, alpha)
    q.chama(CHAMA_NOITE, alpha, cintila=(0.85, 0.15, 13))


def quadro(q, c):
    u = q.u
    tenda = 1 - q.ss(c.latin - 0.5, 0.9)
    latim = q.env(c.latin - 0.3, 0.8, c.philo + 0.3, 1.0)
    grego = q.env(c.philo - 0.3, 0.8, c.title - 0.3, 1.0)
    titulo = q.env(c.title + 0.4, 1.4, c.noaudience - 0.6, 0.9)
    arena = q.env(c.noaudience - 0.5, 1.0, c.honest - 0.6, 1.0)
    linhas = q.env(c.honest - 0.4, 0.8, c.perfect - 0.6, 1.0)
    busto = q.env(c.perfect - 0.5, 1.0, c.mornings - 0.6, 1.0)
    manha = q.env(c.mornings - 0.6, 1.2, c.nights - 0.6, 1.0)
    noite = q.env(c.nights - 0.6, 1.2, c.simple - 0.5, 1.0)
    coroa = q.env(c.simple - 0.5, 1.0, c.dyed - 0.5, 1.0)
    manto = q.ss(c.dyed - 0.5, 1.2)
    escuro = max(tenda, noite)
    vazio = arena * (0.12 * q.ss(c.noapplause, 0.8) + 0.12 * q.ss(c.noone, 0.8))
    q.luz((1 - 0.5 * escuro) * (1 - 0.25 * manha * (1 - q.ss(c.mornings, 3.0))) * (1 - vazio) * tremor(u))
    q.lua(escuro, cx=1610, cy=150, raio=50, crescente=0.45)
    q.lua(manha * q.ss(c.mornings - 0.3, 2.0), cx=1560, cy=380 - 60 * q.ss(c.mornings, 8.0), raio=78, brilho=0.8)

    # ---- fundo ----
    q.sombra(LONGE, max(0.7 * arena, manha, 0.7 * tenda, 0.7 * noite))
    q.sombra(MEIO, max(manha, 0.6 * arena))

    # ---- 1. a tenda (e 8. a noite) ----
    if tenda > 0.002:
        _escrevendo(q, tenda)
    if noite > 0.002:
        _escrevendo(q, noite)
        for i, linha in enumerate(Q630):
            q.sombra(linha, noite, q.ss((c.q630a, c.q630b, c.q630c)[i] - 0.2, 0.8))
        q.credito(CRED_630, q.env(c.q630a - 0.2, 0.8, c.simple - 0.6, 0.8))

    # ---- 2. latim riscado -> grego; os mestres ----
    if latim > 0.002:
        q.sombra(LATIM, latim)
        k = int(round(12 * q.ss(c.greek - 0.3, 0.7)))
        if k:
            q.sombra(RISCO[k], latim)
    if grego > 0.002:
        q.sombra(FILO, grego)
        for i, b in enumerate(MESTRES):
            p = q.ss(c.teachers - 0.3 + i * 0.35, 1.2)
            q.sombra(b, grego, min(1, p * 3), dy=380 * (1 - p))

    # ---- 3. o título ----
    if titulo > 0.002:
        q.sombra(TITULO_GR, titulo)
        q.sombra(TITULO_EN, titulo, q.ss(c.himself - 0.2, 1.0))

    # ---- 4. o anfiteatro vazio ----
    if arena > 0.002:
        q.sombra(ANFITEATRO, arena, 1 - 0.25 * q.ss(c.noapplause, 0.8) - 0.25 * q.ss(c.noone, 0.8))
        cansado = q.ss(c.tired - 0.3, 1.2)
        q.boneco(IMPERADOR, 960, CHAO, {'uarmF': 6, 'farmF': -8, 'uarmB': -4, 'farmB': -6, 'head': 6 + 12 * cansado, 'torso': 3 * cansado},
                 arena, cansado)
        q.foco(0.55 * arena * q.ss(c.reminding - 0.3, 1.2), 960, 620, 300)

    # ---- 5. a mesma linha, seis vezes ----
    if linhas > 0.002:
        inicios = (c.honest + 0.6, c.repeats, c.repeats + 1.0, c.warnings, c.warnings + 0.9, c.warnings + 1.8)
        for j, (camada, t0) in enumerate(zip(LINHAS, inicios)):
            esquece = 0.0 if j == 5 else 0.8 * q.ss(c.forget + 0.35 * j, 1.5)
            q.sombra(camada, linhas, q.ss(t0, 0.6), 1 - esquece)

    # ---- 6. o busto que racha ----
    if busto > 0.002:
        sobe = q.ss(c.perfect - 0.3, 1.4)
        k = int(round(10 * q.ss(c.fighting - 0.2, c.ruined - c.fighting + 0.6)))
        q.sombra(BUSTO[k], busto, min(1, sobe * 3), dy=380 * (1 - sobe))
        if k:
            q.chama(BRASA[k], busto, camada=BUSTO[k], dy=380 * (1 - sobe))
        q.foco(0.55 * busto * q.ss(c.perfect + 0.6, 1.2), 960, 680, 280)

    # ---- 7. a manhã: as pessoas difíceis ----
    if manha > 0.002:
        texto = q.env(c.q21a - 0.2, 0.8, c.inother - 0.3, 1.0)
        for i, linha in enumerate(Q21):
            q.sombra(linha, manha, texto, q.ss((c.q21a, c.q21b, c.deceitful)[i] - 0.2, 0.8))
        q.credito(CRED_21, texto)
        q.boneco(IMPERADOR, 1560, CHAO, {'uarmF': 4, 'farmF': -6, 'uarmB': -4, 'farmB': -6, 'head': 2}, manha, q.ss(c.prepared - 0.5, 1.2))
        entradas = (c.q21b + 1.0, c.ungrateful, c.arrogant, c.deceitful, c.envious, c.unsocial)
        for i, (x, pose, t0) in enumerate(zip(PESSOAS_X, POSES, entradas)):
            anda = q.ss(c.cross + 0.15 * (5 - i), 4.2)
            passo = 26 * math.sin(u * 7 + i) * min(1, anda * 8) * (1 - q.ss(c.notexpect, 0.6))
            p = dict(pose)
            p.update({'legF': passo, 'legB': -passo})
            q.boneco(HOMEM, x + 1100 * anda, BASE - 172 * 1.2, p, manha, q.ss(t0 - 0.2, 0.6))
        q.foco(0.6 * manha * q.ss(c.notexpect, 1.2), 1560, 560, 300)

    # ---- 9. a coroa sem o homem ----
    if coroa > 0.002:
        homem_some = q.ss(c.noman - 0.2, 1.6)
        q.sombra(CAESAR, coroa, q.ss(c.careful + 0.6, 1.0))
        q.boneco(IMPERADOR, 960, CHAO, {'uarmF': 4, 'farmF': -6, 'uarmB': -4, 'farmB': -6, 'head': -2}, coroa, 1 - homem_some)
        ouro = q.ss(c.crown - 0.2, 1.0)
        q.sombra(COROA, coroa, ouro)
        q.chama(COROA_OURO, coroa, ouro, camada=COROA)

    # ---- 10. o manto que tinge ----
    if manto > 0.002:
        some = q.ss(c.nothing + 0.6, 2.0)
        q.sombra(FIGURA, manto, 1 - some)
        k = int(round(24 * q.ss(c.dyed + 0.4, c.nothing - c.dyed + 0.4)))
        if k:
            q.chama(MANTO[k], manto, 0.6, camada=FIGURA)                  # tinta translúcida: as dobras aparecem

    # ---- laterais sempre presentes ----
    q.sombra(LATERAIS)

    # ---- câmera ----
    z_tenda = tenda * 0.16 * (1 - q.ss(0.0, 3.4))
    z_noite = q.env(c.wrote - 0.5, 1.5, c.q630a - 0.8, 1.0) * 0.16
    z_arena = q.env(c.reminding - 0.6, 3.0, c.honest - 0.8, 1.0) * 0.14
    z_busto = q.env(c.fighting - 0.5, 3.0, c.mornings - 0.8, 1.0) * 0.16
    z_paz = q.env(c.notexpect, 2.5, c.nights - 0.8, 1.0) * 0.12
    z_manto = manto * 0.10 * q.ss(c.dyed, 9.0)
    if z_tenda > 0:
        q.camera(1060, 640, 1 + z_tenda)
    elif z_noite > 0:
        q.camera(1060, 640, 1 + z_noite)
    elif z_arena > 0:
        q.camera(960, 600, 1 + z_arena)
    elif z_busto > 0:
        q.camera(960, 640, 1 + z_busto)
    elif z_paz > 0:
        q.camera(1500, 600, 1 + z_paz)
    elif z_manto > 0:
        q.camera(960, 520, 1 + z_manto)

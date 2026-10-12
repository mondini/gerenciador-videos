"""Encerramento padrão (8 s, sem narração) — igual em todos os vídeos.

Vem logo depois da última linha falada ("Old wisdom... for quiet hours.", ver docs/plano-canal.md). Mesmo
painel da abertura (logo Horizonte + "MARBLE & ASH" recortados, sol e "&" em âmbar), agora com o slogan
recortado embaixo, mais apagado. A lanterna acende devagar, o quadro fica parado (espaço para os elementos
da tela final do YouTube, que pedem de 5 a 20 s) e escurece no fim. Sem chamada para inscrição.
"""
from marbleash.cena import *

DURACAO = 8.0
FADE = (1.2, 1.1)             # escurece no último 1,2 s
STILLS = (0.6, 3.0, 7.5)

SLOGAN = 'Old wisdom for quiet hours.'
PAINEL = Camada(objetos.horizonte_painel, 960, 455, 1.6, 625, 64, 'MARBLE & ASH', 'Cinzel-SemiBold.ttf', 0.06, SLOGAN,
                desfoque=1.2, opacidade=0.93, semente=11, pivo=(960, 540), balanco=(1.5, 0.1))
AMBAR = (0.91, 0.64, 0.24)    # amber-500 #E8A33D
SOL = Chama(objetos.horizonte_sol, brilho=28, cor=(0.6, 0.38, 0.12), forca=0.9, gelatina=AMBAR, desfoque=1.2)
E = Chama(objetos.horizonte_e, brilho=14, cor=(0.6, 0.38, 0.12), forca=0.6, gelatina=AMBAR, desfoque=1.2)


def quadro(q, c):
    u = q.u
    q.luz((0.1 + 0.9 * q.ss(0.0, 1.6)) * tremor(u))              # a lanterna acende devagar
    q.sombra(PAINEL)
    q.chama(SOL, q.ss(0.6, 1.2), cintila=(0.97, 0.03, 5), camada=PAINEL)
    q.chama(E, q.ss(1.2, 1.0), camada=PAINEL)
    q.camera(960, 520, 1.035 - 0.035 * q.ss(0.0, DURACAO))          # afasta devagar (a abertura aproxima)

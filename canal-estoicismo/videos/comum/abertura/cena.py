"""Abertura padrão (3 s, sem narração; era 2 s até 12/10/2026) — igual em todos os vídeos.

Logo A — Horizonte + "MARBLE & ASH" (Design System; geometria em docs/identidade-visual.md), no padrão
de sombras: um painel de papel preto cobre o lençol com o logo e o nome RECORTADOS. A lanterna acende
atrás, a luz atravessa os recortes (mármore sobre carvão) e o sol e o "&" ganham gelatina âmbar — a
única brasa da tela. Leve aproximação da câmera; escurece no fim para entrar o bloco seguinte.
Som de transição (SOM, gerado em marbleash/sons.py): sobe no escurecimento do gancho e bate quando o sol acende.
"""
from marbleash.cena import *

DURACAO = 3.0
FADE = (0.5, 0.45)            # escurece nos últimos 0,5 s
STILLS = (0.4, 1.5, 2.4)
SOM = 'brasa'                 # som de transição (marbleash/sons.py), escolhido pelo criador em 12/10/2026
SOM_GOLPE = 0.4               # segundo da peça em que o golpe do som cai (o sol começa a acender)

PAINEL = Camada(objetos.horizonte_painel, desfoque=1.2, opacidade=0.93, semente=11, pivo=(960, 540), balanco=(1.5, 0.1))
AMBAR = (0.91, 0.64, 0.24)    # amber-500 #E8A33D
SOL = Chama(objetos.horizonte_sol, brilho=28, cor=(0.6, 0.38, 0.12), forca=0.9, gelatina=AMBAR, desfoque=1.2)
E = Chama(objetos.horizonte_e, brilho=14, cor=(0.6, 0.38, 0.12), forca=0.6, gelatina=AMBAR, desfoque=1.2)


def quadro(q, c):
    u = q.u
    q.luz((0.15 + 0.85 * q.ss(0.0, 0.9)) * tremor(u))          # a lanterna acende atrás do lençol
    q.sombra(PAINEL)
    q.chama(SOL, q.ss(0.4, 0.8), cintila=(0.97, 0.03, 7), camada=PAINEL)     # o sol âmbar
    q.chama(E, q.ss(1.0, 0.6), camada=PAINEL)                                   # o "&" âmbar
    q.camera(960, 520, 1 + 0.045 * q.ss(0.0, 3.0))                              # aproximação lenta

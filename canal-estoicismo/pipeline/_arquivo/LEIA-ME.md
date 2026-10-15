# Arquivo morto do pipeline (não usar)

Código da primeira versão, nascido de experimentos numa única conversa (11/10/2026). Foi substituído
pela biblioteca `pipeline/marbleash/` e pelos scripts de cena em `videos/video-NN/blocoN/`, que
reproduzem o bloco 1 aprovado **bit a bit** (stills e trechos conferidos pixel a pixel na refatoração).
Fica aqui só para consulta. Nada em `marbleash/` importa estes arquivos. (Os caminhos `videos/video-NN/` e
`videos/video-01/` citados abaixo são os nomes da época; hoje as pastas são `videos/MA-NNN-slug/`.)

| Arquivo | O que era | Para onde foi |
|---|---|---|
| `render2.py` | Estilo antigo de **traço fino** (horizonte, sol, logo antigo, arte do bloco 2), utilidades (easing, sprites) e tempos do vídeo 1 fixos no código (`C1o`/`C2o`). Lia `pace.json` no import. | Easing: `marbleash/anim.py`. Tempos: `videos/video-01/bloco1/tempos.txt`. O traço fino saiu do caminho principal. |
| `shadow.py` | Primeira versão das sombras: telas DAY/NIGHT/GLORY, moldura recortada, bonecos v1, kit de recorte, sprites romanos. | Kit: `marbleash/traco.py` e `bonecos.py`. Arco, portas, pedestal, soldado, moeda, penhasco, fumaça e chama da noite: `objetos.py`. O resto foi descartado. |
| `shadow_bg2.py` | Fundo v2 (linho sem moldura, pinheiro e coluna simples). | Descartado (substituído pela v5). |
| `shadow3.py` | Curvas Catmull-Rom (`cr`, `shape`, `stroke`, `spiral`), o homem refinado, lamparina e chama; domus, mesa e cenário v3. | Curvas: `traco.py`. Homem: `bonecos.homem()`. Lamparina e chama: `objetos.py`. Domus/mesa/cenário v3 descartados. |
| `shadow4.py` | Camadas de profundidade (fundo, meio), templo e mesa em três quartos, estrada. | `cenario.longe()`, `cenario.meio()`, `objetos.templo()`, `objetos.mesa()`. Estrada descartada. |
| `shadow5.py` | Vegetação detalhada (tufos, hera, folhas serrilhadas, flores), pinheiro, coluna com galho, capim; teste de foco e zoom. | Vegetação: `traco.py`. Pinheiro e coluna: `cenario.laterais()` (que repete o sorteio do capim, sem desenhá-lo, para manter o desenho aprovado). |
| `shadow6.py` | O lençol (dobras, luz, pano amontoado, grade sépia) e as **mãos dos manipuladores** (removidas a pedido). | `marbleash/lencol.py`. As mãos não foram levadas. |
| `shadowfilm.py` | Render do bloco 1 do vídeo 1 com tudo fixo no código (tempos, posições, cenas). Também construía mãos sem usar. | Compositor: `marbleash/quadro.py`. Cenas: `videos/video-01/bloco1/cena.py`. |
| `pace.py` | Desacelerava a narração e gravava `pace.json`. | `marbleash/audio.py` + `ma audio`. |
| `ambient.py` | Gerava o som ambiente (só graves: inaudível em notebook e celular). | `marbleash/audio.ambiente()`, com camadas audíveis acrescentadas em 12/10/2026. |
| `pace-previa-free.json` | Mapa de ritmo dos áudios de prévia (plano Free) dos blocos 1–4 do vídeo 1, no ritmo antigo (andamento 0,92). Estava em `videos/video-01/`. | `ma audio` reproduz esses mapas bit a bit (com o ritmo antigo) e grava `blocoN/audio.json`. |

Para rodar este código de novo (por exemplo, para refazer uma referência), ele precisa de uma pasta com
`fonts/` (cópia de `fontes-tipograficas/`), `pace.json` (ex.: `pipeline/_arquivo/pace-previa-free.json`)
e de um ajuste para a fonte Inter do Linux usada em `render2.py`. O roteiro usado na refatoração ficou
em `videos/video-01/trabalho/antigo/rodar_antigo.py` (pasta fora do git).

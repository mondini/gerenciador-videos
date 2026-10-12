# Pipeline de vídeo — Marble & Ash

Código Python que monta os vídeos no padrão **teatro de sombras projetadas** (ver
`docs/estilo-teatro-de-sombras.md`). Uma biblioteca (`marbleash/`) com a arte e o compositor, e, para
cada bloco de cada vídeo, **dados fora do código**: `videos/video-NN/blocoN/` com o script de cena,
os tempos da narração e a análise do áudio. Uma linha de comando (`ma`) faz cada etapa com um comando.

> O bloco 1 do vídeo 1 é o **exemplo oficial**: `videos/video-01/bloco1/cena.py`. Ele reproduz bit a bit
> o render aprovado em 11/10/2026. Copie-o para começar qualquer bloco novo.

---

## 1. Instalação

### No Mac (pasta do canal)
Tudo fica dentro de `canal-estoicismo/` (nada é instalado no sistema):

```bash
cd ~/Projects/gerenciador-de-canais/canal-estoicismo
python3 -m venv .venv
PIP_NO_CACHE_DIR=1 .venv/bin/pip install -r pipeline/requirements.txt
```

O pacote `imageio-ffmpeg` traz um ffmpeg dentro do `.venv` (o pipeline o encontra sozinho).
Opcional, para os tempos automáticos: `.venv/bin/pip install faster-whisper` — o modelo `small.en`
(~460 MB) é baixado na primeira vez para `pipeline/.modelos/`.

Depois disso, use o atalho `./ma` na pasta do canal (ele chama o Python do `.venv`):

```bash
./ma -h
```

### Fontes
Todas em `fontes-tipograficas/` (licença OFL, arquivos `OFL-*.txt`): **Cinzel** (nomes),
**Cormorant Garamond** (citações; padrão de `objetos.letreiro`), **Inter** (créditos), **GFS Baskerville**
(grego). A família **Cormorant** (sem "Garamond") fica só porque o sussurro aprovado do bloco 1 usa ela.
Use o nome do arquivo: `objetos.letreiro('texto', 'Inter-Regular.ttf', tamanho=22, ...)`.

---

## 2. Comandos

Rode na pasta do canal. `VIDEO` = `video-01` (ou só `1`); `BLOCO` = número do bloco.

| Etapa | Comando | O que faz | Gera |
|---|---|---|---|
| Áudio | `./ma audio VIDEO BLOCO` | Detecta as pausas do mp3, alonga levemente as pausas (ritmo final ~150 palavras/min) | `blocoN/audio.json`, `trabalho/blocoN-lento.wav` |
| Tempos | `./ma tempos VIDEO BLOCO` | Sugere o início de cada frase do roteiro (transcritor + pausas) | `blocoN/tempos.txt` (ou `tempos-sugerido.txt` se já existir) |
| Conferir tempos | `./ma deixas VIDEO BLOCO` | Lista as deixas com o tempo no vídeo | — |
| Stills | `./ma stills VIDEO BLOCO 5 12.5 30` | PNGs de conferência nos segundos dados (sem segundos: os `STILLS` da cena) | `previas/stills/blocoN_SSS.SS.png` |
| Render | `./ma render VIDEO BLOCO` | Vídeo do bloco com voz + ambiente a −16 LUFS | `previas/blocoN.mp4` (+ `trabalho/blocoN-video.mp4` sem som) |
| Trecho | `./ma render VIDEO BLOCO --de 20 --ate 30` | Só um trecho, para conferir rápido | `previas/blocoN-20a30s.mp4` |
| Juntar | `./ma juntar VIDEO 1 abertura 2 3` | Junta blocos e peças comuns, na ordem dada, com ambiente contínuo (−16 LUFS); `--4k` também exporta em 4K | `final/video-NN-1-abertura-2-3.mp4` |
| Peça comum | `./ma render comum abertura` | Renderiza uma peça sem narração, igual em todos os vídeos (`videos/comum/<nome>/cena.py`, com `DURACAO`) | `videos/comum/previas/abertura.mp4` |
| YouTube | `./ma youtube videos/video-01/previas/bloco1.mp4` | Recomprime a ~4 Mbps e salva stills lado a lado (inteiros e zoom num degradê) | `...-youtube4mbps.mp4`, `previas/stills/<nome>-youtube/` |
| Comparar | `./ma comparar A.png B.png` | Diferença de pixels (também aceita duas pastas) | — |
| Testes | `.venv/bin/python -m pytest pipeline/testes` | Confere tempos, atalhos de desempenho e os stills de referência | — |

Opções úteis: `render --processos N` (padrão 4), `render --sem-som`, `render --ambiente -20` (ganho do
ambiente em dB), `stills --referencia PASTA` (compara com stills salvos), `tempos --refazer`,
`tempos --sem-transcritor`, `youtube --mbps 4`.

---

## 3. Como criar um bloco novo (passo a passo)

Exemplo: bloco 2 do vídeo 1. Siga na ordem; não pule a conferência dos tempos nem a aprovação do frame.

1. **Áudio.** Salve o mp3 do ElevenLabs em `videos/video-01/audio/` com `bloco2` no nome
   (ex.: `video01-bloco2-starter.mp3`). Se houver mais de um, o comando usa o mais recente; para escolher,
   use `--arquivo`.
2. **Pausas e ritmo:** `./ma audio video-01 2`. Confira a mensagem: número de pausas e duração antes/depois.
3. **Tempos:** `./ma tempos video-01 2`. Ele lê o texto do `## Bloco 2` no `roteiro.md` e grava
   `videos/video-01/bloco2/tempos.txt`, uma linha por frase (ver seção 4). Leia a tabela impressa:
   - frases com origem `pausa` estão exatas; `voz` vem do transcritor (±0,1 s); `estimado`, sem
     transcritor, precisa de conferência ouvindo o áudio;
   - **renomeie** as deixas que a cena vai usar para nomes curtos (`name`, `plague`, `danube`...).
     Só letras, números e `_`. As outras podem ficar como estão.
4. **Script de cena.** Copie `videos/video-01/bloco1/cena.py` para `videos/video-01/bloco2/cena.py` e:
   - troque a docstring (o que acontece em cada cena, seguindo as "Ideias de cena" do roteiro);
   - monte o ELENCO com peças da biblioteca (`cenario.*`, `objetos.*`, `bonecos.*`) — ver seção 5;
   - escreva `quadro(q, c)` usando só deixas de `tempos.txt` (`c.nome`), nunca segundos soltos;
   - ajuste `STILLS` para os momentos-chave do bloco.
   Se faltar uma peça (ex.: máscara da peste, busto), crie a arte nova — ver seção 6.
5. **Frame para aprovação.** `./ma stills video-01 2 <segundos>` e mostre ao criador o frame da cena nova
   mais importante **antes** de renderizar o bloco (regra do canal).
6. **Render:** `./ma render video-01 2` → `videos/video-01/previas/bloco2.mp4`. O comando imprime o tempo
   de render e a loudness final (−16 LUFS).
7. **Compressão do YouTube:** `./ma youtube videos/video-01/previas/bloco2.mp4` e confira os stills
   `*-degrade-zoom.png`: se aparecerem faixas ou blocos nos degradês, a entrega final vai em 4K
   (`./ma juntar ... --4k`).
8. **Vídeo final** (todos os blocos prontos): `./ma juntar video-01 1 abertura 2 3 4 pausa 5 6` → `videos/video-01/final/`
   (a abertura padrão entra logo depois do gancho; peças comuns renderizadas uma vez com `./ma render comum <nome>`).

---

## 4. O arquivo de tempos a partir de um áudio novo

`./ma audio` grava em `blocoN/audio.json` o mp3 usado, as pausas detectadas (silêncio abaixo de −38 dB
por 0,3 s ou mais) e os parâmetros de ritmo (andamento 1,0; cada pausa ganha 10% + 0,05 s → ~150 palavras/min; ficam em `marbleash/audio.py`, `RITMO`). Esse arquivo
é gerado: não edite à mão.

`./ma tempos` cruza três coisas:
1. **o texto** do `## Bloco N` do `roteiro.md` (sem as audio tags), quebrado em frases a cada vírgula,
   ponto, reticências ou fim de linha;
2. **as palavras do transcritor** (faster-whisper, modelo `small.en`), com o tempo de cada palavra — ficam
   guardadas em `audio.json` para não transcrever de novo (`--retranscrever` força);
3. **as pausas**: cada frase é casada, em ordem, com no máximo uma pausa; casou, o início da frase é o fim
   exato da pausa (origem `pausa`).

Formato de `tempos.txt` (comentários com `#`):

```
roof        3.88  A roof over your head.          # pausa
alone_in   27.92  alone in a tent at the edge...  # voz
```

- **SEGUNDO** é sempre no **áudio original** do ElevenLabs. O pipeline converte para o tempo do vídeo
  desacelerado; `./ma deixas` mostra a conversão.
- Para ajustar, troque o número e rode `./ma stills` de novo. Para uma deixa no meio de uma frase,
  acrescente uma linha nova com o nome e o segundo da palavra (veja os tempos das palavras em
  `audio.json`, campo `palavras`).
- Toda cena tem também `c.fim` (fim da narração, no tempo do vídeo).
- Se o áudio mudar (ex.: regravação no plano Starter), rode `./ma audio` e `./ma tempos` de novo: como
  `tempos.txt` já existe, a sugestão vai para `tempos-sugerido.txt`. Copie para ela os nomes usados na
  cena e substitua o `tempos.txt`.

---

## 5. Guia do script de cena

```python
from marbleash.cena import *          # Camada, Boneco, Chama, cenario, objetos, bonecos, ss, env, lerp...

ENTRADA = 0.4        # s de vídeo antes da narração
SAIDA = 1.0          # s depois da narração (o último segundo escurece)
STILLS = (3, 9.5)    # tempos de conferência

TEMPLO = Camada(objetos.templo, desfoque=2.4, opacidade=0.82, semente=4, pivo=(800, BASE), balanco=(2.2, 0.3))

def quadro(q, c):
    s1 = 1 - q.ss(c.imagine, 1.2)              # cena visível até "imagine"
    q.luz(1.0)                                  # sempre primeiro
    sobe = q.ss(c.roof, 1.6)
    q.sombra(TEMPLO, s1, dy=420 * (1 - sobe))   # sobe do chão no "roof"
```

**Elenco** (declarado no topo; nada é desenhado até ser usado; tudo fica em cache):

| Peça | Parâmetros |
|---|---|
| `Camada(arte, *args, ...)` | `desfoque` = distância do lençol em px (personagem ~1; objetos 1,5–3; laterais 4,5; fundo 6–9) · `opacidade` (0,3 no fundo; 0,8–0,86 em objetos) · `semente` liga o balanço na vareta (use números diferentes por peça) · `pivo` = onde a mão segura · `balanco=(px, graus)` · `dobra=False` não entorta nas dobras · `posicao` = onde desenhar uma figura pequena (soldado, moeda) |
| `Boneco(fabrica, escala, desfoque, opacidade)` | `bonecos.homem`, `bonecos.imperador`. Pose: `{'torso', 'head', 'uarmF', 'farmF', 'uarmB', 'farmB', 'legF', 'legB': graus}` (F = frente, B = trás; ângulos somam ao da peça-mãe) |
| `Credito(texto)` | texto do crédito; opções `fonte`, `tamanho`, `cor`, `margem` (padrões do Design System) |
| `Chama(arte, *args, brilho, cor, forca)` | `objetos.chama`, `objetos.chama_noite`: a única cor saturada, com brilho âmbar em volta |

**Quadro** (`q`), chamado a cada quadro com as deixas (`c`):

| Chamada | Efeito |
|---|---|
| `q.u`, `q.ss(t0, dur)`, `q.env(a, ai, b, bo)`, `q.lin(t0, dur)` | tempo e curvas (0→1 suave, envelope sobe/desce, rampa) |
| `q.luz(nivel)` | lanterna: 1 = dia; noite ≈ 0,45–0,5; glória ≈ 1,15. Multiplique por `tremor(q.u)` para tremular |
| `q.lua(alpha)` | lua cheia projetada (disco claro) |
| `q.sombra(camada, *fatores, dx=, dy=)` | projeta a peça; opacidade = da camada × fatores. **Ordem das chamadas = ordem das sombras** |
| `q.multidao(camada, [(dx, dy), ...], *fatores, pesos=)` | muitas cópias (soldados, moedas) |
| `q.boneco(boneco, x, y, pose, *fatores, desfoque=)` | boneco articulado com o pivô do torso em (x, y) |
| `q.foco(forca, cx, cy, raio)` | círculo de luz; o resto cai na penumbra |
| `q.chama(chama, *fatores, cintila=(base, amp, freq), camada=, dy=)` | chama colorida; com `camada`, balança junto |
| `q.camera(cx, cy, zoom)` | aproximação (ex.: `1 + 0.38 * env(...)`) |
| `q.credito(CRED, alpha)` | crédito de fonte na tela (regra fixa do canal): Inter 24 px, `marble-300`, canto inferior esquerdo, margem de 64 px. Não é sombra nem acompanha a câmera. Declare `CRED = Credito('Marcus Aurelius, Meditations 6.30 · trans. George Long')` no elenco e chame `q.credito(CRED, q.env(c.inicio, 0.8, c.fim_da_citacao, 0.8))` (aparece e some suavemente) |

Receitas do padrão aprovado (todas no bloco 1):
- **sobe do chão**: `p = q.ss(c.x, 1.6)` → `dy=420 * (1 - p)`; **desce do teto**: `dy=-460 * (1 - p)`;
  **desliza da direita**: `dx=760 * (1 - p)`;
- **aparece e some**: fator `q.env(c.a, 1.2, c.b, 1.0)`; **troca de cena**: `s1 = 1 - q.ss(c.x, 1.2)`
  e `s2 = q.ss(c.x - 0.2, 1.2)`;
- **caminhar**: `x = lerp(-180, 430, q.ss(0.3, 3.6))`, pernas `±22 * sin(u * 4.2)`;
- **foco + zoom nos momentos-chave**: `q.foco(env, cx, cy, 320)` e `q.camera(cx, cy, 1 + 0.38 * env)`.

Regras: tudo em `quadro()` depende só de `q.u` e das deixas (nada de `random` sem semente fixa);
**sem mãos de manipuladores**; não mude as peças aprovadas (fundo, laterais, lençol) — crie novas.

---

## 6. Arte nova

- Objetos e cenários: funções em `marbleash/objetos.py` ou `marbleash/cenario.py` que desenham numa
  folha do tamanho do quadro e devolvem um sprite (`full(desenho)` ou `layer(desenho)`). Bonecos novos:
  `marbleash/bonecos.py` (peças `Part` + `Puppet`, como o imperador).
- Ferramentas do kit (`marbleash/traco.py`): `shape` (contorno curvo), `stroke` (corte que afina),
  `spiral`, `ell`, `poly`, `holes_row`, `rivet`, `serrated`, `ivy`, `flower`, `tuft`; `INK` = papel,
  `HOLE` = furo por onde a luz passa; `toward` para o três quartos.
- Desenhe com muitos furos e curvas (cachos, bordados, nervuras), como pede o padrão.
- O cache se refaz sozinho quando o código de arte muda. Depois de mexer na biblioteca, rode os testes:
  os stills do bloco 1 precisam continuar idênticos.

---

## 7. Desempenho, cache e referência

- Render no Mac M2: **~1,5–2,0 s por segundo de vídeo** com 4 processos (era ~5 s com o código antigo
  no mesmo Mac). Preparo da arte: ~8 s na primeira vez, ~0,1 s depois.
- Cache em `pipeline/.cache/` (fora do git). `./ma limpar-cache` apaga; é refeito sob demanda.
- Pouca memória? `./ma render ... --processos 2`.
- Referência visual: `videos/video-01/trabalho/referencia/stills/` (fora do git). O teste
  `test_referencia.py` exige igualdade pixel a pixel. Em outro computador (outras versões de bibliotecas),
  gere a referência de novo **antes** de mexer no código:
  `./ma stills video-01 1 --pasta videos/video-01/trabalho/referencia/stills`.

## 8. Problemas comuns

| Mensagem | O que fazer |
|---|---|
| `Falta .../audio.json` | `./ma audio VIDEO BLOCO` |
| `Falta .../tempos.txt` | `./ma tempos VIDEO BLOCO` |
| `deixa 'x' não existe em tempos.txt` | renomeie a linha certa de `tempos.txt` para `x` |
| `Fonte 'Inter-Regular.otf' não encontrada` | copie a fonte para `fontes-tipograficas/` |
| `ffmpeg não encontrado` | instale as dependências (seção 1) ou defina `MA_FFMPEG` |
| Render lento ou Mac travando | menos processos: `--processos 2` |

Código antigo (antes da refatoração): `pipeline/_arquivo/` — não usar.

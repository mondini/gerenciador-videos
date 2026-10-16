# Ideias de canais futuros

Caderno de ideias para canais novos, todos com **animação 2D/motion design** em vez de imagens geradas cena por cena. Serve para lembrar das ideias, escolher quais viram protótipo e guardar pautas, fontes e aprendizados.

- Este arquivo é o **índice**: lista de canais, regras comuns, ferramentas e protótipos.
- Cada canal tem uma ficha em [`canais/`](canais/), com conceito, linhas editoriais, pautas, cuidados e fontes.
- Os nomes são **de trabalho**. O nome público de cada canal é decidido quando ele sair do papel.

> Esta pasta não é um projeto. Quando uma ideia virar canal de verdade, ela ganha a própria pasta (`canal-<nome>/`, com `CLAUDE.md`, como os outros canais) e sai daqui.

Criado em 14/10/2026. Última revisão: 15/10/2026.

---

## 1. Canais planejados

| Ordem | Canal | Idioma | Visual (principal + secundário) | Linhas editoriais | Ficha |
|---|---|---|---|---|---|
| 1 | **Língua e costumes** | PT | Tipografia cinética + mapa | Etimologia ("verdade ou mito?"), mapa das palavras, expressões populares, superstições e simpatias | [lingua-e-costumes.md](canais/lingua-e-costumes.md) |
| 2 | **Brasil por dentro** | PT | Isométrico + infográfico/mapa | Infraestrutura, dinheiro do dia a dia, burocracia, Brasil em mapas, casas, comida de rua, inventos, clima, casos (minidocumentários), bandeiras e brasões | [brasil-por-dentro.md](canais/brasil-por-dentro.md) |
| 3 | **Lendas regionais** | PT | Flat com paleta escura + mapa | Terror folclórico, uma lenda por vídeo | [lendas-regionais.md](canais/lendas-regionais.md) |
| 4 | **Sistemas e padrões** | EN + áudio PT | Partículas/generativo + diagramas em line art | Emergência, biomimética, matemática visual, ritmos brasileiros | [sistemas-e-padroes.md](canais/sistemas-e-padroes.md) |
| 5 | **Ciência do cotidiano** | PT | Flat + line art | Ciência do dia a dia brasileiro, física dos brinquedos de rua, o céu do mês | [ciencia-do-cotidiano.md](canais/ciencia-do-cotidiano.md) |
| 6 | **Futebol com bolinhas** | PT | Flat (prancheta) + infográfico | Táticas, lances históricos, regras | [futebol-com-bolinhas.md](canais/futebol-com-bolinhas.md) |
| — | **Histórias católicas** (arquivada) | EN | A definir (one-line art e silhuetas reprovados) | Santos, parábolas, Mandamentos, salmos; pauta pelo calendário litúrgico | [historias-catolicas.md](canais/historias-catolicas.md) |

Por que essa ordem:
- **1.** Concorrência quase zero, produção quase toda por código, Shorts virais e comentários garantidos.
- **2.** Paga melhor (dinheiro, tecnologia), muito compartilhável e com pautas para anos.
- **3.** Gênero com público fiel no Brasil, e a narração atmosférica se parece com o que já fazemos.
- **4.** Diferencial técnico (simulação de verdade) e RPM de inglês.
- **5** e **6** ficam por último porque a concorrência é maior; precisam de validação com Shorts antes.
- **Histórias católicas** fica fora da fila: já foi canal e voltou para o caderno sem estilo de arte aprovado. Só retomar com um caminho de arte novo.

### De onde veio cada ideia

| Ideia original | Para onde foi |
|---|---|
| Ciência em 60 segundos | **Ciência do cotidiano**, com recorte brasileiro; Shorts como vitrine e vídeos longos como produto |
| História em mapas e linhas do tempo | **Brasil por dentro**, linha "Brasil em mapas" (foco no Brasil, não em Roma) |
| Como as coisas funcionam | **Brasil por dentro**, linha "Infraestrutura", sempre com o recorte brasileiro |
| Curiosidades do Brasil | Distribuída entre **Brasil por dentro** e **Língua e costumes** (amplo demais sozinho) |
| Etimologia visual | **Língua e costumes** |
| Infraestrutura brasileira por dentro | **Brasil por dentro** |
| Sistemas que se organizam sozinhos | **Sistemas e padrões** |
| Biomimética | **Sistemas e padrões**, como série |
| Física dos brinquedos de rua | **Ciência do cotidiano**, como série |
| Canal amplo sobre o Brasil | Dividido em **Brasil por dentro**, **Língua e costumes** e **Lendas regionais**, porque cada linha atrai um público diferente |
| *Nicho novo:* dinheiro do dia a dia | **Brasil por dentro** |
| *Nicho novo:* bandeiras e brasões | **Brasil por dentro**, série de Shorts |
| *Nicho novo:* matemática visual | **Sistemas e padrões** |
| *Nicho novo:* ritmos brasileiros visualizados | **Sistemas e padrões** (ritmo é padrão matemático) |
| *Nicho novo:* o céu do Brasil | **Ciência do cotidiano**, série mensal |
| *Nicho novo:* futebol explicado com bolinhas | Canal próprio: **Futebol com bolinhas** |

Descartadas em 14/10/2026: *Loops para relaxar e focar* e *Sua cidade em números*.

---

## 2. Técnicas visuais

| Técnica | Referências (busca) | Gerar por código? | Ferramenta sugerida | Canais |
|---|---|---|---|---|
| Flat design / motion graphics | "flat motion graphics", "flat 2D explainer animation" | Médio a alto | Remotion (SVG/CSS) | Lendas, Ciência do cotidiano, Futebol |
| Line art animado | "SVG line drawing animation" | **Alto** | Remotion + GSAP DrawSVG; Manim | Ciência do cotidiano, Sistemas e padrões |
| Tipografia cinética | "kinetic typography" | **Alto** | Remotion + GSAP SplitText | Língua e costumes |
| Geométrico / Bauhaus | "geometric loop animation", "bauhaus motion design" | **Alto** | Manim ou Remotion | Sistemas e padrões (ritmos), bandeiras |
| Arte generativa e partículas | "generative art animation" | **Alto**, com simulação de verdade | Python (numpy) + render direto | Sistemas e padrões |
| Isométrico | "isometric animation" | Médio a alto | Remotion + three.js com câmera ortográfica | Brasil por dentro |
| Infográfico e mapa animado | "animated infographic" | **Alto** | Remotion + d3 (d3-geo, d3-shape) | Brasil por dentro, Língua e costumes, Lendas |

Pixel art saiu da lista: só fazia sentido nos loops, que foram descartados.

---

## 3. Ferramentas de animação (sugestão, validar nos protótipos)

**Resumo: não fazer tudo em Python.** A sugestão é dividir assim:

| Parte | Ferramenta | Por quê |
|---|---|---|
| Pipeline do canal (roteiro → narração → render → montagem → backup) | **Python**, no molde do `./ma` | É o fluxo que já funciona: ElevenLabs, ffmpeg e Drive. Não vale reescrever |
| Animação de Língua e costumes, Brasil por dentro, Lendas, Ciência do cotidiano e Futebol | **Remotion** (React + TypeScript) | Ver abaixo |
| Animação de Sistemas e padrões | **Python**: numpy para simular, Manim para matemática e diagramas | Simulação científica e matemática animada são o forte do Python. O Manim foi feito para isso (é a ferramenta do 3Blue1Brown) |

**Por que Remotion para a maior parte:**
- Cada quadro do vídeo é uma página web. Tudo o que o navegador faz bem (SVG, CSS, fontes, tipografia, sombras, gradientes) fica disponível, e é justamente disso que flat, line art, tipografia cinética e infográfico são feitos.
- O **Remotion Studio** mostra o vídeo no navegador com linha do tempo: dá para arrastar e ver qualquer momento sem renderizar. O Manim só mostra o resultado depois de renderizar.
- O ecossistema JavaScript tem as melhores bibliotecas para essas técnicas: **d3** para mapas (com as malhas do IBGE) e gráficos; **GSAP**, gratuito com todos os plugins desde 2025, com DrawSVG (traço que se desenha), SplitText (tipografia) e MorphSVG (forma que vira outra); **three.js** com câmera ortográfica, que dá o isométrico de maquete sem desenhar perspectiva à mão.
- **Sincronia com a narração:** a ElevenLabs devolve o tempo de cada caractere falado (endpoint *with timestamps*). O Python gera um JSON com esses tempos e o Remotion anima cada palavra exatamente quando ela é dita. Para o canal de tipografia, isso é metade do trabalho.
- O Node já está instalado no Mac.

**Como as duas partes conversam:** o Python gera um JSON por vídeo (cenas, textos, tempos da narração, dados) e chama `npx remotion render` com esse JSON. O Remotion devolve o vídeo e o Python segue com montagem, backup e sincronização.

**Cuidados técnicos:**
- O Remotion renderiza quadros em paralelo e fora de ordem. Toda animação tem que ser calculada a partir do número do quadro, e simulações (cardume, trânsito) precisam ser **pré-calculadas** antes do render.
- Licença do Remotion: gratuita para pessoa física e empresas pequenas (até 3 pessoas). Conferir os termos atuais quando o primeiro canal for criado.
- **Isolamento entre canais:** pela regra do repositório, cada canal tem o próprio código. Uma biblioteca de componentes compartilhada entre canais (mapa do Brasil, tipografia) seria uma exceção que só o dono pode autorizar. Decidir isso quando houver dois canais em produção.

**Alternativas descartadas:**
- *Tudo em Python (Manim, moviepy, Pillow):* o Manim é ruim para design gráfico, tipografia e flat, e não tem prévia com linha do tempo. moviepy e Pillow obrigam a desenhar tudo à mão.
- *Motion Canvas:* parecido com o Remotion e bom para explicações, mas a comunidade e o ecossistema são menores.
- *After Effects:* manual e pago, não automatiza.

---

## 4. Regras para todos os canais

1. **Validar com Shorts antes de abrir o canal.** Fazer de 5 a 10 Shorts da ideia e comparar retenção e taxa de inscrição. Custa pouco e evita meses num canal sem tração.
2. **Um público por canal.** O YouTube recomenda pelo público de cada vídeo. Linhas editoriais que atraem pessoas diferentes vão para canais diferentes.
3. **Uma identidade visual por canal:** no máximo uma técnica principal e uma secundária (ver tabela da seção 1).
4. **Produção por código.** Cada canal monta a própria biblioteca de componentes (o mapa, a palavra que se desenha, a maquete) e cada vídeo novo reaproveita peças. A estrutura padrão de canal (seção "Estrutura padrão de um canal" do `CLAUDE.md` da raiz) serve de molde.
5. **Nada de "produzido em massa".** Template é bom; vídeo idêntico com dados trocados é ruim. A política de **conteúdo inautêntico** do YouTube (julho de 2025) pune isso. Cada vídeo precisa de roteiro e gancho próprios.
6. **Idioma é decisão de receita.** Português tem menos concorrência e alcance no WhatsApp; inglês paga várias vezes mais por mil views. Temas universais saem em inglês com **faixa de áudio em português** (o YouTube aceita várias faixas no mesmo vídeo, e título e descrição podem ser traduzidos). Com o texto da tela gerado por código, a versão em português é só renderizar de novo.
7. **Shorts como vitrine, vídeos longos como produto.** Short sozinho paga pouco.
8. **Títulos em forma de pergunta** ("Por que…", "Como funciona…", "De onde vem…") pegam busca o ano inteiro, além do tráfego do algoritmo.
9. **Polêmica boa vs. polêmica ruim.** "Biscoito ou bolacha" gera comentário e é inofensivo. Política partidária, religião e eleição geram comentário e derrubam o canal.
10. **Rigor e fontes na descrição.** Em canal explicativo, a credibilidade é o produto. Mitos populares são ótimos ganchos, desde que o vídeo mostre a fonte.
11. **Narração no ElevenLabs:** todo canal novo nasce com o seu `elevenlabs.json` (voz, modelo, ajustes, regra de créditos), seguindo a regra do `CLAUDE.md` da raiz. Protótipos também: antes de gerar áudio, confirmar o que será gerado e o custo em créditos.

---

## 5. Protótipos

Cada protótipo testa ao mesmo tempo a ideia e a técnica. Os dois primeiros validam o Remotion; o quarto valida a parte em Python.

| # | Protótipo | Canal | Formato | Técnica e ferramenta | O que valida |
|---|---|---|---|---|---|
| 1 | "Forró vem de *for all*? Não." | Língua e costumes | Short, 45s | Tipografia cinética, Remotion + GSAP + timestamps da ElevenLabs | Se o formato prende; se o vídeo sai 100% por código |
| 2 | "Mandioca, aipim ou macaxeira?" | Língua e costumes | Short + vídeo de 5 min | Mapa com dados do ALiB, Remotion + d3-geo | Componente de mapa reutilizável; volume de comentários |
| 3 | "O caminho de um Pix" | Brasil por dentro | 8 a 10 min | Isométrico (three.js ortográfico) + infográfico | Custo real de produzir isométrico; retenção em vídeo longo |
| 4 | "Why traffic jams happen for no reason" | Sistemas e padrões | 6 a 8 min, EN + áudio PT | Simulação em numpy + render em Python | Simulação como linguagem visual; desempenho do áudio duplo |
| 5 | "A Pisadeira" | Lendas regionais | 8 a 12 min | Flat escuro, Remotion | Se o terror folclórico funciona sem imagem realista |
| 6 | "Por que a pipa sobe?" | Ciência do cotidiano | Short + 6 min | Flat + line art, Remotion | Se o recorte de nostalgia segura a concorrência de ciência |
| 7 | "O gol de Carlos Alberto em 1970, passe a passe" | Futebol com bolinhas | Short + 5 min | Prancheta flat, Remotion | Se lance histórico animado (sem imagem real) prende |

---

## 6. Anotações

<!-- Espaço livre: ideias novas, links de referência e resultados dos protótipos, com data. -->

- **14/10/2026, protótipo 1 (Remotion):** Short de 23s renderizado em ~20s, todo a partir de um JSON. Ainda sem narração. Detalhes em [prototipos/forro/](prototipos/forro/).
- **15/10/2026, protótipo 3 (arte conceito):** um quadro de "O caminho de um Pix" com maquete isométrica em three.js + infográfico e mapa do IBGE em d3, tudo no Remotion. Detalhes em [prototipos/pix/](prototipos/pix/).
- **15/10/2026, Histórias católicas:** o canal `canal-historias-biblicas/` foi arquivado e voltou para o caderno como ideia; nenhum dos estilos de arte testados agradou. Ficha, testes e lições em [canais/historias-catolicas.md](canais/historias-catolicas.md).
- **15/10/2026, arte conceito "Fordlândia" (Brasil por dentro, linha "Casos"):** mesmo estilo de maquete num caso histórico, com linha do tempo e mapa das Américas. Detalhes em [prototipos/fordlandia/](prototipos/fordlandia/).

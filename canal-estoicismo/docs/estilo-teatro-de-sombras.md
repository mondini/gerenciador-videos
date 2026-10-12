# Marble & Ash — Padrão visual dos vídeos: Teatro de Sombras Projetadas

Aprovado pelo criador em 11/10/2026 (bloco 1 do vídeo 1). Vale para este e todos os próximos vídeos até nova orientação. Substitui o estilo anterior de "traço fino sobre horizonte".

## O conceito
Não mostramos os bonecos: mostramos **as sombras deles projetadas num lençol iluminado por trás**, como numa apresentação de teatro de sombras filmada. Mundo romano (togas, louros, colunas, aquedutos, pinheiros-mansos, ciprestes, lamparinas a óleo).

## Tela e luz
- Lençol de verdade, preso nos cantos de cima, com dobras irradiando dos cantos; as sombras se deformam levemente sobre as dobras.
- Luz de lanterna: centro quente e claro, bordas escuras (vinheta forte). Sem moldura recortada.
- Na base, o pano amontoado e escuro, com dobras suaves e borda iluminada, escondendo o "chão" do palco.
- Grade de cor sépia (preto quente → marrom → bege → creme). A única cor saturada é o **âmbar das chamas** (lamparinas, fogo), com brilho em volta.
- Grão fotográfico FIXO (não muda entre quadros), poeirinhas e círculos de luz suaves (bokeh).
- A luz muda com a história: dia sépia, noite mais escura com lua projetada (disco claro), momentos de glória com luz mais forte.

## Sombras e profundidade
- Sombras não são pretas: marrom-escuro semitransparente, deixando a luz vazar.
- Desfoque pela distância do pano:
  - Personagem principal: quase nítido (encostado no lençol).
  - Objetos de cena (templo, mesa, lamparina): levemente suaves.
  - Elementos das laterais (pinheiro à esquerda, coluna com galho à direita): bem difusos, como se estivessem perto da lâmpada.
  - Fundo distante (colinas, aqueduto, templo no morro, ciprestes): só vulto claro e muito desfocado.
- Câmera levemente de lado: objetos em três quartos (lateral visível do templo, tampo da mesa visto de cima), linhas fugindo para um ponto à direita fora da tela.
- As laterais da tela são definidas por elementos do cenário entrando de fora (árvore, coluna, galhos), nunca por moldura.

## Desenho dos recortes
- Muitos vetores e curvas: contornos em curva suave, cortes que afinam nas pontas (como tesoura), nada de círculos simples ou polígonos retos.
- Bonecos de perfil, com recortes vazados por onde a luz passa (cabelo em cachos espiralados, olho, dobras da roupa, bordados, coroa de louros), rebites nas articulações e uma vareta fina visível.
- Vegetação rica: copas feitas de tufos de agulhas, folhas de hera com cinco pontas e nervuras, folhas serrilhadas com nervuras, flores de oito pétalas, pinhas, capim fino.
- Arquitetura com detalhe: colunas jônicas com volutas e caneluras, frisos com gregas, frontões, arcos de aqueduto em dois andares.

## Animação
- Tudo balança nas varetas: cada peça do cenário oscila de leve, de forma independente, como se segurada à mão, sem estabilidade perfeita.
- Bonecos articulados (cabeça, braços, antebraços, pernas) com movimentos suaves; entradas pop-up (objetos sobem do chão, descem do teto, deslizam pela lateral).
- **Foco de luz + zoom** nos momentos-chave: a câmera aproxima e um círculo de luz isola o elemento importante, o resto cai na penumbra.
- **Sem mãos de manipuladores** (testadas e removidas a pedido do criador).
- Narração dita o tempo: cada deixa visual é sincronizada com a frase correspondente.

## Áudio e ritmo
- Narração ElevenLabs (voz de senhor ~70 anos). Na montagem: pausas levemente alongadas (+10% + 0,05 s), voz no andamento original (~150 palavras/min).
- Som ambiente gerado por código (sem amostras de terceiros), bem baixo sob a voz; normalização a −16 LUFS.

## Textos na tela
- Citações em Cormorant itálico; nomes em Cinzel; créditos de fonte em Inter (24 px, `marble-300`) no canto inferior esquerdo, margem de 64 px (regra fixa do canal), sobrepostos à imagem — não são sombra; no pipeline: `Credito` e `q.credito()`.

## Qualidade e entrega
- 1920×1080, 30 fps. Antes de entregar, simular a compressão do YouTube (~4 Mbps) e conferir se aparecem faixas/blocos nos degradês. Se aparecerem, exportar em 4K.
- Custo de render: ~1,2 s de processamento por segundo de vídeo no Mac (M2, 4 processos). Conferir em stills antes do render completo.

## Onde está a ferramenta
O código que gera este estilo está em `pipeline/` (biblioteca `pipeline/marbleash/` e comando `./ma`; ver `pipeline/LEIA-ME.md`) na pasta do canal no Mac (`~/Projects/gerenciador-de-canais/canal-estoicismo`). Os dados de cada bloco ficam em `videos/video-NN/blocoN/` (script de cena, tempos, análise do áudio); o modelo oficial é `videos/video-01/bloco1/cena.py`. Todo o trabalho fica centralizado nesta pasta (não há cópia no Claude.ai). Fontes em `fontes-tipograficas/`. Referência visual aprovada: `videos/video-01/previas/frame-referencia-estilo-aprovado.png` (sem as mãos dos manipuladores).

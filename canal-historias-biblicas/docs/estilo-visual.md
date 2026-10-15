# Style bible: one-line art

Fonte da verdade da consistência visual (decisão de 14/10/2026, que substitui a aquarela, o vitral, a iluminura e a pintura viva). Cada cena é desenhada pelo Claude em código (SVG + CSS + JavaScript), não é gerada por IA de imagem. Depois do piloto, ajustes de traço, paleta e animação entram aqui com data.

## Traço

- Linha preta contínua `#2F2E2C`, fina e uniforme (`stroke-width` ~1.5 numa tela de 1920×1080), `stroke-linecap` e `stroke-linejoin` arredondados, sem preenchimento no traço.
- Pequenos laços e cachos nas transições da linha; as pontas terminam em floreios soltos e espiralados.
- O chão é uma linha ondulada que passa das bordas da cena.
- Contornos simples e arredondados. **Sem** sombras, hachuras ou detalhes internos.
- Cenas compactas, centralizadas, com bastante respiro em volta.

## Cor

Manchas pastel chapadas, levemente **deslocadas** do contorno (efeito de impressão fora de registro, ~8–20 px), sem preencher a forma inteira. A mancha é um blob próprio, não o `fill` do contorno.

| Uso | Cor |
|---|---|
| Verde-sálvia | `#B7CBC4` |
| Sálvia claro | `#C9D0BD` |
| Pêssego | `#EBCDB0` |
| Rosa antigo | `#E2B7A8` |
| Azul acinzentado | `#BFCAD5` |
| Creme | `#F0E2CF` |

### Fundos

| Fundo | Céu | Faixa do chão | Quando usar |
|---|---|---|---|
| Céu azul suave (**padrão**) | `#DDE6EA` | `#CCD9E0` | dia, inverno, cenas neutras |
| Amanhecer pêssego | `#F6E3D3` | `#F1D3BD` | começo, esperança, ressurreição |
| Entardecer rosado | `#F1DCD8` | `#E8C7C2` | fim de tarde, despedida, sacrifício |
| Verde sálvia | `#DFE8E1` | `#CFDDD3` | campo, pastoreio, parábolas da natureza |

- O fundo pode mudar entre as cenas de um vídeo quando a hora do dia ou o clima da história muda; dentro de uma cena, nunca.
- Com fundo colorido, as nuvens são manchas claras, quase brancas.
- Noite e interiores escuros não existem no estilo: noite é o mesmo fundo com lua e estrelas de linha; interiores são uma moldura de linha (arco, janela) sobre o fundo claro.

## Profundidade e cenário

- Colinas em 2 ou 3 planos; a mais distante é sempre a mais clara.
- Uma faixa de horizonte separa o céu e o chão.
- Elementos recorrentes: sol (círculo de linha com mancha pêssego deslocada e um laço na cauda), nuvens fofas, pássaros em "m", caminhos sinuosos, oliveiras e arbustos arredondados.

## Personagens e símbolos

- **O tema é representado por símbolos** sempre que der: cruz, pomba, cálice, pães e peixes, chaves, cordeiro, barco, estrela, e os atributos de cada santo (tabela abaixo).
- Pessoas só como **silhuetas simples, sem rosto**, pequenas na cena, em pose parada ou num gesto simples (de pé, sentado, andando, ajoelhado, braço estendido).
- **Evitar:** rostos, multidões (no máximo 2 ou 3 figuras), gestos complexos (lutar, cortar, abraçar em detalhe), fala sincronizada. Quando a história tem uma ação, mostrar o **antes e o depois** em cenas separadas, ou o objeto da ação (a capa partida, não o corte).
- Regras de Jesus, Maria, Deus Pai, Espírito Santo, Eucaristia e anjos: `doutrina-e-fontes.md`.
- Nunca infantil: nada de bichos fofos com olhos, cabeças grandes, cores saturadas ou cenas lotadas.

## Animação

- A cena **já começa completa**. Nunca animar o desenho sendo traçado.
- **Line boil:** o traço treme como desenho feito à mão. Filtro SVG `feTurbulence` + `feDisplacementMap` (`scale` 2–3), trocando o `seed` entre 4 valores a cada ~125 ms. O filtro vai só no grupo das linhas e das manchas, nunca no fundo inteiro (pesa na gravação).
- Movimentos sutis em loop, lentos, com `ease-in-out`: nuvens derivando, sol "respirando", raios girando devagar, pássaros atravessando e batendo as asas, árvores e juncos balançando, folhas ou neve caindo, água ondulando.
- Cada cena tem de 1 a 3 movimentos, não todos ao mesmo tempo. Clima calmo, reverente, contemplativo; nada brusco.
- A troca entre cenas é feita na montagem (dissolve lento), não dentro do HTML.

## Formato técnico

- Uma cena = **um arquivo HTML único** (SVG inline, CSS e JS no mesmo arquivo; sem bibliotecas externas, sem internet).
- Proporção 16:9, `viewBox="0 0 1920 1080"`, ocupando a janela inteira (o desenho escala sem perder nitidez em qualquer resolução de gravação). 9:16 só se os shorts voltarem.
- Fundo da página na cor do céu da cena, sem barra de rolagem nem cursor.
- O loop precisa fechar sem salto (duração dos movimentos em múltiplos do loop da cena) para dar para gravar o tempo que a narração pedir.
- Toda cena nova parte de `biblioteca/elementos/_modelo-cena.html` (line boil, neve, cores e chão prontos).
- **Traço uniforme:** num grupo ampliado ou reduzido, compensar com `style="--traco: (1.5 / escala)"`; senão o traço engrossa ou afina.
- Animação CSS só em elementos escritos direto no SVG, nunca dentro de `<use>` (nem todo navegador anima a cópia).
- **Vídeo da cena:** sai do `pipeline/montar.py`, quadro a quadro (`plano-canal.md`, "Montagem"); por isso o JavaScript da cena só pode usar animações CSS e o timer do line boil, que o renderizador controla. Para uma prévia rápida, dá para abrir no Chrome em tela cheia e gravar uma área 16:9 (⇧⌘5).
- **Texto na tela** (versículos, créditos, títulos) entra no próprio HTML da cena ou num cartão próprio: serifada sóbria, cor do traço, pequena, centralizada, sem animação de digitação.
- Arquivos: `videos/XX-NNN-slug/cenas/cNN-descricao.html` (ex.: `c03-capa-partida.html`).

## Biblioteca de elementos

- Elementos que se repetem (sol, nuvem, pássaro, oliveira, cruz, pomba, silhuetas, atributos de santos) viram SVGs em `biblioteca/elementos/` (`elemento-descricao_v1.svg`), copiados para dentro de cada cena (a cena continua sendo um arquivo único). Cada SVG abre sozinho e guarda as coordenadas da cena de origem; ao reaproveitar, mover com `transform`. Na biblioteca o elemento é estático: o movimento é definido na cena.
- Antes de desenhar um elemento novo, procurar na biblioteca. Reaproveitar elementos, nunca cenas inteiras (`plano-canal.md`, política de conteúdo inautêntico).

## Santos e atributos

Na arte, o santo é reconhecido pelo atributo, não pelo rosto.

| Santo | Atributos fixos | Registrado em |
|---|---|---|
| São Martinho de Tours | capa partida ao meio (mancha rosa antigo), espada, cavalo | 14/10/2026 (TESTE-01) |

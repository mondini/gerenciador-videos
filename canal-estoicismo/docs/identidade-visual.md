# Identidade visual — resumo do Design System (fonte de verdade: Claude Design)

Design System: https://claude.ai/artifact/YD1Vx9JHfUSKFFVMcdkQqh · Canvas de logo, thumbs e banner:
https://claude.ai/artifact/4TczXDna7NDn4JW9jyACkp. Copiado aqui em 12/10/2026 para o pipeline; se o Design
System mudar, atualizar este arquivo.

## Princípios
1. **Silêncio visual** — espaço vazio faz parte do formato. Nada de rostos, estátuas realistas, fotos.
2. **Uma brasa por tela** — só uma coisa em âmbar por quadro.
3. **Pedra cortada** — cantos retos; círculos só como sol, lua ou ponto final de linha.
4. **Sempre igual** — mesma abertura, mesmo encerramento, mesma posição de título em todos os vídeos.

## Cores (60 · 30 · 10)
| Token | Hex | Uso |
|---|---|---|
| `ash-950` | #121110 | vinheta, bordas |
| `ash-900` | #1A1816 | **base (60%)** — fundo |
| `ash-800` | #24211E | faixas, cartões |
| `ash-700` | #3A3530 | listras discretas |
| `marble-100` | #EDE6DA | **secundária (30%)** — texto e linhas |
| `marble-300` | #B8AFA2 | texto secundário, créditos |
| `amber-500` | #E8A33D | **destaque (10%) no vídeo** |
| `amber-400` | #FFB547 | só thumbnails e capas de shorts (20–30% da imagem) |
| `amber-700` | #8A5A1C | brilho atrás do destaque; nunca texto |

## Tipografia
- **Cinzel** (display): títulos, logo, thumbnail; sempre caixa alta. `title` 64 px / 600 / 0.04em (abertura).
- **Cormorant Garamond** (serif): citações (`quote` 48 px / 500, itálico opcional; `quote-small` 28 px).
- **Inter** (sans): créditos e referências (`small` 16 px / 400, em `marble-300`); legendas de shorts (`caption` 44 px / 700).

## Logo A — Horizonte (caixa 200 × 200)
- Sol: meio-disco âmbar `M44 110 A56 56 0 0 1 156 110 Z` (centro 100,110; raio 56).
- Dois cortes cor de fundo atravessando o sol: y = 80 e y = 94, de x 40 a 160, espessura 4.
- Horizonte em `marble-100`, espessura 3: (24–176, y110), (44–156, y124), (60–140, y138), (76–124, y152), (90–110, y166).
- Nome: "MARBLE & ASH" em Cinzel 600, tracking 0.06em, `marble-100`, com o **"&" em âmbar**.
- Assinatura: *Old wisdom for quiet hours.* em Cormorant Garamond itálico 500, `marble-300`.

## Nos vídeos (teatro de sombras)
A grade sépia faz o papel da paleta: sombra ≈ `ash-900`, lençol iluminado ≈ `marble-100`, e a única cor
saturada é o âmbar (chamas, sol do logo, "&"). Textos: nomes em Cinzel, citações em Cormorant Garamond,
créditos em Inter (`marble-300`) no canto inferior esquerdo, com margem de segurança de 64 px.

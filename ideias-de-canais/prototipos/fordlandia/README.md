# Protótipo: "Fordlândia" (arte conceito, linha "Casos")

Segundo teste de visual do canal [Brasil por dentro](../../canais/brasil-por-dentro.md), agora num caso histórico, para comparar com o [quadro do Pix](../pix/). Um quadro só; não é um vídeo final.

- `src/cena.ts`: quadro, câmera isométrica, lugares da maquete e a regra da doença no seringal.
- `src/Maquete.tsx`: a maquete em three.js: rio Tapajós com barco, vila americana, caixa-d'água, serraria com fumaça, galpão, seringal em fileiras e a mata em volta.
- `src/Fordlandia.tsx`: linha do tempo, rótulos, mapa das Américas (d3 + world-atlas) e legenda palavra por palavra.

```bash
npm install
npm run studio   # prévia de 5s: a doença avança pelas fileiras, a mata cresce na cidade, o barco desce o rio
npm run arte     # gera out/arte-conceito.png (quadro 100)
```

## Fatos usados no quadro (15/10/2026)

- Fundada por Henry Ford em 1928, na margem leste do Tapajós, no Pará; a caixa-d'água (cerca de 50 m) é tida como o símbolo da cidade; havia vila no estilo americano e serraria. Revolta do Quebra-Panelas em 1930. Seringueiras plantadas juntas, atacadas por pragas e doenças. Venda ao governo brasileiro em 1945. Fontes: [Wikipedia](https://en.wikipedia.org/wiki/Fordl%C3%A2ndia), [Portal Amazônia](https://portalamazonia.com/amazonia-de-a-a-z/fordlandia/), [Atlas Obscura](https://atlasobscura.com/places/fordlandia).
- Distância Detroit–Fordlândia (~5.800 km em linha reta): calculada pelas coordenadas (Fordlândia 3,83° S, 55,50° W).
- **Fora do quadro de propósito:** o prejuízo da Ford e o preço da venda (as fontes divergem: de US$ 9 a 20 milhões de prejuízo; de US$ 250 mil a 500 mil na venda) e o ano da mudança para Belterra (1933, 1934 ou 1936). Para o vídeo real, `VERIFICAR` no livro *Fordlândia*, de Greg Grandin (2009).

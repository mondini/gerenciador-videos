# Protótipo 3: "O caminho de um Pix" (arte conceito)

Teste de visual do canal [Brasil por dentro](../../canais/brasil-por-dentro.md): um quadro só, para avaliar a cara da animação. Não é um vídeo final.

- `src/cena.ts`: tamanho do quadro, câmera isométrica, lugares da maquete e a rota do Pix.
- `src/Maquete.tsx`: a maquete em three.js (câmera ortográfica): base com corte de terra, ruas, prédios, árvores, carros e o pacote do Pix andando pela rota.
- `src/Pix.tsx`: a camada de infográfico em HTML/SVG por cima (título, etapas, rótulos presos aos prédios, mapa do Brasil com d3 e legenda palavra por palavra).
- `dados/brasil-uf.json`: malha dos estados do IBGE (API de malhas v3, qualidade mínima).

```bash
npm install
npm run studio   # prévia no navegador; a composição tem 5s e o Pix anda a rota toda
npm run arte     # gera out/arte-conceito.png (quadro 86)
```

## Resultado (15/10/2026)

- Quadro 1920x1080 renderizado em ~5s. Precisa de `--gl=angle` no Mac (sem isso o WebGL não abre).
- Tudo é animável a partir do número do quadro: o pacote anda pela rota, a linha se acende atrás dele, as etapas e os rótulos mudam de estado, a onda pulsa no Banco Central, o arco cresce no mapa.
- Textos do quadro são ilustrativos. Antes do vídeo real, conferir com o Banco Central: papel do DICT e do SPI, e o tempo de um Pix (`VERIFICAR`). A distância Porto Alegre–Manaus (~3.100 km em linha reta) foi calculada pelas coordenadas das capitais.

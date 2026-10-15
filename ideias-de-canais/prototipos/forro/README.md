# Protótipo 1: "Forró vem de *for all*? Não."

Teste de conceito do canal [Língua e costumes](../../canais/lingua-e-costumes.md) e do Remotion. Não é um vídeo final.

- `roteiro.json`: as cenas, com tipo, tempos e textos. É o arquivo que o pipeline em Python geraria.
- `src/Short.tsx`: um componente por tipo de cena (pergunta, mito, carimbo, encurta, prova, fim).

```bash
npm install
npm run studio   # prévia no navegador, com linha do tempo
npm run render   # gera out/forro.mp4 a partir do roteiro.json
```

## Resultado (14/10/2026)

- Short vertical 1080x1920, 30 fps, 23s, sem áudio. Render em ~20s no Mac.
- Funcionou: letras entrando uma a uma, máquina de escrever, traço que se desenha (risco e acento), carimbo com mola, contador de ano, palavra que encolhe ("forrobodó" → "forró").
- Tudo saiu do JSON: trocar o texto e renderizar de novo gera outro vídeo, sem mexer no código.
- Não testado: narração e sincronia palavra a palavra com os tempos da ElevenLabs; GSAP e d3 (não foram necessários).

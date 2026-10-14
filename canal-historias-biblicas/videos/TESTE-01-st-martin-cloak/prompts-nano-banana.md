# TESTE-01 — Prompts para o Nano Banana (teste de arte)

Roteiro aprovado em 14/10/2026. As 9 imagens da "Lista de imagens do teste de arte" do `roteiro.md`, **na ordem em que devem ser geradas** (as primeiras servem de referência para as seguintes).

## Como usar

- **Conversa A** (imagens 1 a 5 e 9): uma conversa só no Gemini, na ordem. Quando o prompt disser "anexe", envie a imagem indicada junto com o texto.
- **Conversa B** (imagens 6 a 8): uma conversa nova, anexando a imagem 1 como referência de estilo.
- Se o app deixar escolher entre **Nano Banana** e **Nano Banana Pro**, gere a imagem 1 nos dois e compare: isso decide o modelo do canal.
- Se a marca d'água visível estiver ligada, desligue em Configurações ("Media watermark"), se a opção existir na sua conta.
- Baixe cada imagem no tamanho máximo e salve em `videos/TESTE-01-st-martin-cloak/imagens/` com o nome indicado. Pode gerar 2 ou 3 versões de cada e guardar todas (`_v1`, `_v2`...).
- Copie o bloco inteiro de cada prompt, em inglês, como está.

### Descrição fixa dos personagens (já está dentro de cada prompt)

- **Martin:** young Roman cavalry soldier of the 4th century, about twenty years old, lean, short dark hair, clean-shaven, calm serious face; plain off-white wool tunic with long sleeves, dark brown trousers, simple leather boots, a simple iron ridge helmet (only when riding), a long **deep crimson wool cloak** fastened at the right shoulder with a round bronze brooch, a Roman long sword (spatha) in a plain leather scabbard.
- **Beggar:** thin elderly man, grey beard, bare shoulders and legs, wearing only a torn, faded loincloth-like rag, dignified despite poverty.

---

## 1 ⭐ Cena do portão (âncora de estilo) — Conversa A

Arquivo: `cena_portao-capa_v1.png`

```
Create a 16:9 landscape image.

A devotional watercolor painting in a sacred art style. Earthy palette of ochre, umber, muted olive and deep blue, with warm golden light. Visible brush strokes, soft watercolor paper texture, gentle color bleeding at the edges. Dignified, contemplative mood. Adult proportions and simple, serene faces. This must look like a painting from a sacred art book for adults, not a children's book illustration: no cartoon proportions, no big eyes, no bright saturated colors.

Scene: winter dusk at the stone gate of a Roman city in Gaul in the 4th century. Snow on the ground, light snow falling, a pale golden sky behind the gate. At the foot of the city wall sits a thin elderly beggar with a grey beard, bare shoulders and legs, wearing only a torn, faded rag, shivering. In front of him stands Martin, a young Roman cavalry soldier of about twenty, lean, short dark hair, clean-shaven, calm serious face, plain off-white wool tunic, dark brown trousers, leather boots. He is cutting his long deep crimson wool cloak in half with a Roman long sword, holding one half out toward the beggar. Behind Martin, his brown horse waits. Two passers-by in the middle distance, small and in soft shadow: one is laughing, one walks away with his back turned.

Composition: Martin and the beggar slightly left of center, the arched gate on the right, the crimson cloak as the strongest color in the image. No text, no letters, no signature, no watermark.
```

**Conferir:** parece pintura sacra e não livro infantil? A capa vermelha se destaca? O mendigo está digno?

---

## 2 ⭐ A mesma cena sem personagens — Conversa A (logo depois da 1)

Arquivo: `bg_portao-romano-amiens_v1.png`

```
Using the image you just created (or the attached image), create the exact same scene with all people and the horse removed. Keep the gate, the city wall, the sky, the snow, the light, the camera angle and the painting style exactly the same. Fill the areas where the figures were with the snowy ground and the stone wall, naturally. Add a few faint footprints in the snow in front of the wall. 16:9. No text, no letters, no watermark.
```

**Conferir:** o estilo se manteve igual? Ficaram restos dos personagens?

---

## 3 ⭐ Model sheet de Martinho — Conversa A

Arquivo: `martinho_model-sheet_v1.png` · anexe a imagem 1

```
Create a 16:9 character model sheet of Martin, the young soldier from the attached painting, in the same devotional watercolor style (earthy palette, warm golden light, visible brush strokes, soft paper texture, sacred art for adults, not a children's book).

Show the same man three times, side by side, full body, standing straight, same scale: front view, side profile view facing left, and back view. Martin: young Roman cavalry soldier of the 4th century, about twenty, lean, short dark hair, clean-shaven, calm serious face, plain off-white long-sleeved wool tunic, dark brown trousers, simple leather boots, long deep crimson wool cloak fastened at the right shoulder with a round bronze brooch, a Roman long sword in a plain leather scabbard at his left hip. No helmet.

Plain flat light warm-grey background, no shadow on the background, generous space between the three figures. No text, no labels, no letters, no watermark.
```

**Conferir:** é a mesma pessoa nas três vistas? Roupa e capa iguais às da imagem 1?

---

## 4a ⭐ Martinho a cavalo (perfil), isolado — Conversa A

Arquivo: `martinho_pose-cavalgando-perfil_v1.png` · anexe a imagem 3

```
Using the attached model sheet as the character reference, create a new image of the same Martin, with the same face, clothes and crimson cloak, now riding his brown horse at a slow walk, seen in side profile facing right. He wears a simple iron Roman ridge helmet, the crimson cloak flows behind him over the horse. Calm, upright posture.

Same devotional watercolor style: earthy palette, warm golden light, visible brush strokes, soft paper texture, sacred art for adults, not a children's book.

Single subject (rider and horse together), whole figure inside the frame with margin on all sides, on a plain flat light warm-grey background, no shadow on the background. 4:3 landscape. No text, no letters, no watermark.
```

---

## 4b ⭐ Martinho entregando a meia capa, isolado — Conversa A

Arquivo: `martinho_pose-entregando-capa_v1.png` · anexe a imagem 3

```
Using the attached model sheet as the character reference, create a new image of the same Martin, with the same face and clothes, standing in three-quarter view facing right, slightly bending forward, holding out one half of his deep crimson cloak with both hands, offering it to someone outside the frame. The other half of the cloak still hangs from his right shoulder, with a rough cut edge. His sword is back in its scabbard. Gentle, humble expression.

Same devotional watercolor style: earthy palette, warm golden light, visible brush strokes, soft paper texture, sacred art for adults, not a children's book.

Single subject, full body inside the frame with margin on all sides, on a plain flat light warm-grey background, no shadow on the background. 3:4 portrait. No text, no letters, no watermark.
```

**Conferir (4a e 4b):** o rosto e a roupa continuam os do model sheet? As bordas da aquarela estão limpas contra o fundo cinza?

---

## 5 Mendigo isolado — Conversa A

Arquivo: `mendigo_pose-sentado-encolhido_v1.png` · anexe a imagem 1

```
Using the beggar from the attached painting as the reference, create the same thin elderly man with a grey beard, sitting on the ground hugging his knees, shivering from the cold, wearing only a torn, faded rag, bare shoulders and legs. Head slightly lowered, eyes tired but dignified. Three-quarter view facing left.

Same devotional watercolor style: earthy palette, warm golden light, visible brush strokes, soft paper texture, sacred art for adults, not a children's book.

Single subject, whole figure inside the frame with margin on all sides, on a plain flat light warm-grey background, no shadow on the background. 1:1 square. No text, no letters, no watermark.
```

---

## 9 Comparação de recorte: fundo verde chapado — Conversa A

Arquivo: `martinho_pose-entregando-capa_verde_v1.png` · anexe a imagem 4b

```
Create the exact same image as the attached one, same character, same pose, same painting style, but on a perfectly flat, uniform pure chroma green background (#00B140), with no texture, no gradient and no shadow on the background. 3:4 portrait. No text, no letters, no watermark.
```

**Conferir:** compare a 4b com a 9. O Claude vai recortar as duas e mostrar qual borda fica melhor.

---

## 6 ⭐ A visão: Cristo com a meia capa — Conversa B

Arquivo: `cena_visao-cristo-meia-capa_v1.png` · anexe a imagem 1 como referência de estilo

```
Create a 16:9 landscape image in the same devotional watercolor style as the attached painting: earthy palette, visible brush strokes, soft paper texture, sacred art for adults, not a children's book.

Scene: a night vision of heavenly light. In the center stands Christ, seen from behind in three-quarter rear view, so his face is NOT visible; his head is surrounded by an intense soft golden light. He wears a long plain white robe and, over his shoulders, half of a deep crimson wool cloak with a rough cut edge, the same cloak as in the reference. Around him, at a respectful distance, stand three tall adult angels with large feathered wings, serene and dignified, their faces in soft shadow against the light. No infant cherubs, no childlike angels.

The background is a deep night blue that opens into warm golden light behind Christ, with fine floating specks of light. The crimson half cloak must be clearly recognizable. No text, no letters, no halo with writing, no watermark.
```

**Conferir:** o rosto de Cristo fica de fato escondido? A meia capa é reconhecível? Os anjos são adultos e sérios?

---

## 7 ⭐ Moldura de iluminura vazia (cartão do santo) — Conversa B

Arquivo: `card_moldura-iluminura-santo_v1.png`

```
Create a 16:9 landscape image: an ornate medieval illuminated manuscript page border, in the style of a 14th-century book of hours, painted with gold leaf, lapis blue and deep crimson on aged warm parchment. The decorated border runs around all four edges, with gentle vine scrolls and, woven into the ornament, small painted symbols: a Roman sword, a crimson cloak, a brown horse and a rising sun.

The large center area must be completely EMPTY plain parchment, with no writing, no letters, no initials, no fake text and no figures, because a title will be added later. Flat front view, the page fills the whole frame. No watermark.
```

**Conferir:** o centro ficou vazio, sem letras inventadas? Tem cara de iluminura de verdade?

---

## 8 ⭐ Vitral de São Martinho — Conversa B

Arquivo: `vitral_martinho-capa_v1.png`

```
Create a 16:9 landscape image: a Gothic stained glass window seen from inside a dim stone church, with warm light shining through the glass. The tall arched window is centered and fills most of the frame, with dark stone around it.

The window shows the classic scene of Saint Martin of Tours on horseback, a young Roman soldier, cutting his crimson cloak in half with his sword to share it with a poor man sitting at a city gate. Traditional medieval stained glass: bold dark lead lines, jewel tones of ruby red, cobalt blue, emerald and amber, flat shapes with simple painted details, simple serene adult faces. Sacred art for adults, not a children's illustration.

No text, no letters, no inscription in the glass, no watermark.
```

**Conferir:** parece vitral de igreja? Combina com as aquarelas como se fosse do mesmo canal?

---

## Se algo sair errado

| Problema | O que pedir na mesma conversa |
|---|---|
| Ficou com cara de livro infantil | `Make it look like a classical sacred watercolor painting for adults: more muted earthy colors, realistic adult proportions, less saturated, more visible paper texture.` |
| Apareceu texto ou letras | `Remove all text, letters and writing from the image. Keep everything else identical.` |
| Rosto de Cristo visível | `Turn the figure further away from the viewer so the face is completely hidden, and make the golden light around the head stronger.` |
| Martinho mudou de rosto ou de roupa | Anexe de novo o model sheet: `Keep the face, hair, tunic and crimson cloak exactly as in the attached reference.` |
| Fundo cinza com sombra ou textura | `Make the background a perfectly flat, plain light warm-grey with no shadow, no texture and no gradient.` |

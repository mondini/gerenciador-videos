# Style bible (rascunho até o piloto)

Fonte da verdade da consistência visual. O prompt base, a paleta e o modelo de imagem só ficam fechados depois do teste de arte do piloto; até lá, tudo aqui é ponto de partida.

## Estilos

| Onde | Estilo |
|---|---|
| Cenas (base) | **Aquarela devocional:** tons terrosos, luz dourada, pinceladas visíveis, textura de papel, aspecto de pintura sacra. **Não** de livro infantil |
| Santos e cartões de versículo | **Iluminura / ícone**, com molduras decorativas |
| Aberturas, transições e fechamentos | **Vitral** |

- No piloto, validar só a aquarela e uma transição em vitral; a iluminura entra quando houver um santo.
- "Boho": cortado até haver exemplos concretos (o termo é vago e faz o estilo variar). Se voltar, definir com imagens de referência.

## Pessoas

- Proporções adultas e realistas, rostos simples e serenos, ou perfil, sombra e silhueta. A emoção vem da luz, do céu e da composição, não da expressão facial.
- Evitar rostos ultrarrealistas de IA.
- Planos por personagem: corpo inteiro (distante), médio, silhueta.
- Regras de Jesus, Maria, Deus Pai, Espírito Santo, Eucaristia e anjos: `doutrina-e-fontes.md`.
- Cada personagem fixo tem um **model sheet** (frente, perfil, costas) usado como imagem de referência nas poses seguintes.

## Geração (Gemini, à mão pelo criador)

- **Modelo:** a definir no piloto (Nano Banana ou Nano Banana Pro). Registrar aqui; trocar de modelo muda o estilo.
- **Fluxo por cena:** (1) a cena inteira, para aprovar a composição; (2) pedir ao Gemini a mesma cena **sem os personagens** (fundo limpo); (3) cada personagem e objeto isolado em **fundo neutro claro e liso**, usando a cena como referência. O Claude recorta os elementos e monta as camadas.
- **Fundo para recorte:** neutro claro liso + recorte com BiRefNet (rembg). O fundo chapado verde ou magenta deixa halo nas bordas suaves da aquarela, e as duas cores se confundem com vegetação e com vestes litúrgicas. Comparar as duas abordagens no piloto (5 imagens cada) e registrar o resultado aqui.
- **Nenhum texto, letra ou marca na imagem.** Texto na tela é desenhado na montagem.
- Na montagem, uma textura de papel e grão por cima de tudo faz as camadas parecerem uma pintura só, e não recortes colados.

### Prompt base (rascunho)

```
Devotional watercolor painting in a sacred art style. Earthy palette (ochre, umber, muted olive, deep blue), warm golden light, visible brush strokes, soft watercolor paper texture. Dignified, contemplative mood. Adult proportions, simple serene faces. No text, no letters, no watermark.
```

Para elementos isolados, acrescentar:

```
Single subject, full figure inside the frame with margin, on a plain flat light warm-grey background, no shadow on the background.
```

## Animação

- Troca de poses + câmera lenta (zoom/pan) + parallax suave entre camadas + partículas leves (poeira de luz, nuvens). Animação de membros só no futuro, se necessário.
- Parallax: com camadas separadas (padrão). Mapa de profundidade (Depth Anything) só para cenas que são uma pintura inteira, como os vitrais.
- Cenas de 8 a 15 s, ritmo calmo.

## Biblioteca de assets

- Gerar só o que o roteiro pede; antes de pedir arte nova, procurar no catálogo.
- Meta inicial, conforme os roteiros exigirem: ~15–20 personagens × 5–6 poses, ~100 itens de cena, fundos modulares em camadas (céu, colinas, plano médio, primeiro plano).
- **Nomenclatura:** `personagem_pose-descricao_v1.png` (ex.: `maria_pose-orando_v1.png`), `prop_tabuas-da-lei_v1.png`, `bg_entardecer-deserto_v1.png`.
- **Catálogo:** `biblioteca/catalogo.json`, com nome, tipo, tags, status, prompt usado, modelo e data de geração.

## Santos e atributos

| Santo | Atributos fixos | Registrado em |
|---|---|---|
| (vazio) | | |

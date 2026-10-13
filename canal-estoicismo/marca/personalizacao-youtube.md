# Personalização do canal no YouTube

Tudo o que a tela **YouTube Studio › Personalização** pede. Imagens geradas por `python3 gerar_marca.py`
(nesta pasta), seguindo o Design System do canal.

## Aba "Perfil"

| Campo | O que usar |
|---|---|
| Imagem do banner | `banner.png` (2560 × 1440; texto e logo dentro da área segura de 1546 × 423) |
| Foto | `foto-perfil.png` (800 × 800) |
| Marca d'água do vídeo | `marca-dagua.png` (150 × 150, fundo transparente). Exibir: **Fim do vídeo** |
| Nome | `Marble & Ash` |
| Identificador | `@marbleandashwisdom` |
| Descrição | texto abaixo |
| Links | nenhum por enquanto |
| Informações de contato | e-mail do canal (a definir pelo criador) |

### Descrição (835 caracteres; limite 1000)

```
Old wisdom for quiet hours.

Marble & Ash is a slow, calm channel about Stoic philosophy, built around Marcus Aurelius and his Meditations, with a quiet thread of the Book of Proverbs running through. Two old voices that, centuries apart, kept arriving at the same truths.

Each week, one quiet essay of about ten minutes: a story from Marcus's life, his own words, and what they mean for an ordinary day of work, money, worry and people. Every episode has The Pause, a short moment to breathe and turn the idea into practice.

Made for slow listening: while you clean the house, walk, train, or wind down for sleep. No shouting, no hype, no promises of riches. Just old wisdom, read slowly.

Texts are public-domain translations: Meditations in George Long's translation, Proverbs from the World English Bible.

New essays every week.
```

## Aba "Layout"

- **Trailer do canal** e **vídeo em destaque**: deixar vazio até o MA-001 ser publicado. Depois, MA-001 como
  vídeo em destaque para quem volta ao canal.
- **Seções em destaque**: deixar as padrão. Criar playlists quando houver 3 ou mais vídeos.

## Padrões de upload › Descrição

Modelo que o YouTube coloca em todo upload novo. As partes fixas vêm da descrição do MA-001. O que está
entre `[[ ]]` muda a cada vídeo e sai pronto no pacote de publicação (seção 3); o upload não pode ir ao ar
com nenhum `[[` sobrando. O link usa o identificador `@marbleandashwisdom`.

```
[[TWO STRONG OPENING LINES: they show before "...more"]]

[[SUMMARY: what the episode reads and why it matters today, without giving away the ending]]

Made for slow listening: while you clean the house, take a walk, or try to fall asleep. There is a short guided pause in the middle, a moment to breathe and answer one question for yourself.

CHAPTERS
00:00 [[CHAPTER]]
[[MM:SS CHAPTER]]

SOURCES (all public domain)
- Marcus Aurelius, Meditations [[BOOK.SECTION, ...]], translated by George Long (1862). Text: MIT Internet Classics Archive, classics.mit.edu/Antoninus/meditations.html
- Proverbs [[CHAPTER:VERSE, ...]], World English Bible (public domain). worldenglish.bible
[[OTHER SOURCES, OR DELETE THIS LINE]]

CREDITS
Narration voice generated with ElevenLabs. Script, shadow-theatre animation and ambient sound: Marble & Ash. Fonts: Cinzel, Cormorant Garamond, Inter and GFS Baskerville (SIL Open Font License).

[[ONLY IF THE EPISODE MENTIONS MONEY: Educational content, not financial advice.]]

If this helped you slow down tonight, you can subscribe for one quiet episode at a time: https://www.youtube.com/@marbleandashwisdom?sub_confirmation=1

#Stoicism #MarcusAurelius #Meditations
```

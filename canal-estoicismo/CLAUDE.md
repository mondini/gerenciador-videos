# Canal Marble & Ash (estoicismo) — instruções para o Claude

Esta pasta guarda tudo o que é preciso para produzir os vídeos do canal **Marble & Ash**. O trabalho é feito **uma sessão por vídeo**.

## Comece por aqui
1. `docs/plano-canal.md` — decisões do canal, regras fixas, os 12 vídeos.
2. `docs/estilo-teatro-de-sombras.md` — padrão visual aprovado dos vídeos.
3. `docs/fluxo-por-video.md` — passo a passo de cada sessão.
4. `docs/pacote-de-publicacao-regras.md` — o pacote obrigatório ao concluir cada vídeo.
5. `videos/video-NN/roteiro.md` — roteiro e status do vídeo da sessão.
6. `pipeline/LEIA-ME.md` — como usar o código de montagem.

## Sobre o criador
- Brasileiro; toda conversa e documentação em **pt-BR**. Tudo o que é público no canal sai em **inglês natural**.
- Gosta de construir o roteiro aos poucos, com perguntas, e de aprovar um frame antes de renderizar cenas novas.
- Gera a narração no ElevenLabs v4 (plano Starter), voz de senhor ~70 anos.

## Estrutura da pasta
- `docs/` — plano, estilo, fluxo e regras do pacote.
- `pipeline/` — código Python que gera os vídeos (teatro de sombras projetadas): biblioteca `marbleash/` e a linha de comando (`./ma` na pasta do canal).
- `fontes-tipograficas/` — Cinzel, Cormorant Garamond (e Cormorant, usada no bloco 1 aprovado), Inter (créditos) e GFS Baskerville (grego); todas com licença OFL (arquivos OFL-*.txt).
- `videos/video-NN/` — `roteiro.md`, `audio/`, `blocoN/` (script de cena `cena.py`, deixas `tempos.txt`, análise `audio.json`), `trabalho/` (intermediários), `previas/`, `final/`, `pacote-de-publicacao.md`.

## Regras rápidas
- **Design System sempre:** toda peça visual (vídeo, thumbs, textos na tela, shorts) segue o Design System do canal feito no Claude Design (https://claude.ai/artifact/YD1Vx9JHfUSKFFVMcdkQqh): paleta, tipografia e logo. Na dúvida, consultar antes de criar. Todo o trabalho fica centralizado nesta pasta.
- Só material de domínio público (Meditações: George Long; Provérbios: World English Bible). Crédito na tela, sempre.
- Nunca inventar fonte, versículo, link ou licença.
- Áudios e vídeos são arquivos grandes: ficam fora do git (ver `.gitignore` desta pasta).

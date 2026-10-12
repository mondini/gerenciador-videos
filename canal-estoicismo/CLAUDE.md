# Canal Marble & Ash (estoicismo) — instruções para o Claude

Esta pasta guarda tudo o que é preciso para produzir os vídeos do canal **Marble & Ash**. O trabalho é feito **uma sessão por vídeo**.

> **O canal não é o sistema.** O sistema de gestão (`src/`, `docs/` na raiz, TypeScript) é outro projeto, que só divide o repositório. As regras dele (escopo da v0.1, stack TypeScript, `/grill-me`, `docs/requisitos.md`) **não** valem aqui. Do `CLAUDE.md` da raiz, só a seção "Regras comuns" se aplica. O canal só conversa com o sistema por `./ma sincronizar` (API). Decisões do canal vão para `docs/plano-canal.md`, nunca para `../docs/decisoes.md`.

## Comece por aqui
1. `docs/plano-canal.md` — decisões do canal, regras fixas, os 12 vídeos.
2. `docs/estilo-teatro-de-sombras.md` — padrão visual aprovado dos vídeos.
3. `docs/fluxo-por-video.md` — passo a passo de cada sessão.
4. `docs/pacote-de-publicacao-regras.md` — o pacote obrigatório ao concluir cada vídeo.
   - `docs/guia-embalagem-youtube.md` — **manual de referência** para títulos, thumbnails, descrição, metadados e retenção. Use sempre que for criar ou revisar qualquer um desses itens (roteiro, gancho, Pacote de Publicação, shorts). Quando o guia conflitar com uma decisão já registrada do canal, aponte o conflito ao criador em vez de decidir sozinho.
5. `videos/MA-NNN-slug/roteiro.md` — roteiro do vídeo da sessão. O status sai de `./ma status N`.
6. `pipeline/LEIA-ME.md` — como usar o código de montagem.

## Sobre o criador
- Brasileiro; toda conversa e documentação em **pt-BR**. Tudo o que é público no canal sai em **inglês natural**.
- Gosta de construir o roteiro aos poucos, com perguntas. **Não** quer aprovar stills cena por cena (12/10/2026): conferir os stills internamente, renderizar e entregar o vídeo para revisão.
- Gera a narração no ElevenLabs (plano Starter), voz *Flint — Deep, Raspy, and Warm*, Eleven v4 (detalhes e custo em créditos em `docs/plano-canal.md`).

## Estrutura da pasta
- `docs/` — plano, estilo, fluxo e regras do pacote.
- `pipeline/` — código Python que gera os vídeos (teatro de sombras projetadas): biblioteca `marbleash/` e a linha de comando (`./ma` na pasta do canal).
- `fontes-tipograficas/` — Cinzel, Cormorant Garamond (e Cormorant, usada no bloco 1 aprovado), Inter (créditos) e GFS Baskerville (grego); todas com licença OFL (arquivos OFL-*.txt).
- `canal.json` — nome, prefixo do código (`MA`) e pasta do canal no Drive (`MA - Marble & Ash`).
- `videos/MA-NNN-slug/` — uma pasta por vídeo, com código + slug do nome interno (ex.: `MA-001-the-man-who-had-everything`), o mesmo nome no Drive e no sistema. Dentro: `roteiro.md`, `audio/`, `blocoN/` e `pausa/` (script de cena `cena.py`, deixas `tempos.txt`, análise `audio.json`), `trabalho/` (intermediários), `previas/`, `final/`, `thumbnails/` (A e C), `shorts/`, `pacote-de-publicacao.md`. Nos comandos, o vídeo pode ser `1`, `MA-001` ou a pasta inteira.
- `videos/comum/` — peças sem narração iguais em todos os vídeos (abertura, encerramento).

## Regras rápidas
- **Design System sempre:** toda peça visual (vídeo, thumbs, textos na tela, shorts) segue o Design System do canal feito no Claude Design (https://claude.ai/artifact/YD1Vx9JHfUSKFFVMcdkQqh): paleta, tipografia e logo. Resumo em `docs/identidade-visual.md`; na dúvida, consultar o original antes de criar. Todo o trabalho fica centralizado nesta pasta.
- Só material de domínio público (Meditações: George Long; Provérbios: World English Bible). Crédito na tela, sempre.
- Nunca inventar fonte, versículo, link ou licença.
- Áudios e vídeos são arquivos grandes: ficam fora do git (ver `.gitignore` desta pasta) e vão para o Drive pelo `./ma backup`.

## Status, commits, backup e limpeza (autorizados pelo criador em 12/10/2026)
- **Status:** não escreva tabela de status à mão. Ele vem dos arquivos: `./ma status N` mostra o que existe, o que falta, a etapa do kanban e os créditos do ElevenLabs. O único sinal escrito à mão é o título da seção do roteiro: `## Bloco 2 — O homem (aprovado)`. No `roteiro.md`, mantenha só decisões e notas de produção.
- **Fechar um bloco** = o criador aprovou o texto de um bloco OU a prévia renderizada de um bloco. Nesse momento, **sem pedir**: (1) marcar `(aprovado)` no título da seção, se for o texto; (2) `./ma fechar N` (backup no Drive + sincronizar com o sistema; se o sistema não estiver rodando, avise e siga); (3) **commit** só dos arquivos do canal, `feat(canal-estoicismo): MA-NNN bloco X …`, seguido de **push**.
- **Backup:** automático depois de `./ma audio` (o mp3 pago) e `./ma juntar` (o final). Além disso, `./ma fechar N` ao fechar um bloco, ao entregar thumbnails/shorts/pacote e no fim de toda sessão.
- **Vídeo concluído** (`./ma status` diz CONCLUÍDO): rode `./ma limpar N --apagar` **sem pedir**. Ele refaz o backup e tira do Mac só o que tem cópia no Drive ou é refeito pelo pipeline (`trabalho/`, prévias, stills, simulações). Roteiro, áudios, scripts, final, thumbs, shorts e pacote ficam. Nunca apague nada no Drive.

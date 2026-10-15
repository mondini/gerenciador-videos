# Canal Marble & Ash (estoicismo) — instruções para o Claude

Esta pasta guarda tudo o que é preciso para produzir os vídeos do canal **Marble & Ash**. O trabalho é feito **uma sessão por vídeo**.

> Regras gerais (valem para todos os canais): `CLAUDE.md` da raiz. Aqui ficam só a ficha e as regras deste canal. Todo o trabalho fica nesta pasta; fora dela, só ler o `CLAUDE.md` e a pasta `docs/` da raiz e o `.env` da raiz. Decisões do canal vão para `docs/plano-canal.md`.

## Ficha do canal

| Campo | Valor |
|---|---|
| Nome | Marble & Ash (*Old wisdom for quiet hours.*) |
| Tema | Estoicismo (Marco Aurélio, *Meditações*) cruzado com Provérbios; toque leve de trabalho, finanças e liderança |
| Público | EUA, Reino Unido e Canadá; *slow learning* (ouvir limpando a casa, se exercitando ou para dormir) |
| Idioma público | Inglês |
| YouTube | `@marbleandashwisdom` |
| Prefixo e Drive | `MA` · `MA - Marble & Ash` (`canal.json`) |
| Formato | ~10 min, teatro de sombras projetadas, narração lenta; 5 shorts por vídeo |
| Cadência | 1 vídeo por semana, quintas 14:00 ET (`docs/plano-canal.md`) |
| Narração | ElevenLabs, voz Flint, Eleven v4, modo `site` (`elevenlabs.json`) |
| Ferramentas | Pipeline Python `./ma` (`pipeline/LEIA-ME.md`); Design System no Claude Design |
| Fase | Em produção; o status de cada vídeo sai de `./ma status N` |
| Documentos | `docs/plano-canal.md`, `docs/estilo-teatro-de-sombras.md`, `docs/fluxo-por-video.md`, `docs/pacote-de-publicacao-canal.md` |

## Comece por aqui
1. `docs/plano-canal.md` — decisões do canal, regras fixas, os 12 vídeos.
2. `docs/estilo-teatro-de-sombras.md` — padrão visual aprovado dos vídeos.
3. `docs/fluxo-por-video.md` — passo a passo de cada sessão.
4. Pacote de publicação, obrigatório ao concluir cada vídeo: base comum em `../docs/pacote-de-publicacao.md` + complemento do canal em `docs/pacote-de-publicacao-canal.md`.
   - `../docs/guia-embalagem-youtube.md` (comum a todos os canais) — **manual de referência** para títulos, thumbnails, descrição, metadados e retenção. Use sempre que for criar ou revisar qualquer um desses itens (roteiro, gancho, Pacote de Publicação, shorts). Quando o guia conflitar com uma decisão já registrada do canal, aponte o conflito ao criador em vez de decidir sozinho.
5. `videos/MA-NNN-slug/roteiro.md` — roteiro do vídeo da sessão. O status sai de `./ma status N`.
6. `pipeline/LEIA-ME.md` — como usar o código de montagem.

## Sobre o criador
- Brasileiro; toda conversa e documentação em **pt-BR**. Tudo o que é público no canal sai em **inglês natural**.
- Gosta de construir o roteiro aos poucos, com perguntas. **Não** quer aprovar stills cena por cena nem prévia bloco a bloco (12/10/2026): conferir os stills internamente, renderizar todos os blocos, montar o vídeo e entregar **uma revisão só**, do vídeo inteiro.
- Gera a narração no ElevenLabs (plano Starter), voz *Flint — Deep, Raspy, and Warm*, Eleven v4. Configuração em `elevenlabs.json`; regras da narração (chave, confirmação e custo antes de gerar) no `CLAUDE.md` da raiz. Histórico e custo medido em `docs/plano-canal.md`.

## Estrutura da pasta
- `docs/` — plano, estilo, fluxo, identidade visual e complemento do pacote.
- `pipeline/` — código Python que gera os vídeos (teatro de sombras projetadas): biblioteca `marbleash/` e a linha de comando (`./ma` na pasta do canal).
- `fontes-tipograficas/` — Cinzel, Cormorant Garamond (e Cormorant, usada no bloco 1 aprovado), Inter (créditos) e GFS Baskerville (grego); todas com licença OFL (arquivos OFL-*.txt).
- `canal.json` — nome, prefixo do código (`MA`), pasta do canal no Drive (`MA - Marble & Ash`) e o comando de status do painel (`./ma status --json`).
- `elevenlabs.json` — configuração da narração (regras no `CLAUDE.md` da raiz).
- `creditos-elevenlabs.csv` — um registro por geração de narração (medido pelo saldo, com `./canais creditos` na raiz).
- `calendario.json` — datas de publicação do vídeo longo e dos shorts, lidas pelo painel da raiz (`./canais`). Atualizar sempre que uma data for decidida ou mudar, e marcar `agendado` quando o criador programar no Studio.
- `videos/MA-NNN-slug/` — uma pasta por vídeo, com código + slug do nome interno (ex.: `MA-001-the-man-who-had-everything`), o mesmo nome no Drive. Dentro: `roteiro.md`, `audio/`, `blocoN/` e `pausa/` (script de cena `cena.py`, deixas `tempos.txt`, análise `audio.json`), `trabalho/` (intermediários), `previas/`, `final/`, `thumbnails/` (A, B e C), `shorts/`, `pacote-de-publicacao.md`. Nos comandos, o vídeo pode ser `1`, `MA-001` ou a pasta inteira.
- `videos/comum/` — peças sem narração iguais em todos os vídeos (abertura, encerramento).

## Regras rápidas
- **Design System sempre:** toda peça visual (vídeo, thumbs, textos na tela, shorts) segue o Design System do canal feito no Claude Design (https://claude.ai/artifact/YD1Vx9JHfUSKFFVMcdkQqh): paleta, tipografia e logo. Resumo em `docs/identidade-visual.md`; na dúvida, consultar o original antes de criar. Todo o trabalho fica centralizado nesta pasta.
- Só material de domínio público (Meditações: George Long; Provérbios: World English Bible). Quando o tema pedir outra obra ou tradução, procure a melhor tradução em domínio público e proponha ao criador, que valida (ver regra 1 do plano). Crédito na tela, sempre.
- Nunca inventar fonte, versículo, link ou licença.
- Áudios e vídeos são arquivos grandes: ficam fora do git (ver `.gitignore` desta pasta) e vão para o Drive pelo `./ma backup`.

## Status, commits, backup e limpeza (autorizados pelo criador em 12/10/2026)
- **Status:** não escreva tabela de status à mão. Ele vem dos arquivos: `./ma status N` mostra o que existe, o que falta, a etapa e os créditos do ElevenLabs. O único sinal escrito à mão é o título da seção do roteiro: `## Bloco 2 — O homem (aprovado)`. No `roteiro.md`, mantenha só decisões e notas de produção.
- **Fechar um bloco** = o criador aprovou o texto de um bloco OU o vídeo montado (revisão única, que fecha todos os blocos de uma vez). Nesse momento, **sem pedir**: (1) marcar `(aprovado)` no título da seção, se for o texto; (2) `./ma backup N`. **Commit e push só quando o criador pedir** (regra geral de 14/10/2026).
- **Backup:** automático depois de `./ma audio` (o mp3 pago) e `./ma juntar` (o final). Além disso, `./ma backup N` ao fechar um bloco, ao entregar thumbnails/shorts/pacote e no fim de toda sessão.
- **Vídeo concluído** (`./ma status` diz CONCLUÍDO): rode `./ma limpar N --apagar` **sem pedir**. Ele refaz o backup e tira do Mac só o que tem cópia no Drive ou é refeito pelo pipeline (`trabalho/`, prévias, stills, simulações). Roteiro, áudios, scripts, final, thumbs, shorts e pacote ficam. Nunca apague nada no Drive.

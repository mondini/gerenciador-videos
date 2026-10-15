# Canal de histórias católicas animadas — instruções para o Claude

Esta pasta guarda tudo o que é preciso para produzir os vídeos do canal (nome ainda **a definir**, ver `docs/plano-canal.md`). O trabalho é feito **uma sessão por vídeo**.

> Regras gerais (valem para todos os canais): `CLAUDE.md` da raiz. Aqui ficam só a ficha e as regras deste canal. **Todo o trabalho fica nesta pasta**; fora dela, só ler o `CLAUDE.md` e a pasta `docs/` da raiz e o `.env` da raiz. Nada de reaproveitar arquivos de outro canal sem o criador pedir. Decisões do canal vão para `docs/plano-canal.md`.

## Ficha do canal

| Campo | Valor |
|---|---|
| Nome | A definir (`docs/plano-canal.md`) |
| Tema | Fé católica contada em histórias: santos, parábolas, os 10 Mandamentos, versículos e salmos explicados |
| Público | Adultos 50+ dos EUA, Reino Unido e Canadá. **Nunca infantil** |
| Idioma público | Inglês |
| YouTube | A criar |
| Prefixo e Drive | A definir; `canal.json` é criado quando o nome for escolhido |
| Formato | 8 a 12 min, 16:9, one-line art animado; sem shorts por enquanto |
| Cadência | 1 vídeo por semana; pauta guiada pelo calendário litúrgico |
| Narração | ElevenLabs, Eleven v4, modo `api`; voz a escolher no piloto (`elevenlabs.json`) |
| Ferramentas | Pipeline Python (`pipeline/`) + um HTML/SVG por cena, renderizado em Chrome sem tela |
| Fase | Piloto (`videos/TESTE-01-st-martin-cloak/`) |
| Documentos | `docs/plano-canal.md`, `docs/doutrina-e-fontes.md`, `docs/estilo-visual.md`, `docs/fluxo-por-video.md`, `docs/pacote-de-publicacao-canal.md`, `docs/glossario-pronuncia.md` |

## Comece por aqui
1. `docs/plano-canal.md` — decisões do canal, cadência, formatos, ferramentas, próximos passos.
2. `docs/doutrina-e-fontes.md` — traduções permitidas, Catecismo, representação de pessoas sagradas, checklist doutrinário.
3. `docs/estilo-visual.md` — style bible do one-line art: traço, paleta, fundos, símbolos, animação, formato das cenas.
4. `docs/fluxo-por-video.md` — passo a passo de cada sessão, backup e limpeza.
5. Pacote de publicação, obrigatório ao concluir cada vídeo: base comum em `../docs/pacote-de-publicacao.md` + complemento do canal em `docs/pacote-de-publicacao-canal.md`.
   - `../docs/guia-embalagem-youtube.md` (comum a todos os canais) — manual de referência para títulos, thumbnails, descrição, metadados e retenção. Quando conflitar com uma decisão do canal, aponte o conflito ao criador em vez de decidir sozinho.
6. `docs/glossario-pronuncia.md` — nomes bíblicos e latim para a narração.

## Sobre o criador
- Brasileiro; toda conversa e documentação em **pt-BR**. Tudo o que é público no canal (roteiro, narração, títulos, textos na tela) sai em **inglês natural**.
- Trabalha sozinho, com orçamento limitado: preferir o que é gratuito ou já pago.
- Gosta de construir o roteiro aos poucos, com perguntas. Não quer aprovar stills cena por cena nem prévia bloco a bloco: conferir internamente, montar o vídeo e entregar **uma revisão só**, do vídeo inteiro.

## Regras rápidas
- **Nunca infantil.** O público é adulto, 50+. Nada de títulos, roteiros ou animações com cara de conteúdo para crianças: sem proporções de desenho (cabeça e olhos grandes), sem paleta primária saturada, sem mascotes, sem rimas ou tom cantado, sem "little ones"/"kids", sem moral simplista, sem título cheio de exclamações. Na dúvida, perguntar.
- **Doutrina:** só traduções em domínio público (padrão: Douay-Rheims, revisão Challoner; nunca KJV); doutrina pelo Catecismo, com o número do parágrafo; numeração católica dos Mandamentos; na arte, ninguém tem rosto, e Jesus, Maria e Deus Pai seguem regras próprias de representação. Detalhes em `docs/doutrina-e-fontes.md`.
- **Nunca inventar** citação, versículo, fonte, link ou licença. Se não der para conferir a redação em domínio público, marcar `VERIFICAR`.
- **Promessa do canal:** ordem, liberdade e paz. Nunca prometer prosperidade, cura ou vida fácil.
- **Calendário litúrgico** orienta a pauta: ao sugerir temas, vídeos e roteiros, considerar festas e tempos litúrgicos próximos (`docs/plano-canal.md`).
- **Um vídeo, uma história própria.** Cada roteiro precisa de arco narrativo e virada próprios (política de conteúdo inautêntico do YouTube). Nada de vídeo-modelo com o nome trocado.
- **Arte:** one-line art desenhado pelo Claude em SVG/HTML, um arquivo por cena; o tema vem por símbolos, pessoas só como silhuetas sem rosto (`docs/estilo-visual.md`). Não usar geradores de imagem nem pinturas de acervo.
- Para qualquer afirmação sobre preços, licenças ou políticas atuais (YouTube, ElevenLabs, bancos de música), pesquisar antes de afirmar.
- Áudios e vídeos (vídeos das cenas, final) são arquivos grandes: ficam fora do git (`.gitignore` desta pasta) e vão para o Drive pelo backup.

## Estrutura da pasta (prevista; criada conforme o uso)
- `docs/` — plano, doutrina, estilo, fluxo, complemento do pacote, glossário.
- `canal.json` — nome, prefixo do código e pasta do canal no Drive (criado quando o nome for escolhido). Quando o pipeline tiver status, incluir `"status"` com o comando que imprime o JSON do painel (contrato no `CLAUDE.md` da raiz); até lá o painel estima a etapa pelas pastas.
- `elevenlabs.json` — configuração da narração (regras no `CLAUDE.md` da raiz).
- `creditos-elevenlabs.csv` — um registro por geração de narração (criar na primeira gravação; formato no `CLAUDE.md` da raiz).
- `calendario.json` — datas de publicação, lidas pelo painel da raiz (`./canais`); criar quando a primeira data for decidida.
- `biblioteca/elementos/` — trechos SVG reutilizáveis (sol, nuvem, oliveira, cruz, silhuetas, atributos de santos).
- `pipeline/` — código Python: narração, sons, legendas, backup.
- `videos/XX-NNN-slug/` — uma pasta por vídeo, com código + slug (o mesmo nome no Drive). Dentro: `roteiro.md`, `audio/`, `cenas/` (um HTML por cena), `montagem.json`, `gravacoes/` (vídeo de cada cena), `trabalho/` (intermediários), `final/`, `thumbnails/`, `pacote-de-publicacao.md`.

## Commits, backup e limpeza (autorizados pelo criador em 14/10/2026, mesma base do outro canal)
- **Fechar um bloco** = o criador aprovou o texto de um bloco OU o vídeo montado (revisão única, que fecha todos os blocos). Nesse momento, **sem pedir**: (1) marcar `(aprovado)` no título da seção do roteiro, se for texto; (2) backup no Drive; (3) **commit** só dos arquivos desta pasta, `feat(canal-historias-biblicas): XX-NNN bloco X …`, seguido de **push**.
- **Fim de sessão:** backup, commit e push do que mudou no canal. Fora desses casos, commit só quando o criador pedir.
- **Backup e limpeza:** regras em `docs/fluxo-por-video.md`. Nunca apagar nada no Drive; limpeza só na pasta local, depois do backup.

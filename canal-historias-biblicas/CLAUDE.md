# Canal de histórias católicas animadas — instruções para o Claude

Esta pasta guarda tudo o que é preciso para produzir os vídeos do canal (nome ainda **a definir**, ver `docs/plano-canal.md`). O trabalho é feito **uma sessão por vídeo**.

> **O canal não é o sistema nem o outro canal.** O sistema de gestão (`src/`, `docs/` na raiz) e o `canal-estoicismo/` são projetos à parte, que só dividem o repositório. Do `CLAUDE.md` da raiz valem só as seções "Isolamento entre projetos" e "Regras comuns". **Todo o trabalho fica dentro desta pasta**: não ler, criar nem editar nada fora dela, nem reaproveitar arquivos do outro canal sem o criador pedir. Decisões do canal vão para `docs/plano-canal.md`.

## Comece por aqui
1. `docs/plano-canal.md` — decisões do canal, cadência, formatos, ferramentas, próximos passos.
2. `docs/doutrina-e-fontes.md` — traduções permitidas, Catecismo, representação de pessoas sagradas, checklist doutrinário.
3. `docs/estilo-visual.md` — style bible: estilos, prompt base, regras de rosto, nomenclatura dos assets.
4. `docs/fluxo-por-video.md` — passo a passo de cada sessão, backup e limpeza.
5. `docs/pacote-de-publicacao-regras.md` — o pacote obrigatório ao concluir cada vídeo.
   - `docs/guia-embalagem-youtube.md` — manual de referência para títulos, thumbnails, descrição, metadados e retenção. Quando conflitar com uma decisão do canal, aponte o conflito ao criador em vez de decidir sozinho.
6. `docs/glossario-pronuncia.md` — nomes bíblicos e latim para a narração.

## Sobre o criador
- Brasileiro; toda conversa e documentação em **pt-BR**. Tudo o que é público no canal (roteiro, narração, títulos, textos na tela, prompts de imagem) sai em **inglês natural**.
- Trabalha sozinho, com orçamento limitado: preferir o que é gratuito ou já pago.
- Gosta de construir o roteiro aos poucos, com perguntas. Não quer aprovar stills cena por cena nem prévia bloco a bloco: conferir internamente, montar o vídeo e entregar **uma revisão só**, do vídeo inteiro.

## Regras rápidas
- **Nunca infantil.** O público é adulto, 50+. Nada de títulos, roteiros ou animações com cara de conteúdo para crianças: sem proporções de desenho (cabeça e olhos grandes), sem paleta primária saturada, sem mascotes, sem rimas ou tom cantado, sem "little ones"/"kids", sem moral simplista, sem título cheio de exclamações. Na dúvida, perguntar.
- **Doutrina:** só traduções em domínio público (padrão: Douay-Rheims, revisão Challoner; nunca KJV); doutrina pelo Catecismo, com o número do parágrafo; numeração católica dos Mandamentos; Jesus e Maria nunca com rosto detalhado. Detalhes em `docs/doutrina-e-fontes.md`.
- **Nunca inventar** citação, versículo, fonte, link ou licença. Se não der para conferir a redação em domínio público, marcar `VERIFICAR`.
- **Promessa do canal:** ordem, liberdade e paz. Nunca prometer prosperidade, cura ou vida fácil.
- **Calendário litúrgico** orienta a pauta: ao sugerir temas, vídeos e roteiros, considerar festas e tempos litúrgicos próximos (`docs/plano-canal.md`).
- **Um vídeo, uma história própria.** Cada roteiro precisa de arco narrativo e virada próprios (política de conteúdo inautêntico do YouTube). Nada de vídeo-modelo com o nome trocado.
- **Nenhum texto dentro de imagem gerada.** Texto na tela (versículos, créditos, títulos) é desenhado na montagem.
- Para qualquer afirmação sobre preços, licenças ou políticas atuais (YouTube, Remotion, ElevenLabs, Gemini, Midjourney), pesquisar antes de afirmar.
- Áudios, vídeos e imagens geradas são arquivos grandes: ficam fora do git (`.gitignore` desta pasta) e vão para o Drive pelo backup.

## Estrutura da pasta (prevista; criada conforme o uso)
- `docs/` — plano, doutrina, estilo, fluxo, pacote, guia de embalagem, glossário.
- `canal.json` — nome, prefixo do código e pasta do canal no Drive (criado quando o nome for escolhido).
- `biblioteca/` — assets reutilizáveis (`personagens/`, `props/`, `fundos/`) e `catalogo.json`.
- `pipeline/` — código: Python (recorte, catálogo, áudio, backup) e Remotion (montagem).
- `videos/XX-NNN-slug/` — uma pasta por vídeo, com código + slug (o mesmo nome no Drive e no sistema). Dentro: `roteiro.md`, `audio/`, `imagens/`, `cenas/`, `previas/`, `final/`, `thumbnails/`, `pacote-de-publicacao.md`.

## Commits, backup e limpeza (autorizados pelo criador em 14/10/2026, mesma base do outro canal)
- **Fechar um bloco** = o criador aprovou o texto de um bloco OU o vídeo montado (revisão única, que fecha todos os blocos). Nesse momento, **sem pedir**: (1) marcar `(aprovado)` no título da seção do roteiro, se for texto; (2) backup no Drive; (3) **commit** só dos arquivos desta pasta, `feat(canal-historias-biblicas): XX-NNN bloco X …`, seguido de **push**.
- **Fim de sessão:** backup, commit e push do que mudou no canal. Fora desses casos, commit só quando o criador pedir.
- **Backup e limpeza:** regras em `docs/fluxo-por-video.md`. Nunca apagar nada no Drive; limpeza só na pasta local, depois do backup.

# Plano de melhorias do repositório

Auditoria completa de 14/10/2026: código (painel da raiz, pipelines dos dois canais, protótipo em Remotion), documentação, dependências Python e JavaScript, segurança e o fluxo de trabalho do gerente.

**Como usar este arquivo**
- Aplicar **um item por vez**, numa sessão. Cada item diz o projeto (que também é o escopo do commit: `chore(repo)`, `feat(canal-estoicismo)`, `feat(canal-historias-biblicas)`) e o esforço: **P** (até 1 h), **M** (uma sessão), **G** (várias sessões).
- Itens com **[decisão]** precisam do "sim" do dono antes de começar: mudam uma regra registrada.
- Ao concluir, marcar no próprio item: `✅ feito em DD/MM/AAAA` (e o commit, se houver).
- Este plano não substitui as regras: o `CLAUDE.md` da raiz e o de cada canal continuam valendo.

---

## 1. Retrato em 14/10/2026

- **Marble & Ash:** MA-001 agendado (qui 15/10), MA-002 pronto (qui 22/10), MA-003 com roteiro aprovado e sem narração (~8.187 créditos), MA-004 a MA-012 só no plano. **Folga real: uma semana.** O MA-003 precisa estar pronto até qui 29/10/2026 para a cadência não quebrar.
- **Histórias católicas:** *canal arquivado em 15/10/2026* (voltou para `ideias-de-canais/`); os itens marcados "católico" abaixo ficam sem efeito. Antes: piloto. TESTE-01 montado sem narração; sem `canal.json`, `calendario.json` e `creditos-elevenlabs.csv` (o painel estima a etapa pelas pastas); voz ainda não escolhida.
- **Créditos do ElevenLabs:** saldo de 20.979 de 35.581 (renova em 12/11/2026). Cada vídeo do MA custa ~7.000–8.000 créditos com regravações; 1 vídeo por semana consome ~100% da cota mensal atual, sem sobra para testes. Com o segundo canal narrando, a conta não fecha sem plano maior ou créditos extras (pesquisar preço na hora).
- **Testes:** painel 7 ✅, Marble & Ash 29 ✅ (inclui a comparação pixel a pixel com o render aprovado), histórias católicas sem testes.
- **Segurança:** nenhuma chave no git nem no histórico; `npm audit` sem vulnerabilidades; `.gitignore` cobre `.env`, `credentials*.json` e `token*.json`.

---

## 2. Já corrigido nesta auditoria (14/10/2026, sem commit)

Ainda não há commit: quando o dono pedir, são três commits, um por projeto (`chore(repo)`, `fix(canal-estoicismo)` e `fix(canal-historias-biblicas)`).

| Projeto | O que mudou | Por quê |
|---|---|---|
| raiz | Painel roda o comando de status do `canal.json` **sem shell** (`shlex`), mostra o erro do comando no aviso e não cai com saída inválida | `shell=True` deixava qualquer texto do `canal.json` virar comando de shell; um comando que falhava não dizia o motivo |
| raiz | Célula de créditos vazia ou inválida no CSV conta 0 em vez de derrubar o `./canais` | registro feito "para medir depois" quebrava o painel inteiro |
| raiz | `.env` aceita valor entre aspas simples; cabeçalho do `./canais calendario` mostra a data real de início (inclui ontem) | leitura diferente da do pipeline do MA; cabeçalho dizia uma data e listava outra |
| raiz | `.env` com permissão `600` (só o dono lê) | estava legível por qualquer usuário do Mac, com a chave do ElevenLabs dentro |
| raiz | 3 testes novos no painel | cobrem os casos acima |
| MA | `ma render` e `ma shorts` param com erro se o ffmpeg falhar; o short quebrado é apagado | antes, um mp4 incompleto era tratado como pronto e contava no `ma status` |
| MA | `shorts.txt` entra no backup (`05_projeto/`) | era o único arquivo de projeto fora do Drive |
| MA | `ma juntar` sem bloco numerado dá mensagem clara; `ma -h` lista o comando `shorts` | antes: `StopIteration` sem explicação; comando existia mas não aparecia na ajuda |
| MA | Mensagem de fonte não encontrada atualizada (Inter e GFS Baskerville já estão na pasta) | texto desatualizado |
| MA | `calendario.json`: shorts do MA-002 com título e código reais (o 05 é o da reserva, ter 27/10), como decidido no pacote | estavam "a definir" e a reserva com código `reserva` |
| MA | Textos: `plano-canal.md` (seção Status escrita à mão e errada, encerramento "a criar", meta de 12 vídeos antes de lançar, data de atualização), `LEIA-ME.md` do pipeline ("aprovação do frame", faster-whisper, exemplos), `fluxo-por-video.md`, complemento do pacote (pedia prompt de gerador de imagens, que o canal não usa), cabeçalho do pacote do MA-001 ("AGUARDAR", canal "não criado"), fonte da *Historia Augusta* no roteiro do MA-001 (estava `VERIFICAR`, já confirmada em 12/10), avisos de "histórico" no prompt de refatoração e no `_arquivo/` | contradiziam o estado real ou decisões posteriores |
| Católico | `render.py`: o Chrome escolhe uma porta livre (antes, portas fixas 9333+); se não abrir, o processo e o perfil temporário são apagados | com porta fixa, um Chrome antigo esquecido aberto recebia o render no lugar do novo; dois renders ao mesmo tempo colidiam. Testado com 2 Chromes em paralelo |
| Católico | `montagem.json` com `vento.ate_cena` errado agora para com erro | antes, o vento saía com 2 s sem aviso |
| Católico | `requirements.txt` com versões fixas (as do `.venv` do TESTE-01) | estava sem versão: outra máquina instalaria outras versões |
| Católico | `CLAUDE.md` e `fluxo-por-video.md` sem commit/push automáticos; textos dizendo que o pipeline "não existe" e "gravações de tela" atualizados | contradiziam a regra geral de 14/10/2026 e o código atual |

Memória do Claude atualizada: shorts do MA-001 prontos, falta agendar no Studio.

---

## 3. Python e JavaScript: situação e unificação

### 3.1 Situação

| Onde | Linguagem | Dependências | Ambiente |
|---|---|---|---|
| Painel (`ferramentas/canais.py`) | Python 3.11 | só biblioteca padrão | `python3` do Homebrew; os testes rodam com o `pytest` do **Anaconda** (o Python do Homebrew não tem pytest) |
| Marble & Ash (`pipeline/`) | Python 3.11.6 | numpy, scipy, pillow, opencv, imageio-ffmpeg, faster-whisper (+ ctranslate2, onnxruntime, av), pytest; **versões fixas** | `.venv` do canal (525 MB) + modelo do transcritor (464 MB) |
| Histórias católicas (`pipeline/`) | Python 3.11.6 | numpy, websocket-client, imageio-ffmpeg (fixas desde hoje) | `.venv` do canal (107 MB) + **Google Chrome do sistema**, caminho fixo do macOS |
| Protótipo forró (`ideias-de-canais/`) | TypeScript / Node 22 | Remotion 4.0.528 + React 19 | `node_modules` de 845 MB; 0 vulnerabilidades; 7 versões de correção atrás |

No Mac há três Pythons (Homebrew, Anaconda e o do sistema). Hoje cada comando acerta "por sorte" qual usar.

### 3.2 Vale unificar?

- **Ambientes dos canais num só: não.** A regra de isolamento entre canais existe para um canal não quebrar o outro, e o teste visual do MA depende das versões exatas de numpy, scipy, opencv e pillow (mudou a versão, mudam pixels). Um ambiente único obrigaria os dois canais a atualizar juntos.
- **A forma de criar os ambientes: sim** (item T1). Com o `uv`, cada canal continua com o seu `.venv`, mas os pacotes ficam num cache único do Mac e são copiados para cada ambiente por cópia copy-on-write do APFS, sem ocupar espaço duas vezes. Ambientes criados em segundos, com arquivo de travamento (lock) por canal.
- **O código "de infraestrutura": sim, com decisão do dono** (item T3). Hoje há três leitores do `.env` (painel, MA e, em breve, o católico), o backup no Drive existe só no MA e o canal católico já descreveu as mesmas regras sem código (vai ser escrito de novo), e os dois canais vão precisar do mesmo cliente do ElevenLabs (gerar, medir saldo, registrar no CSV). Isso não é identidade de canal: é encanamento. A arte e o render continuam em cada canal.
- **JavaScript: não há JS de produção.** O único projeto Node é o protótipo do forró. O canal católico renderiza HTML com um script Python de ~170 linhas, sem bibliotecas; o Remotion faria o mesmo trabalho com 845 MB de dependências. Recomendação: **não levar Node para os canais agora**; decidir só quando o canal "Língua e costumes" sair do caderno, e aí escolher **um caminho só de HTML → vídeo** para todos os canais em HTML (o renderizador do canal católico promovido a ferramenta comum, ou o Remotion).
- **Licença do Remotion** (conferida em 14/10/2026): grátis para pessoa física e para empresas com até 3 pessoas, inclusive uso comercial; acima disso, licença de empresa paga. A licença vai mudar "levemente" no Remotion 5.0: reler antes de usar num canal. Fontes: [LICENSE.md do Remotion](https://cdn.jsdelivr.net/npm/remotion@4.0.529/LICENSE.md), [preços](https://www.remotion.dev/docs/pricing).

### 3.3 Itens

- **T1. Ambientes com `uv`** · raiz + cada canal · M. `pyproject.toml` (ou `requirements.in`) + lock por canal; `.python-version` = 3.11 nos dois canais; atualizar a seção 1 do `pipeline/LEIA-ME.md` do MA e o `requirements.txt` do católico. Conferir o teste pixel a pixel depois de recriar o `.venv` do MA.
- **T2. Testes do painel sem depender do Anaconda** · raiz · P. `ferramentas/requirements-dev.txt` com o pytest (ou `uv run --with pytest`) e trocar o comando no `CLAUDE.md` da raiz (`python -m pytest` hoje cai no Python do Anaconda).
- **T3. Núcleo comum na raiz** · raiz · G · **[decisão]**. Pacote `ferramentas/nucleo/` com testes: leitura do `.env`, backup no Drive (o do MA, que já tem testes), cliente do ElevenLabs (gerar com a config do `elevenlabs.json` do canal, saldo antes e depois, linha no CSV), validação do contrato do painel (`canal.json`, `calendario.json`, CSV) e utilidades de ffmpeg (loudness, mixagem, xfade). Cada canal instala uma versão fixa. Muda a regra de isolamento ("um canal não referencia código de fora"): precisa do "sim" do dono e de uma linha nova no `CLAUDE.md` da raiz.
- **T4. Chrome fixo para o canal católico** · católico · M. Hoje o render usa o Chrome instalado, que se atualiza sozinho: o mesmo HTML pode sair diferente de uma semana para outra. Baixar uma versão fixa do *Chrome for Testing* (ou *chrome-headless-shell*) para dentro da pasta do canal, fora do git, com o caminho configurável.
- **T5. `node_modules` do protótipo** · ideias · P. Apagar os 845 MB enquanto o protótipo não for usado (`npm ci` refaz a partir do `package-lock.json`). Só se o dono quiser.

---

## 4. Falhas que ficaram para depois

### 4.1 Lógica

- **L1. "Final" pode ser uma montagem parcial** · MA · M. O `ma status` considera final o mp4 mais recente de `final/`. Uma montagem de teste (`ma juntar 3 1 2`) vira "o final": o status pode dizer CONCLUÍDO, os shorts saem cortados do arquivo errado e a limpeza confia nele. Correção: o `ma juntar` grava `final/montagem.json` (peças na ordem, início e duração de cada uma, ganho do ambiente) e o status só aceita um final que tenha todas as peças do roteiro.
- **L2. Shorts dependem do nome do arquivo final** · MA · P (junto com L1). O `ma shorts` reconstrói a linha do tempo lendo o nome do mp4; `ma juntar --saida OUTRO` quebra os shorts. Com o `montagem.json` do L1, ler de lá.
- **L3. Refazer um short depois do `ma limpar` exige re-renderizar o vídeo todo** · MA · P (junto com L1). A linha do tempo mede a duração em `trabalho/blocoN-video.mp4`, que a limpeza apaga. As durações no `montagem.json` resolvem.
- **L4. A referência visual não tem backup** · MA · P. Os stills de `trabalho/referencia/stills/` (a garantia de que o render continua "bit a bit") não vão para o git nem para o Drive. Se o Mac morrer, a garantia some. Incluir no backup (ex.: `BIBLIOTECA/referencia/`).
- **L5. Thumbnails sem código** · MA · M. As thumbnails do MA-001 e do MA-002 foram feitas com scripts avulsos; só a "receita" ficou no pacote. Criar `ma thumbs N` com um `thumbs.txt` por vídeo (bloco, segundo do quadro, texto, palavra em âmbar), como o `shorts.txt`. Também entra no item A6.
- **L6. Final publicado pode ser sobrescrito no Drive** · MA · P · **[decisão]**. O backup atualiza final, prévias e shorts no Drive sem guardar a versão anterior (decisão registrada: "mídia que dá para gerar de novo"). Mas o arquivo que foi para o YouTube é prova em caso de claim. Proposta: ao marcar `agendado`, copiar o final e os shorts para `07_export/publicado/` e nunca mais tocar neles.
- **L7. Calendário malformado derruba o painel** · raiz · P. Item sem `tipo`, hora inválida ou fuso errado gera erro e o `./canais` não mostra nada. Validar item a item e listar os problemas no aviso do canal.
- **L8. Cache de cenas do canal católico não vê mudanças no renderizador** · católico · P. A assinatura de cada cena só leva o HTML, a duração e as legendas. Mudar a legenda provisória ou o FPS em `render.py` não refaz as cenas já gravadas. Incluir na assinatura o texto de `PREPARA` e o FPS (todas as cenas são refeitas uma vez).
- **L9. CSS e JS copiados em todas as cenas** · católico · M. Cada um dos 25 HTML do TESTE-01 repete o mesmo bloco de estilo (paleta, line boil, animações). Mudar a paleta exige editar 25 arquivos. Criar `biblioteca/base.css` (e `base.js`, se preciso) incluídos por `<link>`, e somar o conteúdo deles na assinatura do L8.
- **L10. Canal católico sem testes** · católico · P. Testes para `linha_do_tempo`, `duracao_fala` e a assinatura das cenas.
- **L11. Leitura frágil da saída do ffmpeg** · MA · P. `pausas`, `mixar`, `loudness` e `duracao_video` leem texto do ffmpeg por expressão regular; se o formato mudar, o erro é um `AttributeError` sem explicação. Como o ffmpeg vem com versão fixa (imageio-ffmpeg), basta trocar por mensagens claras.
- **L12. Pacote com seções diferentes da base** · MA · P · **[decisão]**. A base manda "exatamente 15 seções, com os mesmos títulos", mas os pacotes do MA usam "12. PROMPTS DE CENA" (a base diz "12. CENAS") e têm uma 16ª seção, "BLOCO JSON (dossiê)". Decidir: a seção 16 vira regra do complemento do canal, ou sai.

### 4.2 Segurança

- **S1. Visibilidade do repositório no GitHub** · P · **[decisão]**. O remoto é `github.com/mondini/gerenciador-videos`. Não consegui conferir se é privado (o `gh` não está instalado). Se for público: roteiros antes da publicação, pacotes, pipeline e nomes das pastas do Drive ficam abertos. Recomendo privado.
- **S2. Chave do ElevenLabs com escopo e teto** · P. A documentação do ElevenLabs permite restringir uma chave a certos endpoints e dar a ela uma cota de créditos ([autenticação](https://elevenlabs.io/docs/api-reference/authentication), [chaves](https://elevenlabs.io/docs/overview/administration/workspaces/api-keys)). Antes de o Claude narrar pela API sem o dono olhando (item A1), trocar a chave por uma só com texto para fala + leitura da assinatura e um teto mensal de créditos. Isso limita o estrago de um erro de loop ou de uma chave vazada.
- **S3. OAuth do YouTube (quando chegar o item A9)** · P. Guardar o token fora do repositório (Keychain do macOS ou `~/.config/`), nunca numa pasta sincronizada pelo Google Drive. O `.gitignore` já cobre `token*.json`, mas o mais seguro é o arquivo nem estar no repositório.
- **S4. `canal.json` é código** · P. O comando `"status"` de cada canal é executado pelo painel. Desde hoje sem shell, mas continua sendo um programa: revisar mudanças nesse campo como se fossem código.
- **S5. Repositório fora do Drive** · regra. O `.env` fica na raiz do repositório. Nunca mover o repositório para dentro de uma pasta do Google Drive (a chave subiria para a nuvem).

---

## 5. Rumo ao "roteiro apto → vídeo pronto"

Objetivo do dono: o gerente marca um roteiro como **apto**; o Claude produz tudo e o vídeo aparece pronto para uma revisão única, com o mínimo de idas e vindas.

### 5.1 Onde o gerente ainda trabalha hoje (Marble & Ash)

| Etapa | Hoje | O que dá para tirar das mãos do gerente |
|---|---|---|
| Roteiro | constrói bloco a bloco com o Claude e aprova cada um | continua (é a parte criativa); só muda o fim: "apto" dispara o resto |
| Narração | **cola cada bloco no site do ElevenLabs, baixa 7 mp3, renomeia e envia** | geração pela API, com a voz e o modelo já conferidos no `elevenlabs.json` |
| Créditos | confirma cada geração; o Claude mede o saldo antes e depois | confirmação única no "apto", com teto de créditos por vídeo |
| Tempos, cenas, render | o Claude roda ~5 comandos por bloco × 7 peças | um comando que roda só o que falta |
| Montagem | o Claude digita a ordem (`1 abertura 2 3 4 pausa 5 6 encerramento`) | ordem tirada das seções do roteiro |
| Thumbnails | scripts avulsos | comando reproduzível |
| Shorts | `shorts.txt` escrito à mão | sai das frases marcadas no roteiro |
| Pacote (~43 KB por vídeo) | escrito à mão a partir do anterior | seções fixas por modelo; capítulos com os tempos reais da montagem |
| Calendário | JSON editado à mão | comando que põe o vídeo na próxima quinta livre com os shorts da semana |
| YouTube Studio | **upload, thumbnails, shorts, agendamento e "vídeo relacionado" à mão** | upload e agendamento pela API (com ressalvas, ver A9) |

### 5.2 Como ficaria

1. O gerente aprova o roteiro e diz "apto" (ou roda `./ma apto N`). Isso registra a autorização de narração até X créditos.
2. O Claude, numa sessão: narra pela API → tempos → escreve as cenas e a arte nova → renderiza tudo → monta → confere a compressão do YouTube → thumbnails → shorts → pacote → backup → calendário.
3. O gerente recebe **uma mensagem**: link do vídeo no Drive (e uma cópia leve em 720p para ver no celular), as 3 thumbnails, os 5 shorts e o que precisa de decisão. Responde com os ajustes de uma vez; o Claude refaz só os blocos tocados.
4. Aprovado: o Claude agenda (pela API ou deixa o roteiro pronto para o Studio) e marca `agendado`.

### 5.3 Itens

- **A1. Narração pela API no MA** · MA · M · **[decisão]**. `./ma narrar N`: conta os caracteres de cada bloco, mostra créditos estimados e saldo, pede o "sim", gera os 7 mp3 com a configuração do `elevenlabs.json`, mede o saldo depois, grava a linha no `creditos-elevenlabs.csv` e já roda o `ma audio` de cada bloco. O `voice_id` e o `model_id` já foram conferidos pela API em 14/10. Trocar `"modo": "site"` por `"api"`. Depende de S2.
- **A2. Autorização no "apto"** · raiz · P · **[decisão]**. Hoje a regra exige confirmação a cada geração. Proposta: marcar o roteiro como apto autoriza a narração dele até um teto (ex.: estimativa + 15% para uma regravação); acima disso, perguntar. Exige mudar a seção "Narração" do `CLAUDE.md` da raiz.
- **A3. `./ma produzir N`** · MA · G. Orquestrador que lê o `ma status` e roda, em ordem, só o que falta: áudio, tempos, render de cada peça, juntar (ordem tirada do roteiro), simulação do YouTube, shorts, backup. Cenas e arte continuam sendo escritas pelo Claude; o comando cuida do resto e avisa uma vez a fila e a estimativa de tempo (render: ~1,5–2 s por segundo de vídeo, ~15–20 min por vídeo). Depende de L1.
- **A4. Capítulos automáticos** · MA · P. Com o `montagem.json` do L1, os capítulos da descrição saem com os tempos reais (início de cada bloco no final), em vez de "AJUSTAR NA EDIÇÃO FINAL".
- **A5. Pacote por modelo** · MA (e depois o católico) · M. Separar as seções fixas (licenças, IA, defesa contra claim, riscos padrão) num modelo do canal; o pacote de cada vídeo junta o modelo com o que é do vídeo (títulos, descrição, fontes, citações, capítulos, shorts). Menos texto repetido, menos chance de levar um dado do vídeo anterior para o novo.
- **A6. Thumbnails reproduzíveis** · MA · M. O `ma thumbs N` do L5, com conferência automática do tamanho (1280×720, < 2 MB) e uma prévia em 320×180 lado a lado.
- **A7. Shorts a partir do roteiro** · MA · P. Uma linha `**Short:** NN | TÍTULO | deixa de início | deixa de fim` na seção do bloco (como a linha `**Deixas:**`); o `shorts.txt` passa a ser gerado.
- **A8. `./ma agendar N`** · MA · P. Põe o vídeo na próxima quinta livre do `calendario.json` com os 5 shorts na grade do `plano-canal.md` (inclusive a reserva), já com os títulos do `shorts.txt`. `./ma agendado N` marca tudo como `agendado` depois do Studio.
- **A9. Upload e agendamento pela API do YouTube** · raiz/MA · G · **[decisão]**. Upload, `publishAt`, thumbnail e legendas pela YouTube Data API tirariam o gerente do Studio. Ressalva importante: segundo fontes de terceiros, projetos de API criados depois de 28/07/2020 e **sem auditoria do Google** sobem vídeos travados como privados, e a auditoria pede telas do cliente de upload; a cota de uploads por dia também tem informações conflitantes ([exemplo 1](https://www.ayrshare.com/solutions/google-api-error-403-unverified-app-how-to-fix-the-audit-pipeline/), [exemplo 2](https://postproxy.dev/blog/automate-youtube-uploads/)). Conferir na documentação oficial do Google antes de começar. O teste A/B de thumbnails do Studio provavelmente continua manual (confirmar).
- **A10. Painel com "próxima ação" e folga** · raiz · M. Para cada canal: quantas semanas de vídeos prontos há à frente, data-limite do próximo vídeo (hoje: MA-003 até 29/10), itens `planejado` nas próximas 48 h que ainda não foram agendados no Studio, e créditos necessários até a renovação contra o saldo.
- **A11. Revisão no celular** · MA · P. Junto com o final, uma cópia 720p leve no Drive e uma lista "o que conferir" com os minutos de cada bloco, para o gerente responder tudo numa mensagem.
- **A12. Canal católico no mesmo trilho** · católico · G. Antes do piloto narrado: `canal.json` provisório (o painel mostra o canal pelo nome), `creditos-elevenlabs.csv`, comando de status para o painel, backup e limpeza (de preferência pelo núcleo comum do T3), narração pela API (A1) e legendas SRT.
- **A13. Rotina semanal** · raiz · M. Toda quarta ("métricas e preparação" no plano do MA): relatório com o painel, o que sai na semana e, mais adiante, métricas do YouTube Analytics (CTR, retenção) para orientar títulos e thumbnails.

### 5.4 Decisões que só o dono pode tomar

| # | Decisão | Itens que dependem dela |
|---|---|---|
| D1 | Narração do MA pela API (deixar o modo `site`) | A1 |
| D2 | "Apto" autoriza a narração até um teto de créditos (muda a regra de confirmação por geração) | A2, A3 |
| D3 | Núcleo comum na raiz (muda a regra de isolamento) | T3, A12 |
| D4 | Upload pela API do YouTube (projeto no Google Cloud, OAuth, auditoria) | A9 |
| D5 | Congelar no Drive o final e os shorts publicados | L6 |
| D6 | Repositório privado no GitHub | S1 |
| D7 | Seção 16 (dossiê JSON) no pacote do MA | L12 |
| D8 | Créditos: plano maior ou créditos extras antes do segundo canal narrar | A1, A12 |

---

## 6. Ordem sugerida

1. **Já (antes de 29/10):** decidir D1, D2 e D6; S2 (chave com teto); A1 (narração pela API) para o MA-003 já sair por ela; T2.
2. **Base para automatizar o MA:** L1 + L2 + L3 (manifesto do final), L4, A4, A8, L7.
3. **Automação do MA:** A3 (`ma produzir`), L5/A6 (thumbs), A7 (shorts no roteiro), A5 (pacote por modelo), A11, A10.
4. **Ambientes e núcleo:** T1 (`uv`); com D3, T3 (núcleo comum) a partir do backup e do cliente do ElevenLabs.
5. **Canal católico:** A12, L8, L9, L10, T4.
6. **Studio:** com D4, A9; depois A13.

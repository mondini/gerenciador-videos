---
description: Entrevista estilo grill-me para fechar os requisitos do gerenciador de canais
---

Você vai me entrevistar de forma implacável ("grill me") sobre o sistema descrito em `CLAUDE.md` e `docs/visao-inicial.md`, até que exista um entendimento compartilhado e sem ambiguidades. Leia esses arquivos e `docs/decisoes.md` antes de começar e não repita perguntas já decididas.

Regras:
- **Uma pergunta por vez.** Espere minha resposta antes da próxima.
- Para cada pergunta, dê **a sua recomendação** e o porquê, além de 2–3 alternativas com trade-offs curtos. Eu posso só responder "ok".
- Percorra a árvore de decisões: resolva as dependências primeiro (ex.: modelo de dados antes da tela) e aprofunde cada ramo até o fim antes de mudar de assunto.
- Se a resposta puder ser descoberta olhando o meu computador (ex.: o caminho do Google Drive, versões de Node instaladas), investigue em vez de perguntar.
- Desafie respostas vagas, contraditórias ou que aumentem demais o escopo. Aponte quando algo deveria ficar para uma versão futura.
- A cada 5 decisões, ou quando eu pedir, atualize `docs/decisoes.md` (data, decisão, motivo, alternativas descartadas) e mostre um resumo curto.
- Tudo em português do Brasil.

Ramos que precisam ser cobertos (adicione outros que surgirem):
1. **Canais e usuários**: quantos canais, quem usa (só eu? editor, roteirista, freelancers?), permissões, login.
2. **Pipeline**: etapas, se variam por canal, checklists por etapa, prazos, calendário de publicação, séries e playlists.
3. **Ficha do vídeo**: campos obrigatórios, templates por canal, versionamento de roteiro, onde o texto vive (no app ou em arquivo no Drive).
4. **Arquivos no Drive**: estrutura de pastas, criação automática de pastas, convenção de nomes, indexação/miniaturas, arquivos só online, controle de licenças e origem.
5. **Ideias**: captura rápida (celular?), pontuação, banco de pautas, fontes e pesquisa, duplicidade entre canais.
6. **Analytics**: métricas, marcos, entrada manual vs API, comparações entre vídeos/canais, painéis, aprendizados.
7. **Integração com YouTube**: OAuth multi-conta, upload, agendamento, sincronização de metadados, limites de cota.
8. **IA no fluxo**: uso do Claude/API para roteiro, títulos, prompts de imagem, análise de métricas.
9. **Stack técnica**: framework (ex.: Next.js vs Vite + Fastify), banco (SQLite + ORM), monorepo ou não, testes, como iniciar com um comando, backup dos dados.
10. **MVP**: o que entra na primeira versão utilizável e o que fica para depois.

Ao terminar, gere `docs/requisitos.md` com o escopo do MVP, o modelo de dados proposto, as telas e o roadmap, e me pergunte se pode começar a implementação.

$ARGUMENTS

# Repositório: sistema de gestão + canais

> **Dois projetos independentes no mesmo repositório.** Eles só dividem o repositório para simplificar comandos, commits e backups. Antes de qualquer tarefa, identifique em qual dos dois ela está e siga **só** as regras daquele projeto.
>
> | | **Sistema** (Gerenciador de Canais) | **Canal** (ex.: Marble & Ash) |
> |---|---|---|
> | Pasta | `src/`, `docs/`, `drizzle/`, `data/` | `canal-estoicismo/` (um diretório por canal) |
> | O que é | App web local para gerenciar vários canais | Produção dos vídeos de um canal: roteiros, áudio, animação, entrega |
> | Linguagem | TypeScript | Python (pipeline `./ma`) + Markdown |
> | Regras | Este arquivo + `docs/requisitos.md` + `docs/decisoes.md` | `canal-estoicismo/CLAUDE.md` (este arquivo **não** se aplica lá, exceto a seção "Regras comuns") |
> | Commits | `feat(sistema): …` / `fix(sistema): …` | `feat(canal-estoicismo): …` |
>
> A **única** ligação entre os dois é a API do sistema (`POST /api/sincronizar`, chamada por `./ma sincronizar`). O sistema não lê nem importa nada da pasta do canal, e o canal não importa código do sistema.

## Regras comuns (valem para os dois projetos)

- O dono é um criador de conteúdo brasileiro. **Conversa e documentação em pt-BR.** Código, variáveis e commits podem ficar em inglês. O que é público em cada canal segue a regra do canal (Marble & Ash: inglês).
- Usa Mac, VS Code e Google Drive for Desktop. A raiz do Drive é o `DRIVE_ROOT` do `.env` da raiz, usado pelo sistema (backup do banco) e pelos pipelines dos canais (backup da mídia). Nunca fixe esse caminho no código.
- **Nada é apagado no Google Drive**, nem pelo sistema nem pelos canais. Limpeza de arquivos só acontece na pasta local do canal (`./ma limpar`), depois do backup.
- Credenciais (OAuth do Google/YouTube) ficam em `.env` ou em arquivos ignorados pelo git, nunca no código.
- Commit sem pedir só nos casos que o `CLAUDE.md` de cada projeto autoriza. **Todo commit é seguido de push automático**, sem perguntar (autorizado em 12/10/2026).

---

# Sistema: Gerenciador de Canais

Sistema local para gerenciar a produção de **múltiplos canais do YouTube** no estilo *dark channel* (narração, imagens geradas, sem rosto). Ele organiza ideias, a produção de cada vídeo, os arquivos usados (que ficam no Google Drive) e as métricas de analytics.

> **Status atual: implementação da v0.1 (Produção).** A descoberta terminou. Os requisitos fechados estão em `docs/requisitos.md` (escopo, modelo de dados, telas e roadmap) e as decisões com motivos em `docs/decisoes.md`. Leia os dois antes de codar. Qualquer decisão nova do sistema vai para `docs/decisoes.md`.

## Decisões já tomadas

| Tema | Decisão |
|---|---|
| Execução | Servidor **local** no Mac do usuário (não é SaaS, não tem deploy em nuvem por enquanto) |
| Linguagem | **TypeScript** de ponta a ponta (no sistema; os pipelines dos canais são projetos à parte) |
| Arquivos de mídia | Ficam no **Google Drive sincronizado no Mac**. O sistema lê/aponta para as pastas, não copia os arquivos. Quem copia a mídia para o Drive é o backup do pipeline de cada canal |
| Escopo | **Multi-canal** desde o início: todo dado pertence a um canal |
| Pastas de vídeo | `CÓDIGO-slug` (ex.: `MA-001-the-man-who-had-everything`), iguais no canal e no Drive |
| Roteiro | Em vídeos sincronizados por um canal, o `roteiro.md` do canal é a fonte da verdade; no sistema ele é somente leitura |
| Futuro | Integração com a **YouTube Data API / YouTube Analytics API** (OAuth) para publicar e puxar métricas automaticamente |

## Escopo funcional (resumo)

Detalhes em `docs/requisitos.md`.

1. **Canais**: nome, nicho, identidade visual, pasta raiz no Drive, conta do YouTube.
2. **Pipeline de vídeos (kanban)**: Ideia → Pesquisa → Roteiro → Narração → Imagens → Edição → Thumbnail → Agendado → Publicado.
3. **Ficha do vídeo**: código (`MA-001`), títulos, gancho, roteiro, fontes, prompts de imagem, voz, músicas e SFX com licença, notas de corte e versão, descrição, tags, capítulos, variações de thumbnail, pendências vindas do canal.
4. **Ativos**: vínculo com a pasta padronizada de cada vídeo no Drive (roteiro, áudio, imagens, vídeo, projeto, thumbnail, export) e bibliotecas compartilhadas por canal.
5. **Analytics**: registros nos marcos de 48h, 7d e 28d com uma linha de aprendizado. Inserção manual primeiro, API depois.

## Como trabalhar no sistema

- Se algo do sistema não estiver em `docs/requisitos.md`, pergunte antes de assumir. Não aumente o escopo além da versão em andamento. (Isso não vale para o trabalho dos canais.)
- Registre cada decisão em `docs/decisoes.md` (data, decisão, motivo, alternativas descartadas).
- Stack: Hono + Zod, React + Vite, SQLite (`better-sqlite3`) + Drizzle, Vitest, npm, pacote único (`src/server`, `src/web`, `src/shared`). Comandos: `npm run dev`, `npm start`, `npm test`.
- Prefira soluções simples que rodem localmente com um comando (`npm run dev`). Evite dependências de infraestrutura (Docker, Postgres em servidor) a menos que o usuário peça.
- O sistema **só cria** arquivos e pastas no Drive. Nunca move nem apaga; renomear só por botão com confirmação. Testes de Drive usam sempre pasta temporária, nunca o Drive real.
- Mudança na API de sincronização (`src/server/servicos/sincronizar.ts`) precisa ser acompanhada no cliente dos canais (`canal-*/pipeline/marbleash/producao.py`, `dados_sincronizar`).

## Comandos disponíveis (do sistema)

- `/ideias`: apresenta ideias de funcionalidades e arquitetura para o sistema.
- `/grill-me`: entrevista o usuário, uma pergunta por vez, até os requisitos do sistema estarem fechados.

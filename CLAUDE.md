# Gerenciador de Canais

Sistema local para gerenciar a produção de **múltiplos canais do YouTube** no estilo *dark channel* (narração, imagens geradas, sem rosto). Ele organiza ideias, a produção de cada vídeo, os arquivos usados (que ficam no Google Drive) e as métricas de analytics.

> **Status atual: implementação da v0.1 (Produção).** A descoberta terminou. Os requisitos fechados estão em `docs/requisitos.md` (escopo, modelo de dados, telas e roadmap) e as decisões com motivos em `docs/decisoes.md`. Leia os dois antes de codar. Qualquer decisão nova vai para `docs/decisoes.md`.

## Contexto do dono

- Criador de conteúdo brasileiro que está começando um canal dark (e planeja ter vários).
- Fala português. **Toda conversa, interface e documentação devem estar em pt-BR.** Código, nomes de variáveis e commits podem ficar em inglês.
- Usa Mac, VS Code e Google Drive for Desktop.
- Também quer criar a identidade visual dos canais com o Claude Design (Design System + artes). Isso fica fora deste repositório, mas o sistema pode guardar referências a esses ativos.

## Decisões já tomadas

| Tema | Decisão |
|---|---|
| Execução | Servidor **local** no Mac do usuário (não é SaaS, não tem deploy em nuvem por enquanto) |
| Linguagem | **TypeScript** de ponta a ponta |
| Arquivos de mídia | Ficam no **Google Drive sincronizado no Mac** (Google Drive for Desktop). O sistema lê/aponta para as pastas, não copia os arquivos |
| Escopo | **Multi-canal** desde o início: todo dado pertence a um canal |
| Futuro | Integração com a **YouTube Data API / YouTube Analytics API** (OAuth) para publicar e puxar métricas automaticamente |

Caminho típico do Drive no macOS: `~/Library/CloudStorage/GoogleDrive-<email>/Meu Drive/` (confirmar com o usuário; deve ser configurável e nunca fixo no código).

## Escopo funcional inicial (a refinar no grill-me)

Ver `docs/visao-inicial.md` para os detalhes. Resumo:

1. **Canais**: nome, nicho, identidade visual, pasta raiz no Drive, conta do YouTube.
2. **Pipeline de vídeos (kanban)**: Ideia → Pesquisa → Roteiro → Narração → Edição → Thumbnail → Agendado → Publicado.
3. **Ficha do vídeo**: código (`DC-012`), títulos, gancho, roteiro, fontes, prompts de imagem, voz, músicas e SFX com licença, notas de corte e versão, descrição, tags, capítulos, variações de thumbnail.
4. **Ativos**: vínculo com a pasta padronizada de cada vídeo no Drive (roteiro, áudio, imagens, vídeo, projeto, thumbnail, export) e bibliotecas compartilhadas por canal.
5. **Analytics**: registros nos marcos de 48h, 7d e 28d (views, impressões, CTR, retenção, % aos 30s, duração média, inscritos, tráfego) com uma linha de aprendizado. Inserção manual primeiro, API depois.

## Como trabalhar neste repositório

- Se algo não estiver em `docs/requisitos.md`, pergunte antes de assumir. Não aumente o escopo além da versão em andamento.
- Registre cada decisão em `docs/decisoes.md` (data, decisão, motivo, alternativas descartadas).
- Stack: Hono + Zod, React + Vite, SQLite (`better-sqlite3`) + Drizzle, Vitest, npm, pacote único (`src/server`, `src/web`, `src/shared`). Comandos: `npm run dev`, `npm start`, `npm test`.
- Prefira soluções simples que rodem localmente com um comando (`npm run dev`). Evite dependências de infraestrutura (Docker, Postgres em servidor) a menos que o usuário peça. SQLite é a escolha padrão a discutir.
- O sistema **só cria** arquivos e pastas no Drive. Nunca move nem apaga; renomear só por botão com confirmação. Testes de Drive usam sempre pasta temporária, nunca o Drive real.
- Credenciais (OAuth do Google/YouTube) ficam em `.env`/arquivos ignorados pelo git, nunca no código.

## Comandos disponíveis

- `/ideias`: apresenta ideias de funcionalidades e arquitetura para o sistema.
- `/grill-me`: entrevista o usuário, uma pergunta por vez, até os requisitos estarem fechados.

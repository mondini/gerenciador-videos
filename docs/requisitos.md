# Requisitos: Gerenciador de Canais

Documento consolidado ao fim da entrevista (`/grill-me`) de 2026-10-09. A justificativa de cada decisão está em [`decisoes.md`](decisoes.md).

## 1. Contexto

- **Usuário único** (o dono), sem login. O sistema roda no Mac em `127.0.0.1:4321`.
- **Primeiro canal:** curiosidades de artes marciais com foco em BJJ, em pt-BR, prefixo `BJJ`, cerca de 2 vídeos por semana. É um **experimento de 90 dias**, com critérios de corte definidos no início.
- **Segundo canal:** depois dos 90 dias. O modelo é multi-canal desde já.
- **Fluxo de trabalho:** produção em lote semanal, com estoque de 4 a 6 vídeos prontos antes da primeira publicação.

## 2. Regras gerais (não funcionais)

1. Toda a interface e a documentação ficam em pt-BR. O código pode ficar em inglês.
2. **Drive:** a raiz vem do `DRIVE_ROOT` no `.env` (padrão: `…/GoogleDrive-mondini@gmail.com/Meu Drive/Canais YouTube`). O servidor **não sobe** se a raiz não existir.
3. **O sistema só cria arquivos e pastas no Drive.** Nunca move nem apaga. Renomear acontece só por botão, com confirmação explícita. Os arquivos que o próprio sistema exporta (roteiro `.md`, `fontes_tela.txt`) recebem nomes novos por versão em vez de sobrescrever.
4. As pastas de vídeo são localizadas pelo **prefixo do código** (`BJJ-001_*`), nunca pelo nome completo.
5. A leitura do Drive é **sob demanda**, sem índice nem watcher. Arquivos só online aparecem com ☁️, e nada de vídeo ou áudio é baixado para gerar prévia.
6. O banco SQLite fica em `data/` (fora do Drive). Há backup `.db` em `DRIVE_ROOT/_backup/` ao iniciar e a cada 24h, sem exclusão automática.
7. Segredos (chaves futuras de API, OAuth) ficam só no `.env` ou em arquivos ignorados pelo git.
8. Os campos de publicação respeitam os limites do YouTube: título ≤ 100 caracteres, descrição ≤ 5.000, tags ≤ 500 no total.

## 3. Stack

| Camada | Escolha |
|---|---|
| Estrutura | Pacote único: `src/server`, `src/web`, `src/shared` |
| Servidor | Node 22 + **Hono** + Zod |
| Interface | **React + Vite**, Tailwind + shadcn/ui, dnd-kit (kanban), Recharts (gráficos) |
| Banco | SQLite (`better-sqlite3`) + **Drizzle** + drizzle-kit (migrações) |
| Testes | **Vitest**: domínio, Drive (pasta temporária) e API (SQLite em memória) |
| Comandos | `npm run dev` (desenvolvimento), `npm start` (uso diário), `npm test` |
| Repositório | `git@github.com:mondini/gerenciador-videos.git` |

## 4. Pipeline

Etapas fixas (no código), iguais para todos os canais:

`Ideia → Pesquisa → Roteiro → Narração → Imagens → Edição → Thumbnail → Agendado → Publicado`

- **Checklist:** cada canal tem um modelo por etapa (editável e com padrão sugerido), copiado para o vídeo ao criá-lo. Itens podem ser adicionados ao vídeo avulso. **Não bloqueia** o avanço: pendências aparecem como ⚠️ no card.
- **Grade de publicação** por canal (dias da semana + horário). A data planejada do vídeo é sugerida como o próximo horário livre.
- **Alerta de risco:** faltam menos de 7 dias para a data planejada e o vídeo ainda está antes de Edição.
- **Histórico:** cada mudança de etapa é registrada (para a linha do tempo e os gargalos).
- **Ideia → Pesquisa** cria a pasta do vídeo no Drive, com um aviso na tela.
- **Saída de Roteiro** cria uma versão automática do roteiro.

## 5. Modelo de dados

```
Canal 1─N GradePublicacao       Canal 1─N Formato
Canal 1─N Serie                 Canal 1─N Tema
Canal 1─N ModeloChecklist       Canal 1─N PromptBanco
Canal 1─N Ativo                 Canal 1─1 CriteriosExperimento
Canal 1─N ModeloPromptClaude (v0.2)
Canal 1─N Video
Video N─1 Formato (opcional só enquanto Ideia importada)
Video N─1 Serie (opcional)      Video N─N Tema
Video N─1 Video (derivadoDe, opcional)
Video 1─N HistoricoEtapa        Video 1─N ChecklistItem
Video 1─N VersaoRoteiro         Video 1─N Cena
Video 1─N Fonte                 Fonte N─N Cena
Video 1─N TituloCandidato       Video 1─N VarianteThumbnail
Video N─N Ativo (UsoAtivo)      Video 1─N RegistroAnalytics (máx. 1 por marco)
```

### Entidades e campos principais

**Canal:** nome, nicho, idioma (`pt-BR`), prefixoCodigo (`BJJ`, único), pastaRelativa (relativa ao `DRIVE_ROOT`), urlYoutube?, youtubeChannelId?, modeloDescricao (com variáveis `{titulo}`, `{resumo}`, `{capitulos}`, `{fontes}`, `{creditos}`), tagsPadrao[], vozPadrao (ferramenta, voz, configurações), estiloImagemPadrao (prompt base), referenciasIdentidade (links do Design System e artes).

**GradePublicacao:** canal, diaSemana, hora.

**Formato:** canal, nome (padrões: História · Mito x verdade · Ranking · Origem · Rivalidade), ativo.

**Serie:** canal, nome, descrição, youtubePlaylistId?.

**Tema:** canal, nome (tag livre).

**ModeloChecklist:** canal, etapa, ordem, texto.

**Video:**
- *Identidade:* canal, numero, codigo (`BJJ-001`, único e imutável), tituloProvisorio, tituloFinal?, formato?, serie?, temas, derivadoDe?
- *Planejamento:* etapa, dataPlanejada?, dataPublicacao?, notaApelo, notaIlustracao, notaPesquisa (1–5 cada; soma 3–15)
- *Conteúdo:* gancho (15s), resumo, roteiroAtual (Markdown)
- *Produção:* pastaRelativa?, vozUsada (pré-preenchida pelo canal), duracaoFinal?, notasCorte
- *Publicação:* descricao (pré-preenchida pelo modelo), tags (pré-preenchidas), capitulos, youtubeVideoId?, urlYoutube?

**HistoricoEtapa:** vídeo, etapa, entrouEm.

**ChecklistItem:** vídeo, etapa, ordem, texto, feito, feitoEm?.

**VersaoRoteiro:** vídeo, numero (v1, v2…), conteudo, origem (`manual` | `saida-roteiro`), nota?, arquivoExportado (`01_roteiro/BJJ-001_roteiro_v3.md`), criadoEm.

**Cena:** vídeo, ordem, trechoRoteiro, prompt, ferramenta (texto livre), arquivos[] (relativos a `03_imagens/`), status (`pendente` | `ok` | `refazer`), favorita.

**PromptBanco:** canal, titulo, prompt, ferramenta, cenaOrigem?, arquivoExemplo?.

**Fonte:** vídeo, titulo, linkOuReferencia, tipo (livro · artigo · site · vídeo · entrevista · documento histórico), fatoSustentado, confiabilidade (alta · média · baixa), textoTela.

**TituloCandidato:** vídeo, texto, escolhido.

**VarianteThumbnail:** vídeo, letra (A/B/C), arquivo (em `06_thumbnail/`), escolhida, vencedoraTeste, percentualTempoExibicao?.

**Ativo:** canal, nome, tipo (música · SFX · overlay · foto/arquivo histórico · fonte tipográfica), arquivo (em `01_BIBLIOTECA/`), origem, link, licenca (Domínio público · CC0 · CC-BY · Biblioteca do YouTube · Assinatura · Outra), textoCredito, validoAte?.

**RegistroAnalytics:** vídeo, marco (`48h` | `7d` | `28d`), registradoEm, views, impressoes, ctr, duracaoMediaSeg, retencaoMedia, retencao30s, inscritosGanhos, trafego? (busca, sugeridos, navegação, shorts, externo, em %), aprendizado (obrigatório). Único por (vídeo, marco).

**CriteriosExperimento:** canal, dataInicio, duracaoDias (90), ctrMin (4%), retencao30sMin (65%), retencaoMediaMin (35%), multiplicadorForaDaCurva (2× a mediana de views em 7d), minimoForaDaCurva (1).

**ModeloPromptClaude** (v0.2): canal, tipo (`titulos` | `revisar-roteiro` | `cenas` | `analise` | `ideias`), template.

### Estrutura de pastas criada no Drive

```
DRIVE_ROOT/
├── _backup/                         gerenciador_AAAA-MM-DD.db
└── <pasta do canal>/
    ├── 00_IDENTIDADE/
    ├── 01_BIBLIOTECA/
    └── VIDEOS/
        └── BJJ-001_slug-do-titulo/
            ├── 01_roteiro/      BJJ-001_roteiro_v1.md …
            ├── 02_audio/
            ├── 03_imagens/
            ├── 04_video/
            ├── 05_projeto/      BJJ-001_fontes_tela.txt (v0.2)
            ├── 06_thumbnail/
            └── 07_export/
```

Convenção de arquivos: `BJJ-001_narracao_v2.mp3`, `BJJ-001_thumb_B.png`.

## 6. Telas

### v0.1: Produção

1. **Início:** seletor de canal, vídeos em risco, estoque ("N vídeos prontos = X semanas") e próximos horários vazios da grade.
2. **Kanban do canal:** 9 colunas com arrastar e soltar. O card mostra código, título, miniatura da thumb escolhida, ⚠️ de checklist, alerta de risco, ✅/❌ por subpasta e data planejada. A coluna Ideia é ordenada pela pontuação. Filtros por formato, série e tema.
3. **Nova ideia (rápida):** canal, título provisório, formato e as 3 notas. Mostra o aviso de títulos parecidos.
4. **Colar várias ideias:** uma por linha, com formato "a definir" e aviso de duplicidade por linha.
5. **Ficha do vídeo** (abas):
   - *Básico:* títulos (provisório, candidatos e escolhido), formato, série, temas, notas, datas, derivadoDe.
   - *Roteiro:* gancho, resumo, editor Markdown com pré-visualização, contagem de palavras e duração estimada (~150 palavras/min), "Salvar versão", histórico e diff entre versões.
   - *Cenas:* lista ordenável com prompt, ferramenta, arquivos (com miniatura), status, ⭐ e fontes ligadas. Mostra o progresso ("18/30 ok, 4 refazer").
   - *Fontes:* lista com tipo, fato, confiabilidade, texto de tela e cenas ligadas (⚠️ "sem exibição no vídeo" quando não há cena).
   - *Produção:* voz usada, duração final, notas de corte.
   - *Publicação:* descrição, tags, capítulos, variantes de thumbnail (A/B/C, escolhida, resultado do teste) e links do YouTube.
   - *Arquivos:* listagem por subpasta, com ☁️ para arquivos só online, miniaturas de imagens, "Abrir no Finder" e "Criar pasta" / "Renomear pasta" (com confirmação).
   - *Checklist e histórico:* itens por etapa e linha do tempo das etapas.
6. **Configurações do canal:** dados gerais, grade, formatos, séries, temas, modelos de checklist, padrões (descrição, tags, voz, estilo de imagem) e referências de identidade.
7. **Banco de prompts do canal:** prompts ⭐ com exemplo e origem.

### v0.2: Publicação e análise

8. **Ativos e licenças do canal**, com a marcação de uso na ficha do vídeo.
9. **Na ficha:** descrição montada (`{creditos}`, `{fontes}`, `{capitulos}`), validação de limites, botões **Copiar para o Studio** (título, descrição, tags, capítulos) e **Exportar fontes de tela**.
10. **Registrar marco:** formulário curto (7 campos + tráfego opcional + aprendizado).
11. **Registrar hoje** (na Início): marcos vencidos ou que vencem hoje.
12. **Revisão do experimento:** critérios editáveis, semáforo por critério, dias restantes e gráfico vídeo a vídeo (CTR, % aos 30s e retenção no marco de 7d) com a linha do critério.
13. **O que funciona:** médias no marco de 7d por formato, série e faixa de pontuação, e a linha do tempo dos aprendizados.
14. **Copiar para o Claude:** botões contextuais (títulos, revisar roteiro, cenas/prompts, análise, ideias) e templates editáveis por canal.

## 7. Roadmap

| Versão | Conteúdo | Quando |
|---|---|---|
| **v0.1 Produção** | Seções 4, 5 e telas 1–7, backup, validação do `.env`, testes | Antes de começar o estoque |
| **v0.2 Publicação e análise** | Telas 8–14 | Antes do 1º vídeo publicado |
| v0.3 | API da Anthropic no lugar do "Copiar para o Claude", com as respostas voltando para a ficha | Pós-MVP |
| v0.4 | **YouTube Fase 2:** OAuth (app publicado em "Produção" para os tokens não expirarem), coleta automática dos marcos | Quando o registro manual pesar |
| v0.5 | Marcação automática do checklist pelo conteúdo das pastas | — |
| Futuro | Acesso pelo celular via Tailscale; entidade Pauta e fontes globais (com o 2º canal); comparação entre canais; **YouTube Fase 3** (sincronizar metadados e detectar publicação); **Fase 4** (upload e agendamento, se a auditoria do Google compensar); servidor MCP; miniaturas de vídeo | Conforme a necessidade |

## 8. Recomendações fora do sistema

- Criar o canal do YouTube como **Conta de marca** sob `mondini@gmail.com`.
- Marcar `Meu Drive/Canais YouTube` como **"Disponível off-line"** no Drive for Desktop.
- Usar só a **Biblioteca de Áudio do YouTube** nos 90 dias.
- Preferir um **estilo de imagem ilustrado** (posições de BJJ geradas por IA costumam sair erradas, e imagens realistas exigem a divulgação de conteúdo sintético).

## 9. Pendências que não bloqueiam a implementação

Estes pontos são preenchidos no próprio app, depois que ele existir:

- Nome do canal e nome da pasta do canal no Drive.
- Dias e horário da grade de publicação.
- Gerador de imagens, ferramenta de voz e editor (CapCut ou DaVinci): ficam como texto livre.
- Textos finais dos modelos de checklist e do modelo de descrição (o sistema vem com padrões sugeridos).

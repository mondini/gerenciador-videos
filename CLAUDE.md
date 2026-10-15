# Repositório de canais do YouTube: regras gerais

Este repositório guarda a produção de **vários canais do YouTube**. Não há sistema nem app (só o painel de leitura `./canais`): cada canal é um projeto independente na própria pasta, e todos dividem o repositório para simplificar comandos, commits e backups.

- **Este arquivo** traz as regras gerais, que valem para todos os canais.
- **O `CLAUDE.md` de cada canal** traz a ficha e as regras daquele canal. Ele detalha e pode restringir as regras gerais; se contradisser uma delas, perguntar ao dono.
- Antes de qualquer tarefa, identifique o canal e leia o `CLAUDE.md` dele.

## Canais

| Canal | Pasta | Fase | Idioma público | Prefixo | Commits |
|---|---|---|---|---|---|
| Marble & Ash (estoicismo) | `canal-estoicismo/` | Em produção | Inglês | `MA` | `feat(canal-estoicismo): …` |
| Histórias católicas (nome a definir) | `canal-historias-biblicas/` | Piloto | Inglês | a definir | `feat(canal-historias-biblicas): …` |

Fora dos canais:
- `./canais`: painel de todos os canais (ver "Painel dos canais").
- `docs/`: documentos comuns a todos os canais (pacote de publicação, guia de embalagem).
- `ferramentas/`: código do painel (`canais.py`) e seus testes.
- `ideias-de-canais/`: caderno de ideias de canais futuros e protótipos. Não é canal.

Ao criar, pausar ou encerrar um canal, atualizar esta tabela.

## Isolamento entre canais

- **Trabalho de um canal fica restrito à pasta daquele canal.** Fora dela, só é permitido ler este arquivo, a pasta `docs/` da raiz e o `.env` da raiz (só `DRIVE_ROOT` e `ELEVENLABS_API_KEY`). Nada de ler, criar, editar ou apagar arquivos de outro canal.
- O painel da raiz (`./canais`) lê os arquivos do contrato de cada canal (seção "Painel dos canais") e roda o comando de status dele. Só lê; nunca altera nada no canal.
- Um canal não copia nem referencia scripts, assets, roteiros ou configurações de outro canal. Se algo de um canal parecer útil no outro, perguntar ao dono. O que valer para todos sobe para `docs/` da raiz, com aprovação do dono.
- **Commits:** cada commit tem arquivos de um projeto só (`git add <pasta>`, nunca `git add -A` ou `git add .`).
  - Canal: `feat(canal-<nome>): …` ou `fix(canal-<nome>): …`.
  - Raiz (este arquivo, `docs/`, `ferramentas/`, `canais`, `.env.example`, `.gitignore`): `docs(repo): …` ou `chore(repo): …`.
  - Caderno de ideias: `docs(ideias): …`.

## Regras comuns

- O dono é um criador de conteúdo brasileiro. **Conversa e documentação em pt-BR.** Código, variáveis e commits podem ficar em inglês. O que é público em cada canal segue o idioma do canal (ficha no `CLAUDE.md` dele).
- Usa Mac, VS Code e Google Drive for Desktop. A raiz do Drive é o `DRIVE_ROOT` do `.env` da raiz. Nunca fixe esse caminho no código.
- Credenciais (chave do ElevenLabs, OAuth do Google/YouTube) ficam no `.env` da raiz ou em arquivos ignorados pelo git, nunca no código. O `.env.example` mostra as chaves esperadas, sem valores.
- **Commit e push só quando o dono pedir** (regra geral de 14/10/2026, substitui o commit automático de 12/10/2026). Nada de commit automático ao fechar bloco, e sem ficar lembrando de commits pendentes.
- **Nunca inventar** fonte, citação, versículo, link ou licença. Na dúvida, perguntar ou marcar `VERIFICAR`.
- Para afirmações sobre preços, licenças ou políticas atuais (YouTube, ElevenLabs, bancos de música), pesquisar antes de afirmar.
- **Conteúdo inautêntico:** cada vídeo tem roteiro, gancho e cenas próprios. Nunca um vídeo-modelo com dados ou nomes trocados (política do YouTube).

## Estrutura padrão de um canal

```
canal-<nome>/
  CLAUDE.md                  ficha do canal + regras do canal (obrigatório)
  canal.json                 nome, prefixo do código, pasta no Drive e comando de status
  elevenlabs.json            configuração da narração (obrigatório, ver "Narração")
  creditos-elevenlabs.csv    um registro por geração de narração (ver "Narração")
  calendario.json            publicações planejadas, agendadas e feitas (ver "Painel dos canais")
  .gitignore                 mídia pesada fora do git
  docs/
    plano-canal.md           decisões, cadência, lista de vídeos
    fluxo-por-video.md       passo a passo de cada sessão
    pacote-de-publicacao-canal.md   complemento do pacote (ver "Publicação")
    ...                      estilo visual e outros documentos do canal
  pipeline/                  código de produção, quando houver
  videos/<PREFIXO-NNN-slug>/ uma pasta por vídeo: roteiro.md, audio/, final/, thumbnails/, pacote-de-publicacao.md...
```

**Ficha do canal:** todo `CLAUDE.md` de canal começa com a mesma tabela: nome, tema, público, idioma público, YouTube, prefixo e pasta no Drive, formato, cadência, narração, ferramentas, fase e documentos. Campo indefinido fica "a definir".

## Vídeos: código, etapas e Drive

- **Código:** `PREFIXO-NNN` (ex.: `MA-001`). **Pasta:** `CÓDIGO-slug` (ex.: `MA-001-the-man-who-had-everything`), com o mesmo nome no canal e no Drive.
- **Etapas padrão de um vídeo:** Ideia → Pesquisa → Roteiro → Narração → Imagens → Edição → Thumbnail → Pronto → Agendado → Publicado. *Pronto* = tudo entregue (final, thumbnails, shorts, pacote), falta só agendar. O status sai dos arquivos do vídeo (ex.: `./ma status N` no Marble & Ash) e do `calendario.json`, não de tabela escrita à mão.
- O `roteiro.md` do vídeo, na pasta do canal, é a fonte da verdade do roteiro.
- **Drive:** `DRIVE_ROOT/<pasta_drive do canal.json>/VIDEOS/<CÓDIGO-slug>/`, sempre com as mesmas subpastas: `01_roteiro/`, `02_audio/`, `03_imagens/`, `04_video/`, `05_projeto/`, `06_thumbnail/`, `07_export/`. A biblioteca do canal vai para `DRIVE_ROOT/<pasta_drive>/BIBLIOTECA/`.
- **Nada é apagado no Google Drive.** Limpeza de arquivos só na pasta local do canal, depois do backup.
- Áudios e vídeos ficam fora do git (`.gitignore` do canal) e vão para o Drive pelo backup do canal.

## Narração (ElevenLabs)

Narração é sempre no ElevenLabs (decisão de 14/10/2026), em todos os canais, atuais e futuros.

- **Chave:** uma só, `ELEVENLABS_API_KEY` no `.env` da raiz. Nenhum canal guarda chave na própria pasta.
- **Configuração por canal, obrigatória:** cada canal tem um `elevenlabs.json` na raiz da sua pasta, com modo (`api` ou `site`), voz (nome e `voice_id`), modelo (nome e `model_id`), configurações da voz, idioma, formato de saída e regra de créditos. Antes de gerar qualquer áudio, ler esse arquivo; nunca usar voz ou configuração de outro canal nem valor padrão. Campo `null` é pendência: perguntar ao dono e preencher antes de gerar. Canal novo só começa a narrar com o arquivo completo.
- **Confirmar antes de gerar:** antes de toda geração (inclusive regravação e teste), dizer com clareza o que será gerado (vídeo, blocos, número de caracteres), com qual voz e modelo, **quantos créditos em média** vai custar (pela regra de créditos do `elevenlabs.json`; total e por bloco) e o saldo atual da conta (`./canais creditos`). Só gerar depois do "sim" do dono, para aquela geração. Consultas que não gastam créditos (listar vozes, ver saldo) não precisam de confirmação.
- **Registrar depois de gerar:** uma linha no `creditos-elevenlabs.csv` do canal (`data,video,o_que,caracteres,creditos,origem,nota`). `origem` = `medido` (diferença do saldo antes e depois, pelo `./canais creditos`) ou `estimado` (pelos caracteres, quando não deu para medir). Vale também quando o dono gera pelo site: perguntar ou medir pelo saldo.

## Painel dos canais

`./canais` (na raiz) mostra, numa tela: os vídeos de cada canal por etapa, as próximas publicações de todos os canais (horário de Brasília e do público) e os créditos do ElevenLabs (saldo da conta, gasto por canal, quanto falta gastar nos roteiros abertos). `./canais calendario -d 30` e `./canais creditos` dão o detalhe. Testes: `python -m pytest ferramentas/testes`.

Para aparecer no painel, cada canal mantém:
- **`canal.json`** com `"status"`: comando, rodado na pasta do canal, que imprime `{"videos": [{"codigo", "titulo", "etapa", "concluido", "pendencias", "creditos_pendentes"}]}` com todos os vídeos, inclusive as ideias. Sem esse comando, o painel estima a etapa pelas pastas (`roteiro.md`, `audio/`, `final/`, pacote).
- **`calendario.json`**: `{"fuso": "America/New_York", "itens": [{"data": "AAAA-MM-DD", "hora": "HH:MM", "tipo": "video"|"short", "codigo", "titulo", "situacao": "planejado"|"agendado"|"publicado"}]}`. Atualizar sempre que uma data for decidida ou mudar, e quando o dono agendar no YouTube Studio (`agendado`). Vídeo agendado cuja data passou aparece como Publicado.
- **`creditos-elevenlabs.csv`**: ver "Narração".

## Publicação

- **Pacote de Publicação** obrigatório ao concluir cada vídeo: base comum em `docs/pacote-de-publicacao.md` + complemento do canal em `<canal>/docs/pacote-de-publicacao-canal.md`. Salvo em `videos/<CÓDIGO-slug>/pacote-de-publicacao.md`.
- **Guia de embalagem** (`docs/guia-embalagem-youtube.md`): referência para títulos, thumbnails, descrição, metadados e retenção em todos os canais. Quando conflitar com uma decisão registrada do canal, apontar o conflito ao dono em vez de decidir sozinho.
- Decisões de um canal vão para o `docs/plano-canal.md` dele. Decisões que valem para todos vão para este arquivo.

## Canal novo

1. Criar `canal-<nome>/` com a estrutura padrão. O `CLAUDE.md` começa pela ficha.
2. `canal.json` (com o comando de status), `elevenlabs.json` completo (voz escolhida e testada com o dono), `creditos-elevenlabs.csv` (só o cabeçalho) e `calendario.json`.
3. `docs/plano-canal.md` e `docs/pacote-de-publicacao-canal.md`.
4. Linha nova na tabela "Canais" deste arquivo.
5. Se o canal veio do `ideias-de-canais/`, levar a ficha da ideia para o `plano-canal.md` e tirá-la do caderno.

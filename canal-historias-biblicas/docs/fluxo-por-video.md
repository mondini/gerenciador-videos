# Fluxo de uma sessão por vídeo

Cada vídeo é feito numa sessão própria. No início da sessão, o Claude lê, nesta ordem: `CLAUDE.md` (pasta do canal) → `docs/plano-canal.md` → `docs/doutrina-e-fontes.md` → `docs/estilo-visual.md` → `../docs/pacote-de-publicacao.md` (base comum, na raiz) → `docs/pacote-de-publicacao-canal.md` → `../docs/guia-embalagem-youtube.md` → `videos/XX-NNN-slug/roteiro.md` (se existir).

> O pipeline (`pipeline/`) já renderiza as cenas e monta o vídeo (`pipeline.montar`). Narração pela API, legendas, backup e limpeza ainda não têm código: esses passos são feitos à mão pelo Claude, com as mesmas regras.

## 1. Pauta
- Olhar o calendário litúrgico das próximas 6 a 10 semanas (`plano-canal.md`) e propor temas que caiam em datas próximas.
- Escolher a série (Santos, Mandamentos, Parábolas, Salmos e versículos) e conferir se o vídeo não repete a estrutura de um anterior.

## 2. Roteiro
- Primeiro o **banco de fontes** do tema: versículos (Douay-Rheims), parágrafos do Catecismo e citações de domínio público, já conferidos na fonte, para o criador escolher.
- Depois a **escaleta** do vídeo inteiro (blocos, ideia de cada um, ideias de cena, a virada da história), aprovada pelo criador. Aplicar o teste de originalidade do `plano-canal.md`.
- Então construir bloco a bloco, com perguntas ao criador; nada genérico, nada infantil.
- Cada bloco no roteiro traz: o texto falado (pronto para a narração), a indicação de cena e a lista de assets que ele pede.
- Nomes difíceis: conferir no `glossario-pronuncia.md`; termos novos entram com `VERIFICAR`.
- Ao aprovar cada bloco, o título da seção ganha `(aprovado)` e o bloco é **fechado** (passo 8).
- Antes de fechar o roteiro: passar o checklist doutrinário (`doutrina-e-fontes.md`) e informar o custo estimado de narração (~1 crédito por caractere, total e por bloco).

## 3. Narração
- Com o roteiro todo aprovado, gerar todos os blocos de uma vez pela API do ElevenLabs (Eleven v4, voz e configurações fixas do `elevenlabs.json`, depois de o criador confirmar o custo em créditos). Um arquivo por bloco em `videos/XX-NNN-slug/audio/`.
- Ouvir os termos novos do glossário; se algum sair errado, ajustar e regravar só aquele bloco.
- Backup logo depois (o áudio é pago) e registro do gasto em `creditos-elevenlabs.csv`, medido pelo saldo antes e depois (`./canais creditos`, na raiz).

## 4. Cenas
- O Claude desenha cada cena do roteiro como um HTML único em `videos/XX-NNN-slug/cenas/` (`cNN-descricao.html`), seguindo o `estilo-visual.md`. Antes de desenhar um elemento, procura em `biblioteca/elementos/`; elemento novo que vai se repetir entra lá.
- Conferir as cenas internamente (traço, paleta, loop sem salto, nada infantil), sem pedir aprovação de frames ao criador.
- Junto com as cenas, o `montagem.json` do vídeo: a ordem das cenas e as falas que cada uma cobre.

## 5. Montagem
- `.venv/bin/python -m pipeline.montar videos/XX-NNN-slug`: renderiza as cenas em `gravacoes/` e monta o vídeo em `final/` (detalhes em `plano-canal.md`, "Montagem").
- Com a narração pronta, os tempos das cenas passam a vir do áudio; música licenciada ou por código, mix normalizado e o SRT das legendas.
- Entregar o vídeo montado para a **revisão única** do criador. Ajustes: refazer só as cenas tocadas. Aprovado: fechar (passo 8).

## 6. Entregáveis de publicação
- 3 thumbnails (A, B e C) para o teste A/B do YouTube, 1280×720 PNG < 2 MB, em `thumbnails/`, conferidas em 320×180. Nunca com cara de conteúdo infantil.
- **Pacote de Publicação** (15 seções) em `videos/XX-NNN-slug/pacote-de-publicacao.md`, partindo das seções fixas do pacote do vídeo anterior. Pedir os links do canal ao criador.

## 7. Fechar a sessão
- Backup do que mudou no canal. Commit e push só quando o criador pedir (regra geral de 14/10/2026).
- Anotar decisões novas em `docs/plano-canal.md` (e no `estilo-visual.md` ou `doutrina-e-fontes.md`, se forem dessas áreas).
- Vídeo concluído: limpeza local (abaixo).

## 8. Fechar um bloco (sem pedir ao criador)
Quando o criador aprova o texto de um bloco ou o vídeo montado (a revisão única fecha todos os blocos):
1. Texto: marcar `(aprovado)` no título da seção do roteiro.
2. Backup no Drive.
3. Sem commit: commit e push só quando o criador pedir (regra geral de 14/10/2026).

## Backup no Drive

Destino: `DRIVE_ROOT/<pasta_drive do canal.json>/VIDEOS/<XX-NNN-slug>/` (o `DRIVE_ROOT` vem do `.env` da raiz do repositório; nunca fixar o caminho no código). Subpastas padrão (iguais em todos os canais, ver `CLAUDE.md` da raiz):

| Subpasta | O que vai |
|---|---|
| `01_roteiro/` | `roteiro.md`, `pacote-de-publicacao.md` |
| `02_audio/` | narração (mp3) |
| `03_imagens/` | cenas em HTML (`cenas/`) |
| `04_video/` | vídeos das cenas (`gravacoes/`) e prévias |
| `05_projeto/` | `montagem.json`, linha do tempo |
| `06_thumbnail/` | thumbnails |
| `07_export/` | vídeo final e SRT |

A biblioteca do canal vai para `DRIVE_ROOT/<pasta_drive>/BIBLIOTECA/` (mesma estrutura de `biblioteca/`).

Regras:
- Só copia o que mudou. Arquivos pequenos são comparados pelo conteúdo; mídia grande, por tamanho e data (sem baixar do Drive).
- Cópia por arquivo temporário (`.nome.parcial`) renomeado no fim: o Drive nunca vê arquivo pela metade.
- Texto e projeto (roteiro, pacote, cenas HTML, tempos, thumbnails) que mudaram guardam a versão anterior em `_versoes/<AAAA-MM-DD_HHMMSS>/`; mídia que dá para gerar de novo (prévias, final) é só atualizada.
- **Nunca apaga nada no Drive.**

| Quando | |
|---|---|
| Narração nova (créditos pagos) | logo depois de gerar |
| Vídeos das cenas novos (`gravacoes/`) | depois do render |
| Bloco fechado | passo 8 |
| Vídeo final montado | logo depois de montar |
| Thumbnails ou pacote entregues | ao entregar |
| Fim de toda sessão | sempre |

## Limpeza (vídeo concluído)

Só depois de refazer o backup, e só na pasta local: sai o que tem cópia no Drive ou é refeito pelo pipeline (intermediários, prévias, stills de conferência). Ficam roteiro, áudios, cenas HTML, final, thumbnails e pacote; os vídeos das cenas (`gravacoes/`) saem (estão no Drive e o `pipeline.montar` os renderiza de novo a partir do HTML). A limpeza recusa qualquer caminho fora de `videos/`. Nunca apagar no Drive.

# Fluxo de uma sessão por vídeo

Cada vídeo é feito numa sessão própria. No início da sessão, o Claude lê, nesta ordem: `CLAUDE.md` (pasta do canal) → `docs/plano-canal.md` → `docs/doutrina-e-fontes.md` → `docs/estilo-visual.md` → `docs/pacote-de-publicacao-regras.md` → `docs/guia-embalagem-youtube.md` → `videos/XX-NNN-slug/roteiro.md` (se existir).

> O pipeline (`pipeline/`) ainda não existe; será criado no piloto. Até lá, os passos que citam comandos são feitos à mão pelo Claude, com as mesmas regras.

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
- Com o roteiro todo aprovado, gerar todos os blocos de uma vez pela API do ElevenLabs (Eleven v4, voz e configurações fixas do `plano-canal.md`). Um arquivo por bloco em `videos/XX-NNN-slug/audio/`.
- Ouvir os termos novos do glossário; se algum sair errado, ajustar e regravar só aquele bloco.
- Backup logo depois (o áudio é pago).

## 4. Imagens
- O Claude escreve os prompts de cada cena (prompt base do `estilo-visual.md` + cena + nome de arquivo), já procurando no catálogo o que dá para reaproveitar.
- O criador gera no Gemini e salva em `videos/XX-NNN-slug/imagens/`, seguindo o fluxo do `estilo-visual.md` (cena inteira → cena sem personagens → elementos isolados).
- O Claude recorta os elementos, confere bordas e cataloga em `biblioteca/` o que for reaproveitável.

## 5. Animação e montagem
- Cenas em Remotion a partir de JSON (camadas, poses, câmera, partículas, áudio), sincronizadas pelos tempos do áudio.
- Conferir as cenas internamente, sem pedir aprovação de frames ao criador.
- Montar o vídeo inteiro com música licenciada e mix normalizado, e gerar o SRT das legendas.
- Entregar o vídeo montado para a **revisão única** do criador. Ajustes: refazer só as cenas tocadas. Aprovado: fechar (passo 8).

## 6. Entregáveis de publicação
- 3 thumbnails (A, B e C) para o teste A/B do YouTube, 1280×720 PNG < 2 MB, em `thumbnails/`, conferidas em 320×180. Nunca com cara de conteúdo infantil.
- **Pacote de Publicação** (16 seções) em `videos/XX-NNN-slug/pacote-de-publicacao.md`, partindo das seções fixas do pacote do vídeo anterior. Pedir os links do canal ao criador.

## 7. Fechar a sessão
- Backup, commit e push do que mudou no canal.
- Anotar decisões novas em `docs/plano-canal.md` (e no `estilo-visual.md` ou `doutrina-e-fontes.md`, se forem dessas áreas).
- Vídeo concluído: limpeza local (abaixo).

## 8. Fechar um bloco (sem pedir ao criador)
Quando o criador aprova o texto de um bloco ou o vídeo montado (a revisão única fecha todos os blocos):
1. Texto: marcar `(aprovado)` no título da seção do roteiro.
2. Backup no Drive.
3. Commit só dos arquivos desta pasta: `feat(canal-historias-biblicas): XX-NNN bloco X …`, seguido de push.

## Backup no Drive

Destino: `DRIVE_ROOT/<pasta_drive do canal.json>/VIDEOS/<XX-NNN-slug>/` (o `DRIVE_ROOT` vem do `.env` da raiz do repositório; nunca fixar o caminho no código). Subpastas padrão do sistema de gestão:

| Subpasta | O que vai |
|---|---|
| `01_roteiro/` | `roteiro.md`, `pacote-de-publicacao.md` |
| `02_audio/` | narração (mp3) |
| `03_imagens/` | imagens geradas no Gemini (originais) e recortes |
| `04_video/` | prévias |
| `05_projeto/` | JSON das cenas, tempos |
| `06_thumbnail/` | thumbnails |
| `07_export/` | vídeo final e SRT |

A biblioteca do canal vai para `DRIVE_ROOT/<pasta_drive>/BIBLIOTECA/` (mesma estrutura de `biblioteca/`). Conferir o nome dessa pasta com o sistema de gestão quando o canal for sincronizado.

Regras:
- Só copia o que mudou. Arquivos pequenos são comparados pelo conteúdo; mídia grande, por tamanho e data (sem baixar do Drive).
- Cópia por arquivo temporário (`.nome.parcial`) renomeado no fim: o Drive nunca vê arquivo pela metade.
- Texto e projeto (roteiro, pacote, JSON, tempos, thumbnails) que mudaram guardam a versão anterior em `_versoes/<AAAA-MM-DD_HHMMSS>/`; mídia que dá para gerar de novo (prévias, final) é só atualizada.
- **Nunca apaga nada no Drive.**

| Quando | |
|---|---|
| Narração nova (créditos pagos) | logo depois de gerar |
| Imagens novas do Gemini | ao recebê-las |
| Bloco fechado | passo 8 |
| Vídeo final montado | logo depois de montar |
| Thumbnails ou pacote entregues | ao entregar |
| Fim de toda sessão | sempre |

## Limpeza (vídeo concluído)

Só depois de refazer o backup, e só na pasta local: sai o que tem cópia no Drive ou é refeito pelo pipeline (intermediários, prévias, stills de conferência). Ficam roteiro, áudios, imagens originais, JSON das cenas, final, thumbnails e pacote. A limpeza recusa qualquer caminho fora de `videos/`. Nunca apagar no Drive.

# Fluxo de uma sessão por vídeo

Cada vídeo é feito numa sessão própria. No início da sessão, o Claude lê, nesta ordem: `CLAUDE.md` (pasta do canal) → `docs/plano-canal.md` → `docs/estilo-teatro-de-sombras.md` → `docs/pacote-de-publicacao-regras.md` → `docs/guia-embalagem-youtube.md` → `videos/MA-NNN-slug/roteiro.md` (se existir) → `pipeline/LEIA-ME.md`. Depois, `./ma status N` mostra onde o vídeo parou.

## 1. Preparar o ambiente (começo de toda sessão)
- O ambiente já fica em `.venv/` dentro da pasta. Conferir com `./ma -h`. Se faltar, instalar como em `pipeline/LEIA-ME.md` (seção 1).
- Conferir que o pipeline continua fiel ao padrão aprovado: `.venv/bin/python -m pytest pipeline/testes`.
- Vídeo novo: `./ma novo N` cria a pasta `videos/MA-NNN-slug/` e o `roteiro.md` inicial a partir da ficha do plano.
- Processo do vídeo 2 em diante: ver "Processo mais eficiente" em `docs/plano-canal.md` (inclui as melhorias do pipeline a fazer no começo da sessão do vídeo 2).

## 2. Roteiro (se ainda não estiver aprovado)
- Primeiro o **banco de citações** do tema, já conferidas na fonte. Se o tema pedir outra obra ou tradução, procurar a melhor em domínio público e propor; o criador valida.
- Depois a **escaleta** do vídeo inteiro (blocos, ideias de cena, Pausa), aprovada pelo criador.
- Então construir bloco a bloco, com perguntas ao criador; nada genérico. Anotar no roteiro as frases que dão short.
- Estrutura: gancho → abertura 2 s → blocos → The Pause (falada e curta) → provérbio-ponte → fechamento. Total ~10 min (~1.300–1.500 palavras faladas).
- Conferir cada citação na fonte de domínio público antes de propor; registrar no "Registro de fontes" do roteiro.
- Entregar cada bloco no formato pronto para colar no ElevenLabs.
- Salvar cada bloco em `videos/MA-NNN-slug/roteiro.md`. Ao ser aprovado, o título da seção ganha `(aprovado)` e o bloco é **fechado** (ver passo 8).
- Ao fechar o roteiro, avisar o custo estimado no ElevenLabs (`./ma status N` mostra os créditos do que falta narrar).
- Gancho e retenção seguem `docs/guia-embalagem-youtube.md` (seção 5): confirmar a promessa do título/thumbnail nos primeiros 15 s, falar a palavra-chave principal nos primeiros 30 s, abrir um *loop* para o meio ou o fim.

## 3. Áudio e tempos
- Com o roteiro todo aprovado, o criador gera todos os blocos de uma vez no ElevenLabs (plano Starter, mesma voz) e envia os mp3. Enquanto isso, o Claude já escreve as cenas (por nome de deixa) e cria a arte nova.
- Salvar em `videos/MA-NNN-slug/audio/` com `blocoN` no nome (ex.: `MA-002-bloco2-starter.mp3`).
- `./ma audio N N` — detecta as pausas e alonga-as levemente (ritmo final ~150 palavras/min) (grava `videos/MA-NNN-slug/blocoN/audio.json`).
- `./ma tempos N N` — sugere `videos/MA-NNN-slug/blocoN/tempos.txt` com o início de cada frase (transcritor + pausas + texto do roteiro). Os nomes das deixas vêm da linha `**Deixas:**` de cada seção do roteiro (escrita junto com as cenas); conferir a tabela impressa. `./ma deixas N N` mostra os tempos no vídeo.

## 4. Animação (padrão Teatro de Sombras Projetadas)
- Para cada bloco, escrever o roteiro visual (cenas, entradas, foco de luz, zoom) a partir das ideias de cena do roteiro.
- Criar o script de cena `videos/MA-NNN-slug/blocoN/cena.py` copiando o modelo oficial `videos/MA-001-the-man-who-had-everything/bloco1/cena.py` (passo a passo em `pipeline/LEIA-ME.md`, seção 3). Reaproveitar as peças da biblioteca (`pipeline/marbleash/`); arte nova vai em `objetos.py`, `cenario.py` ou `bonecos.py`.
- Conferir as cenas novas em stills internamente (`./ma stills N N <segundos>`), sem pedir aprovação de frames ao criador (decisão de 12/10/2026); depois renderizar o bloco com `./ma render N N` (prévia com voz e ambiente em `videos/MA-NNN-slug/previas/blocoN.mp4`).
- Não mandar prévias de bloco ao criador: a revisão é **uma só**, do vídeo montado (passo 5).
- Simular a compressão do YouTube (~4 Mbps) e conferir degradês: `./ma youtube videos/MA-NNN-slug/previas/blocoN.mp4`; se aparecerem faixas, exportar em 4K (passo 5).
- Prévias e stills ficam em `videos/MA-NNN-slug/previas/`.

## 5. Montagem final
- `./ma juntar N 1 abertura 2 3 ...` — junta o gancho, a abertura padrão (`videos/comum/abertura`, com o som de transição) e os blocos com as transições do canal (dissolve entre blocos), mixa voz + som ambiente contínuo (−16 LUFS) e grava em `videos/MA-NNN-slug/final/`. Com `--4k`, também exporta ampliado para 4K.
- Entregar o vídeo montado para a **revisão única** do criador. Ajustes pedidos: refazer só os blocos tocados e juntar de novo. Aprovado: fechar (passo 8).

## 6. Entregáveis de publicação
- 3 thumbnails (A Palavra, B Símbolo, C Gancho) para o teste A/B do YouTube, em teatro de sombras com quadros reais do vídeo (ver `docs/plano-canal.md`); os arquivos finais (1280×720 PNG, < 2 MB) vão para `thumbnails/` (`MA-NNN_thumb_A.png`, `MA-NNN_thumb_B.png`, `MA-NNN_thumb_C.png`). Conferir em 320×180.
- Shorts verticais 1080×1920 (5 por vídeo, incluindo um de The Pause *"Take 30 seconds with Marcus Aurelius"*): escrever `videos/MA-NNN-slug/shorts.txt` (trechos por deixa, títulos em inglês) e rodar `./ma shorts N`; saem em `shorts/`. Formato (decisão de 12/10/2026): faixa central com a cena inteira, título em Cinzel em cima, legenda frase a frase embaixo; trechos do próprio vídeo, sem narração nova.
- **Pacote de Publicação** (16 seções, com os shorts prontos para colar) em `videos/MA-NNN-slug/pacote-de-publicacao.md`, partindo das seções fixas do pacote do vídeo anterior — pedir os links do canal ao criador.

## 7. Fechar a sessão
- `./ma fechar N` (backup + sistema), commit e push do que mudou no canal.
- Anotar decisões novas em `docs/plano-canal.md` (o status não se escreve: é o `./ma status`).
- Se `./ma status N` disser CONCLUÍDO: `./ma limpar N --apagar`.

## 8. Fechar um bloco (sem pedir ao criador)
Quando o criador aprova o texto de um bloco ou o vídeo montado (a revisão única fecha todos os blocos):
1. Texto: marcar `(aprovado)` no título da seção do roteiro.
2. `./ma fechar N`: backup no Drive + sincronizar com o sistema de gestão. Se o sistema não estiver rodando, avisar e seguir.
3. Commit só dos arquivos do canal: `feat(canal-estoicismo): MA-NNN bloco X …`, seguido de push.

## Quando fazer backup
| Momento | Como |
|---|---|
| mp3 novo do ElevenLabs (créditos pagos) | automático no `./ma audio` |
| Bloco fechado (texto ou vídeo montado aprovados) | `./ma fechar N` |
| Vídeo final montado | automático no `./ma juntar` |
| Thumbnails, shorts ou pacote entregues | `./ma fechar N` |
| Fim de toda sessão | `./ma fechar N` |
| Vídeo concluído | `./ma limpar N --apagar` (refaz o backup antes de limpar) |

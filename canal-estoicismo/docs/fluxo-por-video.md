# Fluxo de uma sessão por vídeo

Cada vídeo é feito numa sessão própria. No início da sessão, o Claude lê, nesta ordem: `CLAUDE.md` (pasta do canal) → `docs/plano-canal.md` → `docs/estilo-teatro-de-sombras.md` → `docs/pacote-de-publicacao-regras.md` → `videos/video-NN/roteiro.md` (se existir) → `pipeline/LEIA-ME.md`.

## 1. Preparar o ambiente (começo de toda sessão)
- O ambiente já fica em `.venv/` dentro da pasta. Conferir com `./ma -h`. Se faltar, instalar como em `pipeline/LEIA-ME.md` (seção 1).
- Conferir que o pipeline continua fiel ao padrão aprovado: `.venv/bin/python -m pytest pipeline/testes`.

## 2. Roteiro (se ainda não estiver aprovado)
- Construir bloco a bloco, com perguntas ao criador; nada genérico.
- Estrutura: gancho → abertura 2 s → blocos → The Pause (falada e curta) → provérbio-ponte → fechamento. Total ~10 min (~1.300–1.500 palavras faladas).
- Conferir cada citação na fonte de domínio público antes de propor; registrar no "Registro de fontes" do roteiro.
- Entregar cada bloco no formato pronto para colar no ElevenLabs.
- Salvar cada bloco aprovado em `videos/video-NN/roteiro.md`.

## 3. Áudio e tempos
- O criador gera cada bloco no ElevenLabs (plano Starter, mesma voz) e envia o mp3.
- Salvar em `videos/video-NN/audio/` com `blocoN` no nome (ex.: `video01-bloco2-starter.mp3`).
- `./ma audio video-NN N` — detecta as pausas e alonga-as levemente (ritmo final ~150 palavras/min) (grava `videos/video-NN/blocoN/audio.json`).
- `./ma tempos video-NN N` — sugere `videos/video-NN/blocoN/tempos.txt` com o início de cada frase (transcritor + pausas + texto do roteiro). Conferir a tabela impressa e dar nomes curtos às deixas que a cena vai usar. `./ma deixas video-NN N` mostra os tempos no vídeo.

## 4. Animação (padrão Teatro de Sombras Projetadas)
- Para cada bloco, escrever o roteiro visual (cenas, entradas, foco de luz, zoom) a partir das ideias de cena do roteiro.
- Criar o script de cena `videos/video-NN/blocoN/cena.py` copiando o modelo oficial `videos/video-01/bloco1/cena.py` (passo a passo em `pipeline/LEIA-ME.md`, seção 3). Reaproveitar as peças da biblioteca (`pipeline/marbleash/`); arte nova vai em `objetos.py`, `cenario.py` ou `bonecos.py`.
- Mostrar primeiro **um frame** para aprovação quando houver cena nova importante (`./ma stills video-NN N <segundos>`); depois renderizar o bloco com `./ma render video-NN N` (prévia com voz e ambiente em `videos/video-NN/previas/blocoN.mp4`).
- Simular a compressão do YouTube (~4 Mbps) e conferir degradês: `./ma youtube videos/video-NN/previas/blocoN.mp4`; se aparecerem faixas, exportar em 4K (passo 5).
- Prévias e stills ficam em `videos/video-NN/previas/`.

## 5. Montagem final
- `./ma juntar video-NN 1 abertura 2 3 ...` — concatena o gancho, a abertura padrão (`videos/comum/abertura`) e os blocos, mixa voz + som ambiente contínuo (−16 LUFS) e grava em `videos/video-NN/final/`. Com `--4k`, também exporta ampliado para 4K.

## 6. Entregáveis de publicação
- 3 thumbnails (A Palavra, B Símbolo, C Gancho) no canvas de design.
- Shorts verticais 1080×1920 (5–6 por vídeo, incluindo um de The Pause).
- **Pacote de Publicação** (15 seções) em `videos/video-NN/pacote-de-publicacao.md` — pedir os links do canal ao criador.

## 7. Fechar a sessão
- Atualizar o status em `docs/plano-canal.md` e anotar decisões novas.
- Garantir que roteiro, áudios, prévias, final e pacote estão na pasta do canal.

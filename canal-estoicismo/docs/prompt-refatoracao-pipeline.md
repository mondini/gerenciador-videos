> **Histórico:** prompt usado na refatoração do pipeline (11–12/10/2026), já executada. Não é instrução atual: os caminhos `videos/video-NN/` citados aqui hoje são `videos/MA-NNN-slug/`, e o pipeline vigente está descrito em `pipeline/LEIA-ME.md`.

Você vai refatorar o pipeline de produção de vídeos do canal Marble & Ash. Trabalhe com calma e capricho: este código vai ser usado nos próximos 12 vídeos, em sessões separadas, às vezes por modelos menores. Fale comigo em pt-BR.

## Contexto
Leia, nesta ordem, antes de qualquer coisa:
1. `CLAUDE.md`
2. `docs/plano-canal.md`
3. `docs/estilo-teatro-de-sombras.md` (padrão visual APROVADO — não mude o visual)
4. `docs/fluxo-por-video.md`
5. `videos/video-01/roteiro.md`
6. `pipeline/LEIA-ME.md` e todo o código em `pipeline/`

O código nasceu de experimentos feitos numa única conversa e tem estes problemas conhecidos:
- `render2.py` mistura utilidades genéricas com dados do vídeo 1 (tabelas de tempo `C1o`/`C2o`), lê `pace.json` no import e ainda desenha a arte do estilo antigo (traço fino), que não é mais usado.
- `shadow.py` → `shadow_bg2.py` → `shadow3.py` → `shadow4.py` → `shadow5.py` → `shadow6.py` são camadas de experimentos que importam umas às outras, com código duplicado e versões descartadas convivendo com as aprovadas.
- `shadowfilm.py` é o render do bloco 1 do vídeo 1, com tudo fixo no código (tempos, posições, cenas).
- Os tempos de cada frase vêm da detecção de pausas no áudio, cruzada à mão com o texto do roteiro. Não há transcritor disponível (a rede do ambiente bloqueia instalações).
- Muito trabalho pesado acontece no import dos módulos (lento e frágil).

## Objetivo
Transformar isso num pipeline limpo e reutilizável para qualquer vídeo e qualquer bloco, preservando exatamente o visual aprovado.

Arquitetura que sugiro (pode propor algo melhor, justificando):
- Uma biblioteca (ex.: `pipeline/marbleash/`) separada por responsabilidade: áudio (desacelerar, ambiente, mixagem a −16 LUFS), tempos (cues), kit de desenho (curvas, recortes, bonecos articulados), biblioteca de cenário e objetos romanos, compositor do lençol (luz, dobras, desfoque por profundidade, pano na base, grade sépia, chamas em cor, foco de luz, zoom, balanço nas varetas) e render (laço de quadros + ffmpeg).
- Dados de cada vídeo fora do código da biblioteca: `videos/video-NN/` com o roteiro, um arquivo de tempos por bloco (frase → segundo, gerado semi-automaticamente a partir das pausas + texto do roteiro, com ajuste manual possível) e um script de cena por bloco, curto e o mais declarativo possível.
- Uma linha de comando simples, por exemplo: gerar stills de conferência de um bloco em tempos escolhidos, renderizar um bloco, juntar os blocos com o áudio e simular a compressão do YouTube (~4 Mbps).
- Nada pesado no import; arte e máscaras geradas sob demanda e com cache.

## Regras
- **Não mude o visual aprovado.** Antes de refatorar, renderize stills de referência do bloco 1 com o código atual (por exemplo em 3, 9.5, 21.5, 30, 35.5, 41 e 47 s, usando os áudios Free de `videos/video-01/audio/`). Depois da refatoração, renderize os mesmos tempos e compare por diferença de pixels. Me mostre lado a lado e explique qualquer diferença.
- **Sem mãos de manipuladores** (já removidas a pedido).
- Remova do caminho principal o código do estilo antigo de traço fino (arquive em `pipeline/_arquivo/`, não apague).
- Não altere decisões de roteiro, estilo ou regras do canal. Se achar algo incoerente entre os documentos, **liste para mim**, não corrija por conta própria.
- Não faça commit no git sem me perguntar. Áudios e vídeos ficam fora do git.
- Documentação em pt-BR; código e nomes podem ficar em inglês.
- Meça o tempo de render por segundo de vídeo antes e depois (hoje ~20 s por segundo). Não pode piorar; se der para melhorar sem mudar o visual, melhor.

## Como trabalhar
1. Leia tudo e me apresente um plano curto: arquitetura proposta, o que vai para o arquivo morto, riscos. **Espere minha aprovação.**
2. Gere os stills de referência.
3. Refatore em etapas, conferindo os stills a cada etapa importante.
4. Converta o bloco 1 do vídeo 1 para o novo formato (tempos em arquivo de dados + script de cena) como exemplo oficial para os próximos blocos e vídeos.
5. Renderize o bloco 1 completo com o novo pipeline e passe pela simulação de compressão.

## Entregáveis
- Código refatorado em `pipeline/`, funcionando com um comando por etapa.
- `pipeline/LEIA-ME.md` reescrito: instalação, comandos, como criar um bloco novo passo a passo (pensado para um modelo menor seguir sem ajuda) e como gerar o arquivo de tempos a partir de um áudio novo.
- `docs/fluxo-por-video.md` atualizado com os comandos novos.
- Bloco 1 do vídeo 1 no novo formato, com o vídeo renderizado em `videos/video-01/previas/`.
- Um relatório final curto: o que mudou, comparação dos stills, tempo de render antes/depois, incoerências encontradas nos documentos e o que ficou pendente.

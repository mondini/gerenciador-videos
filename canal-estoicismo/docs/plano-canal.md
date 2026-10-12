# Marble & Ash — Plano do Canal

*Old wisdom for quiet hours.* Atualizado em 11/10/2026, ao fim da sessão de criação do canal.

Links (claude.ai):
- Plano colaborativo (Claude Docs): https://claude.ai/code/artifact/41d9cec2-ff3a-493c-83ac-34526173d40f
- Design System: https://claude.ai/artifact/YD1Vx9JHfUSKFFVMcdkQqh
- Canvas de logo, thumbs e banner: https://claude.ai/artifact/4TczXDna7NDn4JW9jyACkp

## Decisões do canal

- **Nome:** Marble & Ash. Mármore = bustos romanos e a pedra onde a sabedoria foi gravada; cinza = *memento mori*; o âmbar = a brasa que ainda brilha.
- **Formato:** canal dark (sem rosto), narração lenta e introspectiva, vídeos em **teatro de sombras projetadas** (ver `estilo-teatro-de-sombras.md`).
- **Idioma:** 100% inglês (público: EUA, Reino Unido, Canadá). O criador é fluente, não nativo — revisar sempre se o inglês soa natural.
- **Uso pretendido:** *slow learning* — ouvir limpando a casa, se exercitando ou tentando dormir.
- **Tema:** estoicismo com foco em **Marco Aurélio** e as *Meditações*, cruzado de forma sutil com **Provérbios** (sabedorias que se encontram, nunca pregação).
- **Posicionamento:** estoicismo sob pressão — toque **muito leve** de finanças, trabalho e liderança nos títulos e exemplos. Mudar o contexto, nunca a promessa. Nunca prometer enriquecimento. Âncora de negócios em ~2/3 dos títulos; um exemplo prático de trabalho/dinheiro por vídeo. Provérbios sobre riqueza guardados: 13:11, 21:5, 22:7.
- **Tom:** poético, calmo, sem ser complexo nem professoral; tom de diário noturno.
- **Duração:** **~10 minutos** por vídeo (decisão do vídeo 1). Cadência planejada: 2 vídeos/semana, 5–6 shorts por vídeo. Meta: 12 vídeos prontos antes de lançar.
- **Ferramentas:** Claude (roteiro, design no Claude Design, montagem do vídeo por código); ElevenLabs (**plano Starter**; voz e custo em "Voz e créditos do ElevenLabs"). Sem Canva nem Photoshop.
- **Futuro (não iniciar sem pedido):** faixas de áudio em espanhol/português no mesmo vídeo; outros canais (história atmosférica, mistérios do universo).

## Identidade visual

- Paleta 60·30·10: carvão `#1A1816`, mármore `#EDE6DA`, âmbar `#E8A33D` (thumbs: âmbar vivo `#FFB547` em 20–30% da imagem).
- Tipografia: **Cinzel** (títulos, nomes, logo), **Cormorant Garamond** (citações, itálico), **Inter** (créditos e legendas).
- Logo: A — Horizonte. Banner: B — Centro silencioso.
- Vídeos: teatro de sombras projetadas (padrão aprovado). Logo e banner continuam na arte de linhas.
- **Thumbnails em sombras (decisão de 12/10/2026):** feitas com quadros reais do vídeo, gradação puxada para o âmbar vivo e texto em Cinzel Black (mármore, destaque em âmbar), sempre à esquerda e longe do canto inferior direito (selo de duração). Assim a capa promete o que o vídeo mostra.
- Thumbnails: **2 versões** para o teste A/B do YouTube (decisão de 12/10/2026; antes eram 3) — A Palavra (1–2 palavras) e C Gancho (até 3 palavras; guia de embalagem). A variante B (Símbolo, sem texto) saiu. O texto da thumb nunca repete o título.

## Estrutura padrão de um vídeo (~10 min)

1. **Gancho** (~45 s): fala direto com a dor do ouvinte, sem entregar a resposta.
2. **Abertura** (3 s; 2 s até 12/10/2026): logo Horizonte + "MARBLE & ASH", com o som de transição **Brasa** (sintetizado por código em `pipeline/marbleash/sons.py`): um sopro sobe no escurecimento do gancho e um golpe grave e macio cai quando o sol acende, com faíscas na cauda.
3. **Blocos de conteúdo** (história/contexto, a fonte antiga, a lição aplicada à vida de hoje).
4. **The Pause** logo após a ideia mais forte.
5. **Provérbio-ponte**.
6. **Fechamento** que volta ao gancho, em calma.

## Transições entre peças (decisão de 12/10/2026)

Aplicadas pelo `./ma juntar`, iguais em todos os vídeos:
- **Bloco → bloco** (e entrada/saída da Pausa): **dissolve de 1,5 s**, sem escuro. Os blocos do meio terminam acesos e a voz do bloco seguinte entra 1,9 s depois do início dele (o intervalo entre as falas continua ~1,4 s).
- **Abertura → bloco 2:** o bloco nasce do escuro em 1,5 s.
- **Gancho → abertura** e **último bloco → encerramento:** o bloco escurece e corta (o último bloco declara `FADE` na cena).
- **Saída da Pausa:** escurece devagar (2,4 s) e o bloco seguinte só começa a aparecer **3 s depois da última frase**.

## The Pause — o diferencial do canal

Momento fixo em todo vídeo em que o espectador pratica o que ouviu.
- Deixa falada: *"Let's pause here."*
- **Precisa funcionar só com áudio:** o narrador guia a respiração em voz alta e **lê a pergunta** (feedback do vídeo 1: a versão muda e longa não funcionava).
- **Curta:** bem menos que 40 s (a prévia de ~40 s foi considerada longa).
- Visual: o sol do logo "respirando" (sobe na inspiração, desce na expiração), adaptado ao lençol de sombras; pergunta na tela.
- Capítulo próprio no YouTube. Vídeo 12 (sono) pode ter uma pausa mais longa encerrando o episódio.
- Formato de short: *"Take 30 seconds with Marcus Aurelius"*.

## Encerramento padrão (decisão de 12/10/2026)

- Última linha falada de todo vídeo, igual sempre: *"[softly] Old wisdom... for quiet hours."* (só o slogan, sem o nome do canal).
- O slogan começa **2 s depois da última frase do roteiro** (12/10/2026). Automático: `./ma tempos` (ou `./ma audio`, se os tempos já existem) acha a frase "Old wisdom" e alonga a pausa antes dela no áudio desacelerado; nada a regravar no ElevenLabs.
- **Nenhuma chamada falada** para inscrição ou comentário (o público ouve para dormir); o pedido fica só na descrição e na tela final do YouTube.
- Visual: o logo Horizonte + slogan em Cormorant Garamond itálico (`marble-300`), peça comum em `videos/comum/` (a criar).

## Voz e créditos do ElevenLabs (desde o vídeo 1, 12/10/2026)

- **Voz:** *Flint — Deep, Raspy, and Warm* (substituiu a voz de senhor ~70 anos usada nas prévias Free).
- **Modelo:** Eleven v4 · **Stability 50%** · **Similarity 75%** · plano **Starter**. Usar sempre a mesma configuração para a voz não mudar entre blocos e vídeos.
- **Custo medido no vídeo 1:** 7 áudios (6 blocos + The Pause), uma gravação de cada, **6.638 créditos** (saldo 35.500 → 28.862). O texto colado tinha ~6.600–6.700 caracteres (com as audio tags) e ~1.180 palavras, para ~8 min de narração (8 min 6 s já no ritmo do canal).
- **Regra para estimar:** **~1 crédito por caractere** do texto colado no ElevenLabs, contando as audio tags e a pontuação. Equivalências aproximadas: ~5,6 créditos por palavra; ~820 créditos por minuto de narração; um vídeo de ~10 min ≈ 6.500–8.000 créditos. Regravações cobram de novo: somar o texto de cada bloco regravado.
- Ao fechar o roteiro de um vídeo, o Claude informa a estimativa de créditos (total e por bloco) antes da gravação.

## Guia de embalagem — decisões do criador (12/10/2026)

Referência: `guia-embalagem-youtube.md`. Onde o guia conflitava com o canal:
- **Texto da thumbnail:** passa a ser no máximo **3 palavras** (antes, 4 na variante C).
- **Cores das thumbnails:** **mantém** a paleta do canal (carvão, mármore, âmbar), apesar de o guia desaconselhar tons marrons/neutros. Conferir a legibilidade em tamanho de celular (320×180).
- **Rostos:** canal dark; as silhuetas fazem o papel do "fator humano".
- **Vídeo 1:** mantém o título de 57 caracteres e o gancho como está (sem regravar para falar a palavra-chave nos primeiros 30 s). Do vídeo 2 em diante, o roteiro segue a seção 5 do guia.

## Regras fixas para todos os vídeos

1. **Somente domínio público:** *Meditações* na tradução de **George Long (1862)** (ou Casaubon, 1634); Sêneca na de Gummere (1917–1925); Provérbios na **World English Bible (WEB)**. Nunca traduções modernas (Hays, Waterfield etc.). Conferir cada citação na fonte antes de aprovar o bloco e anotar onde/quando foi conferida.
2. **Crédito na tela, sempre:** toda citação ou informação de fora mostra a fonte no canto inferior esquerdo (Inter, discreto). Ex.: *Marcus Aurelius, Meditations 6.30 · trans. George Long*; *Proverbs 16:18 · World English Bible*.
3. **Citações:** lidas no inglês antigo da tradução e, logo depois, repetidas em palavras simples ("In other words...", "In simple words...").
4. **Narração pronta para colar no ElevenLabs:** só o texto falado + audio tags (`[softly]`, `[thoughtful]`, `[warmly]`, `[whispers]`, `[sighs]`) e reticências para pausas. Deixas visuais e créditos ficam fora do bloco de texto. Um arquivo de áudio por bloco.
5. **Ritmo:** o ElevenLabs não tem controle de velocidade; na montagem as pausas são levemente alongadas (+10% + 0,05 s) e a voz fica no andamento original, para ~150 palavras/min (decisão de 12/10/2026; antes era −8% de andamento, que deixava ~120 palavras/min, lento demais).
6. **Efeitos de voz:** EM ESPERA — gerar sempre seco.
7. **Construção do roteiro aos poucos:** um bloco por vez, com perguntas ao criador, nada genérico. O criador aprova cada bloco.
8. **Pacote de Publicação** ao concluir cada vídeo (`pacote-de-publicacao-regras.md`). Nunca inventar fonte, versículo, link ou licença — perguntar ou marcar "VERIFICAR". Pedir os links do canal na hora.

## Os 12 vídeos

| # | Nome interno | Título de publicação | Tema central | Provérbio-ponte |
|---|---|---|---|---|
| 1 | The Man Who Had Everything | The Richest Man in Rome Wrote This to Himself Every Night | Poder e humildade | 30:8-9 e 16:18-19 |
| 2 | On Anger | How to Stay Calm When Work and Money Push You to the Edge | Ira | 16:32 |
| 3 | The Last Hour | Memento Mori for Busy Minds: Stop Spending Your Life on Tomorrow | Memento mori | 27:1 |
| 4 | What You Cannot Control | Stoicism for Financial Stress: Let Go of What You Can't Control | Dicotomia do controle | 19:21 |
| 5 | The Noise of Others | Stop Living for Their Approval: Stoic Wisdom for Leaders | Opinião alheia | 29:25 |
| 6 | Holding Your Tongue | The Power of Saying Less: Ancient Proverbs Every Leader Should Hear | Domínio da fala | 17:28 |
| 7 | The Weight of Envy | Stop Comparing Your Life: Proverbs on Envy and True Wealth | Inveja | 14:30 |
| 8 | Mornings | How Marcus Aurelius Started His Day: A Stoic Morning for Deep Work | Propósito matinal | 6:9-11 |
| 9 | The Obstacle | When Everything Fails: The Stoic Art of Rising Again | Dificuldade como caminho | 24:16 |
| 10 | On Gratitude | The Truest Wealth: What Marcus Aurelius Knew About Enough | Gratidão | 15:16 |
| 11 | The Company You Keep | You Become Who You Walk With: Ancient Wisdom on Mentors and Friends | Amizade e influência | 13:20 |
| 12 | Letting Go Before Sleep | Ancient Proverbs Every Leader Should Hear Before Sleep | Reflexão para dormir | 3:24 |

Versículos e citações desta tabela são **pontos de partida**: conferir na WEB/Long antes de usar.

### Formatos (decisão de 12/10/2026)

O formato é a **promessa do título** e serve para comparar o desempenho no experimento de 90 dias (campo Formato do sistema de gestão).

| Formato | O que promete | Vídeos |
|---|---|---|
| História de Marco Aurélio | um momento da vida dele vira a lição | 1 |
| Problema do dia a dia | dor concreta de trabalho ou dinheiro → resposta estoica | 2, 4, 9 |
| Sabedoria para líderes | conselho antigo aplicado a quem lidera | 5, 6 |
| Conceito estoico | uma ideia explicada para a vida de hoje | 3, 7, 10, 11 |
| Ritual guiado | prática para fazer junto (manhã, antes de dormir) | 8, 12 |

### Fichas iniciais (vídeos 2 e 3)

- **Vídeo 2 — On Anger:** a ira como fraqueza, não força; ângulo "quem te irrita tem poder sobre você"; estrutura: gancho sobre a última vez que perdeu a cabeça → visão estoica da raiva → exercício prático de pausa → Provérbios 16:32 → fechamento. Exemplo prático: reunião tensa, cliente que desrespeita. Palavras-chave: stoicism anger, controlling emotions, marcus aurelius anger, self control, calm mind. Thumbs já esboçadas no canvas (ANGER / linhas que se quebram / "Who angers you owns you").
- **Vídeo 3 — The Last Hour:** memento mori para viver melhor; ângulo "o friozinho existencial que acorda a gratidão"; gancho sobre o tempo que não volta → memento mori explicado → não é mórbido, é libertador → Provérbios 27:1 → fechamento. Palavras-chave: memento mori, stoicism death, living fully, marcus aurelius time, mortality.

## Fluxo de produção (uma sessão por vídeo)

Ver `fluxo-por-video.md`.

## Status

Não se escreve à mão: `./ma status N` (na pasta do canal) mostra o que existe e o que falta em cada vídeo, e `./ma sincronizar N` leva isso ao kanban do sistema de gestão.

- MA-001 *The Man Who Had Everything*: produção concluída; faltam thumbnails, shorts e Pacote de Publicação. **Publicação: aguardar a liberação do criador.**
- Vídeos 2–12: roteiros a fazer. Pasta de cada um: `videos/MA-NNN-slug/` (slug do nome interno da tabela acima).

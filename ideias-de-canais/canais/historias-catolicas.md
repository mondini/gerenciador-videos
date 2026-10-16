# Histórias católicas

> Ideia de canal (nome de trabalho). Status: **arquivada**, voltou para o caderno em 15/10/2026. Prioridade: **sem prioridade** (só retomar com novo estilo de arte). Índice em [../README.md](../README.md).

## De onde veio

Foi canal de verdade (`canal-historias-biblicas/`) de 14 a 15/10/2026, na fase de piloto. Voltou para o caderno porque **nenhum estilo de arte agradou** (ver "Testes de arte"). Nada foi publicado e o canal no YouTube não chegou a ser criado.

Todo o material está no histórico do git, no commit `162188f` (pasta `canal-historias-biblicas/`): plano do canal, regras de doutrina, style bible do one-line art, fluxo por vídeo, complemento do pacote de publicação, glossário de pronúncia, o roteiro do TESTE-01 (São Martinho) e o pipeline de render (HTML → vídeo num Chrome sem tela). Para ver um arquivo: `git show 162188f:canal-historias-biblicas/docs/doutrina-e-fontes.md`. Para restaurar a pasta inteira: `git checkout 162188f -- canal-historias-biblicas`. O TESTE-02 (silhuetas) não entrou no git.

## Conceito

A fé católica contada em histórias: vidas de santos, parábolas, os 10 Mandamentos, salmos e versículos explicados. A pauta segue o **calendário litúrgico**, porque a procura por cada tema sobe em datas previsíveis (santos: publicar 7 a 10 dias antes da festa; Advento, Natal, Quaresma, Páscoa; novembro, mês das almas).

## Ficha

| | |
|---|---|
| Idioma | Inglês. Futuro: faixa de áudio em português no mesmo vídeo |
| Público | Adultos 50+ dos EUA, Reino Unido e Canadá. **Nunca infantil** (canal e vídeos marcados como "não é para crianças") |
| Formato | Vídeos de 8 a 12 min, 16:9, 1 por semana; sem Shorts no começo |
| Estrutura do vídeo | Gancho (30 a 45 s) → história em blocos → o que a Igreja ensina (Catecismo) → reflexão ou oração curta |
| Tom | Reverente, caloroso, contemplativo. Promessa: ordem, liberdade e paz; nunca prosperidade, cura ou vida fácil |
| Narração | ElevenLabs (Eleven v4), voz grave, calorosa e pausada; voz não chegou a ser escolhida |
| Visual | **A definir**: os dois estilos testados foram reprovados |

## Séries

| Série | O que promete |
|---|---|
| Santos | a vida de um santo como história, com a virada que o fez santo |
| Mandamentos | um caso moral concreto → o mandamento (numeração católica) → o que o Catecismo ensina |
| Parábolas | a parábola com o contexto da época → o significado → a aplicação hoje |
| Salmos e versículos | contemplação de um texto curto, frase a frase |

## Cuidados (decisões que valem para a retomada)

- **Bíblia:** só Douay-Rheims, revisão Challoner (domínio público); nunca KJV (o público católico percebe). Salmos na numeração da Vulgata, com a mais conhecida entre parênteses: *Psalm 22 (23) · Douay-Rheims*.
- **Doutrina** pelo Catecismo, citado pelo número do parágrafo (*CCC 2052*); o texto em inglês é protegido, então parafrasear.
- **Mandamentos** sempre na numeração católica.
- **Citações de santos** só de edições em domínio público e conferidas; frase "atribuída" sem fonte não entra.
- **Representação:** Deus Pai nunca como figura humana (luz, nuvem, a mão que sai das nuvens); Jesus e Maria de preferência por símbolos, e, se a figura aparecer, sem traços comuns (Cristo como forma de luz, reconhecido pelo nimbo com cruz); anjos adultos e dignos, nada de querubins bebês; santos reconhecidos pelos atributos iconográficos.
- **Nada infantil:** sem cabeças e olhos grandes, sem paleta primária saturada, sem mascotes, rimas, "little ones" ou moral simplista.
- **Conteúdo inautêntico:** cada roteiro com arco e virada próprios; nada de vídeo-modelo com o nome do santo trocado.
- **Música:** só faixas com licença clara ou geradas por código. Obra em domínio público (Bach, gregoriano) não libera a gravação de terceiros.

## Testes de arte (todos reprovados)

| Data | Estilo | Por que não serviu |
|---|---|---|
| até 14/10/2026 | Imagens do Nano Banana | cara de IA, "plástico" |
| até 14/10/2026 | Desenho por código com bonecos geométricos | motivo não registrado |
| até 14/10/2026 | Pintura sacra de acervo animada em camadas ("pintura viva", Remotion) | motivo não registrado |
| 15/10/2026 | One-line art pastel (TESTE-01, 25 cenas em SVG) | fraco: sem contraste, figuras pequenas, câmera parada; parecia fundo de meditação |
| 15/10/2026 | Silhuetas recortadas + vitral nos cartões (TESTE-02, 5 cenas em SVG) | ganhou contraste, luz e ação, mas os **personagens ficaram simplificados demais** |

**Lição:** histórias de santos dependem de personagens com detalhe e expressão. O desenho feito por código em SVG não chegou a esse nível. Antes de retomar, achar um caminho de arte que entregue personagens ricos sem cair na "cara de IA". Testar com uma cena só antes de produzir um vídeo inteiro.

## Pautas

- **São Martinho de Tours** (festa em 11/11): "The Half Cloak", roteiro pronto e com fontes conferidas no TESTE-01 (Sulpício Severo, *Life of St. Martin*, cap. 3, trad. Alexander Roberts, 1894).
- Advento (1º domingo: 29/11/2026), Imaculada Conceição (8/12), Natal.
- Todos os Santos (1º/11) e Fiéis Defuntos (2/11).

## Pautas e anotações

<!-- Novas ideias e resultados, com data. -->

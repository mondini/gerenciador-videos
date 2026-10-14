# Plano do canal

Atualizado em 14/10/2026, na sessão de organização do canal (antes do piloto).

## Decisões do canal

- **Nome, handle e prefixo:** a definir. O prefixo do código dos vídeos (`XX-001`) e a pasta no Drive (`XX - Nome`) saem do nome. Ao escolher, criar `canal.json` (`nome`, `prefixo`, `pasta_drive`).
- **Tema:** fé católica contada em histórias: santos, parábolas, os 10 Mandamentos, versículos e salmos explicados, temas afins. Histórias e roteiros originais; citações literais são raras.
- **Público:** adultos e idosos (**50+**) falantes de inglês (EUA, Reino Unido, Canadá). **Não é conteúdo infantil**: no YouTube, canal e vídeos marcados como "não é para crianças", e nada no título, na thumbnail, na arte ou no tom pode sugerir o contrário (lista de sinais no `CLAUDE.md`).
- **Idioma:** 100% inglês por enquanto. **Futuro (não iniciar sem pedido):** faixa de áudio em português no mesmo vídeo (recurso de áudio multilíngue do YouTube), em vez de um canal separado.
- **Formato:** vídeo animado 16:9 de **8 a 12 minutos** (decisão de 14/10/2026). A ~130–140 palavras por minuto, isso dá ~1.100–1.600 palavras faladas; calibrar no piloto.
- **Shorts:** **o canal começa sem shorts** (14/10/2026). Retomar só quando o criador pedir.
- **Cadência:** **1 vídeo por semana** (14/10/2026). A meta de longo prazo é um acervo grande, mas o volume nunca vem antes da qualidade (ver "Política do YouTube").
- **Tom:** reverente, caloroso, digno, contemplativo. Nunca infantil nem condescendente.
- **Promessa:** ordem, liberdade e paz. Nunca prosperidade, cura ou vida fácil (os santos sofreram; o público 50+ percebe promessa vazia).
- **Fé com razões:** evitar a ideia de "seguir cegamente". O ensino católico apresenta a fé como confiança com razões; enfrentar essa objeção no roteiro quando o tema permitir.

## Política do YouTube (pesquisada em 14/10/2026)

- Em julho de 2026 o YouTube detalhou a política de **conteúdo inautêntico** em três grupos que não monetizam. O que pesa aqui é o primeiro: conteúdo **genérico, repetitivo ou de modelo pronto**, fácil de fazer com IA, com pouca variação entre os vídeos e "sem arco narrativo". Um canal com muito conteúdo assim sai da monetização. Usar IA não é proibido; o alvo são as fábricas de conteúdo.
- Regras do canal por causa disso:
  1. Cada roteiro tem arco narrativo e virada próprios. Teste antes de aprovar a escaleta: *este vídeo tem algo que o anterior não tinha, ou é o anterior com outro nome?*
  2. Cada série tem sua própria promessa (tabela "Formatos"), em vez de um molde único.
  3. Cenas, composições e enquadramentos variam entre os vídeos; os personagens e o estilo se repetem, as cenas não.
- **Conteúdo sintético:** a marcação do YouTube é obrigatória para conteúdo realista que pode ser confundido com real; animação claramente estilizada não precisa. Avaliar em cada vídeo no Pacote de Publicação (seção 9).

## Calendário litúrgico (base da pauta)

O calendário da Igreja é a espinha da programação: a procura por cada tema sobe em datas previsíveis.
- **Santos:** publicar 7 a 10 dias antes da festa.
- **Tempos litúrgicos:** Advento, Natal, Quaresma, Semana Santa, Páscoa, Pentecostes; novembro é o mês das almas.
- **Datas próximas:** Todos os Santos (1º/11), Fiéis Defuntos (2/11), **1º domingo do Advento (29/11/2026)**, Imaculada Conceição (8/12), Natal (25/12).
- Festas móveis e datas de 2027 em diante: conferir no calendário litúrgico oficial antes de pautar.
- Ao sugerir temas, vídeos e roteiros, o Claude sempre olha as próximas 6 a 10 semanas do calendário.

## Formatos (séries)

Cada série é uma promessa diferente de título, para não parecerem o mesmo vídeo:

| Série | O que promete |
|---|---|
| Santos | a vida de um santo contada como história, com a virada que o fez santo |
| Mandamentos | um caso moral concreto → o mandamento (numeração católica) → o que o Catecismo ensina |
| Parábolas | a parábola recontada com contexto da época → o significado → a aplicação hoje |
| Salmos e versículos | contemplação de um texto curto, frase a frase |

Novas séries entram aqui com data e motivo.

## Estrutura padrão de um vídeo (8–12 min)

1. **Gancho** (~30–45 s): a pergunta ou situação humana do vídeo, sem entregar a resposta. Segue a seção 5 do guia de embalagem (promessa confirmada nos primeiros 15 s, palavra-chave nos primeiros 30 s, um *loop* aberto).
2. **História** (o corpo do vídeo, em blocos).
3. **Significado:** o que a Igreja ensina sobre isso (Catecismo).
4. **Reflexão final / oração curta.**

## Ferramentas

- **Roteiro e montagem:** Claude.
- **Voz:** ElevenLabs, **Eleven v4** (lançado em 28/09/2026; é o modelo atual de melhor qualidade da ElevenLabs e aceita IPA entre barras no texto para pronúncia). **Pela API desde o início** (14/10/2026), por script Python, com voz e configurações fixas para a voz não mudar entre blocos e vídeos. Voz: grave, calorosa, pausada; escolher no piloto e registrar aqui (nome, modelo, estabilidade, similaridade). Chave em `.env` desta pasta (fora do git). Estimar o custo ao fechar o roteiro: ~1 crédito por caractere (conferir no piloto).
- **Imagens:** Gemini (Nano Banana), **plano Plus do app**, geradas à mão pelo criador a partir dos prompts do Claude. Modelo exato (Nano Banana ou Nano Banana Pro) a definir no piloto e registrar em `estilo-visual.md`. Geração pela API: decidir depois. Desligar a marca d'água visível nas configurações do app ("Media watermark"), se a conta tiver a opção; a marca invisível SynthID sempre fica. Midjourney só se o Gemini não alcançar a estética (testar antes de assinar).
- **Animação:** Remotion (React), montando as cenas a partir de JSON. Licença: grátis para uso individual e empresas de até 3 pessoas, inclusive comercial (conferido em 14/10/2026). Fixar a versão; a licença muda "levemente" na 5.0, então reconferir antes de atualizar.
- **Python:** recorte dos elementos das imagens (rembg com BiRefNet), catálogo da biblioteca, narração pela API, alinhamento das legendas, **áudios gerados por código** (efeitos, ambiência, transições) quando o criador pedir, backup.
- **Legendas:** arquivo SRT enviado ao YouTube (acessibilidade, tradução automática, boa leitura na TV). Tempos por alinhamento forçado ao texto do roteiro (stable-ts ou WhisperX) ou pelos tempos que a API do ElevenLabs devolve, nunca por transcrição livre (erra nomes bíblicos e latim).
- **Música:** instrumental sacra suave sob a voz. Só faixas com licença clara (Biblioteca de Áudio do YouTube ou equivalente) ou geradas por código. Obras em domínio público (Bach, canto gregoriano) **não** liberam as gravações: gravação de terceiros só com licença. Registrar a licença de cada faixa.
- **Mix:** voz + música normalizadas por ffmpeg (referência do YouTube: ~−14 LUFS). DaVinci Resolve só se precisar.

## Próximos passos

1. Escolher nome, handle e prefixo; criar `canal.json`.
2. Identidade visual do canal (paleta, tipografia, logo): retrabalhar na próxima sessão.
3. **Vídeo piloto:** tema ligado ao calendário (sugestão: Advento, que começa em 29/11/2026); roteiro curto para levantar os assets; prompts para o Gemini; teste de arte com critérios definidos antes (parece pintura sacra? os personagens se mantêm em 5 poses? tem cara de livro infantil?).
4. No piloto: comparar fundo neutro + BiRefNet com fundo chapado (5 imagens cada); escolher a voz; medir palavras por minuto e créditos.
5. Pipeline mínimo: recorte + catálogo, narração pela API, cena em Remotion, backup.

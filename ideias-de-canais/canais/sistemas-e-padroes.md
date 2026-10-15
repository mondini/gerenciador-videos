# Sistemas e padrões

> Ideia de canal (nome de trabalho; o nome público será em inglês). Status: **ideia**. Prioridade: **4**. Índice em [../README.md](../README.md).

## Conceito

Os padrões escondidos no mundo: como cardumes, revoadas e engarrafamentos se organizam sozinhos; o que os engenheiros copiaram da natureza; a matemática por trás das formas e dos ritmos. O diferencial é **simular de verdade** (boids para cardume, modelo de trânsito para o engarrafamento fantasma) em vez de só ilustrar. O canal Primer, em inglês, cresceu exatamente assim.

## Ficha

| | |
|---|---|
| Idioma | **Inglês**, com **faixa de áudio em português** no mesmo vídeo; título e descrição traduzidos |
| Público | Curiosos de ciência e matemática (o mesmo público de Primer e 3Blue1Brown) |
| Formato | Vídeos de 6 a 12 min; Shorts com a simulação mais hipnótica |
| Visual | **Partículas e arte generativa** (principal) + **diagramas em line art** (secundário) |
| Ferramenta | **Python**: numpy para simular, Manim para matemática e diagramas, render direto dos quadros para as partículas |
| Concorrência | Média em inglês (Primer, 3Blue1Brown, Veritasium); quase nada em português |
| Receita | Boa (RPM de inglês) |

## Linhas editoriais

### Sistemas que se organizam sozinhos (emergência)
- Por que o trânsito para sem motivo (engarrafamento fantasma).
- Como um cardume decide para onde ir; como uma revoada de estorninhos não se choca.
- Como um formigueiro acha o caminho mais curto.
- Por que vagalumes (e plateias) acabam piscando e batendo palma juntos.

### Biomimética (série)
O traço da natureza vira o traço da máquina.
- Velcro e o carrapicho.
- O trem-bala japonês e o bico do martim-pescador.
- O prédio Eastgate (Harare), ventilado como um cupinzeiro.
- A pata da lagartixa e os adesivos secos; a folha de lótus e as superfícies que não molham.

### Matemática visual
No estilo 3Blue1Brown. Quase não existe em português, e a faixa de áudio em PT cobre esse público.
- Por que os favos de mel são hexagonais.
- Fibonacci na natureza: onde é verdade e onde é exagero.

### Ritmos brasileiros
Ritmo é padrão matemático. O algoritmo de Euclides gera ritmos tradicionais do mundo todo (o *tresillo*, base de muito ritmo latino e brasileiro, é um deles).
- Por que o samba balança.
- Baião, maracatu, ijexá e bossa nova como rodas geométricas que pulsam no tempo da batida.

## Cuidados

- As simulações precisam ser fiéis ao modelo científico. Citar o modelo e o artigo de origem.
- Fibonacci e "proporção áurea" estão cheios de exagero na internet; o canal deve ser o que corrige, não o que repete.

## Fontes

- Craig Reynolds, *boids* (1987), para cardumes e revoadas.
- Modelo de Nagel-Schreckenberg e experimento de Sugiyama (2008), para engarrafamentos.
- Steven Strogatz, *Sync*, para sincronização.
- Godfried Toussaint, "The Euclidean Algorithm Generates Traditional Musical Rhythms" (2005).

## Protótipo

**"Why traffic jams happen for no reason"**, de 6 a 8 min, em inglês com faixa de áudio em português. Simulação em numpy e render em Python. Valida a simulação como linguagem visual e o desempenho do áudio duplo.

## Pautas e anotações

<!-- Novas pautas e resultados, com data. -->

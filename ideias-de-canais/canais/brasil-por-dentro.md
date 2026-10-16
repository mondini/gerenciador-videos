# Brasil por dentro

> Ideia de canal (nome de trabalho). Status: **ideia**. Prioridade: **2**. Índice em [../README.md](../README.md).

## Conceito

Todo vídeo responde a "**por que / como o Brasil é assim?**". Como funcionam o Pix, Itaipu e a transposição do São Francisco; para onde vai o seu imposto; por que existe cartório; por que a Transamazônica nunca ficou pronta. Sistemas e objetos vistos por dentro, sempre com o recorte brasileiro. Esse recorte é o que um canal estrangeiro não faz: "o caminho de um Pix" no lugar de "o caminho de uma mensagem no WhatsApp".

## Ficha

| | |
|---|---|
| Idioma | Português |
| Público | Adultos que querem entender o país; muito compartilhável em grupos |
| Formato | Vídeos de 8 a 12 min como produto; Shorts como vitrine (bandeiras, curiosidades de um mapa) |
| Visual | **Isométrico** (principal, a cidade e as máquinas como maquete) + **infográfico/mapa** (secundário) |
| Ferramenta | Remotion + three.js com câmera ortográfica (isométrico) + d3 (mapas e gráficos) |
| Concorrência | Baixa em português no formato animado. Em inglês, a régua é Branch Education, Jared Owen, Wendover |
| Receita | A melhor dos canais em PT: dinheiro, tecnologia e energia pagam bem |

## Linhas editoriais

### Infraestrutura por dentro
Inclui a antiga ideia "Como as coisas funcionam", sempre com o recorte brasileiro.
- O caminho de um Pix.
- Itaipu por dentro.
- A transposição do São Francisco.
- Como a energia chega à sua tomada (o sistema interligado nacional).
- **Urna eletrônica: só mais tarde**, quando o canal tiver autoridade, com fonte oficial (TSE), tom estritamente técnico e **nunca perto de eleição**.

### Dinheiro do dia a dia
Finanças é o nicho que mais paga em português.
- Por que o pão francês custa o que custa.
- Para onde vai o imposto da gasolina.
- Como a inflação come o salário.
- Como funciona o FGTS; como nasceu o boleto.
- Por que os juros no Brasil são tão altos.

### Burocracia explicada
Todo mundo sofre com isso e quase ninguém explica de forma visual.
- Por que existe CPF; para que serve o cartório; de onde veio o IPVA; como nasceu a CLT; por que se reconhece firma.

### Brasil em mapas
Junta a antiga "História em mapas" (agora com foco no Brasil) e "Rodovias e ferrovias que contam o Brasil".
- Como o Acre virou brasileiro; Tordesilhas na prática; os ciclos econômicos no mapa.
- Transamazônica, BR-116, Madeira-Mamoré, a ferrovia que ninguém terminou.
- Por que a capital foi para o meio do país.

### Casas do Brasil
Arquitetura popular e regional, cada casa como maquete isométrica.
- Casa de taipa, palafita, enxaimel, casa de fazenda colonial, a laje que vira segundo andar.

### Comida de rua com história
Origem, imigração e variação regional de cada prato.
- Acarajé, pastel de feira, cachorro-quente prensado, tapioca, churrasquinho de gato.

### Inventos brasileiros esquecidos
O objeto se desenhando sozinho.
- Soro antiofídico (Vital Brazil, Butantan).
- Identificador de chamadas: a autoria (Nélio Nicolai) é disputada; mostrar os dois lados.
- Santos Dumont x irmãos Wright: polêmica antiga; mostrar os dois lados.
- Invenções menos conhecidas (pesquisar no INPI).

### Fenômenos do clima brasileiro
No mapa, com fluxos de partículas para vento, nuvens e água.
- Pororoca, friagem na Amazônia, rios voadores, ciclones no Sul, granizo no cerrado.

### Casos (minidocumentários)
Histórias brasileiras de empresas que quebraram, golpes financeiros e projetos que fracassaram, contadas com começo, auge e queda. Mesmo público do "Dinheiro do dia a dia". True crime, games e casos de outros países ficam fora (outro público).
- Fordlândia, a cidade da Ford que a Amazônia engoliu.
- Encol e os prédios que nunca ficaram prontos.
- Varig; Mappin.
- Golpes e pirâmides: Boi Gordo, Avestruz Master, Telexfree (recurso visual "promessa x realidade", com o prometido em fantasma translúcido).
- Recursos: a maquete conta a história (prédios crescendo e apagando), linha do tempo, gráficos de queda e citações reais em cartão, sempre com fonte.

### Bandeiras e brasões (Shorts)
Por que a bandeira do seu estado ou da sua cidade é assim. Muito regional e compartilhável.

## Cuidados

- **Casos:** só fatos documentados (decisão judicial, CVM, Banco Central, imprensa com fonte); quem não foi condenado é "acusado". Sem escândalo político. Nada de recriar capa de jornal ou documento real; arquivo só com licença.
- Sem política partidária. Obras paradas e impostos são explicados com dados, sem culpar governos específicos.
- Dinheiro: explicar, **nunca recomendar investimento**.
- Inventos e polêmicas históricas: sempre os dois lados, com fonte.
- Cuidado com a identidade visual: são muitas linhas, e todas precisam ter a mesma cara (maquete + mapa).

## Fontes

| Tema | Fonte |
|---|---|
| Dados e mapas | IBGE: API de serviços (`servicodados.ibge.gov.br/api/docs`), SIDRA (`apisidra.ibge.gov.br`), Censo 2022, malhas territoriais (GeoJSON) |
| Pix e dinheiro | Banco Central (documentação do Pix, estatísticas), Receita Federal |
| Infraestrutura | Itaipu Binacional, ONS, DNIT, ANTT, Ministério da Integração (São Francisco) |
| Inventos | INPI (patentes), Instituto Butantan |
| Clima | INMET, INPE, CEMADEN; pesquisa de Antonio Nobre sobre os rios voadores |
| Urna (mais tarde) | TSE |

## Protótipo

**"O caminho de um Pix"**, de 8 a 10 min, com isométrico e infográfico. Mede o custo real de produzir isométrico e a retenção em vídeo longo.

## Pautas e anotações

<!-- Novas pautas e resultados, com data. -->

- **15/10/2026:** estilo visual aprovado pelo dono a partir de duas artes conceito: [O caminho de um Pix](../prototipos/pix/) e [Fordlândia](../prototipos/fordlandia/). Mesma identidade (papel creme, maquete com corte de terra, Archivo + IBM Plex Mono, coluna de infográfico à esquerda, legenda palavra por palavra); cada linha editorial pode ter a sua cor de destaque. Linha "Casos" incluída.

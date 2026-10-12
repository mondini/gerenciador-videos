import { sql } from "drizzle-orm";
import { index, integer, primaryKey, sqliteTable, text, uniqueIndex } from "drizzle-orm/sqlite-core";
import { ETAPAS } from "../../shared/etapas";

const id = () => integer("id").primaryKey({ autoIncrement: true });
const criadoEm = () =>
  integer("criado_em", { mode: "timestamp_ms" })
    .notNull()
    .default(sql`(unixepoch() * 1000)`);

export const canal = sqliteTable("canal", {
  id: id(),
  nome: text("nome").notNull(),
  nicho: text("nicho").notNull().default(""),
  idioma: text("idioma").notNull().default("pt-BR"),
  prefixoCodigo: text("prefixo_codigo").notNull().unique(),
  /** Relativa ao DRIVE_ROOT. */
  pastaRelativa: text("pasta_relativa").notNull(),
  urlYoutube: text("url_youtube"),
  youtubeChannelId: text("youtube_channel_id"),
  modeloDescricao: text("modelo_descricao").notNull().default(""),
  tagsPadrao: text("tags_padrao", { mode: "json" }).$type<string[]>().notNull().default(sql`'[]'`),
  vozPadrao: text("voz_padrao").notNull().default(""),
  estiloImagemPadrao: text("estilo_imagem_padrao").notNull().default(""),
  referenciasIdentidade: text("referencias_identidade").notNull().default(""),
  criadoEm: criadoEm(),
});

export const gradePublicacao = sqliteTable("grade_publicacao", {
  id: id(),
  canalId: integer("canal_id").notNull().references(() => canal.id, { onDelete: "cascade" }),
  /** 0 = domingo … 6 = sábado */
  diaSemana: integer("dia_semana").notNull(),
  hora: text("hora").notNull(),
});

export const formato = sqliteTable(
  "formato",
  {
    id: id(),
    canalId: integer("canal_id").notNull().references(() => canal.id, { onDelete: "cascade" }),
    nome: text("nome").notNull(),
    ativo: integer("ativo", { mode: "boolean" }).notNull().default(true),
  },
  (t) => [uniqueIndex("formato_canal_nome").on(t.canalId, t.nome)],
);

export const serie = sqliteTable("serie", {
  id: id(),
  canalId: integer("canal_id").notNull().references(() => canal.id, { onDelete: "cascade" }),
  nome: text("nome").notNull(),
  descricao: text("descricao").notNull().default(""),
  youtubePlaylistId: text("youtube_playlist_id"),
});

export const tema = sqliteTable(
  "tema",
  {
    id: id(),
    canalId: integer("canal_id").notNull().references(() => canal.id, { onDelete: "cascade" }),
    nome: text("nome").notNull(),
  },
  (t) => [uniqueIndex("tema_canal_nome").on(t.canalId, t.nome)],
);

export const modeloChecklist = sqliteTable("modelo_checklist", {
  id: id(),
  canalId: integer("canal_id").notNull().references(() => canal.id, { onDelete: "cascade" }),
  etapa: text("etapa", { enum: ETAPAS }).notNull(),
  ordem: integer("ordem").notNull(),
  texto: text("texto").notNull(),
});

export const video = sqliteTable(
  "video",
  {
    id: id(),
    canalId: integer("canal_id").notNull().references(() => canal.id, { onDelete: "cascade" }),
    numero: integer("numero").notNull(),
    codigo: text("codigo").notNull().unique(),
    tituloProvisorio: text("titulo_provisorio").notNull(),
    tituloFinal: text("titulo_final"),
    /** Nulo = "a definir" (ideias importadas em lote). */
    formatoId: integer("formato_id").references(() => formato.id),
    serieId: integer("serie_id").references(() => serie.id),
    derivadoDeId: integer("derivado_de_id"),
    etapa: text("etapa", { enum: ETAPAS }).notNull().default("Ideia"),
    dataPlanejada: integer("data_planejada", { mode: "timestamp_ms" }),
    dataPublicacao: integer("data_publicacao", { mode: "timestamp_ms" }),
    notaApelo: integer("nota_apelo"),
    notaIlustracao: integer("nota_ilustracao"),
    notaPesquisa: integer("nota_pesquisa"),
    gancho: text("gancho").notNull().default(""),
    resumo: text("resumo").notNull().default(""),
    roteiroAtual: text("roteiro_atual").notNull().default(""),
    pastaRelativa: text("pasta_relativa"),
    vozUsada: text("voz_usada").notNull().default(""),
    duracaoFinalSeg: integer("duracao_final_seg"),
    notasCorte: text("notas_corte").notNull().default(""),
    descricao: text("descricao").notNull().default(""),
    tags: text("tags", { mode: "json" }).$type<string[]>().notNull().default(sql`'[]'`),
    capitulos: text("capitulos").notNull().default(""),
    youtubeVideoId: text("youtube_video_id"),
    urlYoutube: text("url_youtube"),
    /** Marcação "conteúdo alterado ou sintético" do YouTube. */
    marcacaoSintetico: text("marcacao_sintetico", { enum: ["nao-avaliado", "obrigatoria", "nao-obrigatoria"] })
      .notNull()
      .default("nao-avaliado"),
    justificativaSintetico: text("justificativa_sintetico").notNull().default(""),
    /** O que falta, segundo a última sincronização do pipeline do canal (`./ma sincronizar`). */
    pendencias: text("pendencias", { mode: "json" }).$type<string[]>().notNull().default(sql`'[]'`),
    sincronizadoEm: integer("sincronizado_em", { mode: "timestamp_ms" }),
    criadoEm: criadoEm(),
  },
  (t) => [uniqueIndex("video_canal_numero").on(t.canalId, t.numero), index("video_etapa").on(t.canalId, t.etapa)],
);

export const videoTema = sqliteTable(
  "video_tema",
  {
    videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
    temaId: integer("tema_id").notNull().references(() => tema.id, { onDelete: "cascade" }),
  },
  (t) => [primaryKey({ columns: [t.videoId, t.temaId] })],
);

export const historicoEtapa = sqliteTable("historico_etapa", {
  id: id(),
  videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
  etapa: text("etapa", { enum: ETAPAS }).notNull(),
  entrouEm: integer("entrou_em", { mode: "timestamp_ms" }).notNull(),
});

export const checklistItem = sqliteTable("checklist_item", {
  id: id(),
  videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
  etapa: text("etapa", { enum: ETAPAS }).notNull(),
  ordem: integer("ordem").notNull(),
  texto: text("texto").notNull(),
  feito: integer("feito", { mode: "boolean" }).notNull().default(false),
  feitoEm: integer("feito_em", { mode: "timestamp_ms" }),
});

export const versaoRoteiro = sqliteTable(
  "versao_roteiro",
  {
    id: id(),
    videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
    numero: integer("numero").notNull(),
    conteudo: text("conteudo").notNull(),
    origem: text("origem", { enum: ["manual", "saida-roteiro"] }).notNull(),
    nota: text("nota"),
    arquivoExportado: text("arquivo_exportado"),
    criadoEm: criadoEm(),
  },
  (t) => [uniqueIndex("versao_video_numero").on(t.videoId, t.numero)],
);

export const cena = sqliteTable("cena", {
  id: id(),
  videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
  ordem: integer("ordem").notNull(),
  trechoRoteiro: text("trecho_roteiro").notNull().default(""),
  prompt: text("prompt").notNull().default(""),
  ferramenta: text("ferramenta").notNull().default(""),
  arquivos: text("arquivos", { mode: "json" }).$type<string[]>().notNull().default(sql`'[]'`),
  status: text("status", { enum: ["pendente", "ok", "refazer"] }).notNull().default("pendente"),
  favorita: integer("favorita", { mode: "boolean" }).notNull().default(false),
});

export const fonte = sqliteTable("fonte", {
  id: id(),
  videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
  titulo: text("titulo").notNull(),
  linkOuReferencia: text("link_ou_referencia").notNull().default(""),
  tipo: text("tipo", { enum: ["livro", "artigo", "site", "video", "entrevista", "documento-historico"] }).notNull(),
  fatoSustentado: text("fato_sustentado").notNull().default(""),
  confiabilidade: text("confiabilidade", { enum: ["alta", "media", "baixa"] }).notNull().default("media"),
  /** Texto curto exibido no vídeo, ex.: "Fonte: R. Gracie, Carlson Gracie, 2008". */
  textoTela: text("texto_tela").notNull().default(""),
});

export const fonteCena = sqliteTable(
  "fonte_cena",
  {
    fonteId: integer("fonte_id").notNull().references(() => fonte.id, { onDelete: "cascade" }),
    cenaId: integer("cena_id").notNull().references(() => cena.id, { onDelete: "cascade" }),
  },
  (t) => [primaryKey({ columns: [t.fonteId, t.cenaId] })],
);

export const tituloCandidato = sqliteTable("titulo_candidato", {
  id: id(),
  videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
  texto: text("texto").notNull(),
  escolhido: integer("escolhido", { mode: "boolean" }).notNull().default(false),
});

export const varianteThumbnail = sqliteTable(
  "variante_thumbnail",
  {
    id: id(),
    videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
    letra: text("letra").notNull(),
    arquivo: text("arquivo"),
    escolhida: integer("escolhida", { mode: "boolean" }).notNull().default(false),
    vencedoraTeste: integer("vencedora_teste", { mode: "boolean" }).notNull().default(false),
    percentualTempoExibicao: integer("percentual_tempo_exibicao"),
  },
  (t) => [uniqueIndex("thumb_video_letra").on(t.videoId, t.letra)],
);

export const promptBanco = sqliteTable("prompt_banco", {
  id: id(),
  canalId: integer("canal_id").notNull().references(() => canal.id, { onDelete: "cascade" }),
  titulo: text("titulo").notNull(),
  prompt: text("prompt").notNull(),
  ferramenta: text("ferramenta").notNull().default(""),
  cenaOrigemId: integer("cena_origem_id").references(() => cena.id, { onDelete: "set null" }),
  arquivoExemplo: text("arquivo_exemplo"),
});

/**
 * Dossiê de direitos do vídeo, em três tipos:
 * - `direitos`: elemento de terceiros (música, imagem, citação…) com a defesa pronta contra claim;
 * - `ia`: o que foi gerado por IA (voz, imagens, roteiro…);
 * - `monetizacao`: risco de desmonetização, com a mitigação.
 */
export const dossieItem = sqliteTable(
  "dossie_item",
  {
    id: id(),
    videoId: integer("video_id").notNull().references(() => video.id, { onDelete: "cascade" }),
    tipo: text("tipo", { enum: ["direitos", "ia", "monetizacao"] }).notNull(),
    ordem: integer("ordem").notNull().default(0),
    /** direitos/ia: o elemento ou componente; monetizacao: o ponto de risco. */
    elemento: text("elemento").notNull(),
    /** direitos: musica, sfx, imagem, citacao-biblica, citacao-estoica, fonte-tipografica, clipe, outro. ia: voz, imagens, roteiro, musica, thumbnail, outro. */
    categoria: text("categoria").notNull().default(""),
    /** direitos: origem; ia: ferramenta usada. */
    origem: text("origem").notNull().default(""),
    link: text("link").notNull().default(""),
    /** direitos: dominio-publico, licenca, citacao-uso-transformativo, conteudo-proprio, gerado-por-ia. */
    base: text("base").notNull().default(""),
    /** direitos: detalhes da licença/edição/tradução; ia/monetizacao: descrição. */
    descricao: text("descricao").notNull().default(""),
    contestacao: text("contestacao").notNull().default(""),
    provas: text("provas").notNull().default(""),
    risco: text("risco", { enum: ["baixo", "medio", "alto"] }).notNull().default("baixo"),
    mitigacao: text("mitigacao").notNull().default(""),
  },
  (t) => [index("dossie_video").on(t.videoId, t.tipo)],
);

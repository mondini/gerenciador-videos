import { and, asc, count, eq } from "drizzle-orm";
import { z } from "zod";
import { ETAPAS, type Etapa } from "../../shared/etapas";
import { TIPOS_AGENDA } from "../../shared/agenda";
import { fusoValido } from "../../shared/fuso";
import { agendaItem, canal, formato, gradePublicacao, modeloChecklist, serie, tema, video } from "../db/schema";
import type { Contexto } from "./contexto";

export class ConflitoError extends Error {}

export const editarCanalSchema = z
  .object({
    nome: z.string().trim().min(1),
    nicho: z.string(),
    urlYoutube: z.string().trim().nullable(),
    referenciasIdentidade: z.string(),
    modeloDescricao: z.string(),
    tagsPadrao: z.array(z.string().trim().min(1)),
    vozPadrao: z.string(),
    estiloImagemPadrao: z.string(),
    fusoPublico: z.string().refine(fusoValido, "Fuso desconhecido (use o nome IANA, ex.: America/New_York)"),
  })
  .partial();

export const gradeSchema = z.object({
  grade: z.array(z.object({ diaSemana: z.number().int().min(0).max(6), hora: z.string().regex(/^\d{2}:\d{2}$/) })),
});
const hora = z.string().regex(/^([01]\d|2[0-3]):[0-5]\d$/, "Hora no formato HH:MM");
export const agendaSchema = z.object({
  itens: z.array(z.object({
    rotulo: z.string().trim().min(1),
    tipo: z.enum(TIPOS_AGENDA),
    diasApos: z.number().int().min(0).max(30),
    hora,
  })),
});
export const nomeSchema = z.object({ nome: z.string().trim().min(1) });
export const editarFormatoSchema = z.object({ nome: z.string().trim().min(1), ativo: z.boolean() }).partial();
export const serieSchema = z.object({ nome: z.string().trim().min(1), descricao: z.string().default("") });
export const editarSerieSchema = z.object({ nome: z.string().trim().min(1), descricao: z.string() }).partial();
export const checklistSchema = z.object({ textos: z.array(z.string().trim().min(1)) });
export const etapaSchema = z.enum(ETAPAS);

/** Converte violação de unicidade do SQLite em ConflitoError (vira 409). */
function comUnicidade<T>(mensagem: string, fn: () => T): T {
  try {
    return fn();
  } catch (e) {
    if (e instanceof Error && /UNIQUE constraint/.test(e.message)) throw new ConflitoError(mensagem);
    throw e;
  }
}

export function lerConfiguracao(ctx: Contexto, canalId: number) {
  const { db } = ctx;
  const c = db.select().from(canal).where(eq(canal.id, canalId)).get();
  if (!c) return null;
  return {
    canal: c,
    grade: db.select().from(gradePublicacao).where(eq(gradePublicacao.canalId, canalId)).orderBy(asc(gradePublicacao.diaSemana), asc(gradePublicacao.hora)).all(),
    formatos: db.select().from(formato).where(eq(formato.canalId, canalId)).orderBy(asc(formato.id)).all(),
    series: db.select().from(serie).where(eq(serie.canalId, canalId)).orderBy(asc(serie.id)).all(),
    temas: db.select().from(tema).where(eq(tema.canalId, canalId)).orderBy(asc(tema.nome)).all(),
    agenda: db.select().from(agendaItem).where(eq(agendaItem.canalId, canalId)).orderBy(asc(agendaItem.ordem)).all(),
    modelos: db.select().from(modeloChecklist).where(eq(modeloChecklist.canalId, canalId)).orderBy(asc(modeloChecklist.ordem)).all(),
  };
}

export function substituirGrade(ctx: Contexto, canalId: number, grade: z.infer<typeof gradeSchema>["grade"]) {
  ctx.db.transaction((tx) => {
    tx.delete(gradePublicacao).where(eq(gradePublicacao.canalId, canalId)).run();
    if (grade.length) tx.insert(gradePublicacao).values(grade.map((g) => ({ ...g, canalId }))).run();
  });
}

export function substituirAgenda(ctx: Contexto, canalId: number, itens: z.infer<typeof agendaSchema>["itens"]) {
  ctx.db.transaction((tx) => {
    tx.delete(agendaItem).where(eq(agendaItem.canalId, canalId)).run();
    if (itens.length) tx.insert(agendaItem).values(itens.map((m, i) => ({ ...m, canalId, ordem: i + 1 }))).run();
  });
}

export function criarFormato(ctx: Contexto, canalId: number, nome: string) {
  return comUnicidade("Já existe um formato com esse nome", () => ctx.db.insert(formato).values({ canalId, nome }).returning().get());
}

export function editarFormato(ctx: Contexto, id: number, campos: z.infer<typeof editarFormatoSchema>) {
  if (Object.keys(campos).length === 0) throw new Error("inválido: nada para alterar");
  return comUnicidade("Já existe um formato com esse nome", () => ctx.db.update(formato).set(campos).where(eq(formato.id, id)).returning().get());
}

export function criarSerie(ctx: Contexto, canalId: number, dados: z.infer<typeof serieSchema>) {
  return ctx.db.insert(serie).values({ canalId, ...dados }).returning().get();
}

export function editarSerie(ctx: Contexto, id: number, campos: z.infer<typeof editarSerieSchema>) {
  if (Object.keys(campos).length === 0) throw new Error("inválido: nada para alterar");
  return ctx.db.update(serie).set(campos).where(eq(serie.id, id)).returning().get();
}

/** Série em uso não é apagada, para não perder o vínculo dos vídeos. */
export function apagarSerie(ctx: Contexto, id: number): boolean {
  const emUso = ctx.db.select({ n: count() }).from(video).where(eq(video.serieId, id)).get()!.n;
  if (emUso > 0) throw new ConflitoError(`A série está em ${emUso} vídeo(s); remova o vínculo antes de apagar`);
  return ctx.db.delete(serie).where(eq(serie.id, id)).returning().all().length > 0;
}

export function criarTema(ctx: Contexto, canalId: number, nome: string) {
  return comUnicidade("Já existe um tema com esse nome", () => ctx.db.insert(tema).values({ canalId, nome }).returning().get());
}

export function apagarTema(ctx: Contexto, id: number): boolean {
  return ctx.db.delete(tema).where(eq(tema.id, id)).returning().all().length > 0;
}

/** Troca o modelo de checklist de uma etapa. Vídeos existentes mantêm a cópia que já receberam. */
export function substituirChecklist(ctx: Contexto, canalId: number, etapa: Etapa, textos: string[]) {
  ctx.db.transaction((tx) => {
    tx.delete(modeloChecklist).where(and(eq(modeloChecklist.canalId, canalId), eq(modeloChecklist.etapa, etapa))).run();
    if (textos.length) tx.insert(modeloChecklist).values(textos.map((texto, i) => ({ canalId, etapa, ordem: i + 1, texto }))).run();
  });
}

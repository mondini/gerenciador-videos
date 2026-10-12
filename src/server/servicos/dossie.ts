import { asc, eq } from "drizzle-orm";
import { z } from "zod";
import { BASES_DEFESA, MARCACOES, RISCOS, TIPOS_DOSSIE, resumirDossie } from "../../shared/dossie";
import { dossieItem, video } from "../db/schema";
import type { Contexto } from "./contexto";

const texto = z.string().default("");

export const itemDossieSchema = z.object({
  tipo: z.enum(TIPOS_DOSSIE),
  elemento: z.string().trim().min(1, "Informe o elemento"),
  categoria: texto,
  origem: texto,
  link: texto,
  base: z.union([z.enum(BASES_DEFESA), z.literal("")]).default(""),
  descricao: texto,
  contestacao: texto,
  provas: texto,
  risco: z.enum(RISCOS).default("baixo"),
  mitigacao: texto,
});
export type ItemDossie = z.input<typeof itemDossieSchema>;

export const dossieSchema = z.object({
  marcacaoSintetico: z.enum(MARCACOES),
  justificativaSintetico: z.string().default(""),
  itens: z.array(itemDossieSchema),
});

export function lerDossie(ctx: Contexto, videoId: number) {
  const v = ctx.db.select().from(video).where(eq(video.id, videoId)).get();
  if (!v) return null;
  const itens = ctx.db.select().from(dossieItem).where(eq(dossieItem.videoId, videoId)).orderBy(asc(dossieItem.ordem), asc(dossieItem.id)).all();
  return {
    marcacaoSintetico: v.marcacaoSintetico,
    justificativaSintetico: v.justificativaSintetico,
    itens,
    resumo: resumirDossie(itens, v.marcacaoSintetico),
  };
}

/** Substitui o dossiê inteiro do vídeo (usado ao colar o JSON gerado pela sessão de produção e ao salvar a aba). */
export function substituirDossie(ctx: Contexto, videoId: number, entrada: z.input<typeof dossieSchema>) {
  const dados = dossieSchema.parse(entrada);
  ctx.db.transaction((tx) => {
    tx.update(video)
      .set({ marcacaoSintetico: dados.marcacaoSintetico, justificativaSintetico: dados.justificativaSintetico })
      .where(eq(video.id, videoId))
      .run();
    tx.delete(dossieItem).where(eq(dossieItem.videoId, videoId)).run();
    if (dados.itens.length) {
      tx.insert(dossieItem).values(dados.itens.map((i, ordem) => ({ ...i, videoId, ordem }))).run();
    }
  });
  return lerDossie(ctx, videoId)!;
}

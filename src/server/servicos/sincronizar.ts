import { eq } from "drizzle-orm";
import { join } from "node:path";
import { z } from "zod";
import { ETAPAS, indiceEtapa } from "../../shared/etapas";
import { canal, video } from "../db/schema";
import { agoraDe, type Contexto } from "./contexto";
import { criarVideo, moverEtapa } from "./videos";

/**
 * O que o pipeline de um canal (ex.: `./ma sincronizar` do Marble & Ash) manda sobre um vídeo.
 * O canal é a fonte da verdade do roteiro (o roteiro.md) e do que já foi produzido; o sistema só registra.
 */
export const sincronizarSchema = z.object({
  prefixo: z.string().regex(/^[A-Z]{2,5}$/),
  codigo: z.string().regex(/^[A-Z]{2,5}-\d{3}$/),
  /** Nome da pasta do vídeo no canal e no Drive: `MA-001-the-man-who-had-everything`. */
  pasta: z.string().regex(/^[A-Z]{2,5}-\d{3}(-[a-z0-9-]+)?$/),
  nomeInterno: z.string().trim().min(1),
  tituloFinal: z.string().trim().nullish(),
  /** Etapa em que o pipeline mediu o vídeo; o sistema só avança, nunca volta. */
  etapa: z.enum(ETAPAS),
  roteiro: z.string(),
  duracaoFinalSeg: z.number().int().min(0).nullish(),
  pendencias: z.array(z.string()),
});
export type DadosSincronizar = z.input<typeof sincronizarSchema>;

/** Etapas que só o criador decide (no sistema): a sincronização nunca move para elas nem sai delas. */
const ETAPAS_MANUAIS = ["Agendado", "Publicado"] as const;

export function sincronizarVideo(ctx: Contexto, entrada: DadosSincronizar) {
  const d = sincronizarSchema.parse(entrada);
  if (!d.codigo.startsWith(`${d.prefixo}-`) || !d.pasta.startsWith(d.codigo)) {
    throw new Error(`Código inválido: ${d.codigo} não combina com o prefixo ${d.prefixo} ou a pasta ${d.pasta}`);
  }
  const c = ctx.db.select().from(canal).where(eq(canal.prefixoCodigo, d.prefixo)).get();
  if (!c) throw new Error(`Canal com prefixo ${d.prefixo} não existe: cadastre o canal no sistema antes de sincronizar`);

  const avisos: string[] = [];
  let v = ctx.db.select().from(video).where(eq(video.codigo, d.codigo)).get();
  if (v && v.canalId !== c.id) throw new Error(`O vídeo ${d.codigo} não pertence ao canal ${c.nome}`);
  if (!v) {
    const numero = Number(d.codigo.slice(d.prefixo.length + 1));
    v = criarVideo(ctx, { canalId: c.id, tituloProvisorio: d.nomeInterno }, numero).video;
    avisos.push(`Vídeo ${d.codigo} criado no sistema`);
  }

  ctx.db
    .update(video)
    .set({
      tituloProvisorio: d.nomeInterno,
      ...(d.tituloFinal ? { tituloFinal: d.tituloFinal } : {}),
      roteiroAtual: d.roteiro,
      ...(d.duracaoFinalSeg != null ? { duracaoFinalSeg: d.duracaoFinalSeg } : {}),
      // a pasta no Drive tem o mesmo nome da pasta do vídeo no canal (o backup do pipeline a cria)
      pastaRelativa: v.pastaRelativa ?? join(c.pastaRelativa, "VIDEOS", d.pasta),
      pendencias: d.pendencias,
      sincronizadoEm: agoraDe(ctx),
    })
    .where(eq(video.id, v.id))
    .run();

  const atual = v.etapa;
  const manual = (ETAPAS_MANUAIS as readonly string[]).includes(atual) || (ETAPAS_MANUAIS as readonly string[]).includes(d.etapa);
  if (!manual && indiceEtapa(d.etapa) > indiceEtapa(atual)) {
    const r = moverEtapa(ctx, v.id, d.etapa);
    avisos.push(`Etapa: ${atual} → ${d.etapa}`, ...r.avisos.filter((a) => !/checklist/.test(a)));
  }
  const final = ctx.db.select().from(video).where(eq(video.id, v.id)).get()!;
  return { video: final, avisos };
}

import { and, asc, desc, eq, sql } from "drizzle-orm";
import { z } from "zod";
import { ETAPAS, indiceEtapa, type Etapa } from "../../shared/etapas";
import { formatarCodigo } from "../../shared/codigo";
import { acharParecidos } from "../../shared/similaridade";
import { acharPastaVideo, criarPastaVideo, exportarVersaoRoteiro } from "../drive/estrutura";
import { canal, checklistItem, formato, historicoEtapa, modeloChecklist, versaoRoteiro, video } from "../db/schema";
import { agoraDe, type Contexto } from "./contexto";
import { relative } from "node:path";

export const novoVideoSchema = z.object({
  canalId: z.number().int(),
  tituloProvisorio: z.string().trim().min(1),
  /** Nulo/ausente = "a definir" (só para ideias importadas em lote). */
  formatoId: z.number().int().nullish(),
  notaApelo: z.number().int().min(1).max(5).nullish(),
  notaIlustracao: z.number().int().min(1).max(5).nullish(),
  notaPesquisa: z.number().int().min(1).max(5).nullish(),
  derivadoDeId: z.number().int().nullish(),
});
export type NovoVideo = z.input<typeof novoVideoSchema>;

/** `numero` fixo só para vídeos que já nasceram com código fora do sistema (ver sincronizar.ts). */
export function criarVideo(ctx: Contexto, entrada: NovoVideo, numeroFixo?: number) {
  const dados = novoVideoSchema.parse(entrada);
  const agora = agoraDe(ctx);
  return ctx.db.transaction((tx) => {
    const c = tx.select().from(canal).where(eq(canal.id, dados.canalId)).get();
    if (!c) throw new Error(`Canal ${dados.canalId} não existe`);
    if (dados.formatoId != null) {
      const f = tx.select().from(formato).where(and(eq(formato.id, dados.formatoId), eq(formato.canalId, c.id))).get();
      if (!f) throw new Error("Formato não pertence a este canal");
    }
    const ultimo = tx
      .select({ n: sql<number>`coalesce(max(${video.numero}), 0)` })
      .from(video)
      .where(eq(video.canalId, c.id))
      .get();
    const numero = numeroFixo ?? (ultimo?.n ?? 0) + 1;
    const parecidos = acharParecidos(
      dados.tituloProvisorio,
      tx.select().from(video).where(eq(video.canalId, c.id)).all(),
    );
    const criado = tx
      .insert(video)
      .values({
        ...dados,
        numero,
        codigo: formatarCodigo(c.prefixoCodigo, numero),
        vozUsada: c.vozPadrao,
        descricao: c.modeloDescricao,
        tags: c.tagsPadrao,
      })
      .returning()
      .get();
    const modelos = tx
      .select()
      .from(modeloChecklist)
      .where(eq(modeloChecklist.canalId, c.id))
      .orderBy(asc(modeloChecklist.ordem))
      .all();
    if (modelos.length) {
      tx.insert(checklistItem)
        .values(modelos.map((m) => ({ videoId: criado.id, etapa: m.etapa, ordem: m.ordem, texto: m.texto })))
        .run();
    }
    tx.insert(historicoEtapa).values({ videoId: criado.id, etapa: "Ideia", entrouEm: agora }).run();
    return { video: criado, parecidos };
  });
}

export interface ResultadoMover {
  video: typeof video.$inferSelect;
  avisos: string[];
}

/**
 * Move o vídeo de etapa. Efeitos:
 * - ao chegar em Pesquisa (ou além) sem pasta, cria a pasta no Drive;
 * - ao sair de Roteiro para frente, salva uma versão automática do roteiro (e exporta o .md se houver pasta).
 * O checklist não bloqueia: pendências viram apenas aviso.
 */
export function moverEtapa(ctx: Contexto, videoId: number, destino: Etapa): ResultadoMover {
  if (!ETAPAS.includes(destino)) throw new Error(`Etapa inválida: ${destino}`);
  const agora = agoraDe(ctx);
  const v = ctx.db.select().from(video).where(eq(video.id, videoId)).get();
  if (!v) throw new Error(`Vídeo ${videoId} não existe`);
  const c = ctx.db.select().from(canal).where(eq(canal.id, v.canalId)).get()!;
  const avisos: string[] = [];
  if (v.etapa === destino) return { video: v, avisos };

  let pastaRelativa = v.pastaRelativa;
  if (!pastaRelativa && indiceEtapa(destino) >= indiceEtapa("Pesquisa")) {
    const { caminho, criada } = criarPastaVideo(ctx.driveRoot, c.pastaRelativa, v.codigo, v.tituloProvisorio);
    pastaRelativa = relative(ctx.driveRoot, caminho);
    avisos.push(criada ? `Pasta criada no Drive: ${pastaRelativa}` : `Pasta já existia no Drive: ${pastaRelativa}`);
  }

  const saindoDeRoteiro = v.etapa === "Roteiro" && indiceEtapa(destino) > indiceEtapa("Roteiro");
  const pendentes = ctx.db
    .select({ n: sql<number>`count(*)` })
    .from(checklistItem)
    .where(and(eq(checklistItem.videoId, v.id), eq(checklistItem.etapa, v.etapa), eq(checklistItem.feito, false)))
    .get()?.n ?? 0;
  if (pendentes > 0) avisos.push(`${pendentes} item(ns) pendente(s) no checklist de ${v.etapa}`);

  const atualizado = ctx.db.transaction((tx) => {
    if (saindoDeRoteiro && v.roteiroAtual.trim()) {
      const ultima = tx.select().from(versaoRoteiro).where(eq(versaoRoteiro.videoId, v.id)).orderBy(desc(versaoRoteiro.numero)).get();
      if (!ultima || ultima.conteudo !== v.roteiroAtual) {
        const numero = (ultima?.numero ?? 0) + 1;
        const pasta = pastaRelativa ? acharPastaVideo(ctx.driveRoot, c.pastaRelativa, v.codigo) : null;
        const arquivo = pasta ? exportarVersaoRoteiro(pasta, v.codigo, numero, v.roteiroAtual) : null;
        tx.insert(versaoRoteiro)
          .values({
            videoId: v.id,
            numero,
            conteudo: v.roteiroAtual,
            origem: "saida-roteiro",
            arquivoExportado: arquivo ? relative(ctx.driveRoot, arquivo) : null,
          })
          .run();
        avisos.push(`Versão v${numero} do roteiro salva${arquivo ? " e exportada para o Drive" : ""}`);
      }
    }
    tx.insert(historicoEtapa).values({ videoId: v.id, etapa: destino, entrouEm: agora }).run();
    return tx
      .update(video)
      .set({ etapa: destino, pastaRelativa, ...(destino === "Publicado" && !v.dataPublicacao ? { dataPublicacao: agora } : {}) })
      .where(eq(video.id, v.id))
      .returning()
      .get();
  });
  return { video: atualizado, avisos };
}

/** Cria uma ideia por linha (formato "a definir"). Linhas vazias são ignoradas. */
export function importarIdeias(ctx: Contexto, canalId: number, texto: string) {
  return texto
    .split("\n")
    .map((l) => l.replace(/^[\s\-*•\d.)]+/, "").trim())
    .filter(Boolean)
    .map((titulo) => criarVideo(ctx, { canalId, tituloProvisorio: titulo }));
}

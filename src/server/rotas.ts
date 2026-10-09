import { zValidator } from "@hono/zod-validator";
import type { ZodType } from "zod";
import { and, asc, desc, eq, inArray } from "drizzle-orm";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { Hono } from "hono";
import { z } from "zod";
import { ETAPAS } from "../shared/etapas";
import { emRisco } from "../shared/risco";
import { proximoHorarioLivre } from "../shared/grade";
import { statusSubpastas } from "./drive/estrutura";
import { canal, checklistItem, formato, gradePublicacao, versaoRoteiro, video } from "./db/schema";
import { criarCanal, novoCanalSchema } from "./servicos/canais";
import { agoraDe, type Contexto } from "./servicos/contexto";
import { criarVideo, importarIdeias, moverEtapa, novoVideoSchema } from "./servicos/videos";
import { exportarVersaoRoteiro, acharPastaVideo } from "./drive/estrutura";
import { relative } from "node:path";

/** Validador de corpo JSON: erros saem sempre no formato { erro } com status 400. */
const corpo = <T extends ZodType>(schema: T) =>
  zValidator("json", schema, (resultado, c) => {
    if (!resultado.success) {
      return c.json({ erro: resultado.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ") }, 400);
    }
  });

const nota = z.number().int().min(1).max(5).nullable();
const data = z.coerce.date().nullable();

export const editarVideoSchema = z
  .object({
    tituloProvisorio: z.string().trim().min(1),
    tituloFinal: z.string().trim().nullable(),
    formatoId: z.number().int().nullable(),
    serieId: z.number().int().nullable(),
    dataPlanejada: data,
    notaApelo: nota,
    notaIlustracao: nota,
    notaPesquisa: nota,
    gancho: z.string(),
    resumo: z.string(),
    roteiroAtual: z.string(),
    vozUsada: z.string(),
    duracaoFinalSeg: z.number().int().min(0).nullable(),
    notasCorte: z.string(),
    descricao: z.string().max(5000, "A descrição do YouTube aceita até 5.000 caracteres"),
    tags: z.array(z.string()),
    capitulos: z.string(),
    youtubeVideoId: z.string().nullable(),
    urlYoutube: z.string().nullable(),
  })
  .partial();

export function criarRotas(ctx: Contexto) {
  const { db } = ctx;

  return new Hono()
    .get("/api/saude", (c) => c.json({ ok: true }))
    .get("/api/canais", (c) => c.json(db.select().from(canal).orderBy(asc(canal.id)).all()))
    .post("/api/canais", corpo(novoCanalSchema), (c) => c.json(criarCanal(ctx, c.req.valid("json")), 201))

    .get("/api/canais/:id/formatos", (c) =>
      c.json(db.select().from(formato).where(eq(formato.canalId, Number(c.req.param("id")))).orderBy(asc(formato.id)).all()),
    )

    .get("/api/canais/:id/kanban", (c) => {
      const canalId = Number(c.req.param("id"));
      const agora = agoraDe(ctx);
      const canalRow = db.select().from(canal).where(eq(canal.id, canalId)).get();
      if (!canalRow) return c.json({ erro: "Canal não encontrado" }, 404);
      const videos = db.select().from(video).where(eq(video.canalId, canalId)).all();
      const formatos = new Map(db.select().from(formato).where(eq(formato.canalId, canalId)).all().map((f) => [f.id, f.nome]));
      const ids = videos.map((v) => v.id);
      const itens = ids.length ? db.select().from(checklistItem).where(inArray(checklistItem.videoId, ids)).all() : [];
      const cards = videos.map((v) => {
        const pendentes = itens.filter((i) => i.videoId === v.id && i.etapa === v.etapa && !i.feito).length;
        const pasta = v.pastaRelativa ? join(ctx.driveRoot, v.pastaRelativa) : null;
        const arquivos = pasta && existsSync(pasta) ? statusSubpastas(pasta) : null;
        const pontuacao = v.notaApelo != null && v.notaIlustracao != null && v.notaPesquisa != null
          ? v.notaApelo + v.notaIlustracao + v.notaPesquisa
          : null;
        return {
          id: v.id,
          codigo: v.codigo,
          titulo: v.tituloFinal ?? v.tituloProvisorio,
          etapa: v.etapa,
          formato: v.formatoId != null ? (formatos.get(v.formatoId) ?? null) : null,
          dataPlanejada: v.dataPlanejada,
          pontuacao,
          pendentesChecklist: pendentes,
          emRisco: emRisco(v.etapa, v.dataPlanejada, agora),
          arquivos,
        };
      });
      cards.sort((a, b) => (b.pontuacao ?? -1) - (a.pontuacao ?? -1) || a.codigo.localeCompare(b.codigo));
      const grade = db.select().from(gradePublicacao).where(eq(gradePublicacao.canalId, canalId)).all();
      const ocupados = videos.flatMap((v) => (v.dataPlanejada ? [v.dataPlanejada] : []));
      return c.json({
        canal: canalRow,
        etapas: ETAPAS,
        cards,
        proximoHorarioLivre: proximoHorarioLivre(grade, ocupados, agora),
      });
    })

    .post("/api/videos", corpo(novoVideoSchema), (c) => c.json(criarVideo(ctx, c.req.valid("json")), 201))
    .post(
      "/api/canais/:id/ideias",
      corpo(z.object({ texto: z.string() })),
      (c) => c.json(importarIdeias(ctx, Number(c.req.param("id")), c.req.valid("json").texto), 201),
    )

    .get("/api/videos/:id", (c) => {
      const id = Number(c.req.param("id"));
      const v = db.select().from(video).where(eq(video.id, id)).get();
      if (!v) return c.json({ erro: "Vídeo não encontrado" }, 404);
      return c.json({
        video: v,
        checklist: db.select().from(checklistItem).where(eq(checklistItem.videoId, id)).orderBy(asc(checklistItem.ordem)).all(),
        versoes: db.select().from(versaoRoteiro).where(eq(versaoRoteiro.videoId, id)).orderBy(desc(versaoRoteiro.numero)).all(),
      });
    })
    .patch("/api/videos/:id", corpo(editarVideoSchema), (c) => {
      const id = Number(c.req.param("id"));
      const campos = c.req.valid("json");
      if (Object.keys(campos).length === 0) return c.json({ erro: "Nada para alterar" }, 400);
      const atualizado = db.update(video).set(campos).where(eq(video.id, id)).returning().get();
      return atualizado ? c.json(atualizado) : c.json({ erro: "Vídeo não encontrado" }, 404);
    })
    .post("/api/videos/:id/etapa", corpo(z.object({ etapa: z.enum(ETAPAS) })), (c) =>
      c.json(moverEtapa(ctx, Number(c.req.param("id")), c.req.valid("json").etapa)),
    )
    .patch("/api/checklist/:id", corpo(z.object({ feito: z.boolean() })), (c) => {
      const { feito } = c.req.valid("json");
      const item = db
        .update(checklistItem)
        .set({ feito, feitoEm: feito ? agoraDe(ctx) : null })
        .where(eq(checklistItem.id, Number(c.req.param("id"))))
        .returning()
        .get();
      return item ? c.json(item) : c.json({ erro: "Item não encontrado" }, 404);
    })
    .get("/api/videos/:id/arquivos", (c) => {
      const v = db.select().from(video).where(eq(video.id, Number(c.req.param("id")))).get();
      if (!v) return c.json({ erro: "Vídeo não encontrado" }, 404);
      if (!v.pastaRelativa) return c.json({ pasta: null, subpastas: [] });
      const pasta = join(ctx.driveRoot, v.pastaRelativa);
      return c.json({ pasta: v.pastaRelativa, subpastas: existsSync(pasta) ? statusSubpastas(pasta) : [] });
    })
    .post("/api/videos/:id/roteiro/versao", corpo(z.object({ nota: z.string().optional() })), (c) => {
      const v = db.select().from(video).where(eq(video.id, Number(c.req.param("id")))).get();
      if (!v) return c.json({ erro: "Vídeo não encontrado" }, 404);
      if (!v.roteiroAtual.trim()) return c.json({ erro: "O roteiro está vazio" }, 400);
      const canalRow = db.select().from(canal).where(eq(canal.id, v.canalId)).get()!;
      const ultima = db.select().from(versaoRoteiro).where(eq(versaoRoteiro.videoId, v.id)).orderBy(desc(versaoRoteiro.numero)).get();
      if (ultima?.conteudo === v.roteiroAtual) return c.json({ erro: "O roteiro não mudou desde a última versão" }, 409);
      const numero = (ultima?.numero ?? 0) + 1;
      const pasta = v.pastaRelativa ? acharPastaVideo(ctx.driveRoot, canalRow.pastaRelativa, v.codigo) : null;
      const arquivo = pasta ? exportarVersaoRoteiro(pasta, v.codigo, numero, v.roteiroAtual) : null;
      const criada = db
        .insert(versaoRoteiro)
        .values({
          videoId: v.id,
          numero,
          conteudo: v.roteiroAtual,
          origem: "manual",
          nota: c.req.valid("json").nota ?? null,
          arquivoExportado: arquivo ? relative(ctx.driveRoot, arquivo) : null,
        })
        .returning()
        .get();
      return c.json(criada, 201);
    });
}

export type AppType = ReturnType<typeof criarRotas>;

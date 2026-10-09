import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { existsSync, mkdtempSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { eq } from "drizzle-orm";
import { abrirBanco } from "../db";
import { checklistItem, formato, historicoEtapa, versaoRoteiro, video } from "../db/schema";
import { criarCanal } from "./canais";
import { criarVideo, importarIdeias, moverEtapa } from "./videos";
import type { Contexto } from "./contexto";

let raiz: string;
let ctx: Contexto;
let canalId: number;
let formatoId: number;

beforeEach(() => {
  raiz = mkdtempSync(join(tmpdir(), "drive-fake-"));
  const { db } = abrirBanco(":memory:");
  ctx = { db, driveRoot: raiz, agora: () => new Date(2026, 9, 9, 10, 0) };
  const c = criarCanal(ctx, { nome: "Canal BJJ", prefixoCodigo: "BJJ", pastaRelativa: "BJJ - Canal", nicho: "BJJ" });
  canalId = c.id;
  formatoId = db.select().from(formato).where(eq(formato.canalId, c.id)).get()!.id;
});
afterEach(() => rmSync(raiz, { recursive: true, force: true }));

describe("criarCanal", () => {
  it("cria formatos, checklists padrão e a estrutura no Drive", () => {
    expect(ctx.db.select().from(formato).all()).toHaveLength(5);
    expect(existsSync(join(raiz, "BJJ - Canal", "VIDEOS"))).toBe(true);
  });
  it("recusa prefixo inválido e pasta fora da raiz", () => {
    expect(() => criarCanal(ctx, { nome: "x", prefixoCodigo: "bjj", pastaRelativa: "x" })).toThrow();
    expect(() => criarCanal(ctx, { nome: "x", prefixoCodigo: "XXX", pastaRelativa: "../fora" })).toThrow(/fora da raiz/);
  });
});

describe("criarVideo", () => {
  it("gera códigos sequenciais, copia o checklist e registra a etapa Ideia", () => {
    const a = criarVideo(ctx, { canalId, tituloProvisorio: "A origem do BJJ", formatoId }).video;
    const b = criarVideo(ctx, { canalId, tituloProvisorio: "Mito da guarda", formatoId }).video;
    expect([a.codigo, b.codigo]).toEqual(["BJJ-001", "BJJ-002"]);
    expect(ctx.db.select().from(checklistItem).where(eq(checklistItem.videoId, a.id)).all().length).toBeGreaterThan(10);
    expect(ctx.db.select().from(historicoEtapa).where(eq(historicoEtapa.videoId, a.id)).all()).toHaveLength(1);
  });
  it("avisa de títulos parecidos sem bloquear", () => {
    criarVideo(ctx, { canalId, tituloProvisorio: "A origem do jiu-jitsu brasileiro" });
    const r = criarVideo(ctx, { canalId, tituloProvisorio: "Origem do jiu-jitsu brasileiro" });
    expect(r.parecidos.map((p) => p.codigo)).toEqual(["BJJ-001"]);
    expect(r.video.codigo).toBe("BJJ-002");
  });
  it("não cria pasta no Drive para ideias", () => {
    criarVideo(ctx, { canalId, tituloProvisorio: "Ideia solta" });
    expect(readdirSync(join(raiz, "BJJ - Canal", "VIDEOS"))).toEqual([]);
  });
  it("recusa formato de outro canal", () => {
    const outro = criarCanal(ctx, { nome: "Outro", prefixoCodigo: "OUT", pastaRelativa: "Outro" });
    const f = ctx.db.select().from(formato).where(eq(formato.canalId, outro.id)).get()!;
    expect(() => criarVideo(ctx, { canalId, tituloProvisorio: "x", formatoId: f.id })).toThrow(/não pertence/);
  });
});

describe("moverEtapa", () => {
  it("Ideia → Pesquisa cria a pasta no Drive uma única vez", () => {
    const v = criarVideo(ctx, { canalId, tituloProvisorio: "Mito ou verdade?", formatoId }).video;
    const r = moverEtapa(ctx, v.id, "Pesquisa");
    expect(r.video.pastaRelativa).toBe(join("BJJ - Canal", "VIDEOS", "BJJ-001_mito-ou-verdade"));
    expect(r.avisos.some((a) => a.startsWith("Pasta criada"))).toBe(true);
    const volta = moverEtapa(ctx, v.id, "Ideia");
    const de_novo = moverEtapa(ctx, v.id, "Pesquisa");
    expect(volta.video.pastaRelativa).toBe(r.video.pastaRelativa);
    expect(de_novo.avisos.some((a) => a.startsWith("Pasta criada"))).toBe(false);
    expect(readdirSync(join(raiz, "BJJ - Canal", "VIDEOS"))).toHaveLength(1);
  });

  it("avisa de pendências do checklist mas não bloqueia", () => {
    const v = criarVideo(ctx, { canalId, tituloProvisorio: "x", formatoId }).video;
    const r = moverEtapa(ctx, v.id, "Pesquisa");
    expect(r.video.etapa).toBe("Pesquisa");
    expect(r.avisos.some((a) => /pendente/.test(a))).toBe(true);
  });

  it("sair de Roteiro salva a versão e exporta o .md; sem mudança não duplica", () => {
    const v = criarVideo(ctx, { canalId, tituloProvisorio: "Roteiro teste", formatoId }).video;
    moverEtapa(ctx, v.id, "Roteiro");
    ctx.db.update(video).set({ roteiroAtual: "# Meu roteiro" }).where(eq(video.id, v.id)).run();
    const r = moverEtapa(ctx, v.id, "Narração");
    const versoes = ctx.db.select().from(versaoRoteiro).where(eq(versaoRoteiro.videoId, v.id)).all();
    expect(versoes).toHaveLength(1);
    expect(versoes[0]?.origem).toBe("saida-roteiro");
    const arquivo = join(raiz, versoes[0]!.arquivoExportado!);
    expect(readFileSync(arquivo, "utf8")).toBe("# Meu roteiro");
    expect(r.avisos.some((a) => a.includes("v1"))).toBe(true);
    moverEtapa(ctx, v.id, "Roteiro");
    moverEtapa(ctx, v.id, "Narração");
    expect(ctx.db.select().from(versaoRoteiro).where(eq(versaoRoteiro.videoId, v.id)).all()).toHaveLength(1);
  });

  it("registra histórico e a data de publicação", () => {
    const v = criarVideo(ctx, { canalId, tituloProvisorio: "x", formatoId }).video;
    const r = moverEtapa(ctx, v.id, "Publicado");
    expect(r.video.dataPublicacao).toEqual(new Date(2026, 9, 9, 10, 0));
    expect(ctx.db.select().from(historicoEtapa).where(eq(historicoEtapa.videoId, v.id)).all().map((h) => h.etapa)).toEqual(["Ideia", "Publicado"]);
  });
});

describe("importarIdeias", () => {
  it("cria uma ideia por linha com formato a definir, ignorando vazias e marcadores", () => {
    const r = importarIdeias(ctx, canalId, "- Origem do BJJ\n\n2. Mito da guarda fechada\n  \n• Rivalidade Gracie x Machado");
    expect(r.map((x) => x.video.tituloProvisorio)).toEqual(["Origem do BJJ", "Mito da guarda fechada", "Rivalidade Gracie x Machado"]);
    expect(r.every((x) => x.video.formatoId === null)).toBe(true);
    expect(r.map((x) => x.video.codigo)).toEqual(["BJJ-001", "BJJ-002", "BJJ-003"]);
  });
});

import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { abrirBanco } from "./db";
import { createApp } from "./app";

let raiz: string;
let app: ReturnType<typeof createApp>;

const json = (corpo: unknown) => ({
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify(corpo),
});
const patch = (corpo: unknown) => ({ ...json(corpo), method: "PATCH" });

async function criarCanalBase() {
  const r = await app.request("/api/canais", json({ nome: "BJJ", prefixoCodigo: "BJJ", pastaRelativa: "BJJ - Canal", grade: [{ diaSemana: 2, hora: "12:00" }] }));
  return (await r.json()) as { id: number };
}

beforeEach(() => {
  raiz = mkdtempSync(join(tmpdir(), "drive-fake-"));
  const { db } = abrirBanco(":memory:");
  app = createApp({ db, driveRoot: raiz, agora: () => new Date(2026, 9, 9, 10, 0) });
});
afterEach(() => rmSync(raiz, { recursive: true, force: true }));

describe("API", () => {
  it("valida entrada com mensagem em 400", async () => {
    const r = await app.request("/api/canais", json({ nome: "", prefixoCodigo: "x", pastaRelativa: "" }));
    expect(r.status).toBe(400);
    expect(((await r.json()) as { erro: string }).erro).toMatch(/prefixoCodigo/);
  });

  it("recusa pasta de canal fora do Drive com 400", async () => {
    const r = await app.request("/api/canais", json({ nome: "x", prefixoCodigo: "XX", pastaRelativa: "../fora" }));
    expect(r.status).toBe(400);
  });

  it("fluxo: criar canal → importar ideias → pontuar → mover → kanban", async () => {
    const canal = await criarCanalBase();
    const ideias = await app.request(`/api/canais/${canal.id}/ideias`, json({ texto: "Origem do BJJ\nMito da guarda" }));
    const criadas = (await ideias.json()) as { video: { id: number; codigo: string } }[];
    expect(criadas.map((c) => c.video.codigo)).toEqual(["BJJ-001", "BJJ-002"]);

    const id = criadas[1]!.video.id;
    const ed = await app.request(`/api/videos/${id}`, patch({ notaApelo: 5, notaIlustracao: 4, notaPesquisa: 3, dataPlanejada: "2026-10-13T12:00:00.000Z" }));
    expect(ed.status).toBe(200);
    const mov = await app.request(`/api/videos/${id}/etapa`, json({ etapa: "Pesquisa" }));
    expect(((await mov.json()) as { avisos: string[] }).avisos.some((a) => a.startsWith("Pasta criada"))).toBe(true);

    const kanban = (await (await app.request(`/api/canais/${canal.id}/kanban`)).json()) as {
      cards: { codigo: string; pontuacao: number | null; emRisco: boolean; etapa: string; arquivos: unknown[] | null }[];
      proximoHorarioLivre: string | null;
    };
    expect(kanban.cards.map((c) => c.codigo)).toEqual(["BJJ-002", "BJJ-001"]); // ordenado por pontuação
    expect(kanban.cards[0]).toMatchObject({ pontuacao: 12, etapa: "Pesquisa", emRisco: true });
    expect(kanban.cards[0]!.arquivos).toHaveLength(7);
    expect(kanban.cards[1]!.arquivos).toBeNull();
    expect(kanban.proximoHorarioLivre).not.toBeNull();
  });

  it("alterna item do checklist e rejeita notas fora de 1–5", async () => {
    const canal = await criarCanalBase();
    const { video } = (await (await app.request("/api/videos", json({ canalId: canal.id, tituloProvisorio: "x" }))).json()) as { video: { id: number } };
    const ficha = (await (await app.request(`/api/videos/${video.id}`)).json()) as { checklist: { id: number }[] };
    const r = await app.request(`/api/checklist/${ficha.checklist[0]!.id}`, patch({ feito: true }));
    expect(((await r.json()) as { feito: boolean }).feito).toBe(true);
    const ruim = await app.request(`/api/videos/${video.id}`, patch({ notaApelo: 9 }));
    expect(ruim.status).toBe(400);
  });

  it("salva versão manual do roteiro, exporta e recusa duplicar sem mudança", async () => {
    const canal = await criarCanalBase();
    const { video } = (await (await app.request("/api/videos", json({ canalId: canal.id, tituloProvisorio: "Roteiro" }))).json()) as { video: { id: number } };
    await app.request(`/api/videos/${video.id}/etapa`, json({ etapa: "Roteiro" }));
    expect((await app.request(`/api/videos/${video.id}/roteiro/versao`, json({}))).status).toBe(400); // vazio
    await app.request(`/api/videos/${video.id}`, patch({ roteiroAtual: "# v1" }));
    const ok = await app.request(`/api/videos/${video.id}/roteiro/versao`, json({ nota: "primeira" }));
    expect(ok.status).toBe(201);
    expect(((await ok.json()) as { arquivoExportado: string }).arquivoExportado).toMatch(/BJJ-001_roteiro_v1\.md$/);
    expect((await app.request(`/api/videos/${video.id}/roteiro/versao`, json({}))).status).toBe(409);
  });

  it("limita a descrição a 5.000 caracteres", async () => {
    const canal = await criarCanalBase();
    const { video } = (await (await app.request("/api/videos", json({ canalId: canal.id, tituloProvisorio: "x" }))).json()) as { video: { id: number } };
    const r = await app.request(`/api/videos/${video.id}`, patch({ descricao: "a".repeat(5001) }));
    expect(r.status).toBe(400);
  });
});

describe("configurações do canal", () => {
  const put = (corpo: unknown) => ({ ...json(corpo), method: "PUT" });

  it("edita dados, grade, formatos, séries, temas e checklist", async () => {
    const { id } = await criarCanalBase();
    const ed = await app.request(`/api/canais/${id}`, patch({ nicho: "BJJ", tagsPadrao: ["bjj", "jiu-jitsu"], vozPadrao: "Voz X" }));
    expect(ed.status).toBe(200);

    expect((await app.request(`/api/canais/${id}/grade`, put({ grade: [{ diaSemana: 1, hora: "09:00" }, { diaSemana: 4, hora: "18:30" }] }))).status).toBe(200);
    expect((await app.request(`/api/canais/${id}/checklist/Roteiro`, put({ textos: ["Só este item"] }))).status).toBe(200);

    const f = (await (await app.request(`/api/canais/${id}/formatos`, json({ nome: "Tutorial" }))).json()) as { id: number };
    expect((await app.request(`/api/canais/${id}/formatos`, json({ nome: "Tutorial" }))).status).toBe(409);
    expect((await app.request(`/api/formatos/${f.id}`, patch({ ativo: false }))).status).toBe(200);

    const s = (await (await app.request(`/api/canais/${id}/series`, json({ nome: "Faixas" }))).json()) as { id: number };
    const t = (await (await app.request(`/api/canais/${id}/temas`, json({ nome: "guarda" }))).json()) as { id: number };
    expect((await app.request(`/api/canais/${id}/temas`, json({ nome: "guarda" }))).status).toBe(409);

    const cfg = (await (await app.request(`/api/canais/${id}/config`)).json()) as {
      canal: { nicho: string; tagsPadrao: string[] }; grade: unknown[]; formatos: { nome: string; ativo: boolean }[]; series: unknown[]; temas: unknown[];
      modelos: { etapa: string; texto: string }[];
    };
    expect(cfg.canal.tagsPadrao).toEqual(["bjj", "jiu-jitsu"]);
    expect(cfg.grade).toHaveLength(2);
    expect(cfg.formatos.find((x) => x.nome === "Tutorial")?.ativo).toBe(false);
    expect(cfg.modelos.filter((m) => m.etapa === "Roteiro").map((m) => m.texto)).toEqual(["Só este item"]);
    expect(cfg.modelos.some((m) => m.etapa === "Pesquisa")).toBe(true);

    expect((await app.request(`/api/series/${s.id}`, { method: "DELETE" })).status).toBe(200);
    expect((await app.request(`/api/temas/${t.id}`, { method: "DELETE" })).status).toBe(200);
  });

  it("não apaga série em uso e recusa etapa inválida", async () => {
    const { id } = await criarCanalBase();
    const s = (await (await app.request(`/api/canais/${id}/series`, json({ nome: "Faixas" }))).json()) as { id: number };
    const formatos = (await (await app.request(`/api/canais/${id}/formatos`)).json()) as { id: number }[];
    const r = await app.request("/api/videos", json({ canalId: id, tituloProvisorio: "Teste", formatoId: formatos[0]!.id }));
    const { video } = (await r.json()) as { video: { id: number } };
    await app.request(`/api/videos/${video.id}`, patch({ serieId: s.id }));
    expect((await app.request(`/api/series/${s.id}`, { method: "DELETE" })).status).toBe(409);
    expect((await app.request(`/api/canais/${id}/checklist/Nada`, put2({ textos: [] }))).status).toBe(400);
  });
});

const put2 = (corpo: unknown) => ({ method: "PUT", headers: { "content-type": "application/json" }, body: JSON.stringify(corpo) });

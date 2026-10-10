import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import Database from "better-sqlite3";
import { resolverDentro } from "./seguranca";
import {
  SUBPASTAS_VIDEO,
  acharPastaVideo,
  criarEstruturaCanal,
  criarPastaVideo,
  escreverArquivoNovo,
  exportarVersaoRoteiro,
  statusSubpastas,
} from "./estrutura";
import { fazerBackup } from "./backup";

let raiz: string;
beforeEach(() => {
  raiz = mkdtempSync(join(tmpdir(), "drive-fake-"));
});
afterEach(() => rmSync(raiz, { recursive: true, force: true }));

describe("resolverDentro", () => {
  it("aceita caminhos dentro da raiz", () => {
    expect(resolverDentro(raiz, "BJJ", "VIDEOS")).toBe(join(raiz, "BJJ", "VIDEOS"));
  });
  it("recusa escapar da raiz", () => {
    expect(() => resolverDentro(raiz, "..", "fora")).toThrow(/fora da raiz/);
    expect(() => resolverDentro(raiz, "BJJ/../../fora")).toThrow(/fora da raiz/);
    expect(() => resolverDentro(raiz, "/etc")).toThrow(/fora da raiz/);
  });
});

describe("estrutura de pastas", () => {
  it("cria o canal e a pasta do vídeo com as 7 subpastas", () => {
    criarEstruturaCanal(raiz, "BJJ - Canal");
    const { caminho, criada } = criarPastaVideo(raiz, "BJJ - Canal", "BJJ-001", "Mito ou verdade?");
    expect(criada).toBe(true);
    expect(caminho).toBe(join(raiz, "BJJ - Canal", "VIDEOS", "BJJ-001_mito-ou-verdade"));
    expect(readdirSync(caminho).sort()).toEqual([...SUBPASTAS_VIDEO]);
    expect(existsSync(join(raiz, "BJJ - Canal", "00_IDENTIDADE"))).toBe(true);
  });

  it("achar pela prefixo continua funcionando depois de renomear no Finder", () => {
    criarEstruturaCanal(raiz, "C");
    const { caminho } = criarPastaVideo(raiz, "C", "BJJ-002", "Título antigo");
    const novo = join(raiz, "C", "VIDEOS", "BJJ-002_titulo-novo-do-usuario");
    renameSync(caminho, novo);
    expect(acharPastaVideo(raiz, "C", "BJJ-002")).toBe(novo);
    const again = criarPastaVideo(raiz, "C", "BJJ-002", "Outro título qualquer");
    expect(again).toEqual({ caminho: novo, criada: false });
    expect(readdirSync(join(raiz, "C", "VIDEOS"))).toEqual(["BJJ-002_titulo-novo-do-usuario"]);
  });

  it("não confunde BJJ-001 com BJJ-0010", () => {
    criarEstruturaCanal(raiz, "C");
    criarPastaVideo(raiz, "C", "BJJ-010", "dez");
    expect(acharPastaVideo(raiz, "C", "BJJ-001")).toBeNull();
  });

  it("recusa quando há duas pastas com o mesmo código", () => {
    criarEstruturaCanal(raiz, "C");
    mkdirSync(join(raiz, "C", "VIDEOS", "BJJ-003_a"));
    mkdirSync(join(raiz, "C", "VIDEOS", "BJJ-003_b"));
    expect(() => acharPastaVideo(raiz, "C", "BJJ-003")).toThrow(/Mais de uma pasta/);
  });

  it("recriar a estrutura nunca apaga nem altera arquivos existentes", () => {
    criarEstruturaCanal(raiz, "C");
    const { caminho } = criarPastaVideo(raiz, "C", "BJJ-004", "x");
    const arq = join(caminho, "02_audio", "BJJ-004_narracao_v1.mp3");
    writeFileSync(arq, "audio");
    criarPastaVideo(raiz, "C", "BJJ-004", "x");
    criarEstruturaCanal(raiz, "C");
    expect(readFileSync(arq, "utf8")).toBe("audio");
  });

  it("não sai da raiz com pasta de canal maliciosa", () => {
    expect(() => criarEstruturaCanal(raiz, "../fora")).toThrow(/fora da raiz/);
  });
});

describe("nunca sobrescrever", () => {
  it("escreverArquivoNovo falha se o arquivo já existir e preserva o conteúdo", () => {
    const f = join(raiz, "a.txt");
    escreverArquivoNovo(f, "original");
    expect(() => escreverArquivoNovo(f, "novo")).toThrow();
    expect(readFileSync(f, "utf8")).toBe("original");
  });

  it("exporta versões do roteiro com nomes novos e recusa repetir a mesma versão", () => {
    criarEstruturaCanal(raiz, "C");
    const { caminho } = criarPastaVideo(raiz, "C", "BJJ-005", "x");
    const v1 = exportarVersaoRoteiro(caminho, "BJJ-005", 1, "# v1");
    exportarVersaoRoteiro(caminho, "BJJ-005", 2, "# v2");
    expect(v1).toBe(join(caminho, "01_roteiro", "BJJ-005_roteiro_v1.md"));
    expect(() => exportarVersaoRoteiro(caminho, "BJJ-005", 1, "# alterado")).toThrow();
    expect(readFileSync(v1, "utf8")).toBe("# v1");
  });
});

describe("status das subpastas", () => {
  it("conta arquivos por subpasta ignorando ocultos e subdiretórios", () => {
    criarEstruturaCanal(raiz, "C");
    const { caminho } = criarPastaVideo(raiz, "C", "BJJ-006", "x");
    writeFileSync(join(caminho, "06_thumbnail", "BJJ-006_thumb_A.png"), "png");
    writeFileSync(join(caminho, "06_thumbnail", ".DS_Store"), "x");
    mkdirSync(join(caminho, "06_thumbnail", "extras"));
    const status = statusSubpastas(caminho);
    expect(status.find((s) => s.subpasta === "06_thumbnail")).toEqual({ subpasta: "06_thumbnail", arquivos: 1, soOnline: 0 });
    expect(status.find((s) => s.subpasta === "02_audio")?.arquivos).toBe(0);
    expect(status).toHaveLength(7);
  });
});

describe("backup do banco", () => {
  function criarBanco(): string {
    const caminho = join(raiz, "gerenciador.db");
    const db = new Database(caminho);
    db.exec("CREATE TABLE t (x TEXT); INSERT INTO t VALUES ('olá');");
    db.close();
    return caminho;
  }

  it("gera .db restaurável, sem sobras temporárias", async () => {
    const dbPath = criarBanco();
    const destino = join(raiz, "_backup");
    const arquivo = await fazerBackup(dbPath, destino, new Date(2026, 9, 9));
    expect(arquivo).toBe(join(destino, "gerenciador_2026-10-09.db"));
    expect(readdirSync(destino)).toEqual(["gerenciador_2026-10-09.db"]);
    const db = new Database(arquivo!, { readonly: true });
    expect(db.prepare("SELECT x FROM t").get()).toEqual({ x: "olá" });
    db.close();
  });

  it("não sobrescreve o backup do mesmo dia e mantém os antigos", async () => {
    const dbPath = criarBanco();
    const destino = join(raiz, "_backup");
    await fazerBackup(dbPath, destino, new Date(2026, 9, 8));
    const hoje = await fazerBackup(dbPath, destino, new Date(2026, 9, 9));
    const repetido = await fazerBackup(dbPath, destino, new Date(2026, 9, 9));
    expect(hoje).not.toBeNull();
    expect(repetido).toBeNull();
    expect(readdirSync(destino).sort()).toEqual(["gerenciador_2026-10-08.db", "gerenciador_2026-10-09.db"]);
  });
});

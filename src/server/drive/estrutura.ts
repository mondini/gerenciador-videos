import { existsSync, mkdirSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { nomePastaVideo } from "../../shared/codigo";
import { resolverDentro } from "./seguranca";

export const SUBPASTAS_CANAL = ["00_IDENTIDADE", "01_BIBLIOTECA", "VIDEOS"] as const;

export const SUBPASTAS_VIDEO = [
  "01_roteiro",
  "02_audio",
  "03_imagens",
  "04_video",
  "05_projeto",
  "06_thumbnail",
  "07_export",
] as const;

export type SubpastaVideo = (typeof SUBPASTAS_VIDEO)[number];

/** Cria (se faltar) a estrutura do canal. Idempotente: nunca mexe no que já existe. */
export function criarEstruturaCanal(driveRoot: string, pastaCanal: string): string {
  const base = resolverDentro(driveRoot, pastaCanal);
  for (const sub of SUBPASTAS_CANAL) mkdirSync(join(base, sub), { recursive: true });
  return base;
}

/** Acha a pasta do vídeo pelo prefixo do código (`BJJ-001-*`, ou `BJJ-001_*` do formato antigo), tolerando renomeações manuais. */
export function acharPastaVideo(driveRoot: string, pastaCanal: string, codigo: string): string | null {
  const videos = resolverDentro(driveRoot, pastaCanal, "VIDEOS");
  if (!existsSync(videos)) return null;
  const achadas = readdirSync(videos, { withFileTypes: true })
    .filter((e) => e.isDirectory() && (e.name === codigo || e.name.startsWith(`${codigo}-`) || e.name.startsWith(`${codigo}_`)))
    .map((e) => e.name);
  if (achadas.length > 1) {
    throw new Error(`Mais de uma pasta para ${codigo}: ${achadas.join(", ")}. Resolva manualmente no Finder.`);
  }
  return achadas[0] ? join(videos, achadas[0]) : null;
}

/** Cria a pasta do vídeo. Se já existir uma pasta com o mesmo código, devolve ela sem alterar nada. */
export function criarPastaVideo(
  driveRoot: string,
  pastaCanal: string,
  codigo: string,
  titulo: string,
): { caminho: string; criada: boolean } {
  const existente = acharPastaVideo(driveRoot, pastaCanal, codigo);
  if (existente) {
    for (const sub of SUBPASTAS_VIDEO) mkdirSync(join(existente, sub), { recursive: true });
    return { caminho: existente, criada: false };
  }
  const caminho = resolverDentro(driveRoot, pastaCanal, "VIDEOS", nomePastaVideo(codigo, titulo));
  for (const sub of SUBPASTAS_VIDEO) mkdirSync(join(caminho, sub), { recursive: true });
  return { caminho, criada: true };
}

export interface StatusSubpasta {
  subpasta: SubpastaVideo;
  arquivos: number;
  /** Arquivos que o Drive guarda só na nuvem (ainda não baixados). */
  soOnline: number;
}

const MARCA_ONLINE = 0; // st_blocks === 0 em arquivo com tamanho > 0 indica placeholder do File Provider

/** Lista só nomes/metadados: não lê o conteúdo, então não força download de arquivos online. */
export function statusSubpastas(pastaVideo: string): StatusSubpasta[] {
  return SUBPASTAS_VIDEO.map((subpasta) => {
    const dir = join(pastaVideo, subpasta);
    if (!existsSync(dir)) return { subpasta, arquivos: 0, soOnline: 0 };
    let arquivos = 0;
    let soOnline = 0;
    for (const e of readdirSync(dir, { withFileTypes: true })) {
      if (!e.isFile() || e.name.startsWith(".")) continue;
      arquivos++;
      const st = statSync(join(dir, e.name));
      if (st.size > 0 && st.blocks === MARCA_ONLINE) soOnline++;
    }
    return { subpasta, arquivos, soOnline };
  });
}

/** Grava um arquivo novo. Falha se já existir: o sistema nunca sobrescreve nada no Drive. */
export function escreverArquivoNovo(caminho: string, conteudo: string | Buffer): void {
  writeFileSync(caminho, conteudo, { flag: "wx" });
}

export function exportarVersaoRoteiro(pastaVideo: string, codigo: string, versao: number, markdown: string): string {
  const caminho = join(pastaVideo, "01_roteiro", `${codigo}_roteiro_v${versao}.md`);
  escreverArquivoNovo(caminho, markdown);
  return caminho;
}

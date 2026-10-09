import { isAbsolute, relative, resolve, sep } from "node:path";

/** Resolve `relativo` dentro de `raiz` e recusa qualquer caminho que escape dela (.., absolutos). */
export function resolverDentro(raiz: string, ...relativo: string[]): string {
  const base = resolve(raiz);
  const alvo = resolve(base, ...relativo);
  const rel = relative(base, alvo);
  if (rel === "") return alvo;
  if (rel.startsWith("..") || isAbsolute(rel) || rel.split(sep).includes("..")) {
    throw new Error(`Caminho fora da raiz do Drive: ${relativo.join("/")}`);
  }
  return alvo;
}

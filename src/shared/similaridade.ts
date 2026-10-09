import { slugify } from "./codigo";

const palavras = (t: string): Set<string> =>
  new Set(slugify(t).split("-").filter((p) => p.length > 2));

/** Parecença 0–1 entre dois títulos (palavras em comum / palavras no total). */
export function similaridade(a: string, b: string): number {
  const A = palavras(a);
  const B = palavras(b);
  if (A.size === 0 || B.size === 0) return 0;
  let comuns = 0;
  for (const p of A) if (B.has(p)) comuns++;
  return comuns / (A.size + B.size - comuns);
}

export function acharParecidos<T extends { tituloProvisorio: string; tituloFinal?: string | null }>(
  titulo: string,
  existentes: T[],
  limite = 0.5,
): T[] {
  return existentes.filter((v) =>
    Math.max(similaridade(titulo, v.tituloProvisorio), v.tituloFinal ? similaridade(titulo, v.tituloFinal) : 0) >= limite,
  );
}

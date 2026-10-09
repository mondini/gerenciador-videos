export function formatarCodigo(prefixo: string, numero: number): string {
  if (!/^[A-Z]{2,5}$/.test(prefixo)) throw new Error(`Prefixo inválido: ${prefixo}`);
  if (!Number.isInteger(numero) || numero < 1) throw new Error(`Número inválido: ${numero}`);
  return `${prefixo}-${String(numero).padStart(3, "0")}`;
}

export function proximoNumero(existentes: number[]): number {
  return existentes.length === 0 ? 1 : Math.max(...existentes) + 1;
}

/** Slug para nome de pasta: sem acentos, minúsculo, hifenizado, limitado a 40 caracteres. */
export function slugify(texto: string): string {
  const slug = texto
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 40)
    .replace(/-+$/g, "");
  return slug || "sem-titulo";
}

export function nomePastaVideo(codigo: string, titulo: string): string {
  return `${codigo}_${slugify(titulo)}`;
}

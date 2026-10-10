import { existsSync, mkdirSync, renameSync, rmSync } from "node:fs";
import { join } from "node:path";
import Database from "better-sqlite3";

const dataLocal = (d: Date): string =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;

/**
 * Cópia consistente do banco em `<destino>/gerenciador_AAAA-MM-DD.db`.
 * Nunca apaga nem sobrescreve backups: se o do dia já existe, não faz nada.
 */
export async function fazerBackup(dbPath: string, destino: string, agora = new Date()): Promise<string | null> {
  mkdirSync(destino, { recursive: true });
  const final = join(destino, `gerenciador_${dataLocal(agora)}.db`);
  if (existsSync(final)) return null;

  const tmpDb = join(destino, `.tmp_${process.pid}_${Date.now()}.db`);
  const db = new Database(dbPath, { readonly: true, fileMustExist: true });
  try {
    await db.backup(tmpDb);
    // renomear para o nome final só depois de completo evita backup pela metade no Drive
    renameSync(tmpDb, final);
  } finally {
    db.close();
    rmSync(tmpDb, { force: true });
  }
  return final;
}

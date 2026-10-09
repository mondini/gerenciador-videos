import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import Database from "better-sqlite3";
import { drizzle, type BetterSQLite3Database } from "drizzle-orm/better-sqlite3";
import { migrate } from "drizzle-orm/better-sqlite3/migrator";
import * as schema from "./schema";

export type Db = BetterSQLite3Database<typeof schema>;

/** Abre o banco (arquivo ou ":memory:"), liga as chaves estrangeiras e aplica as migrações pendentes. */
export function abrirBanco(caminho: string): { db: Db; sqlite: Database.Database } {
  if (caminho !== ":memory:") mkdirSync(dirname(caminho), { recursive: true });
  const sqlite = new Database(caminho);
  sqlite.pragma("journal_mode = WAL");
  sqlite.pragma("foreign_keys = ON");
  const db = drizzle(sqlite, { schema });
  migrate(db, { migrationsFolder: "drizzle" });
  return { db, sqlite };
}

export { schema };

import { existsSync } from "node:fs";
import { join } from "node:path";
import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { createApp } from "./app";
import { abrirBanco } from "./db";
import { fazerBackup } from "./drive/backup";
import { loadConfig, loadDotEnv } from "./config";

loadDotEnv();

let config;
try {
  config = loadConfig();
} catch (erro) {
  console.error(`\n${(erro as Error).message}\n`);
  process.exit(1);
}

const { db } = abrirBanco(config.dbPath);
const app = createApp({ db, driveRoot: config.DRIVE_ROOT });

const backup = () =>
  fazerBackup(config.dbPath, join(config.DRIVE_ROOT, "_backup"))
    .then((arq) => arq && console.log(`Backup salvo: ${arq}`))
    .catch((e) => console.error("Falha no backup:", e));
void backup();
setInterval(backup, 24 * 60 * 60 * 1000).unref();
if (existsSync("dist/web")) {
  app.use("/*", serveStatic({ root: "./dist/web" }));
  app.get("*", serveStatic({ path: "./dist/web/index.html" }));
}

serve({ fetch: app.fetch, port: config.PORT, hostname: "127.0.0.1" }, ({ port }) => {
  console.log(`Gerenciador de Canais em http://localhost:${port}`);
});

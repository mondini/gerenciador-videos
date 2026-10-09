import { existsSync } from "node:fs";
import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { createApp } from "./app";
import { loadConfig, loadDotEnv } from "./config";

loadDotEnv();

let config;
try {
  config = loadConfig();
} catch (erro) {
  console.error(`\n${(erro as Error).message}\n`);
  process.exit(1);
}

const app = createApp();
if (existsSync("dist/web")) {
  app.use("/*", serveStatic({ root: "./dist/web" }));
  app.get("*", serveStatic({ path: "./dist/web/index.html" }));
}

serve({ fetch: app.fetch, port: config.PORT, hostname: "127.0.0.1" }, ({ port }) => {
  console.log(`Gerenciador de Canais em http://localhost:${port}`);
});

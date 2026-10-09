import { Hono } from "hono";
import { ZodError } from "zod";
import { criarRotas } from "./rotas";
import type { Contexto } from "./servicos/contexto";

export function createApp(ctx: Contexto) {
  const app = new Hono();
  app.onError((erro, c) => {
    if (erro instanceof ZodError) {
      return c.json({ erro: erro.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ") }, 400);
    }
    if (erro instanceof Error && /fora da raiz|Mais de uma pasta|não existe|não pertence|inválid/.test(erro.message)) {
      return c.json({ erro: erro.message }, 400);
    }
    console.error(erro);
    return c.json({ erro: "Erro interno do servidor" }, 500);
  });
  app.route("/", criarRotas(ctx));
  return app;
}

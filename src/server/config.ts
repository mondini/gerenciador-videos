import { existsSync, statSync } from "node:fs";
import { z } from "zod";

const envSchema = z.object({
  DRIVE_ROOT: z.string().min(1, "DRIVE_ROOT é obrigatório"),
  PORT: z.coerce.number().int().positive().default(4321),
});

export type Config = z.infer<typeof envSchema> & { dbPath: string };

export function loadConfig(env: NodeJS.ProcessEnv = process.env): Config {
  const parsed = envSchema.safeParse(env);
  if (!parsed.success) {
    const detalhes = parsed.error.issues.map((i) => `- ${i.path.join(".")}: ${i.message}`).join("\n");
    throw new Error(`Configuração inválida no .env (veja .env.example):\n${detalhes}`);
  }
  const { DRIVE_ROOT } = parsed.data;
  if (!existsSync(DRIVE_ROOT) || !statSync(DRIVE_ROOT).isDirectory()) {
    throw new Error(
      `DRIVE_ROOT não existe: ${DRIVE_ROOT}\n` +
        "Confira se o Google Drive for Desktop está aberto e logado, e crie a pasta antes de iniciar.\n" +
        "O sistema não cria a raiz sozinho para não gravar em um lugar errado.",
    );
  }
  return { ...parsed.data, dbPath: "data/gerenciador.db" };
}

export function loadDotEnv(path = ".env"): void {
  if (existsSync(path)) process.loadEnvFile(path);
}

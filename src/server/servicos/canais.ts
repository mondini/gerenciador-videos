import { z } from "zod";
import { criarEstruturaCanal } from "../drive/estrutura";
import { agendaItem, canal, formato, gradePublicacao, modeloChecklist } from "../db/schema";
import { fusoValido } from "../../shared/fuso";
import { AGENDA_PADRAO, CHECKLIST_PADRAO, FORMATOS_PADRAO } from "./padroes";
import type { Contexto } from "./contexto";
import type { Etapa } from "../../shared/etapas";

export const novoCanalSchema = z.object({
  nome: z.string().trim().min(1),
  nicho: z.string().default(""),
  idioma: z.string().default("pt-BR"),
  prefixoCodigo: z.string().regex(/^[A-Z]{2,5}$/, "Use 2 a 5 letras maiúsculas, ex.: BJJ"),
  /** Pasta do canal, relativa ao DRIVE_ROOT. */
  pastaRelativa: z.string().trim().min(1),
  /** Fuso IANA do público, ex.: America/New_York. */
  fusoPublico: z.string().refine(fusoValido, "Fuso desconhecido (use o nome IANA, ex.: America/New_York)").default("America/Sao_Paulo"),
  grade: z.array(z.object({ diaSemana: z.number().int().min(0).max(6), hora: z.string().regex(/^\d{2}:\d{2}$/) })).default([]),
});
export type NovoCanal = z.input<typeof novoCanalSchema>;

/** Cria o canal com formatos e checklists padrão, e a estrutura de pastas no Drive (só cria, nunca altera). */
export function criarCanal(ctx: Contexto, entrada: NovoCanal) {
  const dados = novoCanalSchema.parse(entrada);
  criarEstruturaCanal(ctx.driveRoot, dados.pastaRelativa);
  return ctx.db.transaction((tx) => {
    const { grade, ...resto } = dados;
    const criado = tx.insert(canal).values(resto).returning().get();
    tx.insert(formato).values(FORMATOS_PADRAO.map((nome) => ({ canalId: criado.id, nome }))).run();
    const modelos = (Object.entries(CHECKLIST_PADRAO) as [Etapa, string[]][]).flatMap(([etapa, textos]) =>
      textos.map((texto, i) => ({ canalId: criado.id, etapa, ordem: i + 1, texto })),
    );
    tx.insert(modeloChecklist).values(modelos).run();
    tx.insert(agendaItem).values(AGENDA_PADRAO.map((m, i) => ({ ...m, canalId: criado.id, ordem: i + 1 }))).run();
    if (grade.length) tx.insert(gradePublicacao).values(grade.map((g) => ({ ...g, canalId: criado.id }))).run();
    return criado;
  });
}

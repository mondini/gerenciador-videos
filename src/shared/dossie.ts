export const TIPOS_DOSSIE = ["direitos", "ia", "monetizacao"] as const;
export type TipoDossie = (typeof TIPOS_DOSSIE)[number];

export const RISCOS = ["baixo", "medio", "alto"] as const;
export type Risco = (typeof RISCOS)[number];

export const BASES_DEFESA = ["dominio-publico", "licenca", "citacao-uso-transformativo", "conteudo-proprio", "gerado-por-ia"] as const;
export const MARCACOES = ["nao-avaliado", "obrigatoria", "nao-obrigatoria"] as const;

export const ROTULO_BASE: Record<string, string> = {
  "dominio-publico": "Domínio público",
  licenca: "Licença",
  "citacao-uso-transformativo": "Citação / uso transformativo",
  "conteudo-proprio": "Conteúdo próprio",
  "gerado-por-ia": "Gerado por IA",
};

export const ROTULO_MARCACAO: Record<string, string> = {
  "nao-avaliado": "Não avaliado",
  obrigatoria: "Obrigatória (marcar no Studio)",
  "nao-obrigatoria": "Não obrigatória",
};

interface ItemResumo { tipo: string; risco: string; contestacao: string }

/** Resumo do dossiê para o card e para o checklist: pendências e pior risco. */
export function resumirDossie(itens: ItemResumo[], marcacao: string) {
  const ordem: Record<string, number> = { baixo: 0, medio: 1, alto: 2 };
  const piorRisco = itens.reduce<Risco | null>((p, i) => (p === null || ordem[i.risco]! > ordem[p]! ? (i.risco as Risco) : p), null);
  return {
    total: itens.length,
    piorRisco,
    direitosSemContestacao: itens.filter((i) => i.tipo === "direitos" && !i.contestacao.trim()).length,
    marcacaoPendente: marcacao === "nao-avaliado",
  };
}

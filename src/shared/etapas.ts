export const ETAPAS = [
  "Ideia",
  "Pesquisa",
  "Roteiro",
  "Narração",
  "Imagens",
  "Edição",
  "Thumbnail",
  "Agendado",
  "Publicado",
] as const;

export type Etapa = (typeof ETAPAS)[number];

export const indiceEtapa = (etapa: Etapa): number => ETAPAS.indexOf(etapa);

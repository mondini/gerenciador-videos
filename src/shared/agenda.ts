import { instanteNoFuso, lerHora, partesNoFuso } from "./fuso";

export const TIPOS_AGENDA = ["short", "reserva"] as const;
export type TipoAgenda = (typeof TIPOS_AGENDA)[number];

/** Material do modelo de agenda do canal, relativo ao upload do vídeo longo. */
export interface ItemModeloAgenda {
  rotulo: string;
  /** `short`: corte deste vídeo; `reserva`: short guardado de um vídeo anterior. */
  tipo: TipoAgenda;
  /** Dias de calendário depois do dia do upload (0 = mesmo dia), no fuso do público. */
  diasApos: number;
  /** "HH:MM" no fuso do público. */
  hora: string;
}

export interface MaterialAgendado {
  rotulo: string;
  tipo: "longo" | TipoAgenda;
  quando: Date;
}

/** Agenda de um vídeo: o longo no instante do upload e cada material do modelo no dia e hora do fuso do público. */
export function montarAgenda(upload: Date, fuso: string, modelo: ItemModeloAgenda[]): MaterialAgendado[] {
  const base = partesNoFuso(upload, fuso);
  const materiais: MaterialAgendado[] = modelo.map((m) => ({
    rotulo: m.rotulo,
    tipo: m.tipo,
    quando: instanteNoFuso(base.ano, base.mes, base.dia + m.diasApos, ...lerHora(m.hora), fuso),
  }));
  return [{ rotulo: "Vídeo longo", tipo: "longo" as const, quando: upload }, ...materiais].sort((a, b) => a.quando.getTime() - b.quando.getTime());
}

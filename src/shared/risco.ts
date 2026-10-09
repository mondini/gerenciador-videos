import { ETAPAS, indiceEtapa, type Etapa } from "./etapas";

const DIA_MS = 24 * 60 * 60 * 1000;
export const DIAS_ALERTA = 7;

/** Em risco: faltam menos de 7 dias (ou já passou) e o vídeo ainda não chegou em Edição. */
export function emRisco(etapa: Etapa, dataPlanejada: Date | null, hoje: Date): boolean {
  if (!dataPlanejada) return false;
  if (indiceEtapa(etapa) >= ETAPAS.indexOf("Edição")) return false;
  return (dataPlanejada.getTime() - hoje.getTime()) / DIA_MS < DIAS_ALERTA;
}

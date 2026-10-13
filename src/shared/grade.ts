import { instanteNoFuso, lerHora, partesNoFuso } from "./fuso";

export interface Horario {
  /** 0 = domingo … 6 = sábado */
  diaSemana: number;
  /** "HH:MM", 24h, no fuso do público do canal */
  hora: string;
}

const minuto = (d: Date): number => Math.floor(d.getTime() / 60_000);

/** Próximo horário da grade (no fuso do público), depois de `agora`, que ainda não está ocupado. Procura até 1 ano à frente. */
export function proximoHorarioLivre(grade: Horario[], ocupados: Date[], agora: Date, fuso: string): Date | null {
  if (grade.length === 0) return null;
  const usados = new Set(ocupados.map(minuto));
  const hoje = partesNoFuso(agora, fuso);
  for (let dia = 0; dia <= 365; dia++) {
    const diaSemana = new Date(Date.UTC(hoje.ano, hoje.mes - 1, hoje.dia + dia)).getUTCDay();
    const doDia = grade
      .filter((h) => h.diaSemana === diaSemana)
      .map((h) => instanteNoFuso(hoje.ano, hoje.mes, hoje.dia + dia, ...lerHora(h.hora), fuso))
      .sort((a, b) => a.getTime() - b.getTime());
    for (const candidato of doDia) {
      if (candidato > agora && !usados.has(minuto(candidato))) return candidato;
    }
  }
  return null;
}

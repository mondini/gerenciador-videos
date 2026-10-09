export interface Horario {
  /** 0 = domingo … 6 = sábado */
  diaSemana: number;
  /** "HH:MM", 24h */
  hora: string;
}

const chave = (d: Date): string =>
  `${d.getFullYear()}-${d.getMonth()}-${d.getDate()} ${d.getHours()}:${d.getMinutes()}`;

/** Próximo horário da grade, depois de `agora`, que ainda não está ocupado. Procura até 1 ano à frente. */
export function proximoHorarioLivre(grade: Horario[], ocupados: Date[], agora: Date): Date | null {
  if (grade.length === 0) return null;
  const usados = new Set(ocupados.map(chave));
  for (let dia = 0; dia <= 365; dia++) {
    const base = new Date(agora.getFullYear(), agora.getMonth(), agora.getDate() + dia);
    const doDia = grade
      .filter((h) => h.diaSemana === base.getDay())
      .map((h) => {
        const [hh, mm] = h.hora.split(":").map(Number) as [number, number];
        return new Date(base.getFullYear(), base.getMonth(), base.getDate(), hh, mm);
      })
      .sort((a, b) => a.getTime() - b.getTime());
    for (const candidato of doDia) {
      if (candidato > agora && !usados.has(chave(candidato))) return candidato;
    }
  }
  return null;
}

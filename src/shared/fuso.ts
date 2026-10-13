/** Datas em um fuso IANA (ex.: "America/New_York"), com o horário de verão resolvido pelo Intl. */

export interface Partes {
  ano: number;
  /** 1–12 */
  mes: number;
  dia: number;
  hora: number;
  minuto: number;
  /** 0 = domingo … 6 = sábado */
  diaSemana: number;
}

const formatadores = new Map<string, Intl.DateTimeFormat>();
function formatador(fuso: string): Intl.DateTimeFormat {
  let f = formatadores.get(fuso);
  if (!f) {
    f = new Intl.DateTimeFormat("en-US", {
      timeZone: fuso, hourCycle: "h23", year: "numeric", month: "numeric", day: "numeric", hour: "numeric", minute: "numeric",
    });
    formatadores.set(fuso, f);
  }
  return f;
}

export function fusoValido(fuso: string): boolean {
  try {
    formatador(fuso);
    return true;
  } catch {
    return false;
  }
}

/** Data e hora de parede de um instante no fuso. */
export function partesNoFuso(instante: Date, fuso: string): Partes {
  const p = Object.fromEntries(formatador(fuso).formatToParts(instante).map((x) => [x.type, Number(x.value)]));
  const ano = p.year!, mes = p.month!, dia = p.day!;
  return { ano, mes, dia, hora: p.hour!, minuto: p.minute!, diaSemana: new Date(Date.UTC(ano, mes - 1, dia)).getUTCDay() };
}

/** Diferença (ms) entre a hora de parede do fuso e o UTC naquele instante. */
function deslocamento(instante: Date, fuso: string): number {
  const p = partesNoFuso(instante, fuso);
  return Date.UTC(p.ano, p.mes - 1, p.dia, p.hora, p.minuto) - Math.floor(instante.getTime() / 60_000) * 60_000;
}

/** Instante correspondente a uma data e hora de parede no fuso. Dias além do fim do mês são normalizados (dia 32 = dia 1 do mês seguinte). */
export function instanteNoFuso(ano: number, mes: number, dia: number, hora: number, minuto: number, fuso: string): Date {
  const parede = Date.UTC(ano, mes - 1, dia, hora, minuto);
  const primeiro = parede - deslocamento(new Date(parede), fuso);
  // segunda passada: corrige quando o palpite caiu do outro lado de uma troca de horário de verão
  return new Date(parede - deslocamento(new Date(primeiro), fuso));
}

/** "HH:MM" → [hora, minuto] */
export const lerHora = (hora: string): [number, number] => hora.split(":").map(Number) as [number, number];

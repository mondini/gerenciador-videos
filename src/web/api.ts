import { hc } from "hono/client";
import type { AppType } from "../server/rotas";

export const api = hc<AppType>("/");

/** Lê o JSON de uma resposta e lança Error com a mensagem do servidor quando não for 2xx. */
export async function ler<T>(promessa: Promise<{ ok: boolean; json(): Promise<unknown> }>): Promise<T> {
  const res = await promessa;
  const corpo = (await res.json()) as T & { erro?: string };
  if (!res.ok) throw new Error(corpo.erro ?? "Erro inesperado");
  return corpo;
}

export const NOMES_DIAS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

export const fmtData = (iso: string | null | undefined): string =>
  iso ? new Date(iso).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "—";

/** ISO → valor de <input type="datetime-local"> no fuso local. */
export const paraInputData = (iso: string | null | undefined): string => {
  if (!iso) return "";
  const d = new Date(iso);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
};

/** Fusos oferecidos no cadastro do canal (o público principal). */
export const FUSOS = [
  { id: "America/New_York", nome: "Nova York", detalhe: "EUA, leste" },
  { id: "America/Chicago", nome: "Chicago", detalhe: "EUA, centro" },
  { id: "America/Los_Angeles", nome: "Los Angeles", detalhe: "EUA, oeste" },
  { id: "Europe/London", nome: "Londres", detalhe: "Reino Unido" },
  { id: "America/Sao_Paulo", nome: "Brasília", detalhe: "Brasil" },
  { id: "Europe/Lisbon", nome: "Lisboa", detalhe: "Portugal" },
];

/** "America/New_York" → "Nova York"; fuso fora da lista → nome da cidade do IANA. */
export const nomeFuso = (fuso: string): string =>
  FUSOS.find((x) => x.id === fuso)?.nome ?? (fuso.split("/").pop() ?? fuso).replace(/_/g, " ");

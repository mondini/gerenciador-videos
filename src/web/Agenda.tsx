import { useEffect, useState } from "react";
import { instanteNoFuso, lerHora, partesNoFuso } from "../shared/fuso";
import { api, ler, nomeFuso } from "./api";
import { botao, campo, Rotulo } from "./ui";

type Material = { rotulo: string; tipo: "longo" | "short" | "reserva"; quando: string };
type Agenda = { fusoPublico: string; dataPlanejada: string | null; materiais: Material[] };

const FUSO_LOCAL = Intl.DateTimeFormat().resolvedOptions().timeZone;
const p2 = (n: number) => String(n).padStart(2, "0");

const dia = (iso: string, fuso: string) =>
  new Date(iso).toLocaleDateString("pt-BR", { timeZone: fuso, weekday: "short", day: "2-digit", month: "2-digit", year: "numeric" });
const hora = (iso: string, fuso: string) => new Date(iso).toLocaleTimeString("pt-BR", { timeZone: fuso, hour: "2-digit", minute: "2-digit" });
/** Diferença em minutos entre o fuso do público e o local naquele instante (muda quando um dos dois troca de horário de verão). */
const diferenca = (iso: string, fuso: string) => {
  const a = partesNoFuso(new Date(iso), fuso), b = partesNoFuso(new Date(iso), FUSO_LOCAL);
  return (Date.UTC(a.ano, a.mes - 1, a.dia, a.hora, a.minuto) - Date.UTC(b.ano, b.mes - 1, b.dia, b.hora, b.minuto)) / 60_000;
};

/** Agenda de publicação do vídeo: a data de upload (= data planejada) e o que programar no YouTube Studio para cada material. */
export function AgendaAba({ videoId, codigo, titulo, dataPlanejada, onSalvo, onAviso }: {
  videoId: number; codigo: string; titulo: string; dataPlanejada: string | null; onSalvo: () => void; onAviso: (m: string, erro?: boolean) => void;
}) {
  const [agenda, setAgenda] = useState<Agenda | null>(null);
  const [f, setF] = useState({ data: "", hora: "" });

  useEffect(() => {
    ler<Agenda>(api.api.videos[":id"].agenda.$get({ param: { id: String(videoId) } })).then((a) => {
      setAgenda(a);
      if (a.dataPlanejada) {
        const p = partesNoFuso(new Date(a.dataPlanejada), a.fusoPublico);
        setF({ data: `${p.ano}-${p2(p.mes)}-${p2(p.dia)}`, hora: `${p2(p.hora)}:${p2(p.minuto)}` });
      }
    }, (e) => onAviso(e.message, true));
  }, [videoId, dataPlanejada]);
  if (!agenda) return <p>Carregando…</p>;

  const fuso = agenda.fusoPublico;
  const doisFusos = fuso !== FUSO_LOCAL;
  const sujo = (() => {
    if (!f.data || !f.hora) return false;
    if (!agenda.dataPlanejada) return true;
    const p = partesNoFuso(new Date(agenda.dataPlanejada), fuso);
    return f.data !== `${p.ano}-${p2(p.mes)}-${p2(p.dia)}` || f.hora !== `${p2(p.hora)}:${p2(p.minuto)}`;
  })();
  const mudaHorarioVerao = doisFusos && new Set(agenda.materiais.map((m) => diferenca(m.quando, fuso))).size > 1;

  async function salvar() {
    const [ano, mes, d] = f.data.split("-").map(Number) as [number, number, number];
    try {
      await ler(api.api.videos[":id"].$patch({ param: { id: String(videoId) }, json: { dataPlanejada: instanteNoFuso(ano, mes, d, ...lerHora(f.hora), fuso).toISOString() } }));
      onAviso("Data de upload salva.");
      onSalvo();
    } catch (e) { onAviso((e as Error).message, true); }
  }

  const configurar = (m: Material) => {
    const programar = `Visibilidade → Programar: ${dia(m.quando, FUSO_LOCAL)} às ${hora(m.quando, FUSO_LOCAL)}${doisFusos ? ` (${nomeFuso(FUSO_LOCAL)})` : ""}.`;
    if (m.tipo === "longo") return <>Envie o vídeo longo. {programar}</>;
    if (m.tipo === "short") return <>{programar} Vídeo relacionado → <b>{codigo} · {titulo}</b>.</>;
    return <>{programar} Vídeo relacionado → o vídeo longo de onde saiu este short.</>;
  };

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-end gap-3">
        <Rotulo texto={`Data de upload desejada (${nomeFuso(fuso)})`}><input type="date" className={campo} value={f.data} onChange={(e) => setF({ ...f, data: e.target.value })} /></Rotulo>
        <Rotulo texto="Hora"><input type="time" className={campo} value={f.hora} onChange={(e) => setF({ ...f, hora: e.target.value })} /></Rotulo>
        <button className={botao} disabled={!sujo} onClick={salvar}>Salvar data</button>
      </div>
      <p className="mb-4 text-xs text-slate-500">
        É a mesma data planejada da aba Básico. Os materiais seguem o modelo de agenda do canal (Configurações → Agenda), no fuso do público ({nomeFuso(fuso)}).
      </p>

      {agenda.materiais.length === 0 ? (
        <p className="text-sm text-slate-600">Escolha a data de upload para ver a agenda.</p>
      ) : (
        <>
          {mudaHorarioVerao && (
            <p className="mb-3 rounded border border-amber-200 bg-amber-50 px-3 py-2 text-sm">
              ⚠️ O horário de verão muda durante esta agenda: a diferença entre {nomeFuso(fuso)} e {nomeFuso(FUSO_LOCAL)} não é a mesma em todos os itens. As horas abaixo já estão ajustadas.
            </p>
          )}
          {doisFusos && <p className="mb-3 text-sm text-slate-600">No Studio, confira o fuso mostrado ao lado da hora ao programar e use a coluna desse fuso.</p>}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-200 text-xs uppercase text-slate-500">
                <tr>
                  <th className="py-2 pr-3">Material</th>
                  <th className="py-2 pr-3">{doisFusos ? nomeFuso(fuso) : "Data e hora"}</th>
                  {doisFusos && <th className="py-2 pr-3">{nomeFuso(FUSO_LOCAL)} (seu horário)</th>}
                  <th className="py-2">O que configurar no Studio</th>
                </tr>
              </thead>
              <tbody>
                {agenda.materiais.map((m) => (
                  <tr key={`${m.rotulo}-${m.quando}`} className={`border-b border-slate-100 align-top ${m.tipo === "longo" ? "bg-slate-50 font-medium" : ""}`}>
                    <td className="py-2 pr-3">{m.tipo === "longo" ? "🎬" : "📱"} {m.rotulo}</td>
                    <td className="whitespace-nowrap py-2 pr-3">{dia(m.quando, fuso)}<br /><b>{hora(m.quando, fuso)}</b></td>
                    {doisFusos && <td className="whitespace-nowrap py-2 pr-3">{dia(m.quando, FUSO_LOCAL)}<br /><b>{hora(m.quando, FUSO_LOCAL)}</b></td>}
                    <td className="py-2 font-normal">{configurar(m)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

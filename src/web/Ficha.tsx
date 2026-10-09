import { useCallback, useEffect, useState } from "react";
import { api, fmtData, ler, paraInputData } from "./api";
import { botao, botaoClaro, campo, Modal, Rotulo } from "./ui";

type Video = {
  id: number; codigo: string; canalId: number; etapa: string; tituloProvisorio: string; tituloFinal: string | null;
  formatoId: number | null; dataPlanejada: string | null; notaApelo: number | null; notaIlustracao: number | null; notaPesquisa: number | null;
  gancho: string; resumo: string; roteiroAtual: string; pastaRelativa: string | null;
};
type Item = { id: number; etapa: string; texto: string; feito: boolean };
type Versao = { id: number; numero: number; origem: string; nota: string | null; criadoEm: string; arquivoExportado: string | null };
type Ficha = { video: Video; checklist: Item[]; versoes: Versao[] };
type Arquivos = { pasta: string | null; subpastas: { subpasta: string; arquivos: number; soOnline: number }[] };

const ABAS = ["Básico", "Roteiro", "Checklist", "Arquivos"] as const;
const PALAVRAS_POR_MIN = 150;

export function FichaVideo({ videoId, onFechar, onAlterado, onAviso }: { videoId: number; onFechar: () => void; onAlterado: () => void; onAviso: (m: string, erro?: boolean) => void }) {
  const [ficha, setFicha] = useState<Ficha | null>(null);
  const [aba, setAba] = useState<(typeof ABAS)[number]>("Básico");
  const [formatos, setFormatos] = useState<{ id: number; nome: string }[]>([]);

  const carregar = useCallback(async () => {
    try {
      const f = await ler<Ficha>(api.api.videos[":id"].$get({ param: { id: String(videoId) } }));
      setFicha(f);
      setFormatos(await ler(api.api.canais[":id"].formatos.$get({ param: { id: String(f.video.canalId) } })));
    } catch (e) {
      onAviso((e as Error).message, true);
    }
  }, [videoId]);
  useEffect(() => { void carregar(); }, [carregar]);

  if (!ficha) return <Modal titulo="Carregando…" onFechar={onFechar} largo><p>Carregando…</p></Modal>;
  const v = ficha.video;

  return (
    <Modal titulo={`${v.codigo} · ${v.tituloFinal ?? v.tituloProvisorio}`} onFechar={onFechar} largo>
      <div className="mb-4 flex gap-1 border-b border-slate-200">
        {ABAS.map((a) => (
          <button key={a} onClick={() => setAba(a)} className={`-mb-px border-b-2 px-3 py-1.5 text-sm font-medium ${aba === a ? "border-slate-900 text-slate-900" : "border-transparent text-slate-500 hover:text-slate-800"}`}>
            {a}
          </button>
        ))}
        <span className="ml-auto self-center rounded bg-slate-100 px-2 py-0.5 text-xs">Etapa: {v.etapa}</span>
      </div>
      {aba === "Básico" && <Basico v={v} formatos={formatos} onSalvo={() => { void carregar(); onAlterado(); }} onAviso={onAviso} />}
      {aba === "Roteiro" && <Roteiro v={v} versoes={ficha.versoes} onSalvo={() => { void carregar(); onAlterado(); }} onAviso={onAviso} />}
      {aba === "Checklist" && <Checklist itens={ficha.checklist} etapaAtual={v.etapa} onMudou={() => { void carregar(); onAlterado(); }} onAviso={onAviso} />}
      {aba === "Arquivos" && <ArquivosAba videoId={v.id} etapa={v.etapa} onAviso={onAviso} />}
    </Modal>
  );
}

function Basico({ v, formatos, onSalvo, onAviso }: { v: Video; formatos: { id: number; nome: string }[]; onSalvo: () => void; onAviso: (m: string, erro?: boolean) => void }) {
  const [f, setF] = useState({
    tituloProvisorio: v.tituloProvisorio, tituloFinal: v.tituloFinal ?? "", formatoId: v.formatoId ?? "",
    dataPlanejada: paraInputData(v.dataPlanejada), notaApelo: v.notaApelo ?? "", notaIlustracao: v.notaIlustracao ?? "", notaPesquisa: v.notaPesquisa ?? "",
    gancho: v.gancho, resumo: v.resumo,
  });
  const n = (x: number | "") => (x === "" ? null : x);

  async function salvar() {
    try {
      await ler(api.api.videos[":id"].$patch({
        param: { id: String(v.id) },
        json: {
          tituloProvisorio: f.tituloProvisorio, tituloFinal: f.tituloFinal.trim() || null, formatoId: n(f.formatoId as number | ""),
          dataPlanejada: f.dataPlanejada ? new Date(f.dataPlanejada).toISOString() : null,
          notaApelo: n(f.notaApelo as number | ""), notaIlustracao: n(f.notaIlustracao as number | ""), notaPesquisa: n(f.notaPesquisa as number | ""),
          gancho: f.gancho, resumo: f.resumo,
        },
      }));
      onAviso("Salvo.");
      onSalvo();
    } catch (e) {
      onAviso((e as Error).message, true);
    }
  }

  const sel = (chave: "notaApelo" | "notaIlustracao" | "notaPesquisa", rotulo: string) => (
    <Rotulo texto={rotulo}>
      <select className={campo} value={f[chave]} onChange={(e) => setF({ ...f, [chave]: e.target.value ? Number(e.target.value) : "" })}>
        <option value="">—</option>
        {[1, 2, 3, 4, 5].map((x) => <option key={x}>{x}</option>)}
      </select>
    </Rotulo>
  );

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <Rotulo texto="Título provisório"><input className={campo} value={f.tituloProvisorio} onChange={(e) => setF({ ...f, tituloProvisorio: e.target.value })} /></Rotulo>
      <Rotulo texto={`Título final (${f.tituloFinal.length}/100)`}><input className={campo} maxLength={100} value={f.tituloFinal} onChange={(e) => setF({ ...f, tituloFinal: e.target.value })} /></Rotulo>
      <Rotulo texto="Formato">
        <select className={campo} value={f.formatoId} onChange={(e) => setF({ ...f, formatoId: e.target.value ? Number(e.target.value) : "" })}>
          <option value="">A definir</option>
          {formatos.map((o) => <option key={o.id} value={o.id}>{o.nome}</option>)}
        </select>
      </Rotulo>
      <Rotulo texto="Data planejada de publicação"><input type="datetime-local" className={campo} value={f.dataPlanejada} onChange={(e) => setF({ ...f, dataPlanejada: e.target.value })} /></Rotulo>
      <div className="grid grid-cols-3 gap-3 sm:col-span-2">{sel("notaApelo", "Apelo (1–5)")}{sel("notaIlustracao", "Ilustrar (1–5)")}{sel("notaPesquisa", "Pesquisa (1–5)")}</div>
      <div className="sm:col-span-2"><Rotulo texto="Gancho dos primeiros 15s"><textarea className={`${campo} h-20`} value={f.gancho} onChange={(e) => setF({ ...f, gancho: e.target.value })} /></Rotulo></div>
      <div className="sm:col-span-2"><Rotulo texto="Resumo"><textarea className={`${campo} h-20`} value={f.resumo} onChange={(e) => setF({ ...f, resumo: e.target.value })} /></Rotulo></div>
      <div className="sm:col-span-2"><button className={botao} onClick={salvar}>Salvar</button></div>
    </div>
  );
}

function Roteiro({ v, versoes, onSalvo, onAviso }: { v: Video; versoes: Versao[]; onSalvo: () => void; onAviso: (m: string, erro?: boolean) => void }) {
  const [texto, setTexto] = useState(v.roteiroAtual);
  const palavras = texto.trim() ? texto.trim().split(/\s+/).length : 0;
  const minutos = palavras / PALAVRAS_POR_MIN;
  const sujo = texto !== v.roteiroAtual;

  async function salvarTexto() {
    try {
      await ler(api.api.videos[":id"].$patch({ param: { id: String(v.id) }, json: { roteiroAtual: texto } }));
      onAviso("Roteiro salvo.");
      onSalvo();
    } catch (e) { onAviso((e as Error).message, true); }
  }
  async function salvarVersao() {
    try {
      if (sujo) await salvarTexto();
      const r = await ler<Versao>(api.api.videos[":id"].roteiro.versao.$post({ param: { id: String(v.id) }, json: {} }));
      onAviso(`Versão v${r.numero} salva${r.arquivoExportado ? " e exportada para o Drive" : " (a pasta do vídeo ainda não existe, então não foi exportada)"}.`);
      onSalvo();
    } catch (e) { onAviso((e as Error).message, true); }
  }

  return (
    <div className="grid gap-4 lg:grid-cols-[1fr_16rem]">
      <div>
        <textarea className={`${campo} h-96 font-mono leading-relaxed`} value={texto} onChange={(e) => setTexto(e.target.value)} placeholder="Escreva o roteiro em Markdown…" />
        <div className="mt-2 flex flex-wrap items-center gap-2">
          <button className={botao} onClick={salvarTexto} disabled={!sujo}>Salvar roteiro</button>
          <button className={botaoClaro} onClick={salvarVersao}>Salvar versão</button>
          <span className="ml-auto text-sm text-slate-500">{palavras} palavras · ~{minutos.toFixed(1)} min {minutos > 0 && (minutos < 8 || minutos > 10) ? "(meta: 8–10 min)" : ""}</span>
        </div>
      </div>
      <aside>
        <h3 className="mb-2 text-sm font-semibold">Versões</h3>
        {versoes.length === 0 && <p className="text-sm text-slate-500">Nenhuma ainda. Uma versão é criada automaticamente ao sair da etapa Roteiro.</p>}
        <ul className="space-y-2 text-sm">
          {versoes.map((x) => (
            <li key={x.id} className="rounded border border-slate-200 p-2">
              <div className="font-medium">v{x.numero} <span className="font-normal text-slate-500">({x.origem === "manual" ? "manual" : "automática"})</span></div>
              <div className="text-xs text-slate-500">{fmtData(x.criadoEm)}</div>
              {x.nota && <div className="text-xs">{x.nota}</div>}
              <div className="text-xs">{x.arquivoExportado ? "📄 no Drive" : "sem arquivo no Drive"}</div>
            </li>
          ))}
        </ul>
      </aside>
    </div>
  );
}

function Checklist({ itens, etapaAtual, onMudou, onAviso }: { itens: Item[]; etapaAtual: string; onMudou: () => void; onAviso: (m: string, erro?: boolean) => void }) {
  const etapas = [...new Set(itens.map((i) => i.etapa))];
  async function alternar(i: Item) {
    try {
      await ler(api.api.checklist[":id"].$patch({ param: { id: String(i.id) }, json: { feito: !i.feito } }));
      onMudou();
    } catch (e) { onAviso((e as Error).message, true); }
  }
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {etapas.map((etapa) => {
        const lista = itens.filter((i) => i.etapa === etapa);
        const feitos = lista.filter((i) => i.feito).length;
        return (
          <section key={etapa} className={`rounded-lg border p-3 ${etapa === etapaAtual ? "border-slate-900" : "border-slate-200"}`}>
            <h3 className="mb-2 flex justify-between text-sm font-semibold">{etapa}{etapa === etapaAtual && " (atual)"}<span className="font-normal text-slate-500">{feitos}/{lista.length}</span></h3>
            <ul className="space-y-1">
              {lista.map((i) => (
                <li key={i.id}>
                  <label className="flex items-start gap-2 text-sm">
                    <input type="checkbox" className="mt-0.5" checked={i.feito} onChange={() => alternar(i)} />
                    <span className={i.feito ? "text-slate-400 line-through" : ""}>{i.texto}</span>
                  </label>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </div>
  );
}

function ArquivosAba({ videoId, etapa, onAviso }: { videoId: number; etapa: string; onAviso: (m: string, erro?: boolean) => void }) {
  const [dados, setDados] = useState<Arquivos | null>(null);
  useEffect(() => {
    ler<Arquivos>(api.api.videos[":id"].arquivos.$get({ param: { id: String(videoId) } })).then(setDados, (e) => onAviso(e.message, true));
  }, [videoId, etapa]);
  if (!dados) return <p>Carregando…</p>;
  if (!dados.pasta) return <p className="text-sm text-slate-600">A pasta no Drive é criada automaticamente quando o vídeo sai de <b>Ideia</b> para <b>Pesquisa</b>.</p>;
  return (
    <div>
      <p className="mb-3 break-all text-sm text-slate-600">Pasta: <code>{dados.pasta}</code></p>
      <ul className="grid gap-2 sm:grid-cols-2">
        {dados.subpastas.map((s) => (
          <li key={s.subpasta} className="flex items-center justify-between rounded border border-slate-200 px-3 py-2 text-sm">
            <span className="font-mono">{s.subpasta}</span>
            <span>{s.arquivos > 0 ? `✅ ${s.arquivos}` : "❌ vazia"}{s.soOnline > 0 && ` · ☁️ ${s.soOnline} só online`}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

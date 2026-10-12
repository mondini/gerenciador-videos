import { useEffect, useState } from "react";
import { BASES_DEFESA, MARCACOES, RISCOS, ROTULO_BASE, ROTULO_MARCACAO, type TipoDossie } from "../shared/dossie";
import { api, ler } from "./api";
import { botao, botaoClaro, campo, Rotulo } from "./ui";

type Item = {
  tipo: TipoDossie; elemento: string; categoria: string; origem: string; link: string; base: string;
  descricao: string; contestacao: string; provas: string; risco: string; mitigacao: string;
};
type Dossie = { marcacaoSintetico: string; justificativaSintetico: string; itens: Item[] };

const vazio = (tipo: TipoDossie): Item => ({ tipo, elemento: "", categoria: "", origem: "", link: "", base: "", descricao: "", contestacao: "", provas: "", risco: "baixo", mitigacao: "" });

const SECOES: { tipo: TipoDossie; titulo: string; ajuda: string }[] = [
  { tipo: "direitos", titulo: "Elementos de terceiros e defesa contra claim", ajuda: "Música, SFX, imagem de acervo, fonte tipográfica, citação bíblica ou estoica, clipe. Um item por elemento." },
  { tipo: "ia", titulo: "Uso de IA", ajuda: "Voz, imagens, roteiro, música, thumbnail: o que foi gerado por IA e com qual ferramenta." },
  { tipo: "monetizacao", titulo: "Riscos de monetização", ajuda: "Conteúdo reaproveitado ou inautêntico, aviso financeiro, tema sensível e como mitigar." },
];

export function DossieAba({ videoId, onAviso, onSalvo }: { videoId: number; onAviso: (m: string, erro?: boolean) => void; onSalvo: () => void }) {
  const [d, setD] = useState<Dossie | null>(null);
  const [colar, setColar] = useState("");
  const [sujo, setSujo] = useState(false);

  useEffect(() => {
    ler<Dossie>(api.api.videos[":id"].dossie.$get({ param: { id: String(videoId) } })).then(setD, (e) => onAviso(e.message, true));
  }, [videoId]);
  if (!d) return <p>Carregando…</p>;

  const mudar = (novo: Dossie) => { setD(novo); setSujo(true); };
  const atualizar = (i: number, parcial: Partial<Item>) => mudar({ ...d, itens: d.itens.map((x, j) => (j === i ? { ...x, ...parcial } : x)) });

  async function enviar(dados: Dossie) {
    try {
      const salvo = await ler<Dossie>(api.api.videos[":id"].dossie.$put({ param: { id: String(videoId) }, json: dados as never }));
      setD(salvo);
      setSujo(false);
      onAviso("Dossiê salvo.");
      onSalvo();
      return true;
    } catch (e) {
      onAviso((e as Error).message, true);
      return false;
    }
  }

  async function importar() {
    let cru: unknown;
    try {
      cru = JSON.parse(colar.replace(/^```(?:json)?\s*|\s*```$/g, "").trim());
    } catch {
      return onAviso("O texto colado não é um JSON válido.", true);
    }
    if (d!.itens.length && !confirm("Isto substitui TODO o dossiê atual deste vídeo. Continuar?")) return;
    if (await enviar(cru as Dossie)) setColar("");
  }

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 p-3">
        <h3 className="mb-2 text-sm font-semibold">Conteúdo alterado ou sintético (YouTube)</h3>
        <div className="grid gap-3 sm:grid-cols-[16rem_1fr]">
          <Rotulo texto="Marcação no Studio">
            <select className={campo} value={d.marcacaoSintetico} onChange={(e) => mudar({ ...d, marcacaoSintetico: e.target.value })}>
              {MARCACOES.map((m) => <option key={m} value={m}>{ROTULO_MARCACAO[m]}</option>)}
            </select>
          </Rotulo>
          <Rotulo texto="Justificativa">
            <input className={campo} value={d.justificativaSintetico} onChange={(e) => mudar({ ...d, justificativaSintetico: e.target.value })} />
          </Rotulo>
        </div>
      </section>

      {SECOES.map((s) => (
        <section key={s.tipo}>
          <div className="mb-1 flex items-center justify-between">
            <h3 className="text-sm font-semibold">{s.titulo}</h3>
            <button className={botaoClaro} onClick={() => mudar({ ...d, itens: [...d.itens, vazio(s.tipo)] })}>+ Item</button>
          </div>
          <p className="mb-2 text-xs text-slate-500">{s.ajuda}</p>
          <div className="space-y-3">
            {d.itens.map((it, i) => it.tipo !== s.tipo ? null : (
              <div key={i} className="grid gap-2 rounded-lg border border-slate-200 p-3 sm:grid-cols-3">
                <Rotulo texto={s.tipo === "monetizacao" ? "Ponto de risco" : "Elemento"}><input className={campo} value={it.elemento} onChange={(e) => atualizar(i, { elemento: e.target.value })} /></Rotulo>
                {s.tipo !== "monetizacao" && <Rotulo texto="Categoria"><input className={campo} value={it.categoria} onChange={(e) => atualizar(i, { categoria: e.target.value })} /></Rotulo>}
                {s.tipo === "direitos" && (
                  <Rotulo texto="Base">
                    <select className={campo} value={it.base} onChange={(e) => atualizar(i, { base: e.target.value })}>
                      <option value="">—</option>
                      {BASES_DEFESA.map((b) => <option key={b} value={b}>{ROTULO_BASE[b]}</option>)}
                    </select>
                  </Rotulo>
                )}
                {s.tipo !== "monetizacao" && <Rotulo texto={s.tipo === "ia" ? "Ferramenta" : "Origem"}><input className={campo} value={it.origem} onChange={(e) => atualizar(i, { origem: e.target.value })} /></Rotulo>}
                {s.tipo === "direitos" && <Rotulo texto="Link da licença/fonte"><input className={campo} value={it.link} onChange={(e) => atualizar(i, { link: e.target.value })} /></Rotulo>}
                {s.tipo !== "ia" && (
                  <Rotulo texto="Risco">
                    <select className={campo} value={it.risco} onChange={(e) => atualizar(i, { risco: e.target.value })}>
                      {RISCOS.map((r) => <option key={r}>{r}</option>)}
                    </select>
                  </Rotulo>
                )}
                <div className="sm:col-span-3"><Rotulo texto={s.tipo === "direitos" ? "Detalhes (edição, tradução, licença, validade)" : "Descrição"}><textarea className={`${campo} h-14`} value={it.descricao} onChange={(e) => atualizar(i, { descricao: e.target.value })} /></Rotulo></div>
                {s.tipo === "direitos" && (
                  <>
                    <div className="sm:col-span-2"><Rotulo texto="Texto de contestação (pronto para colar no Studio)"><textarea className={`${campo} h-20`} value={it.contestacao} onChange={(e) => atualizar(i, { contestacao: e.target.value })} /></Rotulo></div>
                    <Rotulo texto="Provas a anexar"><textarea className={`${campo} h-20`} value={it.provas} onChange={(e) => atualizar(i, { provas: e.target.value })} /></Rotulo>
                  </>
                )}
                {s.tipo === "monetizacao" && <div className="sm:col-span-3"><Rotulo texto="Mitigação"><textarea className={`${campo} h-14`} value={it.mitigacao} onChange={(e) => atualizar(i, { mitigacao: e.target.value })} /></Rotulo></div>}
                <div className="sm:col-span-3 text-right">
                  <button className="text-xs text-red-600 hover:underline" onClick={() => mudar({ ...d, itens: d.itens.filter((_, j) => j !== i) })}>Remover item</button>
                </div>
              </div>
            ))}
            {d.itens.every((x) => x.tipo !== s.tipo) && <p className="text-sm text-slate-400">Nenhum item.</p>}
          </div>
        </section>
      ))}

      <div className="flex items-center gap-3">
        <button className={botao} onClick={() => void enviar(d)} disabled={!sujo}>Salvar dossiê</button>
        {sujo && <span className="text-xs text-amber-700">Alterações não salvas</span>}
      </div>

      <details className="rounded-lg border border-dashed border-slate-300 p-3">
        <summary className="cursor-pointer text-sm font-medium">Colar JSON da sessão de produção</summary>
        <p className="my-2 text-xs text-slate-500">Cole o bloco JSON do "pacote de publicação". Ele substitui o dossiê inteiro deste vídeo.</p>
        <textarea className={`${campo} h-40 font-mono text-xs`} value={colar} onChange={(e) => setColar(e.target.value)} placeholder='{ "marcacaoSintetico": "obrigatoria", "itens": [ … ] }' />
        <button className={`${botaoClaro} mt-2`} onClick={importar} disabled={!colar.trim()}>Importar</button>
      </details>
    </div>
  );
}

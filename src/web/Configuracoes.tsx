import { useCallback, useEffect, useState } from "react";
import { ETAPAS } from "../shared/etapas";
import { api, ler, NOMES_DIAS } from "./api";
import { botao, botaoClaro, campo, Modal, Rotulo } from "./ui";

type Aviso = (m: string, erro?: boolean) => void;
type Canal = {
  id: number; nome: string; nicho: string; prefixoCodigo: string; pastaRelativa: string; urlYoutube: string | null;
  referenciasIdentidade: string; modeloDescricao: string; tagsPadrao: string[]; vozPadrao: string; estiloImagemPadrao: string;
};
type Config = {
  canal: Canal;
  grade: { id: number; diaSemana: number; hora: string }[];
  formatos: { id: number; nome: string; ativo: boolean }[];
  series: { id: number; nome: string; descricao: string }[];
  temas: { id: number; nome: string }[];
  modelos: { id: number; etapa: string; ordem: number; texto: string }[];
};

const ABAS = ["Geral", "Grade", "Formatos e séries", "Temas", "Checklists", "Padrões"] as const;

export function ConfiguracoesCanal({ canalId, onFechar, onAlterado, onAviso }: { canalId: number; onFechar: () => void; onAlterado: () => void; onAviso: Aviso }) {
  const [cfg, setCfg] = useState<Config | null>(null);
  const [aba, setAba] = useState<(typeof ABAS)[number]>("Geral");

  const carregar = useCallback(async () => {
    try {
      setCfg(await ler<Config>(api.api.canais[":id"].config.$get({ param: { id: String(canalId) } })));
    } catch (e) {
      onAviso((e as Error).message, true);
    }
  }, [canalId]);
  useEffect(() => { void carregar(); }, [carregar]);

  /** Executa uma chamada, recarrega e avisa; erros viram aviso vermelho. */
  const rodar = useCallback(async (fn: () => Promise<unknown>, ok = "Salvo.") => {
    try {
      await fn();
      onAviso(ok);
      await carregar();
      onAlterado();
    } catch (e) {
      onAviso((e as Error).message, true);
    }
  }, [carregar, onAlterado, onAviso]);

  if (!cfg) return <Modal titulo="Carregando…" onFechar={onFechar} largo><p>Carregando…</p></Modal>;

  return (
    <Modal titulo={`Configurações · ${cfg.canal.nome}`} onFechar={onFechar} largo>
      <div className="mb-4 flex flex-wrap gap-1 border-b border-slate-200">
        {ABAS.map((a) => (
          <button key={a} onClick={() => setAba(a)} className={`-mb-px border-b-2 px-3 py-1.5 text-sm font-medium ${aba === a ? "border-slate-900 text-slate-900" : "border-transparent text-slate-500 hover:text-slate-800"}`}>
            {a}
          </button>
        ))}
      </div>
      {/* abas ficam montadas (só escondidas) para não perder o que foi digitado */}
      <div hidden={aba !== "Geral"}><Geral canal={cfg.canal} rodar={rodar} /></div>
      <div hidden={aba !== "Grade"}><Grade canalId={canalId} grade={cfg.grade} rodar={rodar} /></div>
      <div hidden={aba !== "Formatos e séries"}><FormatosESeries canalId={canalId} cfg={cfg} rodar={rodar} /></div>
      <div hidden={aba !== "Temas"}><Temas canalId={canalId} temas={cfg.temas} rodar={rodar} /></div>
      <div hidden={aba !== "Checklists"}><Checklists canalId={canalId} modelos={cfg.modelos} rodar={rodar} /></div>
      <div hidden={aba !== "Padrões"}><Padroes canal={cfg.canal} rodar={rodar} /></div>
    </Modal>
  );
}

type Rodar = (fn: () => Promise<unknown>, ok?: string) => Promise<void>;

function Geral({ canal, rodar }: { canal: Canal; rodar: Rodar }) {
  const [f, setF] = useState({ nome: canal.nome, nicho: canal.nicho, urlYoutube: canal.urlYoutube ?? "", referenciasIdentidade: canal.referenciasIdentidade });
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <Rotulo texto="Nome do canal"><input className={campo} value={f.nome} onChange={(e) => setF({ ...f, nome: e.target.value })} /></Rotulo>
      <Rotulo texto="Nicho"><input className={campo} value={f.nicho} onChange={(e) => setF({ ...f, nicho: e.target.value })} /></Rotulo>
      <Rotulo texto="Prefixo do código"><input className={`${campo} bg-slate-100`} value={canal.prefixoCodigo} disabled /></Rotulo>
      <Rotulo texto="Pasta no Drive (relativa à raiz)"><input className={`${campo} bg-slate-100`} value={canal.pastaRelativa} disabled /></Rotulo>
      <div className="sm:col-span-2"><Rotulo texto="URL do canal no YouTube"><input className={campo} value={f.urlYoutube} onChange={(e) => setF({ ...f, urlYoutube: e.target.value })} placeholder="https://www.youtube.com/@..." /></Rotulo></div>
      <div className="sm:col-span-2"><Rotulo texto="Referências de identidade (links do Design System e das artes)"><textarea className={`${campo} h-24`} value={f.referenciasIdentidade} onChange={(e) => setF({ ...f, referenciasIdentidade: e.target.value })} /></Rotulo></div>
      <div className="sm:col-span-2">
        <button className={botao} disabled={!f.nome.trim()} onClick={() => rodar(() => ler(api.api.canais[":id"].$patch({ param: { id: String(canal.id) }, json: { nome: f.nome, nicho: f.nicho, urlYoutube: f.urlYoutube.trim() || null, referenciasIdentidade: f.referenciasIdentidade } })))}>Salvar</button>
        <p className="mt-2 text-xs text-slate-500">O prefixo e a pasta não mudam depois de criados, porque os códigos e as pastas dos vídeos dependem deles.</p>
      </div>
    </div>
  );
}

function Grade({ canalId, grade, rodar }: { canalId: number; grade: Config["grade"]; rodar: Rodar }) {
  const [itens, setItens] = useState(grade.map(({ diaSemana, hora }) => ({ diaSemana, hora })));
  const [novo, setNovo] = useState({ diaSemana: 2, hora: "12:00" });
  return (
    <div className="max-w-md">
      <p className="mb-3 text-sm text-slate-600">Dias e horários de publicação. A data planejada dos vídeos é sugerida como o próximo horário livre desta grade.</p>
      <ul className="mb-3 space-y-1">
        {itens.length === 0 && <li className="text-sm text-slate-500">Nenhum horário.</li>}
        {itens.map((g, i) => (
          <li key={`${g.diaSemana}-${g.hora}`} className="flex items-center justify-between rounded border border-slate-200 px-3 py-1.5 text-sm">
            <span>{NOMES_DIAS[g.diaSemana]} às {g.hora}</span>
            <button className="text-slate-400 hover:text-red-600" onClick={() => setItens(itens.filter((_, j) => j !== i))} aria-label="Remover">×</button>
          </li>
        ))}
      </ul>
      <div className="mb-4 flex items-center gap-2">
        <select className={`${campo} w-auto`} value={novo.diaSemana} onChange={(e) => setNovo({ ...novo, diaSemana: Number(e.target.value) })}>
          {NOMES_DIAS.map((n, i) => <option key={n} value={i}>{n}</option>)}
        </select>
        <input type="time" className={`${campo} w-auto`} value={novo.hora} onChange={(e) => setNovo({ ...novo, hora: e.target.value })} />
        <button className={botaoClaro} disabled={!novo.hora || itens.some((g) => g.diaSemana === novo.diaSemana && g.hora === novo.hora)} onClick={() => setItens([...itens, novo].sort((a, b) => a.diaSemana - b.diaSemana || a.hora.localeCompare(b.hora)))}>Adicionar</button>
      </div>
      <button className={botao} onClick={() => rodar(() => ler(api.api.canais[":id"].grade.$put({ param: { id: String(canalId) }, json: { grade: itens } })))}>Salvar grade</button>
    </div>
  );
}

function FormatosESeries({ canalId, cfg, rodar }: { canalId: number; cfg: Config; rodar: Rodar }) {
  const [formato, setFormato] = useState("");
  const [serie, setSerie] = useState({ nome: "", descricao: "" });
  return (
    <div className="grid gap-6 sm:grid-cols-2">
      <section>
        <h3 className="mb-2 text-sm font-semibold">Formatos</h3>
        <ul className="mb-3 space-y-1">
          {cfg.formatos.map((f) => (
            <li key={f.id} className="flex items-center justify-between rounded border border-slate-200 px-3 py-1.5 text-sm">
              <span className={f.ativo ? "" : "text-slate-400 line-through"}>{f.nome}</span>
              <button className="text-xs text-slate-500 hover:text-slate-900" onClick={() => rodar(() => ler(api.api.formatos[":id"].$patch({ param: { id: String(f.id) }, json: { ativo: !f.ativo } })))}>{f.ativo ? "Desativar" : "Reativar"}</button>
            </li>
          ))}
        </ul>
        <form className="flex gap-2" onSubmit={(e) => { e.preventDefault(); void rodar(() => ler(api.api.canais[":id"].formatos.$post({ param: { id: String(canalId) }, json: { nome: formato } })), "Formato criado.").then(() => setFormato("")); }}>
          <input className={campo} value={formato} onChange={(e) => setFormato(e.target.value)} placeholder="Novo formato" required />
          <button className={botaoClaro}>Adicionar</button>
        </form>
        <p className="mt-2 text-xs text-slate-500">Formatos não são apagados, só desativados: os vídeos antigos continuam com o deles.</p>
      </section>
      <section>
        <h3 className="mb-2 text-sm font-semibold">Séries</h3>
        <ul className="mb-3 space-y-1">
          {cfg.series.length === 0 && <li className="text-sm text-slate-500">Nenhuma série.</li>}
          {cfg.series.map((s) => (
            <li key={s.id} className="flex items-start justify-between rounded border border-slate-200 px-3 py-1.5 text-sm">
              <span>{s.nome}{s.descricao && <span className="block text-xs text-slate-500">{s.descricao}</span>}</span>
              <button className="text-slate-400 hover:text-red-600" onClick={() => { if (confirm(`Apagar a série "${s.nome}"?`)) void rodar(() => ler(api.api.series[":id"].$delete({ param: { id: String(s.id) } })), "Série apagada."); }} aria-label="Apagar">×</button>
            </li>
          ))}
        </ul>
        <form className="space-y-2" onSubmit={(e) => { e.preventDefault(); void rodar(() => ler(api.api.canais[":id"].series.$post({ param: { id: String(canalId) }, json: serie })), "Série criada.").then(() => setSerie({ nome: "", descricao: "" })); }}>
          <input className={campo} value={serie.nome} onChange={(e) => setSerie({ ...serie, nome: e.target.value })} placeholder="Nova série" required />
          <input className={campo} value={serie.descricao} onChange={(e) => setSerie({ ...serie, descricao: e.target.value })} placeholder="Descrição (opcional)" />
          <button className={botaoClaro}>Adicionar</button>
        </form>
      </section>
    </div>
  );
}

function Temas({ canalId, temas, rodar }: { canalId: number; temas: Config["temas"]; rodar: Rodar }) {
  const [nome, setNome] = useState("");
  return (
    <div className="max-w-md">
      <p className="mb-3 text-sm text-slate-600">Temas são etiquetas livres para agrupar os vídeos (ex.: guarda, raspagem, campeonatos).</p>
      <div className="mb-3 flex flex-wrap gap-2">
        {temas.length === 0 && <span className="text-sm text-slate-500">Nenhum tema.</span>}
        {temas.map((t) => (
          <span key={t.id} className="flex items-center gap-1 rounded-full bg-slate-100 px-2.5 py-1 text-sm">
            {t.nome}
            <button className="text-slate-400 hover:text-red-600" onClick={() => rodar(() => ler(api.api.temas[":id"].$delete({ param: { id: String(t.id) } })), "Tema apagado.")} aria-label={`Apagar ${t.nome}`}>×</button>
          </span>
        ))}
      </div>
      <form className="flex gap-2" onSubmit={(e) => { e.preventDefault(); void rodar(() => ler(api.api.canais[":id"].temas.$post({ param: { id: String(canalId) }, json: { nome } })), "Tema criado.").then(() => setNome("")); }}>
        <input className={campo} value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Novo tema" required />
        <button className={botaoClaro}>Adicionar</button>
      </form>
    </div>
  );
}

function Checklists({ canalId, modelos, rodar }: { canalId: number; modelos: Config["modelos"]; rodar: Rodar }) {
  const [etapa, setEtapa] = useState<(typeof ETAPAS)[number]>("Pesquisa");
  const [rascunhos, setRascunhos] = useState<Record<string, string[]>>({});
  const salvos = modelos.filter((m) => m.etapa === etapa).sort((a, b) => a.ordem - b.ordem).map((m) => m.texto);
  const itens = rascunhos[etapa] ?? salvos;
  const sujo = JSON.stringify(itens) !== JSON.stringify(salvos);
  const mudar = (novos: string[]) => setRascunhos({ ...rascunhos, [etapa]: novos });
  const mover = (i: number, d: -1 | 1) => { const n = [...itens]; [n[i], n[i + d]] = [n[i + d]!, n[i]!]; mudar(n); };

  return (
    <div className="max-w-xl">
      <p className="mb-3 text-sm text-slate-600">O modelo de cada etapa é copiado para cada vídeo novo. Mudar aqui não altera os vídeos que já existem.</p>
      <div className="mb-3 flex flex-wrap gap-1">
        {ETAPAS.map((e) => (
          <button key={e} onClick={() => setEtapa(e)} className={`rounded-full px-3 py-1 text-xs font-medium ${etapa === e ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"}`}>{e}{rascunhos[e] ? " •" : ""}</button>
        ))}
      </div>
      <ul className="mb-3 space-y-1">
        {itens.length === 0 && <li className="text-sm text-slate-500">Sem itens nesta etapa.</li>}
        {itens.map((t, i) => (
          <li key={i} className="flex items-center gap-1">
            <input className={campo} value={t} onChange={(e) => mudar(itens.map((x, j) => (j === i ? e.target.value : x)))} />
            <button className="px-1 text-slate-400 hover:text-slate-800 disabled:opacity-30" disabled={i === 0} onClick={() => mover(i, -1)} aria-label="Subir">↑</button>
            <button className="px-1 text-slate-400 hover:text-slate-800 disabled:opacity-30" disabled={i === itens.length - 1} onClick={() => mover(i, 1)} aria-label="Descer">↓</button>
            <button className="px-1 text-slate-400 hover:text-red-600" onClick={() => mudar(itens.filter((_, j) => j !== i))} aria-label="Remover">×</button>
          </li>
        ))}
      </ul>
      <div className="flex gap-2">
        <button className={botaoClaro} onClick={() => mudar([...itens, ""])}>+ Item</button>
        <button className={botao} disabled={!sujo || itens.some((t) => !t.trim())} onClick={() => rodar(() => ler(api.api.canais[":id"].checklist[":etapa"].$put({ param: { id: String(canalId), etapa }, json: { textos: itens } }))).then(() => setRascunhos(({ [etapa]: _, ...resto }) => resto))}>Salvar {etapa}</button>
      </div>
    </div>
  );
}

function Padroes({ canal, rodar }: { canal: Canal; rodar: Rodar }) {
  const [f, setF] = useState({ modeloDescricao: canal.modeloDescricao, tags: canal.tagsPadrao.join(", "), vozPadrao: canal.vozPadrao, estiloImagemPadrao: canal.estiloImagemPadrao });
  const tags = f.tags.split(",").map((t) => t.trim()).filter(Boolean);
  const tamanho = tags.join(",").length;
  return (
    <div className="grid gap-4">
      <Rotulo texto="Modelo de descrição (variáveis: {titulo} {resumo} {capitulos} {fontes} {creditos})"><textarea className={`${campo} h-36 font-mono`} value={f.modeloDescricao} onChange={(e) => setF({ ...f, modeloDescricao: e.target.value })} /></Rotulo>
      <Rotulo texto={`Tags padrão, separadas por vírgula (${tamanho}/500 caracteres)`}><input className={campo} value={f.tags} onChange={(e) => setF({ ...f, tags: e.target.value })} /></Rotulo>
      <Rotulo texto="Voz padrão (ferramenta, voz e configurações)"><input className={campo} value={f.vozPadrao} onChange={(e) => setF({ ...f, vozPadrao: e.target.value })} /></Rotulo>
      <Rotulo texto="Estilo de imagem padrão (prompt base)"><textarea className={`${campo} h-24`} value={f.estiloImagemPadrao} onChange={(e) => setF({ ...f, estiloImagemPadrao: e.target.value })} /></Rotulo>
      <div><button className={botao} disabled={tamanho > 500} onClick={() => rodar(() => ler(api.api.canais[":id"].$patch({ param: { id: String(canal.id) }, json: { modeloDescricao: f.modeloDescricao, tagsPadrao: tags, vozPadrao: f.vozPadrao, estiloImagemPadrao: f.estiloImagemPadrao } })))}>Salvar padrões</button></div>
    </div>
  );
}

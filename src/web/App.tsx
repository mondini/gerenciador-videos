import { useCallback, useEffect, useState } from "react";
import { api, fmtData, ler } from "./api";
import { ConfiguracoesCanal } from "./Configuracoes";
import { CriarCanal } from "./CriarCanal";
import { FichaVideo } from "./Ficha";
import { Kanban, type DadosKanban } from "./Kanban";
import { ColarIdeias, NovaIdeia } from "./NovasIdeias";
import { botao, botaoClaro, useAviso } from "./ui";

type Canal = { id: number; nome: string; prefixoCodigo: string };

export function App() {
  const { mostrar, painel } = useAviso();
  const [canais, setCanais] = useState<Canal[] | null>(null);
  const [canalId, setCanalId] = useState<number | null>(null);
  const [kanban, setKanban] = useState<DadosKanban | null>(null);
  const [modal, setModal] = useState<"ideia" | "lote" | "config" | null>(null);
  const [aberto, setAberto] = useState<number | null>(null);

  const carregarCanais = useCallback(async () => {
    try {
      const lista = await ler<Canal[]>(api.api.canais.$get());
      setCanais(lista);
      setCanalId((atual) => (atual && lista.some((c) => c.id === atual) ? atual : (lista[0]?.id ?? null)));
    } catch (e) {
      mostrar((e as Error).message, true);
    }
  }, []);
  useEffect(() => { void carregarCanais(); }, [carregarCanais]);

  const carregarKanban = useCallback(async () => {
    if (canalId == null) return;
    try {
      setKanban(await ler<DadosKanban>(api.api.canais[":id"].kanban.$get({ param: { id: String(canalId) } })));
    } catch (e) {
      mostrar((e as Error).message, true);
    }
  }, [canalId]);
  useEffect(() => { void carregarKanban(); }, [carregarKanban]);

  if (canais === null) return <main className="p-6 text-slate-500">Carregando…{painel}</main>;
  if (canais.length === 0) return <main className="min-h-screen bg-slate-100 p-4"><CriarCanal onCriado={carregarCanais} onErro={(m) => mostrar(m, true)} />{painel}</main>;

  const prontos = kanban?.cards.filter((c) => ["Thumbnail", "Agendado"].includes(c.etapa)).length ?? 0;

  return (
    <main className="min-h-screen bg-slate-100 p-4">
      <header className="mb-4 flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-semibold">Gerenciador de Canais</h1>
        {canais.length > 1 && (
          <select className="rounded-md border border-slate-300 bg-white px-2 py-1 text-sm" value={canalId ?? ""} onChange={(e) => setCanalId(Number(e.target.value))}>
            {canais.map((c) => <option key={c.id} value={c.id}>{c.nome}</option>)}
          </select>
        )}
        {canais.length === 1 && <span className="text-slate-600">{canais[0]?.nome}</span>}
        <div className="ml-auto flex items-center gap-3 text-sm text-slate-600">
          {kanban && <span title="Vídeos em Thumbnail ou Agendado">Prontos/agendados: <b>{prontos}</b></span>}
          {kanban?.proximoHorarioLivre && <span>Próximo horário livre: <b>{fmtData(kanban.proximoHorarioLivre)}</b></span>}
          <button className={botaoClaro} onClick={() => setModal("config")}>Configurações</button>
          <button className={botaoClaro} onClick={() => setModal("lote")}>Colar várias ideias</button>
          <button className={botao} onClick={() => setModal("ideia")}>+ Nova ideia</button>
        </div>
      </header>

      {kanban ? <Kanban dados={kanban} onAbrir={setAberto} onMovido={carregarKanban} onAviso={mostrar} /> : <p className="text-slate-500">Carregando…</p>}

      {modal === "ideia" && canalId != null && <NovaIdeia canalId={canalId} onFechar={() => setModal(null)} onCriada={carregarKanban} onAviso={mostrar} />}
      {modal === "lote" && canalId != null && <ColarIdeias canalId={canalId} onFechar={() => setModal(null)} onCriada={carregarKanban} onAviso={mostrar} />}
      {modal === "config" && canalId != null && <ConfiguracoesCanal canalId={canalId} onFechar={() => setModal(null)} onAlterado={() => { void carregarCanais(); void carregarKanban(); }} onAviso={mostrar} />}
      {aberto != null && <FichaVideo videoId={aberto} onFechar={() => setAberto(null)} onAlterado={carregarKanban} onAviso={mostrar} />}
      {painel}
    </main>
  );
}

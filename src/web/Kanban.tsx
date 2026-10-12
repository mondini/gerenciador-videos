import { DndContext, PointerSensor, useDraggable, useDroppable, useSensor, useSensors, type DragEndEvent } from "@dnd-kit/core";
import { api, fmtData, ler } from "./api";

export type Card = {
  id: number;
  codigo: string;
  titulo: string;
  etapa: string;
  formato: string | null;
  dataPlanejada: string | null;
  pontuacao: number | null;
  pendentesChecklist: number;
  /** O que falta segundo o pipeline do canal (`./ma sincronizar`). */
  pendencias: string[];
  emRisco: boolean;
  arquivos: { subpasta: string; arquivos: number; soOnline: number }[] | null;
};

export type DadosKanban = { etapas: string[]; cards: Card[]; proximoHorarioLivre: string | null };

function CardVideo({ card, onAbrir }: { card: Card; onAbrir: (id: number) => void }) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({ id: card.id });
  const style = transform ? { transform: `translate(${transform.x}px, ${transform.y}px)` } : undefined;
  const faltando = card.arquivos?.filter((a) => a.arquivos === 0).length ?? 0;
  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      onClick={() => onAbrir(card.id)}
      className={`cursor-grab rounded-lg border bg-white p-2.5 text-sm shadow-sm ${card.emRisco ? "border-red-300" : "border-slate-200"} ${isDragging ? "z-40 opacity-80 shadow-lg" : ""}`}
    >
      <div className="flex items-center justify-between text-xs text-slate-500">
        <span className="font-mono font-semibold text-slate-700">{card.codigo}</span>
        <span>{card.pontuacao != null ? `★ ${card.pontuacao}/15` : ""}</span>
      </div>
      <div className="mt-1 font-medium leading-snug">{card.titulo}</div>
      <div className="mt-1.5 flex flex-wrap gap-1 text-xs">
        <span className="rounded bg-slate-100 px-1.5 py-0.5">{card.formato ?? "formato a definir"}</span>
        {card.pendentesChecklist > 0 && <span className="rounded bg-amber-100 px-1.5 py-0.5 text-amber-800" title="Itens pendentes no checklist desta etapa">⚠️ {card.pendentesChecklist}</span>}
        {card.pendencias.length > 0 && <span className="rounded bg-sky-100 px-1.5 py-0.5 text-sky-800" title={`Falta (pipeline do canal):\n${card.pendencias.join("\n")}`}>🎬 falta {card.pendencias.length}</span>}
        {card.emRisco && <span className="rounded bg-red-100 px-1.5 py-0.5 text-red-800" title="Faltam menos de 7 dias e ainda não chegou em Edição">⏰ risco</span>}
        {card.arquivos && (
          <span className="rounded bg-slate-100 px-1.5 py-0.5" title={card.arquivos.map((a) => `${a.subpasta}: ${a.arquivos}${a.soOnline ? ` (${a.soOnline} ☁️)` : ""}`).join("\n")}>
            {faltando === 0 ? "✅" : "❌"} {card.arquivos.length - faltando}/{card.arquivos.length}
          </span>
        )}
      </div>
      {card.dataPlanejada && <div className="mt-1 text-xs text-slate-500">📅 {fmtData(card.dataPlanejada)}</div>}
    </div>
  );
}

function Coluna({ etapa, cards, onAbrir }: { etapa: string; cards: Card[]; onAbrir: (id: number) => void }) {
  const { setNodeRef, isOver } = useDroppable({ id: etapa });
  return (
    <section ref={setNodeRef} className={`flex w-64 shrink-0 flex-col rounded-xl p-2 ${isOver ? "bg-slate-300" : "bg-slate-200/70"}`}>
      <h3 className="mb-2 flex items-center justify-between px-1 text-sm font-semibold text-slate-700">
        {etapa}
        <span className="rounded-full bg-white px-2 text-xs font-normal">{cards.length}</span>
      </h3>
      <div className="flex min-h-24 flex-1 flex-col gap-2">
        {cards.map((c) => <CardVideo key={c.id} card={c} onAbrir={onAbrir} />)}
      </div>
    </section>
  );
}

export function Kanban({ dados, onAbrir, onMovido, onAviso }: { dados: DadosKanban; onAbrir: (id: number) => void; onMovido: () => void; onAviso: (m: string, erro?: boolean) => void }) {
  const sensores = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 6 } }));

  async function aoSoltar(e: DragEndEvent) {
    if (!e.over) return;
    const card = dados.cards.find((c) => c.id === e.active.id);
    const etapa = String(e.over.id);
    if (!card || card.etapa === etapa) return;
    try {
      const r = await ler<{ avisos: string[] }>(api.api.videos[":id"].etapa.$post({ param: { id: String(card.id) }, json: { etapa: etapa as never } }));
      r.avisos.forEach((a) => onAviso(`${card.codigo}: ${a}`));
    } catch (err) {
      onAviso((err as Error).message, true);
    }
    onMovido();
  }

  return (
    <DndContext sensors={sensores} onDragEnd={aoSoltar}>
      <div className="flex gap-3 overflow-x-auto pb-4">
        {dados.etapas.map((etapa) => (
          <Coluna key={etapa} etapa={etapa} cards={dados.cards.filter((c) => c.etapa === etapa)} onAbrir={onAbrir} />
        ))}
      </div>
    </DndContext>
  );
}

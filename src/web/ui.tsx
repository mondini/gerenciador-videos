import { useEffect, useState, type ReactNode } from "react";

export const botao =
  "rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50";
export const botaoClaro =
  "rounded-md border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50";
export const campo =
  "w-full rounded-md border border-slate-300 bg-white px-2 py-1.5 text-sm focus:border-slate-500 focus:outline-none";

export function Rotulo({ texto, children }: { texto: string; children: ReactNode }) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block font-medium text-slate-700">{texto}</span>
      {children}
    </label>
  );
}

export function Modal({ titulo, onFechar, children, largo }: { titulo: string; onFechar: () => void; children: ReactNode; largo?: boolean }) {
  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onFechar();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onFechar]);
  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/40 p-4" onMouseDown={onFechar}>
      <div
        className={`mt-8 w-full ${largo ? "max-w-4xl" : "max-w-lg"} rounded-xl bg-white shadow-xl`}
        onMouseDown={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between border-b border-slate-200 px-5 py-3">
          <h2 className="text-lg font-semibold">{titulo}</h2>
          <button className="text-2xl leading-none text-slate-400 hover:text-slate-700" onClick={onFechar} aria-label="Fechar">
            ×
          </button>
        </div>
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}

export function useAviso() {
  const [avisos, setAvisos] = useState<{ id: number; texto: string; erro: boolean }[]>([]);
  const mostrar = (texto: string, erro = false) => {
    const id = Date.now() + Math.random();
    setAvisos((a) => [...a, { id, texto, erro }]);
    setTimeout(() => setAvisos((a) => a.filter((x) => x.id !== id)), erro ? 7000 : 4500);
  };
  const painel = (
    <div className="fixed bottom-4 right-4 z-[60] flex max-w-sm flex-col gap-2">
      {avisos.map((a) => (
        <div key={a.id} className={`rounded-md px-3 py-2 text-sm shadow-lg ${a.erro ? "bg-red-600 text-white" : "bg-slate-900 text-white"}`}>
          {a.texto}
        </div>
      ))}
    </div>
  );
  return { mostrar, painel };
}

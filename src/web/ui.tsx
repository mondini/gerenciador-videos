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

export function Modal({ titulo, onFechar, children, largo, aoLadoDoTitulo }: { titulo: string; onFechar: () => void; children: ReactNode; largo?: boolean; aoLadoDoTitulo?: ReactNode }) {
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
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold">{titulo}</h2>
            {aoLadoDoTitulo}
          </div>
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

const CRITERIOS = [
  {
    nome: "Apelo (1–5)",
    pergunta: "Você clicaria nesse título? Quanto a ideia desperta curiosidade ou emoção.",
    exemplos: ["1: \"História da cidade X em 1850\" (genérico, sem gancho)", "3: \"Por que a cidade X foi abandonada\"", "5: \"A cidade que desapareceu em uma noite e ninguém explica\""],
  },
  {
    nome: "Ilustrar (1–5)",
    pergunta: "Dá para ilustrar com imagens geradas, sem posições ou cenas complexas?",
    exemplos: ["1: lutas corpo a corpo, mãos e rostos em detalhe, textos legíveis", "3: pessoas em cenários simples, algumas ações", "5: paisagens, objetos, mapas e construções"],
  },
  {
    nome: "Pesquisa (1–5)",
    pergunta: "Há fontes confiáveis e suficientes para escrever o roteiro com segurança?",
    exemplos: ["1: poucos relatos, versões que se contradizem", "3: algumas boas fontes, mas com lacunas", "5: documentação farta (livros, arquivos, artigos) e fácil de achar"],
  },
];

/** Ícone (i) que abre a explicação das três notas de uma ideia. */
export function InfoNotas() {
  const [aberto, setAberto] = useState(false);
  return (
    <span className="relative inline-block">
      <button
        type="button"
        aria-label="O que significam as notas"
        aria-expanded={aberto}
        onClick={() => setAberto((a) => !a)}
        className="flex h-5 w-5 items-center justify-center rounded-full border border-slate-400 text-xs font-semibold italic text-slate-500 hover:bg-slate-100"
      >
        i
      </button>
      {aberto && (
        <div className="absolute left-0 top-7 z-10 w-80 max-w-[85vw] space-y-3 rounded-lg border border-slate-200 bg-white p-3 text-xs shadow-lg">
          <div className="flex items-start justify-between">
            <p className="text-slate-600">Dê de 1 (pior) a 5 (melhor) em cada critério. A soma ajuda a priorizar as ideias.</p>
            <button type="button" className="ml-2 text-base leading-none text-slate-400 hover:text-slate-700" onClick={() => setAberto(false)} aria-label="Fechar">×</button>
          </div>
          {CRITERIOS.map((c) => (
            <div key={c.nome}>
              <div className="font-semibold text-slate-800">{c.nome}</div>
              <div className="text-slate-600">{c.pergunta}</div>
              <ul className="mt-1 list-disc pl-4 text-slate-500">{c.exemplos.map((e) => <li key={e}>{e}</li>)}</ul>
            </div>
          ))}
        </div>
      )}
    </span>
  );
}

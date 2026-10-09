import { useState } from "react";
import { api, ler, NOMES_DIAS } from "./api";
import { botao, campo, Rotulo } from "./ui";

export function CriarCanal({ onCriado, onErro }: { onCriado: () => void; onErro: (m: string) => void }) {
  const [nome, setNome] = useState("");
  const [prefixo, setPrefixo] = useState("BJJ");
  const [pasta, setPasta] = useState("");
  const [dias, setDias] = useState<number[]>([2, 5]);
  const [hora, setHora] = useState("12:00");
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    try {
      await ler(
        api.api.canais.$post({
          json: {
            nome,
            prefixoCodigo: prefixo.toUpperCase(),
            pastaRelativa: pasta || `${prefixo.toUpperCase()} - ${nome}`,
            grade: dias.map((diaSemana) => ({ diaSemana, hora })),
          },
        }),
      );
      onCriado();
    } catch (err) {
      onErro((err as Error).message);
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form onSubmit={enviar} className="mx-auto mt-16 max-w-md space-y-4 rounded-xl bg-white p-6 shadow">
      <h1 className="text-xl font-semibold">Criar o primeiro canal</h1>
      <p className="text-sm text-slate-600">
        O sistema cria a pasta do canal dentro da raiz do Drive configurada no <code>.env</code>. Nada existente é alterado.
      </p>
      <Rotulo texto="Nome do canal">
        <input className={campo} value={nome} onChange={(e) => setNome(e.target.value)} required autoFocus />
      </Rotulo>
      <Rotulo texto="Prefixo do código (2 a 5 letras)">
        <input className={campo} value={prefixo} onChange={(e) => setPrefixo(e.target.value.toUpperCase())} maxLength={5} required />
      </Rotulo>
      <Rotulo texto="Pasta do canal no Drive (opcional)">
        <input className={campo} value={pasta} onChange={(e) => setPasta(e.target.value)} placeholder={`${prefixo} - ${nome || "Nome do canal"}`} />
      </Rotulo>
      <fieldset>
        <legend className="mb-1 text-sm font-medium text-slate-700">Grade de publicação</legend>
        <div className="flex flex-wrap items-center gap-2">
          {NOMES_DIAS.map((n, i) => (
            <label key={n} className="flex items-center gap-1 text-sm">
              <input type="checkbox" checked={dias.includes(i)} onChange={(e) => setDias(e.target.checked ? [...dias, i] : dias.filter((d) => d !== i))} />
              {n}
            </label>
          ))}
          <input type="time" className="ml-2 rounded-md border border-slate-300 px-2 py-1 text-sm" value={hora} onChange={(e) => setHora(e.target.value)} />
        </div>
      </fieldset>
      <button className={botao} disabled={enviando}>
        {enviando ? "Criando…" : "Criar canal"}
      </button>
    </form>
  );
}

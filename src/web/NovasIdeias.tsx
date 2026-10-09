import { useEffect, useState } from "react";
import { api, ler } from "./api";
import { botao, botaoClaro, campo, Modal, Rotulo } from "./ui";

type Formato = { id: number; nome: string };
type Parecidos = { codigo: string; tituloProvisorio: string }[];

const NOTAS = [1, 2, 3, 4, 5];

export function NovaIdeia({ canalId, onFechar, onCriada, onAviso }: { canalId: number; onFechar: () => void; onCriada: () => void; onAviso: (m: string, erro?: boolean) => void }) {
  const [formatos, setFormatos] = useState<Formato[]>([]);
  const [titulo, setTitulo] = useState("");
  const [formatoId, setFormatoId] = useState<number | "">("");
  const [notas, setNotas] = useState<{ apelo: number | ""; ilustracao: number | ""; pesquisa: number | "" }>({ apelo: "", ilustracao: "", pesquisa: "" });

  useEffect(() => {
    ler<Formato[]>(api.api.canais[":id"].formatos.$get({ param: { id: String(canalId) } })).then(setFormatos, (e) => onAviso(e.message, true));
  }, [canalId]);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    if (formatoId === "") return onAviso("Escolha o formato.", true);
    try {
      const r = await ler<{ video: { codigo: string }; parecidos: Parecidos }>(
        api.api.videos.$post({
          json: {
            canalId,
            tituloProvisorio: titulo,
            formatoId,
            notaApelo: notas.apelo || null,
            notaIlustracao: notas.ilustracao || null,
            notaPesquisa: notas.pesquisa || null,
          },
        }),
      );
      onAviso(`${r.video.codigo} criado.`);
      if (r.parecidos.length) onAviso(`Parecido com: ${r.parecidos.map((p) => `${p.codigo} "${p.tituloProvisorio}"`).join(", ")}`);
      onCriada();
      onFechar();
    } catch (err) {
      onAviso((err as Error).message, true);
    }
  }

  const nota = (rotulo: string, chave: keyof typeof notas, dica: string) => (
    <Rotulo texto={`${rotulo} (1–5)`}>
      <select className={campo} value={notas[chave]} onChange={(e) => setNotas({ ...notas, [chave]: e.target.value ? Number(e.target.value) : "" })} title={dica}>
        <option value="">—</option>
        {NOTAS.map((n) => <option key={n}>{n}</option>)}
      </select>
    </Rotulo>
  );

  return (
    <Modal titulo="Nova ideia" onFechar={onFechar}>
      <form onSubmit={enviar} className="space-y-4">
        <Rotulo texto="Título provisório">
          <input className={campo} value={titulo} onChange={(e) => setTitulo(e.target.value)} required autoFocus />
        </Rotulo>
        <Rotulo texto="Formato">
          <select className={campo} value={formatoId} onChange={(e) => setFormatoId(e.target.value ? Number(e.target.value) : "")} required>
            <option value="">Escolha…</option>
            {formatos.map((f) => <option key={f.id} value={f.id}>{f.nome}</option>)}
          </select>
        </Rotulo>
        <div className="grid grid-cols-3 gap-3">
          {nota("Apelo", "apelo", "Você clicaria nesse título?")}
          {nota("Ilustrar", "ilustracao", "Dá para ilustrar sem posições complexas?")}
          {nota("Pesquisa", "pesquisa", "Há fontes confiáveis suficientes?")}
        </div>
        <div className="flex justify-end gap-2">
          <button type="button" className={botaoClaro} onClick={onFechar}>Cancelar</button>
          <button className={botao}>Criar</button>
        </div>
      </form>
    </Modal>
  );
}

export function ColarIdeias({ canalId, onFechar, onCriada, onAviso }: { canalId: number; onFechar: () => void; onCriada: () => void; onAviso: (m: string, erro?: boolean) => void }) {
  const [texto, setTexto] = useState("");
  const linhas = texto.split("\n").filter((l) => l.trim()).length;

  async function enviar() {
    try {
      const r = await ler<{ video: { codigo: string }; parecidos: Parecidos }[]>(api.api.canais[":id"].ideias.$post({ param: { id: String(canalId) }, json: { texto } }));
      onAviso(`${r.length} ideia(s) criada(s). O formato fica "a definir" até a triagem.`);
      const dup = r.filter((x) => x.parecidos.length);
      if (dup.length) onAviso(`${dup.length} ideia(s) parecida(s) com outras já existentes: ${dup.map((d) => d.video.codigo).join(", ")}`);
      onCriada();
      onFechar();
    } catch (err) {
      onAviso((err as Error).message, true);
    }
  }

  return (
    <Modal titulo="Colar várias ideias" onFechar={onFechar}>
      <p className="mb-2 text-sm text-slate-600">Uma ideia por linha. Marcadores e numeração no início são ignorados.</p>
      <textarea className={`${campo} h-56 font-mono`} value={texto} onChange={(e) => setTexto(e.target.value)} autoFocus />
      <div className="mt-3 flex items-center justify-between">
        <span className="text-sm text-slate-500">{linhas} linha(s)</span>
        <div className="flex gap-2">
          <button className={botaoClaro} onClick={onFechar}>Cancelar</button>
          <button className={botao} onClick={enviar} disabled={linhas === 0}>Criar {linhas || ""} ideia(s)</button>
        </div>
      </div>
    </Modal>
  );
}

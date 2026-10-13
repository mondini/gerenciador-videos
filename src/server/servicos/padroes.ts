import type { ItemModeloAgenda } from "../../shared/agenda";
import type { Etapa } from "../../shared/etapas";

export const FORMATOS_PADRAO = ["História", "Mito x verdade", "Ranking", "Origem", "Rivalidade"];

export const CHECKLIST_PADRAO: Partial<Record<Etapa, string[]>> = {
  Ideia: ["Formato definido", "Notas de apelo, ilustração e pesquisa dadas"],
  Pesquisa: ["Pelo menos 3 fontes registradas", "Fato sustentado preenchido em cada fonte", "Texto de tela de cada fonte escrito"],
  Roteiro: [
    "Gancho dos 15s escrito",
    "CTA no meio e no fim",
    "Leitura em voz alta feita",
    "Duração estimada entre 8 e 10 min",
    "Fatos conferidos contra as fontes",
  ],
  Narração: ["Narração gerada ou gravada", "Áudio ouvido inteiro", "Áudio salvo em 02_audio"],
  Imagens: ["Todas as cenas com status ok", "Posições de luta conferidas (anatomia correta)", "Imagens salvas em 03_imagens"],
  Edição: ["Montagem concluída", "Fontes exibidas na tela", "Legenda .srt gerada", "Export salvo em 07_export"],
  Thumbnail: ["2 a 3 variações criadas", "Variante escolhida", "Arquivos salvos em 06_thumbnail"],
  Agendado: ["Título final definido", "Descrição, tags e capítulos prontos", "Dossiê de direitos preenchido (contestações, uso de IA, riscos)", "Divulgação de conteúdo sintético conferida", "Agendado no YouTube Studio"],
};

/** Semana padrão: o longo no dia do upload, 4 shorts dele e 1 short da reserva (igual à migração 0003). */
export const AGENDA_PADRAO: ItemModeloAgenda[] = [
  { rotulo: "Short 1 (o corte mais forte)", tipo: "short", diasApos: 0, hora: "18:00" },
  { rotulo: "Short 2", tipo: "short", diasApos: 1, hora: "12:00" },
  { rotulo: "Short 3", tipo: "short", diasApos: 2, hora: "12:00" },
  { rotulo: "Short 4", tipo: "short", diasApos: 4, hora: "10:00" },
  { rotulo: "Short da reserva (no 1º vídeo: o short 5 dele mesmo)", tipo: "reserva", diasApos: 5, hora: "10:00" },
];

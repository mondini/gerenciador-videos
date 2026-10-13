import { describe, expect, it } from "vitest";
import { formatarCodigo, nomePastaVideo, proximoNumero, slugify } from "./codigo";
import { emRisco } from "./risco";
import { proximoHorarioLivre } from "./grade";
import { fusoValido, instanteNoFuso, partesNoFuso } from "./fuso";
import { montarAgenda } from "./agenda";

describe("código do vídeo", () => {
  it("formata com zeros à esquerda", () => {
    expect(formatarCodigo("BJJ", 1)).toBe("BJJ-001");
    expect(formatarCodigo("BJJ", 123)).toBe("BJJ-123");
  });
  it("rejeita prefixo e número inválidos", () => {
    expect(() => formatarCodigo("bjj", 1)).toThrow();
    expect(() => formatarCodigo("BJJ", 0)).toThrow();
  });
  it("calcula o próximo número sem repetir, mesmo com buracos", () => {
    expect(proximoNumero([])).toBe(1);
    expect(proximoNumero([1, 2, 5])).toBe(6);
  });
});

describe("slug e nome da pasta", () => {
  it("remove acentos e símbolos", () => {
    expect(slugify("A origem do Jiu-Jitsu: Maeda & Gracie!")).toBe("a-origem-do-jiu-jitsu-maeda-gracie");
  });
  it("limita o tamanho sem terminar em hífen", () => {
    const s = slugify("uma história muito longa sobre a família Gracie e o início do jiu-jitsu");
    expect(s.length).toBeLessThanOrEqual(40);
    expect(s.endsWith("-")).toBe(false);
  });
  it("usa um valor padrão para título vazio", () => {
    expect(slugify("  !!! ")).toBe("sem-titulo");
  });
  it("monta o nome da pasta", () => {
    expect(nomePastaVideo("BJJ-001", "Mito ou verdade?")).toBe("BJJ-001-mito-ou-verdade");
  });
});

describe("alerta de risco", () => {
  const hoje = new Date(2026, 9, 9);
  it("alerta quando faltam menos de 7 dias e ainda está antes de Edição", () => {
    expect(emRisco("Roteiro", new Date(2026, 9, 14), hoje)).toBe(true);
  });
  it("não alerta com 7 dias ou mais", () => {
    expect(emRisco("Roteiro", new Date(2026, 9, 16), hoje)).toBe(false);
  });
  it("não alerta de Edição em diante", () => {
    expect(emRisco("Edição", new Date(2026, 9, 10), hoje)).toBe(false);
  });
  it("não alerta sem data planejada e alerta se a data já passou", () => {
    expect(emRisco("Ideia", null, hoje)).toBe(false);
    expect(emRisco("Pesquisa", new Date(2026, 9, 1), hoje)).toBe(true);
  });
});

describe("próximo horário livre da grade", () => {
  // 2026-10-09 é sexta-feira; grade às 12:00 de Brasília (UTC-3) = 15:00Z
  const grade = [
    { diaSemana: 2, hora: "12:00" },
    { diaSemana: 5, hora: "12:00" },
  ];
  const sp = "America/Sao_Paulo";
  it("escolhe o próximo horário depois de agora", () => {
    expect(proximoHorarioLivre(grade, [], new Date("2026-10-09T11:00:00Z"), sp)).toEqual(new Date("2026-10-09T15:00:00Z"));
  });
  it("passa para o próximo dia da grade se o horário de hoje já passou", () => {
    expect(proximoHorarioLivre(grade, [], new Date("2026-10-09T16:00:00Z"), sp)).toEqual(new Date("2026-10-13T15:00:00Z"));
  });
  it("pula horários ocupados", () => {
    const ocupados = [new Date("2026-10-09T15:00:00Z"), new Date("2026-10-13T15:00:00Z")];
    expect(proximoHorarioLivre(grade, ocupados, new Date("2026-10-09T11:00:00Z"), sp)).toEqual(new Date("2026-10-16T15:00:00Z"));
  });
  it("lê a grade no fuso do público, inclusive depois do fim do horário de verão", () => {
    const ny = "America/New_York";
    const terca = [{ diaSemana: 2, hora: "14:00" }];
    expect(proximoHorarioLivre(terca, [], new Date("2026-10-09T11:00:00Z"), ny)).toEqual(new Date("2026-10-13T18:00:00Z")); // EDT, UTC-4
    expect(proximoHorarioLivre(terca, [], new Date("2026-11-01T12:00:00Z"), ny)).toEqual(new Date("2026-11-03T19:00:00Z")); // EST, UTC-5
  });
  it("devolve null com a grade vazia", () => {
    expect(proximoHorarioLivre([], [], new Date(), sp)).toBeNull();
  });
});

describe("fuso", () => {
  it("converte hora de parede em instante e de volta", () => {
    const ny = "America/New_York";
    expect(instanteNoFuso(2026, 10, 27, 14, 0, ny)).toEqual(new Date("2026-10-27T18:00:00Z"));
    expect(instanteNoFuso(2026, 11, 1, 10, 0, ny)).toEqual(new Date("2026-11-01T15:00:00Z"));
    expect(instanteNoFuso(2026, 10, 32, 10, 0, ny)).toEqual(new Date("2026-11-01T15:00:00Z")); // dia além do mês
    expect(partesNoFuso(new Date("2026-10-27T18:00:00Z"), ny)).toMatchObject({ ano: 2026, mes: 10, dia: 27, hora: 14, minuto: 0, diaSemana: 2 });
  });
  it("valida o nome do fuso", () => {
    expect(fusoValido("America/New_York")).toBe(true);
    expect(fusoValido("Nova York")).toBe(false);
  });
});

describe("agenda de publicação", () => {
  const ny = "America/New_York";
  const modelo = [
    { rotulo: "Short 1", tipo: "short" as const, diasApos: 0, hora: "18:00" },
    { rotulo: "Short 4", tipo: "short" as const, diasApos: 4, hora: "10:00" },
    { rotulo: "Short da reserva", tipo: "reserva" as const, diasApos: 5, hora: "10:00" },
  ];
  it("coloca o longo no upload e cada material no dia e hora do fuso do público", () => {
    // terça 27/10/2026 14:00 EDT; sábado 31/10 ainda em EDT; domingo 1º/11 já em EST
    const agenda = montarAgenda(new Date("2026-10-27T18:00:00Z"), ny, modelo);
    expect(agenda.map((m) => [m.tipo, m.rotulo, m.quando.toISOString()])).toEqual([
      ["longo", "Vídeo longo", "2026-10-27T18:00:00.000Z"],
      ["short", "Short 1", "2026-10-27T22:00:00.000Z"],
      ["short", "Short 4", "2026-10-31T14:00:00.000Z"],
      ["reserva", "Short da reserva", "2026-11-01T15:00:00.000Z"],
    ]);
  });
  it("usa o dia do upload no fuso do público, não o do servidor", () => {
    // 23:30 de domingo em Nova York já é segunda em UTC; o short de 1 dia depois cai na segunda de Nova York
    const agenda = montarAgenda(new Date("2026-10-12T03:30:00Z"), ny, [{ rotulo: "S", tipo: "short", diasApos: 1, hora: "12:00" }]);
    expect(agenda[1]!.quando).toEqual(new Date("2026-10-12T16:00:00Z"));
  });
});

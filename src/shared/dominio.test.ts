import { describe, expect, it } from "vitest";
import { formatarCodigo, nomePastaVideo, proximoNumero, slugify } from "./codigo";
import { emRisco } from "./risco";
import { proximoHorarioLivre } from "./grade";

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
    expect(nomePastaVideo("BJJ-001", "Mito ou verdade?")).toBe("BJJ-001_mito-ou-verdade");
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
  // 2026-10-09 é sexta-feira
  const grade = [
    { diaSemana: 2, hora: "12:00" },
    { diaSemana: 5, hora: "12:00" },
  ];
  it("escolhe o próximo horário depois de agora", () => {
    expect(proximoHorarioLivre(grade, [], new Date(2026, 9, 9, 8, 0))).toEqual(new Date(2026, 9, 9, 12, 0));
  });
  it("passa para o próximo dia da grade se o horário de hoje já passou", () => {
    expect(proximoHorarioLivre(grade, [], new Date(2026, 9, 9, 13, 0))).toEqual(new Date(2026, 9, 13, 12, 0));
  });
  it("pula horários ocupados", () => {
    const ocupados = [new Date(2026, 9, 9, 12, 0), new Date(2026, 9, 13, 12, 0)];
    expect(proximoHorarioLivre(grade, ocupados, new Date(2026, 9, 9, 8, 0))).toEqual(new Date(2026, 9, 16, 12, 0));
  });
  it("devolve null com a grade vazia", () => {
    expect(proximoHorarioLivre([], [], new Date())).toBeNull();
  });
});

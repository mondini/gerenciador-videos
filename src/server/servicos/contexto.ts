import type { Db } from "../db";

export interface Contexto {
  db: Db;
  driveRoot: string;
  agora?: () => Date;
}

export const agoraDe = (ctx: Contexto): Date => (ctx.agora ? ctx.agora() : new Date());

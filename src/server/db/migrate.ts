import { abrirBanco } from "./index";

const { sqlite } = abrirBanco("data/gerenciador.db");
sqlite.close();
console.log("Migrações aplicadas em data/gerenciador.db");

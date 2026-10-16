// Dados da cena: tamanho do quadro, câmera isométrica, lugares da maquete e a rota do Pix.
import {OrthographicCamera, Vector3} from 'three';

export const LARGURA = 1920;
export const ALTURA = 1080;
export const FPS = 30;
export const DURACAO = 150;

export const COR = {
  papel: '#F3EADB',
  papelEscuro: '#E6D9C3',
  tinta: '#1F2B30',
  tintaSuave: '#6B7579',
  pix: '#1FB5A6',
  pixClaro: '#9FE3DA',
  consulta: '#E8A33D',
  base: '#EFE4D0',
  terra: '#C7754B',
  terraEscura: '#9C5535',
  rua: '#D5CDBF',
  faixa: '#F7F1E6',
  grama: '#A9C27A',
  gramaEscura: '#7FA05A',
};

// Câmera isométrica: olha na diagonal (1, 1, 1) para o alvo.
export const CAMERA = {
  alvo: new Vector3(-2.7, 0.2, 3.3),
  distancia: 40,
  zoom: 47,
};

export const posicaoCamera = () =>
  CAMERA.alvo.clone().add(new Vector3(1, 1, 1).normalize().multiplyScalar(CAMERA.distancia));

// Mesmo cálculo do react-three-fiber, para posicionar rótulos em HTML sobre a maquete.
const cameraHtml = (() => {
  const c = new OrthographicCamera(-LARGURA / 2, LARGURA / 2, ALTURA / 2, -ALTURA / 2, 0.1, 200);
  c.position.copy(posicaoCamera());
  c.lookAt(CAMERA.alvo);
  c.zoom = CAMERA.zoom;
  c.updateProjectionMatrix();
  c.updateMatrixWorld();
  return c;
})();

export const naTela = (x: number, y: number, z: number) => {
  const v = new Vector3(x, y, z).project(cameraHtml);
  return {x: ((v.x + 1) / 2) * LARGURA, y: ((1 - v.y) / 2) * ALTURA};
};

// Lugares da maquete, em [x, z] no chão.
export const LUGAR = {
  casa: [-7, 4.6],
  bancoA: [-3.4, 0.4],
  dict: [-8.2, -1.0],
  bc: [1.4, -3.6],
  bancoB: [7.4, -2.2],
  barraca: [7, 4.8],
} as const;

type Ponto = readonly [number, number];

// A rota do dinheiro, pelas ruas: casa → seu banco → Banco Central → banco de quem recebe → barraca.
export const ROTA: Ponto[] = [
  [-7, 4.6],
  [-7, 2.6],
  [-3.4, 2.6],
  [-3.4, 0.4],
  [-1.2, 0.4],
  [-1.2, -3.6],
  [1.4, -3.6],
  [3.8, -3.6],
  [3.8, -2.2],
  [7.4, -2.2],
  [7.4, 2.6],
  [7, 2.6],
  [7, 4.8],
];

// Desvio da consulta de chave: seu banco pergunta ao DICT de quem é a chave.
export const CONSULTA: Ponto[] = [
  [-3.4, 0.4],
  [-5.2, 0.4],
  [-5.2, -1.0],
  [-8.2, -1.0],
];

export const comprimento = (rota: Ponto[]) =>
  rota.slice(1).reduce((s, p, i) => s + Math.hypot(p[0] - rota[i][0], p[1] - rota[i][1]), 0);

// Ponto da rota a uma distância d do início.
export const pontoNaRota = (rota: Ponto[], d: number): [number, number] => {
  let resto = d;
  for (let i = 1; i < rota.length; i++) {
    const [ax, az] = rota[i - 1];
    const [bx, bz] = rota[i];
    const seg = Math.hypot(bx - ax, bz - az);
    if (resto <= seg) return [ax + ((bx - ax) * resto) / seg, az + ((bz - az) * resto) / seg];
    resto -= seg;
  }
  const fim = rota[rota.length - 1];
  return [fim[0], fim[1]];
};

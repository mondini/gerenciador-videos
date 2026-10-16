// Dados da cena: tamanho do quadro, câmera isométrica e lugares da maquete.
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
  destaque: '#C9772E',
  destaqueClaro: '#F3D3B0',
  base: '#E9DEC8',
  terra: '#B8693F',
  terraEscura: '#8E4D2C',
  chao: '#C9A877',
  grama: '#9DB86C',
  mata: ['#2F5A34', '#3F6B3A', '#4F7D3F', '#365F38'],
  rio: '#5E9FB0',
  rioClaro: '#8CC3CF',
  seringa: ['#4E8A3C', '#D9B640', '#A0663A'],
};

// Câmera isométrica: olha na diagonal (1, 1, 1) para o alvo.
export const CAMERA = {
  alvo: new Vector3(-2.7, 0.4, 3.3),
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

// Lugares da maquete, em [x, z] no chão. O rio corre pela borda da frente (z alto).
export const LUGAR = {
  caixa: [-1.4, 1.2],
  serraria: [3.6, 3.2],
  vila: [-6.2, 2.6],
  seringal: [2.2, -3.6],
  rio: [-4, 6.6],
  barco: [4.2, 6.5],
} as const;

// Seringal: fileiras de árvores plantadas lado a lado.
export const SERINGAL = {x0: -3.4, z0: -6.6, colunas: 12, fileiras: 6, passo: 1.0};

// Saúde de cada seringueira no quadro: 0 sadia, 1 amarela, 2 seca, 3 sem folhas.
// A doença entra pelo canto do fundo à direita e avança pelas fileiras.
export const doenca = (col: number, fil: number, frame: number) => {
  const dist = Math.hypot(SERINGAL.colunas - 1 - col, fil);
  const frente = 1 + frame * 0.07;
  return Math.max(0, Math.min(3, frente - dist));
};

// Pseudoaleatório fixo, para a mata sair igual em todo render.
export const aleatorio = (semente: number) => {
  const x = Math.sin(semente * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

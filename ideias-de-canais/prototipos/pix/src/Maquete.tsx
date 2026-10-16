// A maquete isométrica: base, ruas, prédios, árvores, carros e o Pix andando pela rota.
import {useThree} from '@react-three/fiber';
import {useLayoutEffect} from 'react';
import {useCurrentFrame} from 'remotion';
import {CAMERA, CONSULTA, COR, LUGAR, ROTA, comprimento, pontoNaRota, posicaoCamera} from './cena';

type V3 = [number, number, number];

const Camera = () => {
  const camera = useThree((s) => s.camera);
  useLayoutEffect(() => {
    camera.position.copy(posicaoCamera());
    camera.lookAt(CAMERA.alvo);
    camera.zoom = CAMERA.zoom;
    camera.updateProjectionMatrix();
  }, [camera]);
  return null;
};

// Caixa com base no chão: pos é o centro da base.
const Caixa = ({
  pos,
  tam,
  cor,
  brilho,
  opacidade = 1,
  sombra = true,
}: {
  pos: V3;
  tam: V3;
  cor: string;
  brilho?: number;
  opacidade?: number;
  sombra?: boolean;
}) => (
  <mesh position={[pos[0], pos[1] + tam[1] / 2, pos[2]]} castShadow={sombra} receiveShadow>
    <boxGeometry args={tam} />
    <meshStandardMaterial
      color={cor}
      roughness={0.85}
      emissive={brilho ? cor : '#000000'}
      emissiveIntensity={brilho ?? 0}
      transparent={opacidade < 1}
      opacity={opacidade}
    />
  </mesh>
);

// Faixas de janela nas duas faces que a câmera vê (+x e +z).
const Janelas = ({pos, tam, andares, cor}: {pos: V3; tam: V3; andares: number; cor: string}) => {
  const [x, y, z] = pos;
  const [w, h, d] = tam;
  const passo = h / (andares + 1);
  return (
    <>
      {Array.from({length: andares}, (_, i) => {
        const yy = y + passo * (i + 0.75);
        return (
          <group key={i}>
            <Caixa pos={[x + w / 2 + 0.01, yy, z]} tam={[0.04, passo * 0.45, d * 0.8]} cor={cor} sombra={false} />
            <Caixa pos={[x, yy, z + d / 2 + 0.01]} tam={[w * 0.8, passo * 0.45, 0.04]} cor={cor} sombra={false} />
          </group>
        );
      })}
    </>
  );
};

const Predio = ({x, z, tam, cor, andares, janela = '#2E3F47'}: {x: number; z: number; tam: V3; cor: string; andares: number; janela?: string}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={tam} cor={cor} />
    <Caixa pos={[x, tam[1], z]} tam={[tam[0] + 0.12, 0.12, tam[2] + 0.12]} cor="#F7F1E6" />
    <Janelas pos={[x, 0, z]} tam={tam} andares={andares} cor={janela} />
  </group>
);

const Banco = ({x, z, cor}: {x: number; z: number; cor: string}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[3, 0.25, 3]} cor="#F7F1E6" />
    <Predio x={x} z={z} tam={[2.4, 3, 2.4]} cor={cor} andares={4} />
    {/* colunas da fachada */}
    {[-0.8, -0.27, 0.27, 0.8].map((dz) => (
      <mesh key={dz} position={[x + 1.35, 0.25 + 0.55, z + dz]} castShadow>
        <cylinderGeometry args={[0.08, 0.08, 1.1, 12]} />
        <meshStandardMaterial color="#F7F1E6" roughness={0.8} />
      </mesh>
    ))}
    <Caixa pos={[x + 1.35, 1.35, z]} tam={[0.3, 0.14, 2.2]} cor="#F7F1E6" />
  </group>
);

const BancoCentral = ({x, z, pulso}: {x: number; z: number; pulso: number}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[3.6, 0.35, 2.8]} cor="#D9CFBF" />
    <Caixa pos={[x, 0.35, z]} tam={[2.6, 0.9, 1.9]} cor="#3A4A52" />
    <Caixa pos={[x, 1.25, z]} tam={[2.2, 5.9, 1.5]} cor="#2C3A41" />
    {/* frisos verticais da fachada */}
    {[-0.75, -0.45, -0.15, 0.15, 0.45, 0.75].map((d) => (
      <group key={d}>
        <Caixa pos={[x + 1.11, 1.45, z + d * 0.9]} tam={[0.05, 5.4, 0.06]} cor="#8FA3AA" sombra={false} />
        <Caixa pos={[x + d * 1.3, 1.45, z + 0.76]} tam={[0.06, 5.4, 0.05]} cor="#8FA3AA" sombra={false} />
      </group>
    ))}
    <Caixa pos={[x, 7.15, z]} tam={[2.4, 0.18, 1.7]} cor="#3A4A52" />
    {/* onda no chão: o SPI está trabalhando */}
    {[0, 0.5].map((atraso) => {
      const t = (pulso + atraso) % 1;
      return (
        <mesh key={atraso} position={[x, 0.37, z]} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[1.6 + t * 1.6, 1.68 + t * 1.6, 64]} />
          <meshBasicMaterial color={COR.pix} transparent opacity={(1 - t) * 0.8} />
        </mesh>
      );
    })}
  </group>
);

const Dict = ({x, z}: {x: number; z: number}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[2.2, 0.2, 1.8]} cor="#D9CFBF" />
    {[-0.5, 0.5].map((dz) => (
      <group key={dz}>
        <Caixa pos={[x, 0.2, z + dz]} tam={[1.2, 1.7, 0.8]} cor="#46565E" />
        {[0.45, 0.8, 1.15, 1.5].map((y) => (
          <group key={y}>
            <Caixa pos={[x + 0.61, 0.2 + y, z + dz]} tam={[0.03, 0.14, 0.6]} cor="#2A363C" sombra={false} />
            <Caixa pos={[x + 0.63, 0.2 + y + 0.03, z + dz + 0.22]} tam={[0.02, 0.06, 0.06]} cor={COR.consulta} brilho={1.2} sombra={false} />
          </group>
        ))}
      </group>
    ))}
  </group>
);

const Casa = ({x, z}: {x: number; z: number}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[2.2, 1.5, 2]} cor="#F2C14E" />
    <mesh position={[x, 1.5 + 0.55, z]} rotation={[0, Math.PI / 4, 0]} castShadow>
      <coneGeometry args={[1.75, 1.1, 4]} />
      <meshStandardMaterial color={COR.terra} roughness={0.9} flatShading />
    </mesh>
    <Caixa pos={[x + 1.11, 0, z + 0.3]} tam={[0.04, 0.9, 0.5]} cor="#7A4A30" sombra={false} />
    <Caixa pos={[x + 1.11, 0.6, z - 0.5]} tam={[0.04, 0.45, 0.45]} cor="#2E3F47" sombra={false} />
    <Caixa pos={[x - 0.4, 0.6, z + 1.01]} tam={[0.5, 0.45, 0.04]} cor="#2E3F47" sombra={false} />
    <Caixa pos={[x + 0.4, 0.6, z + 1.01]} tam={[0.5, 0.45, 0.04]} cor="#2E3F47" sombra={false} />
  </group>
);

// O celular de quem paga, flutuando sobre a casa.
const Celular = ({x, z, frame}: {x: number; z: number; frame: number}) => {
  const y = 4.1 + Math.sin(frame / 14) * 0.08;
  return (
    <group position={[x, y, z]} rotation={[-0.15, Math.PI / 4, 0]}>
      <mesh castShadow>
        <boxGeometry args={[0.8, 1.45, 0.1]} />
        <meshStandardMaterial color="#1F2B30" roughness={0.4} />
      </mesh>
      <mesh position={[0, 0, 0.051]}>
        <planeGeometry args={[0.68, 1.28]} />
        <meshStandardMaterial color={COR.pix} emissive={COR.pix} emissiveIntensity={0.6} />
      </mesh>
      <mesh position={[0, -0.05, 0.053]}>
        <planeGeometry args={[0.5, 0.18]} />
        <meshBasicMaterial color="#FFFFFF" />
      </mesh>
      <mesh position={[0, 0.3, 0.053]}>
        <planeGeometry args={[0.34, 0.06]} />
        <meshBasicMaterial color="#E9FBF8" />
      </mesh>
    </group>
  );
};

const Barraca = ({x, z}: {x: number; z: number}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[2.4, 0.85, 1.2]} cor="#F7F1E6" />
    <Caixa pos={[x, 0.85, z]} tam={[2.5, 0.06, 1.3]} cor="#B9A98F" />
    {/* pastéis no balcão */}
    {[-0.8, -0.4, 0, 0.4].map((dx) => (
      <mesh key={dx} position={[x + dx, 0.95, z + 0.25]} rotation={[-Math.PI / 2, 0, 0]} castShadow>
        <circleGeometry args={[0.17, 16, 0, Math.PI]} />
        <meshStandardMaterial color="#E9B44C" side={2} />
      </mesh>
    ))}
    {[
      [-1.15, -0.6],
      [1.15, -0.6],
      [-1.15, 0.6],
      [1.15, 0.6],
    ].map(([dx, dz]) => (
      <Caixa key={`${dx}${dz}`} pos={[x + dx, 0, z + dz]} tam={[0.07, 2.1, 0.07]} cor="#8C8273" />
    ))}
    {/* toldo listrado de feira */}
    {Array.from({length: 7}, (_, i) => (
      <Caixa
        key={i}
        pos={[x - 1.2 + 0.4 * i, 2.1, z]}
        tam={[0.4, 0.1, 1.55]}
        cor={i % 2 ? '#F7F1E6' : '#2F7FC1'}
      />
    ))}
    {/* caixotes de feira */}
    <Caixa pos={[x + 1.6, 0, z + 0.4]} tam={[0.6, 0.45, 0.5]} cor="#C8955B" />
    <Caixa pos={[x + 1.6, 0.45, z + 0.4]} tam={[0.6, 0.45, 0.5]} cor="#B7834B" />
  </group>
);

const Arvore = ({x, z, cor, escala = 1}: {x: number; z: number; cor: string; escala?: number}) => (
  <group position={[x, 0, z]} scale={escala}>
    <mesh position={[0, 0.45, 0]} castShadow>
      <cylinderGeometry args={[0.07, 0.1, 0.9, 8]} />
      <meshStandardMaterial color="#6E4B33" />
    </mesh>
    <mesh position={[0, 1.15, 0]} castShadow>
      <icosahedronGeometry args={[0.6, 0]} />
      <meshStandardMaterial color={cor} roughness={0.9} flatShading />
    </mesh>
  </group>
);

const Carro = ({x, z, cor, giro = 0}: {x: number; z: number; cor: string; giro?: number}) => (
  <group position={[x, 0.02, z]} rotation={[0, giro, 0]}>
    <Caixa pos={[0, 0.08, 0]} tam={[0.9, 0.28, 0.45]} cor={cor} />
    <Caixa pos={[-0.05, 0.36, 0]} tam={[0.5, 0.22, 0.4]} cor="#DDE6E8" />
  </group>
);

const Onibus = ({x, z, giro = 0}: {x: number; z: number; giro?: number}) => (
  <group position={[x, 0.02, z]} rotation={[0, giro, 0]}>
    <Caixa pos={[0, 0.08, 0]} tam={[2.1, 0.6, 0.55]} cor="#F2C14E" />
    <Caixa pos={[0, 0.4, 0.28]} tam={[1.8, 0.18, 0.02]} cor="#2E3F47" sombra={false} />
    <Caixa pos={[0, 0.4, -0.28]} tam={[1.8, 0.18, 0.02]} cor="#2E3F47" sombra={false} />
  </group>
);

type Ponto = readonly [number, number];

// Linha do caminho, desenhada até a distância "ate"; o resto fica apagado.
const Caminho = ({rota, ate, cor, apagada}: {rota: Ponto[]; ate: number; cor: string; apagada: string}) => {
  const pecas: React.ReactNode[] = [];
  let andado = 0;
  for (let i = 1; i < rota.length; i++) {
    const [ax, az] = rota[i - 1];
    const [bx, bz] = rota[i];
    const seg = Math.hypot(bx - ax, bz - az);
    const feito = Math.max(0, Math.min(seg, ate - andado));
    const peca = (de: number, a: number, c: string, b: number, k: string) => {
      if (a - de < 0.001) return;
      const t0 = de / seg;
      const t1 = a / seg;
      const cx = ax + (bx - ax) * ((t0 + t1) / 2);
      const cz = az + (bz - az) * ((t0 + t1) / 2);
      const len = (a - de) + 0.16;
      const horiz = Math.abs(bx - ax) > 0.001;
      pecas.push(
        <Caixa key={k} pos={[cx, 0.03, cz]} tam={horiz ? [len, 0.07, 0.16] : [0.16, 0.07, len]} cor={c} brilho={b} sombra={false} />,
      );
    };
    peca(0, feito, cor, 0.9, `f${i}`);
    peca(feito, seg, apagada, 0, `a${i}`);
    andado += seg;
  }
  return <>{pecas}</>;
};

const Pacote = ({x, z, frame, rastro}: {x: number; z: number; frame: number; rastro: [number, number][]}) => {
  const y = 0.9 + Math.sin(frame / 6) * 0.06;
  return (
    <group>
      {rastro.map(([rx, rz], i) => (
        <mesh key={i} position={[rx, 0.6, rz]}>
          <boxGeometry args={[0.28 - i * 0.035, 0.28 - i * 0.035, 0.28 - i * 0.035]} />
          <meshBasicMaterial color={COR.pix} transparent opacity={0.55 - i * 0.08} />
        </mesh>
      ))}
      <mesh position={[x, y, z]} rotation={[frame / 20, frame / 15, 0]} castShadow>
        <boxGeometry args={[0.6, 0.6, 0.6]} />
        <meshStandardMaterial color={COR.pix} emissive={COR.pix} emissiveIntensity={0.9} />
      </mesh>
      <mesh position={[x, y, z]}>
        <sphereGeometry args={[0.85, 24, 16]} />
        <meshBasicMaterial color={COR.pixClaro} transparent opacity={0.25} />
      </mesh>
      <pointLight position={[x, y + 0.3, z]} color={COR.pix} intensity={6} distance={4} />
    </group>
  );
};

export const distanciaDoPix = (frame: number, total: number) => Math.min(total, (frame / 150) * total);

export const Maquete = () => {
  const frame = useCurrentFrame();
  const total = comprimento(ROTA);
  const d = distanciaDoPix(frame, total);
  const [px, pz] = pontoNaRota(ROTA, d);
  const rastro = [1, 2, 3, 4, 5].map((k) => pontoNaRota(ROTA, Math.max(0, d - k * 0.32)));
  // A consulta ao DICT acontece logo que o Pix chega ao seu banco.
  const consulta = Math.max(0, Math.min(1, (d - 7.8) / 1.5)) * comprimento(CONSULTA);

  return (
    <>
      <Camera />
      <hemisphereLight args={['#FFF6E8', '#B9A58A', 1.4]} />
      <directionalLight
        position={[-6, 16, 9]}
        intensity={2.2}
        color="#FFF1DC"
        castShadow
        shadow-mapSize={[4096, 4096]}
        shadow-camera-left={-16}
        shadow-camera-right={16}
        shadow-camera-top={16}
        shadow-camera-bottom={-16}
        shadow-bias={-0.0004}
      />

      {/* base da maquete, com o corte de terra à mostra */}
      <Caixa pos={[0, -0.95, 0]} tam={[21, 0.25, 15]} cor={COR.terraEscura} />
      <Caixa pos={[0, -0.7, 0]} tam={[21, 0.6, 15]} cor={COR.terra} />
      <Caixa pos={[0, -0.1, 0]} tam={[21, 0.1, 15]} cor={COR.base} />

      {/* quadras de grama */}
      {[
        [-7.6, 5.2, 4.8, 3.6],
        [-8.1, -3.4, 4.6, 7.8],
        [-3.2, -3.4, 3, 7.8],
        [1.3, -3.4, 4, 7.8],
        [7.4, -3.4, 5.6, 7.8],
        [1.3, 5.2, 7.2, 3.6],
        [7.6, 5.2, 4.8, 3.6],
      ].map(([x, z, w, dd]) => (
        <Caixa key={`${x}${z}`} pos={[x, 0, z]} tam={[w, 0.04, dd]} cor={COR.grama} />
      ))}

      {/* ruas */}
      <Caixa pos={[0, 0, 2.6]} tam={[21, 0.02, 1.3]} cor={COR.rua} />
      {[-5.2, -1.2, 3.8].map((x) => (
        <Caixa key={x} pos={[x, 0, -2.45]} tam={[1.3, 0.02, 10.1]} cor={COR.rua} />
      ))}
      {Array.from({length: 14}, (_, i) => -10 + i * 1.5).map((x) => (
        <Caixa key={x} pos={[x, 0.02, 2.95]} tam={[0.6, 0.01, 0.07]} cor={COR.faixa} sombra={false} />
      ))}

      {/* o caminho do Pix e a consulta de chave */}
      <Caminho rota={CONSULTA} ate={consulta} cor={COR.consulta} apagada="#E9D8B8" />
      <Caminho rota={ROTA} ate={d} cor={COR.pix} apagada="#BFD9D3" />

      <Casa x={LUGAR.casa[0]} z={LUGAR.casa[1]} />
      <Celular x={LUGAR.casa[0]} z={LUGAR.casa[1]} frame={frame} />
      <Banco x={LUGAR.bancoA[0]} z={LUGAR.bancoA[1]} cor="#E07A5F" />
      <Dict x={LUGAR.dict[0]} z={LUGAR.dict[1]} />
      <BancoCentral x={LUGAR.bc[0]} z={LUGAR.bc[1]} pulso={frame / 40} />
      <Banco x={LUGAR.bancoB[0]} z={LUGAR.bancoB[1]} cor="#5B8DB8" />
      <Barraca x={LUGAR.barraca[0]} z={LUGAR.barraca[1]} />

      {/* vizinhança */}
      <Predio x={-2.8} z={-6} tam={[2, 3.6, 1.6]} cor="#9CC5C0" andares={5} />
      <Predio x={7.6} z={-5.6} tam={[2.6, 2.6, 2.2]} cor="#E9D27E" andares={3} />
      <Predio x={0.2} z={5.2} tam={[2.2, 1.4, 1.8]} cor="#B9CBE0" andares={2} />
      <Predio x={2.9} z={5.6} tam={[1.6, 2, 1.6]} cor="#E7B7A3" andares={2} />

      {[
        [-9.3, 3.9, '#F4C430', 1],
        [-4.8, 5.8, '#6E9C4E', 0.9],
        [-4.6, 4.2, '#F4C430', 0.8],
        [-6.6, 0.7, '#6E9C4E', 1],
        [-8.8, -4.6, '#6E9C4E', 0.9],
        [-2.6, -2.2, '#F4C430', 1.1],
        [3.0, -0.8, '#6E9C4E', 0.85],
        [5.0, -4.6, '#F4C430', 1],
        [9.3, 4.2, '#6E9C4E', 0.9],
        [9.6, 0.2, '#F4C430', 0.8],
        [4.6, 6.2, '#F4C430', 0.9],
        [-1.6, 6.2, '#6E9C4E', 0.8],
        [9.2, -4, '#6E9C4E', 0.8],
      ].map(([x, z, c, e]) => (
        <Arvore key={`${x}${z}`} x={x as number} z={z as number} cor={c as string} escala={e as number} />
      ))}

      <Carro x={-8.8 + ((frame * 0.05) % 2)} z={2.25} cor="#C8553D" />
      <Carro x={1.6 - ((frame * 0.04) % 2)} z={2.95} cor="#3D6E8F" />
      <Carro x={-1.55} z={-5.2 + ((frame * 0.03) % 1.5)} cor="#F7F1E6" giro={Math.PI / 2} />
      <Onibus x={4.15} z={-5.4} giro={Math.PI / 2} />

      <Pacote x={px} z={pz} frame={frame} rastro={rastro} />
    </>
  );
};

// A maquete isométrica da Fordlândia: rio, vila americana, caixa-d'água, serraria, seringal doente e a mata voltando.
import {useThree} from '@react-three/fiber';
import {useLayoutEffect, useMemo} from 'react';
import {useCurrentFrame} from 'remotion';
import {Color, ExtrudeGeometry, Shape} from 'three';
import {CAMERA, COR, LUGAR, SERINGAL, aleatorio, doenca, posicaoCamera} from './cena';

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

// Telhado de duas águas: a cumeeira corre no eixo x.
const Telhado = ({pos, largura, comprimento, altura, cor}: {pos: V3; largura: number; comprimento: number; altura: number; cor: string}) => {
  const geo = useMemo(() => {
    const s = new Shape();
    s.moveTo(-largura / 2, 0);
    s.lineTo(largura / 2, 0);
    s.lineTo(0, altura);
    s.closePath();
    const g = new ExtrudeGeometry(s, {depth: comprimento, bevelEnabled: false});
    g.translate(0, 0, -comprimento / 2);
    g.rotateY(Math.PI / 2);
    return g;
  }, [largura, comprimento, altura]);
  return (
    <mesh geometry={geo} position={pos} castShadow receiveShadow>
      <meshStandardMaterial color={cor} roughness={0.9} flatShading />
    </mesh>
  );
};

const Casa = ({x, z, telhado}: {x: number; z: number; telhado: string}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[1.3, 0.75, 1.0]} cor="#F4EFE4" />
    <Telhado pos={[x, 0.75, z]} largura={1.2} comprimento={1.45} altura={0.5} cor={telhado} />
    {/* varanda */}
    <Caixa pos={[x + 0.2, 0, z + 0.62]} tam={[0.9, 0.06, 0.28]} cor="#D9CBB2" />
    <Caixa pos={[x + 0.2, 0.06, z + 0.74]} tam={[0.9, 0.04, 0.04]} cor="#F4EFE4" />
    <Caixa pos={[x - 0.3, 0.25, z + 0.51]} tam={[0.28, 0.25, 0.03]} cor="#3B4A52" sombra={false} />
    <Caixa pos={[x + 0.66, 0.25, z]} tam={[0.03, 0.25, 0.3]} cor="#3B4A52" sombra={false} />
  </group>
);

const CaixaDagua = ({x, z}: {x: number; z: number}) => {
  const altura = 5.4;
  return (
    <group>
      {[
        [-0.55, -0.55],
        [0.55, -0.55],
        [-0.55, 0.55],
        [0.55, 0.55],
      ].map(([dx, dz]) => (
        <Caixa key={`${dx}${dz}`} pos={[x + dx, 0, z + dz]} tam={[0.1, altura, 0.1]} cor="#8C969A" />
      ))}
      {/* travamentos em X das pernas */}
      {[1.4, 2.8, 4.2].map((y) => (
        <group key={y}>
          <Caixa pos={[x, y, z + 0.55]} tam={[1.1, 0.06, 0.06]} cor="#8C969A" sombra={false} />
          <Caixa pos={[x + 0.55, y, z]} tam={[0.06, 0.06, 1.1]} cor="#8C969A" sombra={false} />
        </group>
      ))}
      <mesh position={[x, altura + 0.6, z]} castShadow>
        <cylinderGeometry args={[0.95, 0.95, 1.2, 28]} />
        <meshStandardMaterial color="#C3CCCF" roughness={0.5} metalness={0.2} />
      </mesh>
      <mesh position={[x, altura + 1.45, z]} castShadow>
        <coneGeometry args={[1.0, 0.5, 28]} />
        <meshStandardMaterial color="#9DA8AC" roughness={0.5} metalness={0.2} />
      </mesh>
      {/* faixa com o nome, sem letras */}
      <mesh position={[x, altura + 0.65, z]}>
        <cylinderGeometry args={[0.96, 0.96, 0.22, 28, 1, true]} />
        <meshStandardMaterial color={COR.destaque} roughness={0.6} />
      </mesh>
    </group>
  );
};

const Fumaca = ({x, z, y0, frame}: {x: number; z: number; y0: number; frame: number}) => (
  <>
    {[0, 1, 2, 3, 4].map((i) => {
      const t = ((frame / 45 + i / 5) % 1 + 1) % 1;
      return (
        <mesh key={i} position={[x - t * 1.2, y0 + t * 2.2, z + t * 0.4]}>
          <sphereGeometry args={[0.2 + t * 0.35, 12, 10]} />
          <meshStandardMaterial color="#EDE6DA" transparent opacity={0.75 * (1 - t)} roughness={1} />
        </mesh>
      );
    })}
  </>
);

const Serraria = ({x, z, frame}: {x: number; z: number; frame: number}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[3.2, 1.3, 1.9]} cor="#B58B5C" />
    <Telhado pos={[x, 1.3, z]} largura={2.1} comprimento={3.4} altura={0.7} cor="#5D6B70" />
    {/* frestas das tábuas */}
    {[-1.2, -0.6, 0, 0.6, 1.2].map((dx) => (
      <Caixa key={dx} pos={[x + dx, 0, z + 0.96]} tam={[0.03, 1.3, 0.02]} cor="#8D6A44" sombra={false} />
    ))}
    <Caixa pos={[x - 0.3, 0, z + 0.96]} tam={[0.8, 0.9, 0.03]} cor="#4A3A2B" sombra={false} />
    <mesh position={[x + 1.2, 1.9, z - 0.4]} castShadow>
      <cylinderGeometry args={[0.2, 0.26, 3.8, 14]} />
      <meshStandardMaterial color="#8E4D2C" roughness={0.9} />
    </mesh>
    <Fumaca x={x + 1.2} z={z - 0.4} y0={4} frame={frame} />
    {/* toras empilhadas na beira do rio */}
    {[0, 1, 2, 3, 4].map((i) => (
      <mesh
        key={i}
        position={[x - 1.4 + (i % 3) * 0.32 + (i > 2 ? 0.16 : 0), 0.16 + (i > 2 ? 0.28 : 0), z + 1.7]}
        rotation={[Math.PI / 2, 0, 0]}
        castShadow
      >
        <cylinderGeometry args={[0.15, 0.15, 1.3, 10]} />
        <meshStandardMaterial color="#8A6440" roughness={0.9} />
      </mesh>
    ))}
  </group>
);

const Galpao = ({x, z}: {x: number; z: number}) => (
  <group>
    <Caixa pos={[x, 0, z]} tam={[2.6, 2.0, 1.6]} cor="#C9BBA0" />
    <Telhado pos={[x, 2.0, z]} largura={1.8} comprimento={2.8} altura={0.5} cor="#5D6B70" />
    {[0.5, 1.3].map((y) =>
      [-0.8, 0, 0.8].map((dx) => (
        <Caixa key={`${y}${dx}`} pos={[x + dx, y, z + 0.81]} tam={[0.45, 0.4, 0.03]} cor="#3B4A52" sombra={false} />
      )),
    )}
  </group>
);

const Barco = ({x, z}: {x: number; z: number}) => (
  <group position={[x, -0.2, z]}>
    <Caixa pos={[0, 0, 0]} tam={[2.6, 0.38, 0.95]} cor="#F4EFE4" />
    <Caixa pos={[0, 0.3, 0]} tam={[2.62, 0.08, 0.97]} cor="#B5432E" sombra={false} />
    <Caixa pos={[-0.15, 0.38, 0]} tam={[1.8, 0.42, 0.72]} cor="#F4EFE4" />
    <Caixa pos={[-0.15, 0.55, 0.37]} tam={[1.5, 0.14, 0.02]} cor="#3B4A52" sombra={false} />
    <Caixa pos={[-0.15, 0.8, 0]} tam={[2.0, 0.06, 0.86]} cor="#B5432E" />
    <Caixa pos={[0.5, 0.86, 0]} tam={[0.14, 0.45, 0.14]} cor="#3B4A52" />
  </group>
);

const Seringueira = ({x, z, estado}: {x: number; z: number; estado: number}) => {
  const cor = useMemo(() => {
    const [sadia, amarela, seca] = COR.seringa.map((c) => new Color(c));
    if (estado <= 1) return sadia.clone().lerp(amarela, estado);
    return amarela.clone().lerp(seca, Math.min(1, estado - 1));
  }, [estado]);
  const copa = estado <= 2 ? 1 - estado * 0.12 : Math.max(0, 0.76 * (3 - estado));
  return (
    <group position={[x, 0, z]}>
      {/* folhas caídas no chão */}
      {estado > 1.4 ? (
        <mesh position={[0.05, 0.035, 0.05]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
          <circleGeometry args={[0.18 + Math.min(1, estado - 1.4) * 0.22, 7]} />
          <meshStandardMaterial color="#B07A3E" roughness={1} />
        </mesh>
      ) : null}
      <mesh position={[0, 0.4, 0]} castShadow>
        <cylinderGeometry args={[0.05, 0.07, 0.8, 6]} />
        <meshStandardMaterial color="#7A5A3E" />
      </mesh>
      {estado > 2.2 ? (
        <>
          <Caixa pos={[0.12, 0.6, 0]} tam={[0.25, 0.03, 0.03]} cor="#7A5A3E" sombra={false} />
          <Caixa pos={[0, 0.7, -0.1]} tam={[0.03, 0.03, 0.22]} cor="#7A5A3E" sombra={false} />
        </>
      ) : null}
      {copa > 0.02 ? (
        <mesh position={[0, 0.95, 0]} scale={copa} castShadow>
          <icosahedronGeometry args={[0.42, 0]} />
          <meshStandardMaterial color={cor} roughness={0.9} flatShading />
        </mesh>
      ) : null}
    </group>
  );
};

const ArvoreMata = ({x, z, escala, cor, palmeira}: {x: number; z: number; escala: number; cor: string; palmeira: boolean}) =>
  palmeira ? (
    <group position={[x, 0, z]} scale={escala}>
      <mesh position={[0, 1.1, 0]} castShadow>
        <cylinderGeometry args={[0.05, 0.07, 2.2, 6]} />
        <meshStandardMaterial color="#6E5A44" />
      </mesh>
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <mesh key={i} position={[0, 2.2, 0]} rotation={[0, (i * Math.PI) / 3, 0.55]} castShadow>
          <boxGeometry args={[0.06, 0.04, 1.2]} />
          <meshStandardMaterial color={cor} />
        </mesh>
      ))}
    </group>
  ) : (
    <group position={[x, 0, z]} scale={escala}>
      <mesh position={[0, 0.5, 0]} castShadow>
        <cylinderGeometry args={[0.08, 0.12, 1.0, 6]} />
        <meshStandardMaterial color="#5E4632" />
      </mesh>
      <mesh position={[0, 1.35, 0]} castShadow>
        <icosahedronGeometry args={[0.75, 0]} />
        <meshStandardMaterial color={cor} roughness={0.95} flatShading />
      </mesh>
      <mesh position={[0.35, 1.0, 0.2]} castShadow>
        <icosahedronGeometry args={[0.45, 0]} />
        <meshStandardMaterial color={cor} roughness={0.95} flatShading />
      </mesh>
    </group>
  );

// A mata em volta: faixa da direita e canto do fundo à esquerda.
const MATA = (() => {
  const arvores: {x: number; z: number; escala: number; cor: string; palmeira: boolean}[] = [];
  let s = 1;
  const plantar = (x0: number, x1: number, z0: number, z1: number, passo: number) => {
    for (let x = x0; x <= x1; x += passo)
      for (let z = z0; z <= z1; z += passo) {
        s++;
        arvores.push({
          x: x + (aleatorio(s) - 0.5) * passo * 0.8,
          z: z + (aleatorio(s + 99) - 0.5) * passo * 0.8,
          escala: 0.75 + aleatorio(s + 7) * 0.6,
          cor: COR.mata[Math.floor(aleatorio(s + 3) * COR.mata.length)],
          palmeira: aleatorio(s + 11) < 0.22,
        });
      }
  };
  plantar(8.6, 10.2, -7.1, 4.4, 1.15);
  plantar(-10.2, -4.6, -7.1, -2.4, 1.15);
  return arvores;
})();

// Mudas que a mata vai empurrando para dentro da cidade.
const INVASAO: [number, number, number][] = [
  [7.6, 1.6, 0],
  [7.9, -0.6, 10],
  [6.6, 3.8, 25],
  [-3.6, -1.6, 15],
  [-8.2, -1.6, 5],
  [-9.6, 0.4, 20],
  [-9.8, 3.4, 30],
  [-5.0, -1.3, 40],
  [5.8, 0.2, 45],
  [1.4, -0.9, 55],
];

export const Maquete = () => {
  const frame = useCurrentFrame();

  return (
    <>
      <Camera />
      <hemisphereLight args={['#FFF3E0', '#A58E6A', 1.35]} />
      <directionalLight
        position={[-7, 15, 9]}
        intensity={2.3}
        color="#FFE8C8"
        castShadow
        shadow-mapSize={[4096, 4096]}
        shadow-camera-left={-16}
        shadow-camera-right={16}
        shadow-camera-top={16}
        shadow-camera-bottom={-16}
        shadow-bias={-0.0004}
      />

      {/* base: corte de terra, chão firme até o rio e o leito do rio */}
      <Caixa pos={[0, -0.95, 0]} tam={[21, 0.25, 15]} cor={COR.terraEscura} />
      <Caixa pos={[0, -0.7, -1.25]} tam={[21, 0.6, 12.5]} cor={COR.terra} />
      <Caixa pos={[0, -0.1, -1.25]} tam={[21, 0.1, 12.5]} cor={COR.base} />
      <Caixa pos={[0, -0.7, 6.25]} tam={[21, 0.45, 2.5]} cor="#4C8697" />
      <Caixa pos={[0, -0.25, 6.25]} tam={[21, 0.12, 2.5]} cor={COR.rio} opacidade={0.92} sombra={false} />
      {[0, 1, 2, 3, 4, 5].map((i) => {
        const x = ((i * 3.7 + frame * 0.03) % 21) - 10.5;
        return <Caixa key={i} pos={[x, -0.12, 5.6 + (i % 3) * 0.7]} tam={[1.2, 0.01, 0.06]} cor={COR.rioClaro} sombra={false} />;
      })}

      {/* clareira da cidade, gramado do seringal e chão da mata */}
      <Caixa pos={[-1.6, 0, 1.6]} tam={[19.6, 0.03, 6.6]} cor={COR.chao} />
      <Caixa pos={[2.1, 0, -4.3]} tam={[12.8, 0.03, 6.2]} cor={COR.grama} />
      <Caixa pos={[9.4, 0, -1.3]} tam={[2.2, 0.03, 12.4]} cor="#55784A" />
      <Caixa pos={[-7.4, 0, -4.8]} tam={[6.2, 0.03, 5.4]} cor="#55784A" />

      {/* ruas de terra */}
      <Caixa pos={[-2.4, 0.01, 4.0]} tam={[16, 0.02, 0.8]} cor="#E2CDA3" />
      <Caixa pos={[-0.4, 0.01, 1.4]} tam={[0.8, 0.02, 5.2]} cor="#E2CDA3" />
      <Caixa pos={[-5.6, 0.01, 1.6]} tam={[8.4, 0.02, 0.6]} cor="#E2CDA3" />

      {/* píer */}
      <Caixa pos={[-0.4, 0.02, 5.4]} tam={[0.9, 0.08, 1.9]} cor="#8A6440" />
      {[4.8, 5.6, 6.2].map((z) => (
        <Caixa key={z} pos={[0.1, -0.5, z]} tam={[0.1, 0.6, 0.1]} cor="#6B4C30" />
      ))}

      {/* vila americana */}
      {[-9.2, -7.6, -6.0, -4.4, -2.8].map((x, i) => (
        <group key={x}>
          <Casa x={x} z={2.7} telhado={i % 2 ? '#3E6E5C' : '#B5432E'} />
          {i < 4 ? <Casa x={x + 0.4} z={0.4} telhado={i % 2 ? '#B5432E' : '#3E6E5C'} /> : null}
        </group>
      ))}

      <CaixaDagua x={LUGAR.caixa[0]} z={LUGAR.caixa[1]} />
      <Serraria x={LUGAR.serraria[0]} z={LUGAR.serraria[1]} frame={frame} />
      <Galpao x={3.2} z={0.2} />
      <Barco x={LUGAR.barco[0] - frame * 0.012} z={LUGAR.barco[1]} />

      {/* seringal: fileiras retas, e a doença avançando */}
      {Array.from({length: SERINGAL.colunas}, (_, c) =>
        Array.from({length: SERINGAL.fileiras}, (_, f) => (
          <Seringueira
            key={`${c}-${f}`}
            x={SERINGAL.x0 + c * SERINGAL.passo}
            z={SERINGAL.z0 + f * SERINGAL.passo}
            estado={doenca(c, f, frame)}
          />
        )),
      )}

      {MATA.map((a, i) => (
        <ArvoreMata key={i} {...a} />
      ))}
      {INVASAO.map(([x, z, inicio], i) => {
        const e = Math.max(0, Math.min(0.75, (frame - inicio) / 80));
        return e > 0.02 ? <ArvoreMata key={i} x={x} z={z} escala={e} cor={COR.mata[i % 4]} palmeira={i % 3 === 0} /> : null;
      })}
    </>
  );
};

// Quadro completo: maquete isométrica (three.js) + camada de infográfico em HTML/SVG (d3 para o mapa).
import {loadFont as carregarArchivo} from '@remotion/google-fonts/Archivo';
import {loadFont as carregarMono} from '@remotion/google-fonts/IBMPlexMono';
import {ThreeCanvas} from '@remotion/three';
import {geoMercator, geoPath} from 'd3-geo';
import type {FeatureCollection} from 'geojson';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import brasil from '../dados/brasil-uf.json';
import {ALTURA, COR, LARGURA, LUGAR, ROTA, comprimento, naTela, pontoNaRota} from './cena';
import {Maquete, distanciaDoPix} from './Maquete';

const {fontFamily: archivo} = carregarArchivo('normal', {weights: ['500', '700', '800'], subsets: ['latin']});
const {fontFamily: mono} = carregarMono('normal', {weights: ['500'], subsets: ['latin']});

const ETAPAS = [
  {ate: 5.6, titulo: 'Você aperta "enviar"', texto: 'O celular manda a ordem para o seu banco.'},
  {ate: 16.6, titulo: 'Seu banco acha a chave', texto: 'Consulta o DICT, o diretório de chaves do Pix.'},
  {ate: 24, titulo: 'O Banco Central liquida', texto: 'No SPI, o dinheiro passa de um banco para o outro.'},
  {ate: Infinity, titulo: 'A barraca recebe', texto: 'O banco de quem recebe põe o valor na conta.'},
];

const LEGENDA = 'No Banco Central, o SPI passa o dinheiro de um banco para o outro.'.split(' ');

const Rotulo = ({
  x,
  y,
  texto,
  sub,
  ativo,
  apagado,
  abaixo,
}: {
  x: number;
  y: number;
  texto: string;
  sub?: string;
  ativo?: boolean;
  apagado?: boolean;
  abaixo?: boolean;
}) => {
  const ponta = (
    <div
      style={{
        width: 0,
        height: 0,
        borderLeft: '8px solid transparent',
        borderRight: '8px solid transparent',
        [abaixo ? 'borderBottom' : 'borderTop']: `9px solid ${ativo ? COR.pix : '#FFFDF8'}`,
      }}
    />
  );
  return (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      transform: abaixo ? 'translate(-50%, 0)' : 'translate(-50%, -100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      opacity: apagado ? 0.55 : 1,
    }}
  >
    {abaixo ? ponta : null}
    <div
      style={{
        background: ativo ? COR.pix : '#FFFDF8',
        color: ativo ? '#FFFFFF' : COR.tinta,
        borderRadius: 14,
        padding: sub ? '8px 16px 9px' : '8px 16px',
        boxShadow: '0 6px 18px rgba(60, 40, 20, 0.16)',
        textAlign: 'center',
        whiteSpace: 'nowrap',
      }}
    >
      <div style={{fontFamily: archivo, fontWeight: 700, fontSize: 22, lineHeight: 1.1}}>{texto}</div>
      {sub ? (
        <div style={{fontFamily: mono, fontSize: 15, marginTop: 3, opacity: ativo ? 0.9 : 0.6, letterSpacing: 0.5}}>
          {sub}
        </div>
      ) : null}
    </div>
    {abaixo ? null : ponta}
  </div>
  );
};

// Mapa do Brasil (malha do IBGE) com o arco de Porto Alegre a Manaus.
// O IBGE segue a regra do GeoJSON (anel externo anti-horário); o d3 espera o contrário.
const malha: FeatureCollection = {
  ...(brasil as unknown as FeatureCollection),
  features: (brasil as unknown as FeatureCollection).features.map((f) => {
    const g = f.geometry as {type: string; coordinates: number[][][] | number[][][][]};
    const inverte = (poligono: number[][][]) => poligono.map((anel) => [...anel].reverse());
    const coordinates =
      g.type === 'Polygon'
        ? inverte(g.coordinates as number[][][])
        : (g.coordinates as number[][][][]).map(inverte);
    return {...f, geometry: {...g, coordinates} as FeatureCollection['features'][number]['geometry']};
  }),
};

const Mapa = ({progresso}: {progresso: number}) => {
  const L = 250;
  const projecao = geoMercator().fitSize([L, L], malha);
  const caminho = geoPath(projecao);
  const poa = projecao([-51.23, -30.03])!;
  const mao = projecao([-60.02, -3.1])!;
  const meio = [(poa[0] + mao[0]) / 2 + 70, (poa[1] + mao[1]) / 2 + 10];
  const arco = `M${poa[0]},${poa[1]} Q${meio[0]},${meio[1]} ${mao[0]},${mao[1]}`;
  return (
    <svg width={L} height={L} style={{overflow: 'visible'}}>
      {malha.features.map((f) => {
        const uf = (f.properties as {codarea: string}).codarea;
        const destaque = uf === '43' || uf === '13';
        return (
          <path
            key={uf}
            d={caminho(f) ?? ''}
            fill={destaque ? '#CDEDE8' : COR.papelEscuro}
            stroke="#FFFDF8"
            strokeWidth={1}
          />
        );
      })}
      <path d={arco} fill="none" stroke={COR.pix} strokeOpacity={0.25} strokeWidth={4} strokeDasharray="2 7" strokeLinecap="round" />
      <path d={arco} fill="none" stroke={COR.pix} strokeWidth={4} strokeLinecap="round" pathLength={1} strokeDasharray={`${progresso} 1`} />
      <circle cx={poa[0]} cy={poa[1]} r={6} fill={COR.tinta} />
      <circle cx={mao[0]} cy={mao[1]} r={6} fill={COR.pix} stroke="#FFFDF8" strokeWidth={2} />
      <text x={poa[0] + 12} y={poa[1] + 6} fontFamily={archivo} fontWeight={700} fontSize={16} fill={COR.tinta}>
        Porto Alegre
      </text>
      <text x={mao[0] - 4} y={mao[1] - 14} fontFamily={archivo} fontWeight={700} fontSize={16} fill={COR.tinta}>
        Manaus
      </text>
    </svg>
  );
};

export const Pix = () => {
  const frame = useCurrentFrame();
  const total = comprimento(ROTA);
  const d = distanciaDoPix(frame, total);
  const etapa = ETAPAS.findIndex((e) => d < e.ate);
  const [px, pz] = pontoNaRota(ROTA, d);
  const pacote = naTela(px, 1.35, pz);
  const palavra = Math.floor(interpolate(frame, [70, 130], [0, LEGENDA.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));

  const r = (lugar: readonly [number, number], y: number) => naTela(lugar[0], y, lugar[1]);
  const casa = r(LUGAR.casa, 5.1);
  const bancoA = r(LUGAR.bancoA, 4.3);
  const dict = naTela(LUGAR.dict[0] + 0.9, 3.4, LUGAR.dict[1] - 0.9);
  const bc = r(LUGAR.bc, 7.6);
  const bancoB = naTela(LUGAR.bancoB[0] + 1.5, 0.3, LUGAR.bancoB[1] + 1.5);
  const barraca = r(LUGAR.barraca, 2.6);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse 70% 80% at 62% 48%, #FBF5EA 0%, ${COR.papel} 55%, #EADDC7 100%)`,
      }}
    >
      {/* grade de pontos do papel */}
      <AbsoluteFill
        style={{
          backgroundImage: 'radial-gradient(rgba(31,43,48,0.10) 1.2px, transparent 1.2px)',
          backgroundSize: '28px 28px',
        }}
      />

      <ThreeCanvas width={LARGURA} height={ALTURA} orthographic flat shadows camera={{near: 0.1, far: 200}}>
        <Maquete />
      </ThreeCanvas>

      {/* rótulos presos à maquete */}
      <Rotulo x={casa.x} y={casa.y} texto="Você" sub="paga R$ 12,00" apagado={etapa > 0} />
      <Rotulo x={bancoA.x} y={bancoA.y} texto="Seu banco" apagado={etapa > 1} />
      <Rotulo x={dict.x} y={dict.y} texto="DICT" sub="diretório de chaves" apagado={etapa > 1} />
      <Rotulo x={bc.x} y={bc.y} texto="Banco Central" sub="SPI" ativo={etapa === 2} />
      <Rotulo x={bancoB.x} y={bancoB.y} texto="Banco de quem recebe" abaixo />
      <Rotulo x={barraca.x} y={barraca.y} texto="Barraca de pastel" />
      <div
        style={{
          position: 'absolute',
          left: pacote.x,
          top: pacote.y,
          transform: 'translate(-50%, -100%)',
          fontFamily: mono,
          fontWeight: 500,
          fontSize: 18,
          color: COR.tinta,
          background: COR.pixClaro,
          borderRadius: 8,
          padding: '3px 9px',
        }}
      >
        R$ 12,00
      </div>

      {/* coluna do infográfico */}
      <div style={{position: 'absolute', left: 88, top: 78, width: 520}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 12}}>
          <div style={{display: 'flex', gap: 4}}>
            <div style={{width: 12, height: 12, borderRadius: 3, background: '#2E9E5B'}} />
            <div style={{width: 12, height: 12, borderRadius: 3, background: '#F2C14E'}} />
            <div style={{width: 12, height: 12, borderRadius: 3, background: '#2F5DA8'}} />
          </div>
          <div style={{fontFamily: archivo, fontWeight: 700, fontSize: 18, letterSpacing: 4, color: COR.tintaSuave}}>
            BRASIL POR DENTRO
          </div>
        </div>
        <div
          style={{
            fontFamily: archivo,
            fontWeight: 800,
            fontSize: 84,
            lineHeight: 0.98,
            letterSpacing: -2,
            color: COR.tinta,
            marginTop: 22,
          }}
        >
          O caminho
          <br />
          de um <span style={{color: COR.pix}}>Pix</span>
        </div>

        <div style={{marginTop: 44, display: 'flex', flexDirection: 'column', gap: 18}}>
          {ETAPAS.map((e, i) => {
            const feita = i < etapa;
            const atual = i === etapa;
            return (
              <div key={e.titulo} style={{display: 'flex', gap: 16, alignItems: 'flex-start', opacity: i > etapa ? 0.45 : 1}}>
                <div
                  style={{
                    width: 38,
                    height: 38,
                    flexShrink: 0,
                    borderRadius: 19,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontFamily: mono,
                    fontSize: 18,
                    fontWeight: 500,
                    background: atual ? COR.pix : feita ? COR.tinta : 'transparent',
                    color: atual || feita ? '#FFFFFF' : COR.tinta,
                    border: atual || feita ? 'none' : `2px solid ${COR.tinta}`,
                    boxShadow: atual ? `0 0 0 6px ${COR.pixClaro}` : 'none',
                  }}
                >
                  {feita ? '✓' : i + 1}
                </div>
                <div>
                  <div style={{fontFamily: archivo, fontWeight: 700, fontSize: 26, color: COR.tinta, lineHeight: 1.15}}>
                    {e.titulo}
                  </div>
                  {atual ? (
                    <div style={{fontFamily: archivo, fontWeight: 500, fontSize: 20, color: COR.tintaSuave, marginTop: 4, lineHeight: 1.3, maxWidth: 400}}>
                      {e.texto}
                    </div>
                  ) : null}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* cartão do mapa */}
      <div
        style={{
          position: 'absolute',
          left: 88,
          bottom: 70,
          width: 430,
          background: 'rgba(255, 253, 248, 0.82)',
          borderRadius: 22,
          padding: '22px 24px',
          boxShadow: '0 10px 30px rgba(60, 40, 20, 0.10)',
          display: 'flex',
          gap: 18,
          alignItems: 'center',
        }}
      >
        <div style={{width: 170, height: 170, flexShrink: 0}}>
          <div style={{transform: 'scale(0.68)', transformOrigin: 'top left'}}>
            <Mapa progresso={interpolate(frame, [30, 140], [0.05, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
          </div>
        </div>
        <div>
          <div style={{fontFamily: mono, fontSize: 15, color: COR.tintaSuave, letterSpacing: 1}}>DISTÂNCIA</div>
          <div style={{fontFamily: archivo, fontWeight: 800, fontSize: 40, color: COR.tinta, lineHeight: 1.05, marginTop: 4}}>
            3.100 km
          </div>
          <div style={{fontFamily: archivo, fontWeight: 500, fontSize: 19, color: COR.tintaSuave, marginTop: 6, lineHeight: 1.3}}>
            em linha reta, e o Pix chega em segundos
          </div>
        </div>
      </div>

      {/* legenda da narração, palavra por palavra */}
      <div
        style={{
          position: 'absolute',
          left: 600,
          right: 60,
          bottom: 56,
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <div
          style={{
            fontFamily: archivo,
            fontWeight: 700,
            fontSize: 30,
            background: 'rgba(31, 43, 48, 0.86)',
            color: '#FFFFFF',
            borderRadius: 16,
            padding: '14px 26px',
            whiteSpace: 'nowrap',
            textAlign: 'center',
            lineHeight: 1.3,
          }}
        >
          {LEGENDA.map((p, i) => (
            <span key={i} style={{color: i < palavra ? '#FFFFFF' : i === palavra ? COR.pixClaro : 'rgba(255,255,255,0.4)'}}>
              {p}{' '}
            </span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

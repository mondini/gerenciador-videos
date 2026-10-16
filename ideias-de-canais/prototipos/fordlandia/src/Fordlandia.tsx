// Quadro completo: maquete isométrica (three.js) + linha do tempo, mapa das Américas (d3) e legenda.
import {loadFont as carregarArchivo} from '@remotion/google-fonts/Archivo';
import {loadFont as carregarMono} from '@remotion/google-fonts/IBMPlexMono';
import {ThreeCanvas} from '@remotion/three';
import {geoMercator, geoPath} from 'd3-geo';
import type {Feature, FeatureCollection, MultiPolygon, Polygon} from 'geojson';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {feature} from 'topojson-client';
import type {GeometryCollection, Topology} from 'topojson-specification';
import mundo from 'world-atlas/countries-110m.json';
import {ALTURA, COR, LARGURA, LUGAR, naTela} from './cena';
import {Maquete} from './Maquete';

const {fontFamily: archivo} = carregarArchivo('normal', {weights: ['500', '700', '800'], subsets: ['latin']});
const {fontFamily: mono} = carregarMono('normal', {weights: ['500'], subsets: ['latin']});

const ETAPAS = [
  {ano: '1928', titulo: 'Ford funda a cidade no Tapajós', texto: ''},
  {ano: '1930', titulo: 'A Revolta do Quebra-Panelas', texto: ''},
  {ano: 'anos 30', titulo: 'Pragas tomam o seringal', texto: 'Plantadas lado a lado, as seringueiras adoecem uma atrás da outra.'},
  {ano: '1945', titulo: 'A Ford vende tudo ao governo', texto: ''},
];
const ETAPA_ATUAL = 2;

const LEGENDA = 'Plantadas lado a lado, as seringueiras viraram um banquete para pragas e fungos.'.split(' ');

const Rotulo = ({
  x,
  y,
  texto,
  sub,
  ativo,
}: {
  x: number;
  y: number;
  texto: string;
  sub?: string;
  ativo?: boolean;
}) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      transform: 'translate(-50%, -100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    }}
  >
    <div
      style={{
        background: ativo ? COR.destaque : '#FFFDF8',
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
        <div style={{fontFamily: mono, fontSize: 15, marginTop: 3, opacity: ativo ? 0.9 : 0.6, letterSpacing: 0.5}}>{sub}</div>
      ) : null}
    </div>
    <div
      style={{
        width: 0,
        height: 0,
        borderLeft: '8px solid transparent',
        borderRight: '8px solid transparent',
        borderTop: `9px solid ${ativo ? COR.destaque : '#FFFDF8'}`,
      }}
    />
  </div>
);

const topo = mundo as unknown as Topology<{countries: GeometryCollection}>;
const paises = feature(topo, topo.objects.countries) as FeatureCollection<Polygon | MultiPolygon>;

// Mapa das Américas com o arco de Detroit à Fordlândia.
const Mapa = ({progresso}: {progresso: number}) => {
  const L = 190;
  const A = 230;
  const recorte: Feature = {
    type: 'Feature',
    properties: {},
    geometry: {type: 'MultiPoint', coordinates: [[-105, 50], [-35, -35]]},
  };
  const projecao = geoMercator().fitSize([L, A], recorte);
  const caminho = geoPath(projecao);
  const detroit = projecao([-83.05, 42.33])!;
  const ford = projecao([-55.5, -3.83])!;
  const meio = [(detroit[0] + ford[0]) / 2 + 60, (detroit[1] + ford[1]) / 2 - 10];
  const arco = `M${detroit[0]},${detroit[1]} Q${meio[0]},${meio[1]} ${ford[0]},${ford[1]}`;
  return (
    <svg width={L} height={A} style={{overflow: 'hidden', borderRadius: 12}}>
      <rect width={L} height={A} fill="#E4EEF0" />
      {paises.features.map((f, i) => {
        const id = String(f.id);
        const destaque = id === '076' || id === '840';
        return <path key={i} d={caminho(f) ?? ''} fill={destaque ? COR.destaqueClaro : COR.papelEscuro} stroke="#FFFDF8" strokeWidth={0.6} />;
      })}
      <path d={arco} fill="none" stroke={COR.destaque} strokeOpacity={0.3} strokeWidth={3} strokeDasharray="2 6" strokeLinecap="round" />
      <path d={arco} fill="none" stroke={COR.destaque} strokeWidth={3} strokeLinecap="round" pathLength={1} strokeDasharray={`${progresso} 1`} />
      <circle cx={detroit[0]} cy={detroit[1]} r={5} fill={COR.tinta} />
      <circle cx={ford[0]} cy={ford[1]} r={5} fill={COR.destaque} stroke="#FFFDF8" strokeWidth={2} />
      <text x={detroit[0] - 8} y={detroit[1] - 10} fontFamily={archivo} fontWeight={700} fontSize={14} fill={COR.tinta} textAnchor="middle">
        Detroit
      </text>
      <text x={ford[0] - 8} y={ford[1] + 20} fontFamily={archivo} fontWeight={700} fontSize={14} fill={COR.tinta} textAnchor="middle">
        Fordlândia
      </text>
    </svg>
  );
};

export const Fordlandia = () => {
  const frame = useCurrentFrame();
  const palavra = Math.floor(interpolate(frame, [60, 140], [0, LEGENDA.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));

  const caixa = naTela(LUGAR.caixa[0], 7.6, LUGAR.caixa[1]);
  const vila = naTela(-8.0, 1.8, 1.6);
  const serraria = naTela(LUGAR.serraria[0], 2.4, LUGAR.serraria[1]);
  const seringal = naTela(LUGAR.seringal[0], 1.8, LUGAR.seringal[1]);
  const rio = naTela(-7.5, 0.3, 6.4);
  const mata = naTela(9.4, 3.2, -6.0);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse 70% 80% at 62% 48%, #FBF5EA 0%, ${COR.papel} 55%, #EADDC7 100%)`,
      }}
    >
      <AbsoluteFill
        style={{
          backgroundImage: 'radial-gradient(rgba(31,43,48,0.10) 1.2px, transparent 1.2px)',
          backgroundSize: '28px 28px',
        }}
      />

      <ThreeCanvas width={LARGURA} height={ALTURA} orthographic flat shadows camera={{near: 0.1, far: 200}}>
        <Maquete />
      </ThreeCanvas>

      <Rotulo x={caixa.x} y={caixa.y} texto="Caixa-d'água" sub="o símbolo da cidade" />
      <Rotulo x={vila.x} y={vila.y} texto="Vila Americana" />
      <Rotulo x={serraria.x} y={serraria.y} texto="Serraria" />
      <Rotulo x={seringal.x} y={seringal.y} texto="Seringal" sub="pragas e fungos" ativo />
      <Rotulo x={rio.x} y={rio.y} texto="Rio Tapajós" />
      <Rotulo x={mata.x} y={mata.y} texto="Floresta" />

      {/* coluna da linha do tempo */}
      <div style={{position: 'absolute', left: 88, top: 78, width: 520}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 12}}>
          <div style={{display: 'flex', gap: 4}}>
            <div style={{width: 12, height: 12, borderRadius: 3, background: '#2E9E5B'}} />
            <div style={{width: 12, height: 12, borderRadius: 3, background: '#F2C14E'}} />
            <div style={{width: 12, height: 12, borderRadius: 3, background: '#2F5DA8'}} />
          </div>
          <div style={{fontFamily: archivo, fontWeight: 700, fontSize: 18, letterSpacing: 4, color: COR.tintaSuave}}>
            BRASIL POR DENTRO · CASOS
          </div>
        </div>
        <div style={{fontFamily: archivo, fontWeight: 800, fontSize: 92, lineHeight: 0.95, letterSpacing: -2.5, color: COR.tinta, marginTop: 22}}>
          Fordlândia
        </div>
        <div style={{fontFamily: archivo, fontWeight: 700, fontSize: 27, lineHeight: 1.15, color: COR.destaque, marginTop: 10, whiteSpace: 'nowrap'}}>
          A cidade da Ford que a Amazônia engoliu
        </div>

        <div style={{marginTop: 46, position: 'relative'}}>
          <div style={{position: 'absolute', left: 87, top: 14, bottom: 14, width: 2, background: 'rgba(31,43,48,0.18)'}} />
          {ETAPAS.map((e, i) => {
            const atual = i === ETAPA_ATUAL;
            const futura = i > ETAPA_ATUAL;
            return (
              <div key={e.ano} style={{display: 'flex', gap: 18, alignItems: 'flex-start', marginBottom: 20, opacity: futura ? 0.45 : 1}}>
                <div style={{width: 64, textAlign: 'right', whiteSpace: 'nowrap', fontFamily: mono, fontSize: 15, color: atual ? COR.destaque : COR.tintaSuave, paddingTop: 6, flexShrink: 0}}>
                  {e.ano}
                </div>
                <div
                  style={{
                    width: 14,
                    height: 14,
                    marginTop: 8,
                    marginLeft: -2,
                    flexShrink: 0,
                    borderRadius: 7,
                    background: atual ? COR.destaque : futura ? COR.papel : COR.tinta,
                    border: futura ? `2px solid ${COR.tinta}` : 'none',
                    boxShadow: atual ? `0 0 0 6px ${COR.destaqueClaro}` : 'none',
                    position: 'relative',
                  }}
                />
                <div>
                  <div style={{fontFamily: archivo, fontWeight: 700, fontSize: 25, color: COR.tinta, lineHeight: 1.15}}>{e.titulo}</div>
                  {atual ? (
                    <div style={{fontFamily: archivo, fontWeight: 500, fontSize: 19, color: COR.tintaSuave, marginTop: 4, lineHeight: 1.3, maxWidth: 380}}>
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
          padding: '20px 22px',
          boxShadow: '0 10px 30px rgba(60, 40, 20, 0.10)',
          display: 'flex',
          gap: 20,
          alignItems: 'center',
        }}
      >
        <div style={{transform: 'scale(0.8)', transformOrigin: 'left center', width: 152, height: 184, flexShrink: 0}}>
          <Mapa progresso={interpolate(frame, [20, 120], [0.05, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
        </div>
        <div>
          <div style={{fontFamily: mono, fontSize: 15, color: COR.tintaSuave, letterSpacing: 1}}>DE DETROIT AO TAPAJÓS</div>
          <div style={{fontFamily: archivo, fontWeight: 800, fontSize: 40, color: COR.tinta, lineHeight: 1.05, marginTop: 4}}>5.800 km</div>
          <div style={{fontFamily: archivo, fontWeight: 500, fontSize: 19, color: COR.tintaSuave, marginTop: 6, lineHeight: 1.3}}>
            em linha reta, da sede da Ford até a cidade na floresta
          </div>
        </div>
      </div>

      {/* legenda da narração, palavra por palavra */}
      <div style={{position: 'absolute', left: 600, right: 60, bottom: 56, display: 'flex', justifyContent: 'center'}}>
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
            lineHeight: 1.3,
          }}
        >
          {LEGENDA.map((p, i) => (
            <span key={i} style={{color: i < palavra ? '#FFFFFF' : i === palavra ? COR.destaqueClaro : 'rgba(255,255,255,0.4)'}}>
              {p}{' '}
            </span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

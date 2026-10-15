import type {CSSProperties, ReactNode} from 'react';
import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {loadFont as carregarTitulo} from '@remotion/google-fonts/ArchivoBlack';
import {loadFont as carregarTexto} from '@remotion/google-fonts/Inter';

const {fontFamily: titulo} = carregarTitulo();
const {fontFamily: texto} = carregarTexto('normal', {weights: ['400', '700'], subsets: ['latin', 'latin-ext']});

const cor = {
  fundo: '#F4EAD5',
  tinta: '#1F1A17',
  suave: '#7A6F66',
  laranja: '#E8871E',
  vermelho: '#D62839',
};

type Tempo = {inicio: number; fim: number};
export type Cena = Tempo &
  (
    | {tipo: 'pergunta'; pre: string; palavra: string}
    | {tipo: 'mito'; pre: string; palavra: string; nota: string}
    | {tipo: 'carimbo'; palavra: string; carimbo: string}
    | {tipo: 'encurta'; longa: string; curta: string; nota: string}
    | {tipo: 'prova'; de: number; ano: number; texto: string; nota: string}
    | {tipo: 'fim'; pre: string; texto: string}
  );
export type Roteiro = {cenas: Cena[]};

// --- utilitários de animação -------------------------------------------------

const useMola = (atraso = 0, damping = 14) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - atraso, fps, config: {damping}});
};

const faixa = (frame: number, de: number, ate: number, saida: [number, number] = [0, 1]) =>
  interpolate(frame, [de, ate], saida, {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

/** Texto que sobe e aparece com mola. */
const Surge = ({atraso = 0, children, style}: {atraso?: number; children: ReactNode; style?: CSSProperties}) => {
  const p = useMola(atraso);
  return (
    <div style={{opacity: p, transform: `translateY(${(1 - p) * 60}px)`, ...style}}>{children}</div>
  );
};

/** Palavra com as letras entrando uma a uma. */
const LetraALetra = ({palavra, atraso = 0, style}: {palavra: string; atraso?: number; style?: CSSProperties}) => (
  <div style={{display: 'flex', justifyContent: 'center', ...style}}>
    {[...palavra].map((letra, i) => (
      <Letra key={i} atraso={atraso + i * 3}>
        {letra === ' ' ? ' ' : letra}
      </Letra>
    ))}
  </div>
);

const Letra = ({atraso, children}: {atraso: number; children: ReactNode}) => {
  const p = useMola(atraso, 11);
  return (
    <span style={{display: 'inline-block', opacity: Math.min(1, p * 2), transform: `translateY(${(1 - p) * 160}px)`}}>
      {children}
    </span>
  );
};

/** Traço SVG que se desenha sozinho (line art). */
const Traco = ({d, caixa, inicio, duracao, largura, cor: stroke, style}: {
  d: string;
  /** Largura e altura do viewBox; manter a proporção da área na tela para o traço não deformar. */
  caixa: [number, number];
  inicio: number;
  duracao: number;
  largura: number;
  cor: string;
  style?: CSSProperties;
}) => {
  const frame = useCurrentFrame();
  const progresso = faixa(frame, inicio, inicio + duracao);
  return (
    <svg viewBox={`0 0 ${caixa[0]} ${caixa[1]}`} preserveAspectRatio="none" style={{position: 'absolute', overflow: 'visible', ...style}}>
      <path
        d={d}
        pathLength={1}
        fill="none"
        stroke={stroke}
        strokeWidth={largura}
        strokeLinecap="round"
        strokeDasharray={1}
        strokeDashoffset={1 - progresso}
      />
    </svg>
  );
};

const estilos = {
  pre: {fontFamily: texto, fontWeight: 700, fontSize: 64, color: cor.suave},
  palavra: {fontFamily: titulo, fontSize: 250, color: cor.tinta, lineHeight: 1.1},
  nota: {fontFamily: texto, fontWeight: 400, fontSize: 52, color: cor.tinta, textAlign: 'center', maxWidth: 860, lineHeight: 1.3},
} satisfies Record<string, CSSProperties>;

// --- cenas -------------------------------------------------------------------

const Pergunta = ({pre, palavra}: {pre: string; palavra: string}) => (
  <>
    <Surge style={estilos.pre}>{pre}</Surge>
    <LetraALetra palavra={palavra} atraso={10} style={estilos.palavra} />
  </>
);

const Mito = ({pre, palavra, nota}: {pre: string; palavra: string; nota: string}) => {
  const frame = useCurrentFrame();
  const visiveis = Math.floor(faixa(frame, 10, 10 + palavra.length * 3, [0, palavra.length]));
  const cursor = Math.floor(frame / 8) % 2 === 0 ? 1 : 0;
  return (
    <>
      <Surge style={estilos.pre}>{pre}</Surge>
      <div style={{...estilos.palavra, fontSize: 200, color: cor.laranja}}>
        {palavra.slice(0, visiveis)}
        <span style={{opacity: cursor, color: cor.tinta}}>|</span>
      </div>
      <Surge atraso={45} style={estilos.nota}>{nota}</Surge>
    </>
  );
};

const Carimbo = ({palavra, carimbo}: {palavra: string; carimbo: string}) => {
  const p = useMola(16, 9);
  return (
    <div style={{position: 'relative', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{position: 'relative', ...estilos.palavra, fontSize: 200, color: cor.laranja, opacity: 0.55}}>
        {palavra}
        <Traco d="M 0 130 L 760 100" caixa={[760, 220]} inicio={2} duracao={12} largura={22} cor={cor.tinta} style={{inset: 0, width: '100%', height: '100%'}} />
      </div>
      <div
        style={{
          position: 'absolute',
          fontFamily: titulo,
          fontSize: 200,
          color: cor.vermelho,
          border: `16px solid ${cor.vermelho}`,
          borderRadius: 24,
          padding: '0 40px',
          opacity: Math.min(1, p * 3),
          transform: `rotate(-14deg) scale(${interpolate(p, [0, 1], [3, 1])})`,
        }}
      >
        {carimbo}
      </div>
    </div>
  );
};

const Encurta = ({longa, curta, nota}: {longa: string; curta: string; nota: string}) => {
  const frame = useCurrentFrame();
  // "forró" é "forrobodó" encurtado: o começo fica, o resto cai, e o acento se desenha.
  const sem = (s: string) => s.normalize('NFD').replace(/\p{M}/gu, '');
  const raiz = sem(curta);
  const comeco = longa.slice(0, raiz.length - 1);
  const ultima = sem(longa[raiz.length - 1]);
  const resto = longa.slice(raiz.length);

  const queda = faixa(frame, 30, 50);
  const zoom = faixa(frame, 48, 66, [1, 1.6]);
  return (
    <>
      <Surge style={{...estilos.palavra, fontSize: 150, transform: `scale(${zoom})`}}>
        <span>{comeco}</span>
        <span style={{position: 'relative', display: 'inline-block'}}>
          {ultima}
          <Traco d="M 30 0 L 75 -22" caixa={[100, 50]} inicio={66} duracao={10} largura={18} cor={cor.vermelho} style={{left: 0, top: '22%', width: '100%', height: '30%'}} />
        </span>
        <span
          style={{
            display: 'inline-block',
            overflow: 'hidden',
            verticalAlign: 'bottom',
            maxWidth: `${(1 - queda) * resto.length}em`,
            color: cor.suave,
          }}
        >
          <span style={{display: 'inline-block', opacity: 1 - queda, transform: `translateY(${queda * 120}px) rotate(${queda * 18}deg)`}}>
            {resto}
          </span>
        </span>
      </Surge>
      <Surge atraso={80} style={{...estilos.nota, marginTop: 80}}>{nota}</Surge>
    </>
  );
};

const Prova = ({de, ano, texto: frase, nota}: {de: number; ano: number; texto: string; nota: string}) => {
  const frame = useCurrentFrame();
  const valor = Math.round(faixa(frame, 4, 40, [de, ano]));
  return (
    <>
      <div style={{...estilos.palavra, fontSize: 280, color: frame > 40 ? cor.vermelho : cor.tinta}}>{valor}</div>
      <Surge atraso={42} style={{...estilos.nota, fontWeight: 700}}>{frase}</Surge>
      <Surge atraso={72} style={{...estilos.nota, color: cor.laranja, fontWeight: 700, marginTop: 40}}>{nota}</Surge>
    </>
  );
};

const Fim = ({pre, texto: frase}: {pre: string; texto: string}) => (
  <>
    <Surge style={estilos.pre}>{pre}</Surge>
    {frase.split(' ').map((p, i) => (
      <Surge key={i} atraso={8 + i * 6} style={{...estilos.palavra, fontSize: 150, color: i === 0 ? cor.tinta : cor.laranja}}>
        {p}
      </Surge>
    ))}
  </>
);

const conteudo = (cena: Cena) => {
  switch (cena.tipo) {
    case 'pergunta': return <Pergunta {...cena} />;
    case 'mito': return <Mito {...cena} />;
    case 'carimbo': return <Carimbo {...cena} />;
    case 'encurta': return <Encurta {...cena} />;
    case 'prova': return <Prova {...cena} />;
    case 'fim': return <Fim {...cena} />;
  }
};

/** Cada cena some nos últimos quadros, menos a última. */
const Palco = ({duracao, ultima, children}: {duracao: number; ultima: boolean; children: ReactNode}) => {
  const frame = useCurrentFrame();
  const opacity = ultima ? 1 : interpolate(frame, [duracao - 6, duracao], [1, 0], {extrapolateLeft: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', gap: 24, padding: 60, opacity}}>
      {children}
    </AbsoluteFill>
  );
};

export const Short = ({cenas}: Roteiro) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: cor.fundo}}>
      <div style={{position: 'absolute', top: 140, width: '100%', textAlign: 'center', fontFamily: texto, fontWeight: 700, fontSize: 34, letterSpacing: 8, color: cor.suave}}>
        LÍNGUA E COSTUMES
      </div>
      {cenas.map((cena, i) => {
        const duracao = Math.round((cena.fim - cena.inicio) * fps);
        return (
          <Sequence key={i} from={Math.round(cena.inicio * fps)} durationInFrames={duracao}>
            <Palco duracao={duracao} ultima={i === cenas.length - 1}>
              {conteudo(cena)}
            </Palco>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

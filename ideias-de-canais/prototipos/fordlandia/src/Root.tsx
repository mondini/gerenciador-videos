import {Composition} from 'remotion';
import {Fordlandia} from './Fordlandia';
import {ALTURA, DURACAO, FPS, LARGURA} from './cena';

export const Root = () => (
  <Composition
    id="Fordlandia"
    component={Fordlandia}
    width={LARGURA}
    height={ALTURA}
    fps={FPS}
    durationInFrames={DURACAO}
  />
);

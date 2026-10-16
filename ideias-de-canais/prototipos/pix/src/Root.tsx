import {Composition} from 'remotion';
import {Pix} from './Pix';
import {ALTURA, DURACAO, FPS, LARGURA} from './cena';

export const Root = () => (
  <Composition
    id="Pix"
    component={Pix}
    width={LARGURA}
    height={ALTURA}
    fps={FPS}
    durationInFrames={DURACAO}
  />
);

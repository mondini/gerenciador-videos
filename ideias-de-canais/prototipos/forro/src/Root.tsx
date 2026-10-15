import {Composition} from 'remotion';
import roteiro from '../roteiro.json';
import {Short, type Roteiro} from './Short';

const FPS = 30;

export const Root = () => (
  <Composition
    id="Short"
    component={Short}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={1}
    defaultProps={roteiro as Roteiro}
    // A duração vem do roteiro, inclusive quando ele chega por --props.
    calculateMetadata={({props}) => ({
      durationInFrames: Math.ceil(Math.max(...props.cenas.map((c) => c.fim)) * FPS),
    })}
  />
);

import React from 'react';
import {Composition} from 'remotion';
import {N001, TOTAL} from './N001';
import {N001v, TOTAL as TOTV, starts as SV} from './N001v';
import {N001w, TOTAL as TOTW} from './N001w';
import {Avatar} from './Avatar';
import {N002} from './N002';
import {N003} from './N003';
import {N004} from './N004';
import {Cover001, Cover002, Cover003, Cover004} from './Cover';
export const Root: React.FC = () => (
  <>
  <Composition id="Cover004" component={Cover004} durationInFrames={1} fps={30} width={1080} height={1920} />
  <Composition id="N004" component={N004.Comp} durationInFrames={N004.TOTAL} fps={30} width={1080} height={1920} />
  <Composition id="Cover003" component={Cover003} durationInFrames={1} fps={30} width={1080} height={1920} />
  <Composition id="N003" component={N003.Comp} durationInFrames={N003.TOTAL} fps={30} width={1080} height={1920} />
  <Composition id="Cover002" component={Cover002} durationInFrames={1} fps={30} width={1080} height={1920} />
  <Composition id="N002" component={N002.Comp} durationInFrames={N002.TOTAL} fps={30} width={1080} height={1920} />
  <Composition id="Cover001" component={Cover001} durationInFrames={1} fps={30} width={1080} height={1920} />
  <Composition id="Avatar" component={Avatar} durationInFrames={1} fps={30} width={1080} height={1080} />
  <Composition id="N001w" component={N001w} durationInFrames={TOTW} fps={30} width={1080} height={1920} defaultProps={{upto: 99}} />
  <Composition id="N001v" component={N001v} durationInFrames={TOTV} fps={30} width={1080} height={1920} defaultProps={{upto: 99}} />
  <Composition id="N001" component={N001} durationInFrames={TOTAL} fps={30} width={1080} height={1920} />
  </>
);

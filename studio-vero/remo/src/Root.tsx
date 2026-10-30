import React from 'react';
import {Composition} from 'remotion';
import {N001, TOTAL} from './N001';
import {N001v, TOTAL as TOTV, starts as SV} from './N001v';
import {N001w, TOTAL as TOTW} from './N001w';
import {Avatar} from './Avatar';
import {Cover001} from './Cover';
export const Root: React.FC = () => (
  <>
  <Composition id="Cover001" component={Cover001} durationInFrames={1} fps={30} width={1080} height={1920} />
  <Composition id="Avatar" component={Avatar} durationInFrames={1} fps={30} width={1080} height={1080} />
  <Composition id="N001w" component={N001w} durationInFrames={TOTW} fps={30} width={1080} height={1920} defaultProps={{upto: 99}} />
  <Composition id="N001v" component={N001v} durationInFrames={TOTV} fps={30} width={1080} height={1920} defaultProps={{upto: 99}} />
  <Composition id="N001" component={N001} durationInFrames={TOTAL} fps={30} width={1080} height={1920} />
  </>
);

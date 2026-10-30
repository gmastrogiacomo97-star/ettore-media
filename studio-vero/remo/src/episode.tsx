import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C, F, Paper, Masthead, Mark, ease, easeIO} from './kit';
import {Pop, Float} from './motion';

export type Line = {text: string; start: number; end: number; words: [string, number][]};
export type Word = [string, number, number];
export const FPS = 30;
export const fr = (s: number) => Math.round(s * FPS);
const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const norm = (t: string) => t.toLowerCase().normalize('NFD').replace(/[^a-z0-9]/g, '');

/* everything a scene needs: local frame for a word/time */
export type Ctx = {i: number; r: (sec: number) => number; at: (token: string, after?: number) => number; line: Line};

export const makeEpisode = (ep: string, num: number, timing: Line[], words: Word[], scenes: React.FC<{c: Ctx}>[]) => {
  const starts = timing.map((t, i) => (i === 0 ? 0 : fr(t.start) - 5));
  const TOTAL = fr(timing[timing.length - 1].end + 1.4);
  const len = (i: number) => (i + 1 < starts.length ? starts[i + 1] : TOTAL) - starts[i];
  const atSec = (token: string, after = 0) => { const n = norm(token); const w = words.find((w) => w[1] >= after - 1e-3 && norm(w[0]).startsWith(n)); return w ? w[1] : after; };

  const Scene: React.FC<{i: number; children: React.ReactNode}> = ({i, children}) => {
    const f = useCurrentFrame(); const {fps} = useVideoConfig(); const L = len(i);
    const inn = i === 0 ? 1 : spring({frame: f, fps, config: {damping: 18, stiffness: 140}});
    const out = i + 1 < starts.length ? interpolate(f, [L - 7, L], [0, 1], {...cl, easing: easeIO}) : 0;
    const cam = interpolate(f, [0, L], [1, 1.035]); const rot = noise2D('cam' + i, f * 0.008, 0) * 0.5;
    return <AbsoluteFill style={{opacity: Math.min(1, inn * 1.6) * (1 - out), transform: `scale(${cam * (0.92 + 0.08 * inn) * (1 + out * 0.12)}) rotate(${rot}deg)`,
      filter: `blur(${(1 - Math.min(1, inn)) * 14 + out * 16}px)`}}>{children}</AbsoluteFill>;
  };

  const Subs: React.FC = () => {
    const f = useCurrentFrame(); const t = f / FPS;
    let i = 0; for (let k = 0; k < timing.length; k++) if (t >= timing[k].start - 0.2) i = k;
    const line = timing[i];
    const op = interpolate(t, [line.start - 0.2, line.start - 0.05, line.end + 0.25, line.end + 0.45], [0, 1, 1, 0], cl);
    return (
      <div style={{position: 'absolute', top: 1600, left: 100, right: 100, textAlign: 'center', fontFamily: F.sans, fontWeight: 700, fontSize: 40, lineHeight: 1.3, opacity: op}}>
        {line.words.map(([w, ws], k) => { const p = interpolate(t, [ws - 0.03, ws + 0.1], [0, 1], cl);
          return <span key={k} style={{display: 'inline-block', marginRight: '0.28em', color: p > 0.5 ? C.ink : 'rgba(20,20,20,0.25)', transform: `translateY(${(1 - p) * 6}px) scale(${1 + Math.sin(p * Math.PI) * 0.08})`}}>{w}</span>; })}
      </div>
    );
  };

  const Comp: React.FC = () => {
    const f = useCurrentFrame();
    return (
      <Paper>
        <Masthead num={num} />
        {scenes.map((S, i) => {
          const c: Ctx = {i, line: timing[i], r: (sec) => fr(sec) - starts[i], at: (tok, after) => fr(atSec(tok, after ?? timing[i].start - 0.3)) - starts[i]};
          return <Sequence key={i} from={starts[i]} durationInFrames={len(i)}><Scene i={i}><S c={c} /></Scene></Sequence>;
        })}
        <Subs />
        <Audio src={staticFile(`${ep}/voice.wav`)} />
        <Audio src={staticFile(`${ep}/music.wav`)} volume={0.45} />
        <div style={{position: 'absolute', top: 1780, left: 90, right: 90, height: 4, background: 'rgba(20,20,20,0.12)'}}>
          <div style={{height: 4, width: `${(f / TOTAL) * 100}%`, background: C.red}} />
        </div>
      </Paper>
    );
  };
  return {Comp, TOTAL, starts, atSec};
};

export const At: React.FC<{top: number; children: React.ReactNode}> = ({top, children}) => <div style={{position: 'absolute', top, left: 0, width: '100%'}}>{children}</div>;

/* shared sign-off */
export const SignOff: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const draw = interpolate(f, [0, 22], [0, 1], {...cl, easing: ease});
  const dot = spring({frame: f - 16, fps, config: {damping: 8, stiffness: 200}});
  const tS = c.at('spiego'), tN = c.at('prossimo') - 4;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 380, width: '100%', display: 'flex', justifyContent: 'center'}}><Float seed="mark" amp={4}><Mark size={300} draw={draw} dot={dot} /></Float></div>
      <At top={740}><Pop text="Sono *Vero*" size={130} at={4} /></At>
      <At top={900}><Pop text="un’AI che ti spiega cosa c’è dietro le cose" size={34} weight={500} font={F.mono} at={tS} stagger={0.4} tracking={0} color={C.mute} /></At>
      <At top={1130}><Pop text={'Il prossimo perché\nlo scegli *tu.*'} size={92} at={tN} /></At>
      <div style={{position: 'absolute', top: 1400 + Math.sin(f * 0.25) * 14, width: '100%', textAlign: 'center', opacity: f > tN + 20 ? 1 : 0, fontFamily: F.sans, fontWeight: 700, fontSize: 40, color: C.red}}>scrivilo nei commenti ↓</div>
    </AbsoluteFill>
  );
};

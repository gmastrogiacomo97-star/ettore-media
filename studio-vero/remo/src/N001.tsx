import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, F, Paper, Masthead, Kinetic, Note, Mark, ease, easeIO, fade, useSpring} from './kit';
import {Cup, Grounds} from './Cup';
import timing from '../public/n001/timing.json';

const FPS = 30, GAP = [0.35, 0.45, 0.35, 0.3, 0.55, 0.5, 0.6, 1.2];
export const starts: number[] = []; let acc = 0;
timing.forEach((t, i) => { starts.push(Math.round(acc * FPS)); acc += t.dur + GAP[i]; });
export const TOTAL = Math.round(acc * FPS);
const len = (i: number) => (i + 1 < starts.length ? starts[i + 1] : TOTAL) - starts[i];

/* scene wrapper: quick ink-wipe out at the end */
const Scene: React.FC<{i: number; children: React.ReactNode}> = ({i, children}) => {
  const f = useCurrentFrame(); const L = len(i);
  const out = i + 1 < starts.length ? interpolate(f, [L - 7, L], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeIO}) : 0;
  return <AbsoluteFill style={{opacity: 1 - out, transform: `translateY(${-out * 60}px)`}}>{children}</AbsoluteFill>;
};

const Price: React.FC<{v: string; size: number; delay?: number; color?: string; instant?: boolean}> = ({v, size, delay = 0, color = C.red, instant = false}) => {
  const f = useCurrentFrame() + (instant ? 40 : 0);
  return (
    <div style={{fontFamily: F.serif, fontWeight: 800, fontSize: size, color, letterSpacing: -size * 0.015, lineHeight: 1, display: 'flex', justifyContent: 'center'}}>
      {v.split('').map((ch, i) => {
        const p = interpolate(f, [delay + i * 2, delay + i * 2 + 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
        return <span key={i} style={{display: 'inline-block', transform: `translateY(${(1 - p) * 0.5}em) rotate(${(1 - p) * 6}deg)`, opacity: p}}>{ch}</span>;
      })}
    </div>
  );
};

/* 1 — hook */
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const push = interpolate(f, [0, 10, len(0)], [1.07, 1.0, 1.04], {easing: ease});
  const cupIn = 1;
  return (
    <AbsoluteFill style={{transform: `scale(${push})`}}>
      <div style={{position: 'absolute', top: 380, width: '100%'}}><Price v="1,29 €" size={300} instant /></div>
      <div style={{position: 'absolute', top: 720, width: '100%'}}><Kinetic text="per un caffè al bar." size={70} weight={600} delay={-30} /></div>
      <div style={{position: 'absolute', top: 960, width: '100%', display: 'flex', justifyContent: 'center', transform: `translateY(${(1 - cupIn) * 300}px)`, opacity: cupIn}}>
        <Cup size={640} />
      </div>
      <Note delay={-20}>media italiana · agosto 2026</Note>
    </AbsoluteFill>
  );
};

/* 2 — the coffee inside is worth cents */
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const heap = interpolate(f, [16, 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const cents = interpolate(f, [22, 52], [0, 4], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const cupShift = interpolate(f, [0, 18], [0, 1], {extrapolateRight: 'clamp', easing: easeIO});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 360, width: '100%'}}><Kinetic text={'Il caffè dentro\nvale *3-4 centesimi.*'} size={112} /></div>
      <div style={{position: 'absolute', top: 820, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 10, alignItems: 'flex-end'}}>
        <div style={{transform: `translateX(${-cupShift * 20}px) scale(${1 - cupShift * 0.12})`, transformOrigin: 'bottom center'}}><Cup size={460} /></div>
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: 30, opacity: heap, transform: `translateY(${(1 - heap) * 60}px)`}}>
          <div style={{fontFamily: F.serif, fontWeight: 800, fontSize: 120, color: C.red, lineHeight: 1, marginBottom: 20, whiteSpace: 'nowrap'}}>{`0,0${Math.round(cents)} €`}</div>
          <Grounds size={300} k={heap} />
          <div style={{fontFamily: F.mono, fontSize: 32, color: C.ink, marginTop: 12}}>7 grammi</div>
        </div>
      </div>
      <Note delay={20}>caffè crudo 4,44 €/kg · FIPE, apr. 2024 · calcolo di Vero</Note>
    </AbsoluteFill>
  );
};

const SCENES = [S1, S2];

/* subtitles: phrase, word highlight estimated from character length */
const Subs: React.FC = () => {
  const f = useCurrentFrame();
  let i = 0; for (let k = 0; k < starts.length; k++) if (f >= starts[k]) i = k;
  const t = timing[i]; const lf = f - starts[i] - 4; const durF = t.dur * FPS;
  const words = t.text.split(' '); const total = t.text.length; let c = 0;
  const show = fade(f - starts[i], 0, 6) * (1 - fade(f - starts[i], len(i) - 6, len(i)));
  return (
    <div style={{position: 'absolute', top: 1640, left: 90, right: 90, textAlign: 'center', fontFamily: F.sans, fontWeight: 700, fontSize: 40, lineHeight: 1.3, opacity: show}}>
      {words.map((w, k) => {
        const on = lf >= (c / total) * durF; c += w.length + 1;
        return <span key={k} style={{color: on ? C.ink : 'rgba(20,20,20,0.28)', transition: 'none'}}>{w} </span>;
      })}
    </div>
  );
};

export const N001: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Paper>
      <Masthead num={1} />
      {SCENES.map((S, i) => (
        <Sequence key={i} from={starts[i]} durationInFrames={len(i)}><Scene i={i}><S /></Scene></Sequence>
      ))}
      <Subs />
      {timing.map((_, i) => (
        <Sequence key={'a' + i} from={starts[i] + 3}><Audio src={staticFile(`n001/${String(i).padStart(2, '0')}.wav`)} /></Sequence>
      ))}
      <Audio src={staticFile('n001/music.wav')} volume={0.55} />
      {/* progress rule */}
      <div style={{position: 'absolute', top: 1780, left: 90, right: 90, height: 4, background: 'rgba(20,20,20,0.12)'}}>
        <div style={{height: 4, width: `${(f / TOTAL) * 100}%`, background: C.red}} />
      </div>
    </Paper>
  );
};

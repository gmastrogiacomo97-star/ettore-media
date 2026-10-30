import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, F, Paper, Masthead, Kinetic, Note, Mark, ease, easeIO} from './kit';
import {Cup, Grounds} from './Cup';
import {BeanPour, Scale, CoinStack, Count, Coin} from './props';
import timing from '../public/n001v/timing.json';

const FPS = 30;
const GAP = [0.25, 0.3, 0.45, 0.35, 0.45, 0.45, 0.5, 1.3];
export const starts: number[] = []; let acc = 0;
timing.forEach((t, i) => { starts.push(Math.round(acc * FPS)); acc += t.dur + GAP[i]; });
export const TOTAL = Math.round(acc * FPS);
const len = (i: number) => (i + 1 < starts.length ? starts[i + 1] : TOTAL) - starts[i];
const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

/* scene transition: incoming rises with a spring, outgoing lifts away; a red rule sweeps across */
const Scene: React.FC<{i: number; children: React.ReactNode}> = ({i, children}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const L = len(i);
  const inn = i === 0 ? 1 : spring({frame: f, fps, config: {damping: 20, stiffness: 120}});
  const out = i + 1 < starts.length ? interpolate(f, [L - 8, L], [0, 1], {...cl, easing: easeIO}) : 0;
  return <AbsoluteFill style={{opacity: Math.min(1, inn * 1.4) * (1 - out), transform: `translateY(${(1 - inn) * 140 - out * 120}px)`}}>{children}</AbsoluteFill>;
};
const Sweep: React.FC = () => {
  const f = useCurrentFrame();
  return <>{starts.slice(1).map((s, k) => {
    const p = interpolate(f, [s - 6, s + 8], [0, 1], cl); if (p <= 0 || p >= 1) return null;
    return <div key={k} style={{position: 'absolute', left: 0, right: 0, top: interpolate(p, [0, 1], [1920, -40], {easing: easeIO}), height: 10, background: C.red, opacity: 0.9}} />;
  })}</>;
};

/* A — hook: question, and the lens that looks behind */
const A: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const tLens = Math.round(2.35 * fps);
  const lens = spring({frame: f - tLens, fps, config: {damping: 16, stiffness: 70, mass: 1}});
  const lx = interpolate(lens, [0, 1], [1300, 560]), ly = 980, LR = 240;
  const push = interpolate(f, [0, len(0)], [1.0, 1.05]);
  const q = interpolate(f, [tLens + 6, tLens + 20], [0, 1], {...cl, easing: ease});
  return (
    <AbsoluteFill style={{transform: `scale(${push})`}}>
      <div style={{position: 'absolute', top: 300, width: '100%'}}><Kinetic text="Perché un caffè al bar costa" size={64} weight={600} delay={-40} /></div>
      <div style={{position: 'absolute', top: 390, width: '100%', textAlign: 'center'}}>
        <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 250, color: C.red, letterSpacing: -4, lineHeight: 1}}>1,29 €<span style={{color: C.ink}}>?</span></span>
      </div>
      {/* cup + lens with x-ray inside */}
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <defs><clipPath id="lensclip"><circle cx={lx} cy={ly} r={LR - 20} /></clipPath></defs>
        <g transform="translate(220,730)"><Cup size={640} /></g>
        <g clipPath="url(#lensclip)">
          <rect x="0" y="0" width="1080" height="1920" fill={C.paper2} />
          <g transform={`translate(${lx - 150},${ly - 40})`}><Grounds size={300} k={lens} /></g>
          <text x={lx} y={ly - 70} textAnchor="middle" fontFamily={F.serif} fontWeight="800" fontSize="96" fill={C.red}>0,04 €</text>
          <text x={lx} y={ly + 150} textAnchor="middle" fontFamily={F.mono} fontSize="28" fill={C.ink}>7 g di caffè</text>
        </g>
        <circle cx={lx} cy={ly} r={LR - 10} fill="none" stroke={C.ink} strokeWidth="22" />
        <circle cx={lx} cy={ly} r={LR + 4} fill="none" stroke={C.ink} strokeOpacity="0.15" strokeWidth="6" />
        <line x1={lx + LR * 0.7} y1={ly + LR * 0.7} x2={lx + LR * 1.15} y2={ly + LR * 1.15} stroke={C.ink} strokeWidth="34" strokeLinecap="round" />
        <circle cx={lx + LR * 1.15} cy={ly + LR * 1.15} r="14" fill={C.red} />
      </svg>
      <div style={{position: 'absolute', top: 1330, width: '100%', opacity: q, transform: `translateY(${(1 - q) * 30}px)`}}>
        <Kinetic text={'…se il caffè dentro\nvale *4 centesimi?*'} size={78} delay={tLens + 6} />
      </div>
    </AbsoluteFill>
  );
};

/* B — the 7 grams */
const B: React.FC = () => {
  const f = useCurrentFrame();
  const grams = interpolate(f, [14, 70], [0, 7], {...cl, easing: ease});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 320, width: '100%'}}><Kinetic text={'Facciamo\ni conti.'} size={150} /></div>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        {/* hopper */}
        <path d="M400 700 L680 700 L600 830 L480 830 Z" fill="#2A2A28" />
        <rect x="515" y="830" width="50" height="34" fill="#2A2A28" />
        <g transform="translate(540,1250) scale(1.45)">
          <Scale x={0} y={0} grams={grams}>
            <BeanPour n={46} sx={0} sy={-262} px={0} py={-30} t0={10} t1={60} w={200} />
          </Scale>
        </g>
      </svg>
      <Note delay={40} y={1480}>7 grammi per un espresso</Note>
    </AbsoluteFill>
  );
};

/* C — the maths */
const C3: React.FC = () => {
  const f = useCurrentFrame();
  const eq = interpolate(f, [4, 30], [0, 1], {...cl, easing: ease});
  const line = '7 g × 4,44 €/kg';
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 340, width: '100%', textAlign: 'center', fontFamily: F.mono, fontSize: 64, color: C.ink}}>
        {line.slice(0, Math.round(line.length * eq))}<span style={{opacity: f % 16 < 8 ? 1 : 0}}>▍</span>
      </div>
      <div style={{position: 'absolute', top: 460, width: '100%', textAlign: 'center', opacity: interpolate(f, [30, 40], [0, 1], cl)}}>
        <span style={{fontFamily: F.serif, fontWeight: 600, fontSize: 150, color: C.ink, verticalAlign: 'top'}}>≈ </span>
        <Count from={0} to={0.04} t0={32} t1={62} size={200} />
      </div>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform="translate(540,1300) scale(2.2)">
          <ellipse cx="0" cy="12" rx="120" ry="14" fill="#000" opacity="0.08" />
          <CoinStack x={0} y={0} n={4} t0={36} />
        </g>
      </svg>
      <Note delay={50} y={1480}>caffè crudo · FIPE 2024 · più calo di tostatura</Note>
    </AbsoluteFill>
  );
};

const SCENES = [A, B, C3];

const Subs: React.FC = () => {
  const f = useCurrentFrame();
  let i = 0; for (let k = 0; k < starts.length; k++) if (f >= starts[k]) i = k;
  const t = timing[i]; const lf = f - starts[i] - 3; const durF = t.dur * FPS;
  const words = t.text.split(' '); const total = t.text.length; let c = 0;
  const op = interpolate(f - starts[i], [0, 5, len(i) - 5, len(i)], [0, 1, 1, 0], cl);
  return (
    <div style={{position: 'absolute', top: 1600, left: 100, right: 100, textAlign: 'center', fontFamily: F.sans, fontWeight: 700, fontSize: 40, lineHeight: 1.3, opacity: op}}>
      {words.map((w, k) => { const on = lf >= (c / total) * durF * 0.95; c += w.length + 1;
        return <span key={k} style={{color: on ? C.ink : 'rgba(20,20,20,0.25)'}}>{w} </span>; })}
    </div>
  );
};

export const N001v: React.FC<{upto?: number}> = ({upto = 99}) => {
  const f = useCurrentFrame();
  const n = Math.min(SCENES.length, upto);
  return (
    <Paper>
      <Masthead num={1} />
      {SCENES.slice(0, n).map((S, i) => (
        <Sequence key={i} from={starts[i]} durationInFrames={len(i)}><Scene i={i}><S /></Scene></Sequence>
      ))}
      <Sweep />
      <Subs />
      {timing.slice(0, n).map((_, i) => (
        <Sequence key={'a' + i} from={starts[i] + 2}><Audio src={staticFile(`n001v/${String(i).padStart(2, '0')}.wav`)} /></Sequence>
      ))}
      <Audio src={staticFile('n001v/music.wav')} volume={0.5} />
      <div style={{position: 'absolute', top: 1780, left: 90, right: 90, height: 4, background: 'rgba(20,20,20,0.12)'}}>
        <div style={{height: 4, width: `${(f / TOTAL) * 100}%`, background: C.red}} />
      </div>
    </Paper>
  );
};

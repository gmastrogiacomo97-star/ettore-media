import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C, F, Paper, Masthead, ease, easeIO} from './kit';
import {Cup, Grounds} from './Cup';
import {BeanPour, Scale, CoinStack} from './props';
import {Pop, Roll, Float, Marker, Slam} from './motion';
import timing from '../public/n001w/timing.json';
import {D, E, Fm, G, Hs} from './scenes2';

const FPS = 30;
const fr = (s: number) => Math.round(s * FPS);
export const starts: number[] = timing.map((t, i) => (i === 0 ? 0 : fr(t.start) - 5));
export const TOTAL = fr(timing[timing.length - 1].end + 1.4);
const len = (i: number) => (i + 1 < starts.length ? starts[i + 1] : TOTAL) - starts[i];
const rel = (i: number, sec: number) => fr(sec) - starts[i];        // absolute voice time -> scene-local frame
const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

/* scene wrapper: blur-zoom transition in and out + slow camera drift */
const Scene: React.FC<{i: number; children: React.ReactNode}> = ({i, children}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const L = len(i);
  const inn = i === 0 ? 1 : spring({frame: f, fps, config: {damping: 18, stiffness: 140}});
  const out = i + 1 < starts.length ? interpolate(f, [L - 7, L], [0, 1], {...cl, easing: easeIO}) : 0;
  const cam = interpolate(f, [0, L], [1, 1.035]);
  const rot = noise2D('cam' + i, f * 0.008, 0) * 0.5;
  return (
    <AbsoluteFill style={{opacity: Math.min(1, inn * 1.6) * (1 - out),
      transform: `scale(${cam * (0.92 + 0.08 * inn) * (1 + out * 0.12)}) rotate(${rot}deg)`,
      filter: `blur(${(1 - Math.min(1, inn)) * 14 + out * 16}px)`}}>
      {children}
    </AbsoluteFill>
  );
};

const At: React.FC<{top: number; children: React.ReactNode; left?: number; width?: number | string}> = ({top, children, left = 0, width = '100%'}) =>
  <div style={{position: 'absolute', top, left, width}}>{children}</div>;

/* A — hook */
const A: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const tQ = rel(0, timing[0].segs[1][0]);                               // "se il caffè dentro…"
  const shrink = interpolate(f, [9, 22], [0, 1], {...cl, easing: ease});
  const cupIn = spring({frame: f - 8, fps, config: {damping: 14, stiffness: 90}});
  const lens = spring({frame: f - tQ + 4, fps, config: {damping: 15, stiffness: 80, mass: 0.9}});
  const lx = interpolate(lens, [0, 1], [1350, 560]), ly = 1010, LR = 240;
  const qBounce = spring({frame: f - 30, fps, config: {damping: 6, stiffness: 180}});
  return (
    <AbsoluteFill>
      {/* PERCHÉ slams, then shrinks to the top */}
      <div style={{position: 'absolute', top: interpolate(shrink, [0, 1], [640, 270]), width: '100%', textAlign: 'center',
        transform: `scale(${interpolate(shrink, [0, 1], [1, 0.42])})`, transformOrigin: 'center top'}}>
        <Slam at={-4}><span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 230, color: C.ink, letterSpacing: -6}}>Perché</span></Slam>
      </div>
      <At top={385}><Pop text="un caffè al bar costa" size={64} weight={600} at={14} /></At>
      <At top={470}>
        <Float seed="price" amp={5}>
          <div style={{textAlign: 'center', whiteSpace: 'nowrap'}}>
            <Roll value="1,29 €" size={240} at={12} />
            <span style={{display: 'inline-block', fontFamily: F.serif, fontWeight: 800, fontSize: 240, color: C.ink, lineHeight: 1,
              transform: `translateY(${(1 - qBounce) * -300}px) rotate(${noise2D('q', f * 0.05, 0) * 8}deg)`, opacity: f > 30 ? 1 : 0}}>?</span>
          </div>
        </Float>
      </At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <defs><clipPath id="lensclipw"><circle cx={lx} cy={ly} r={LR - 20} /></clipPath></defs>
        <g transform={`translate(220,${760 + (1 - cupIn) * 1250}) rotate(${(1 - cupIn) * -14} 320 260)`}><Cup size={640} /></g>
        <g clipPath="url(#lensclipw)">
          <rect x="0" y="0" width="1080" height="1920" fill={C.paper2} />
          <g transform={`translate(${lx - 150},${ly - 30})`}><Grounds size={300} k={lens} /></g>
          <text x={lx} y={ly - 70} textAnchor="middle" fontFamily={F.serif} fontWeight="800" fontSize="100" fill={C.red}>0,04 €</text>
          <text x={lx} y={ly + 160} textAnchor="middle" fontFamily={F.mono} fontSize="28" fill={C.ink}>7 g di caffè</text>
        </g>
        <g transform={`rotate(${(1 - lens) * 25} ${lx} ${ly})`}>
          <circle cx={lx} cy={ly} r={LR - 10} fill="none" stroke={C.ink} strokeWidth="22" />
          <line x1={lx + LR * 0.7} y1={ly + LR * 0.7} x2={lx + LR * 1.15} y2={ly + LR * 1.15} stroke={C.ink} strokeWidth="34" strokeLinecap="round" />
          <circle cx={lx + LR * 1.15} cy={ly + LR * 1.15} r="14" fill={C.red} />
          <path d={`M${lx - LR * 0.55},${ly - LR * 0.35} A ${LR * 0.65} ${LR * 0.65} 0 0 1 ${lx - LR * 0.1},${ly - LR * 0.62}`} stroke="#fff" strokeWidth="10" fill="none" strokeLinecap="round" opacity="0.7" />
        </g>
      </svg>
      <At top={1330}><Pop text={'…se il caffè dentro'} size={78} at={tQ} /></At>
      <At top={1420}><Pop text={'vale *4 centesimi?*'} size={78} at={tQ + 12} /></At>
      <At top={1500}><div style={{marginLeft: 470}}><Marker at={tQ + 30} width={420} height={12} /></div></At>
    </AbsoluteFill>
  );
};

/* B — the 7 grams */
const B: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const tSeven = rel(1, timing[1].segs[2][0]);
  const grams = interpolate(f, [tSeven - 18, tSeven + 22], [0, 7], {...cl, easing: ease});
  const hop = spring({frame: f - 4, fps, config: {damping: 14, stiffness: 110}});
  const sc = spring({frame: f - 2, fps, config: {damping: 15, stiffness: 100}});
  return (
    <AbsoluteFill>
      <At top={290}><Pop text="Facciamo" size={160} at={2} stagger={1.4} /></At>
      <At top={460}><Pop text="i *conti.*" size={160} at={10} stagger={1.4} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(0,${(1 - hop) * -500})`}>
          <path d="M400 720 L680 720 L600 850 L480 850 Z" fill="#2A2A28" />
          <rect x="515" y="850" width="50" height="30" fill="#2A2A28" />
        </g>
        <g transform={`translate(540,${1270 + (1 - sc) * 600}) scale(1.45)`}>
          <Scale x={0} y={0} grams={grams}>
            <BeanPour n={46} sx={0} sy={-262} px={0} py={-30} t0={tSeven - 20} t1={tSeven + 20} w={200} />
          </Scale>
        </g>
      </svg>
      <At top={1470}><Pop text="7 grammi in una tazzina" size={40} weight={500} font={F.mono} at={tSeven + 6} stagger={0.6} tracking={0} /></At>
    </AbsoluteFill>
  );
};

/* C — the maths */
const Tok: React.FC<{t: string; at: number; dx: number; dy: number; size?: number; color?: string; font?: string}> = ({t, at, dx, dy, size = 70, color = C.ink, font = F.mono}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - at, fps, config: {damping: 13, stiffness: 150}});
  return <span style={{display: 'inline-block', margin: '0 14px', fontFamily: font, fontSize: size, color, opacity: Math.min(1, s * 1.5),
    transform: `translate(${(1 - s) * dx}px,${(1 - s) * dy}px) rotate(${(1 - s) * 20}deg)`, filter: `blur(${(1 - Math.min(1, s)) * 8}px)`}}>{t}</span>;
};
const C3: React.FC = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const tRes = rel(2, timing[2].segs[1][0]);
  const eq = spring({frame: f - tRes + 4, fps, config: {damping: 10, stiffness: 160}});
  return (
    <AbsoluteFill>
      <At top={330}><div style={{textAlign: 'center', whiteSpace: 'nowrap'}}>
        <Tok t="7 g" at={4} dx={-500} dy={0} /><Tok t="×" at={10} dx={0} dy={-300} color={C.red} /><Tok t="4,44 €/kg" at={14} dx={500} dy={0} />
      </div></At>
      <At top={470}><div style={{textAlign: 'center', whiteSpace: 'nowrap'}}>
        <span style={{display: 'inline-block', fontFamily: F.serif, fontWeight: 600, fontSize: 150, color: C.ink, verticalAlign: 'top',
          transform: `rotate(${(1 - eq) * 180}deg) scale(${eq})`}}>≈ </span>
        <Roll value="0,04 €" size={210} at={tRes} dur={22} />
      </div></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform="translate(540,1300) scale(2.2)">
          <ellipse cx="0" cy="12" rx="120" ry="14" fill="#000" opacity="0.08" />
          <CoinStack x={0} y={0} n={4} t0={tRes + 4} gap={6} />
        </g>
      </svg>
      <At top={1470}><Pop text="caffè crudo · FIPE 2024 · più calo di tostatura" size={28} weight={500} font={F.mono} at={tRes + 16} stagger={0.3} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

const wrap = (Comp: React.FC<{r: (s: number) => number; segs: number[][]}>, i: number): React.FC => () => <Comp r={(sec) => rel(i, sec)} segs={timing[i].segs as number[][]} />;
const SCENES = [A, B, C3, wrap(D, 3), wrap(E, 4), wrap(Fm, 5), wrap(G, 6), wrap(Hs, 7)];

/* subtitles: exact word timing from forced alignment */
const Subs: React.FC = () => {
  const f = useCurrentFrame(); const t = f / FPS;
  let i = 0; for (let k = 0; k < timing.length; k++) if (t >= timing[k].start - 0.2) i = k;
  const line = timing[i]; const words = line.words as [string, number][];
  const op = interpolate(t, [line.start - 0.2, line.start - 0.05, line.end + 0.25, line.end + 0.45], [0, 1, 1, 0], cl);
  return (
    <div style={{position: 'absolute', top: 1600, left: 100, right: 100, textAlign: 'center', fontFamily: F.sans, fontWeight: 700, fontSize: 40, lineHeight: 1.3, opacity: op}}>
      {words.map(([w, ws], k) => {
        const p = interpolate(t, [ws - 0.03, ws + 0.1], [0, 1], cl);
        return <span key={k} style={{display: 'inline-block', marginRight: '0.28em', color: p > 0.5 ? C.ink : 'rgba(20,20,20,0.25)', transform: `translateY(${(1 - p) * 6}px) scale(${1 + Math.sin(p * Math.PI) * 0.08})`}}>{w}</span>; })}
    </div>
  );
};

export const N001w: React.FC<{upto?: number}> = ({upto = 99}) => {
  const f = useCurrentFrame();
  const n = Math.min(SCENES.length, upto);
  return (
    <Paper>
      <Masthead num={1} />
      {SCENES.slice(0, n).map((S, i) => (
        <Sequence key={i} from={starts[i]} durationInFrames={len(i)}><Scene i={i}><S /></Scene></Sequence>
      ))}
      <Subs />
      <Audio src={staticFile('n001w/voice.wav')} />
      <Audio src={staticFile('n001w/music.wav')} volume={0.45} />
      <div style={{position: 'absolute', top: 1780, left: 90, right: 90, height: 4, background: 'rgba(20,20,20,0.12)'}}>
        <div style={{height: 4, width: `${(f / TOTAL) * 100}%`, background: C.red}} />
      </div>
    </Paper>
  );
};

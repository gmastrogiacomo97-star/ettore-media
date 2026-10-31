import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C, F, ease} from './kit';
import {Pop, Roll, Float, Slam} from './motion';
import {makeEpisode, Ctx, At, SignOff} from './episode';
import timing from '../public/n003/timing.json';
import words from '../public/n003/words.json';

const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const WATER = '#6FB7E0', WATER_D = '#3E8FC0', BLUE = '#2F6FA0';
const useS = (at: number, cfg = {damping: 14, stiffness: 130}) => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return spring({frame: f - at, fps, config: cfg}); };

/* plastic bottle */
const Bottle: React.FC<{x: number; y: number; s?: number; fill?: number; label?: string}> = ({x, y, s = 1, fill = 0.85, label = 'ACQUA'}) => {
  const f = useCurrentFrame(); const top = 120 + (1 - fill) * 480;
  const wave = Array.from({length: 9}).map((_, k) => `L${30 + k * 20} ${top + noise2D('bw', k * 0.5, f * 0.05) * 6}`).join(' ');
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <defs><clipPath id={`b${x}`}><path d="M80 0 h40 v40 c0 30 70 50 70 110 v420 c0 30 -20 40 -40 40 h-100 c-20 0 -40 -10 -40 -40 v-420 c0 -60 70 -80 70 -110 z" /></clipPath></defs>
      <ellipse cx="100" cy="620" rx="100" ry="14" fill="#000" opacity="0.1" />
      <path d="M80 0 h40 v40 c0 30 70 50 70 110 v420 c0 30 -20 40 -40 40 h-100 c-20 0 -40 -10 -40 -40 v-420 c0 -60 70 -80 70 -110 z" fill="#EAF5FB" />
      <g clipPath={`url(#b${x})`}><path d={`M10 ${top} ${wave} L190 ${top} V620 H10 Z`} fill={WATER} opacity="0.85" />
        <rect x="30" y="120" width="14" height="420" rx="7" fill="#fff" opacity="0.5" /></g>
      <path d="M80 0 h40 v40 c0 30 70 50 70 110 v420 c0 30 -20 40 -40 40 h-100 c-20 0 -40 -10 -40 -40 v-420 c0 -60 70 -80 70 -110 z" fill="none" stroke={C.ink} strokeWidth="7" />
      <rect x="72" y="-22" width="56" height="30" rx="6" fill={BLUE} stroke={C.ink} strokeWidth="6" />
      <rect x="10" y="260" width="180" height="110" fill={C.red} />
      <text x="100" y="328" textAnchor="middle" fontFamily={F.serif} fontWeight="800" fontSize="40" fill="#fff">{label}</text>
    </g>
  );
};

/* glass under a tap with a running stream */
const TapGlass: React.FC<{x: number; y: number; s?: number; fill?: number}> = ({x, y, s = 1, fill = 0.7}) => {
  const f = useCurrentFrame(); const top = 220 + (1 - fill) * 200;
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <path d="M20 0 h150 a20 20 0 0 1 20 20 v40 h-40 v-20 h-130 z" fill="#B8B2A6" stroke={C.ink} strokeWidth="7" strokeLinejoin="round" />
      <rect x="150" y="60" width="40" height="22" fill="#B8B2A6" stroke={C.ink} strokeWidth="6" />
      <rect x="163" y="82" width="14" height={top + 120} fill={WATER} opacity={0.75 + 0.2 * Math.sin(f * 0.6)} />
      <ellipse cx="170" cy="560" rx="110" ry="12" fill="#000" opacity="0.1" />
      <path d={`M80 ${top + 80} L260 ${top + 80} L245 550 L95 550 Z`} fill={WATER} opacity="0.7" />
      <path d="M70 240 L270 240 L250 555 L90 555 Z" fill="none" stroke={C.ink} strokeWidth="7" strokeLinejoin="round" />
    </g>
  );
};

/* isometric 1000-litre tank filling */
const Cube: React.FC<{x: number; y: number; size: number; fill: number; tint?: string}> = ({x, y, size, fill, tint = WATER}) => {
  const a = size, dx = a * 0.5, dy = a * 0.28; const h = a * fill;
  return (
    <g transform={`translate(${x},${y})`}>
      <ellipse cx={dx / 2 + a / 2} cy={a + dy + 20} rx={a * 0.7} ry="16" fill="#000" opacity="0.08" />
      {/* water */}
      <path d={`M0 ${a} L${a} ${a} L${a} ${a - h} L0 ${a - h} Z`} fill={tint} opacity="0.9" />
      <path d={`M${a} ${a} L${a + dx} ${a - dy} L${a + dx} ${a - dy - h} L${a} ${a - h} Z`} fill={WATER_D} opacity="0.9" />
      <path d={`M0 ${a - h} L${a} ${a - h} L${a + dx} ${a - dy - h} L${dx} ${a - dy - h} Z`} fill="#A8D6F0" opacity="0.95" />
      {/* cage */}
      <g fill="none" stroke={C.ink} strokeWidth="6" strokeLinejoin="round">
        <path d={`M0 0 L${a} 0 L${a} ${a} L0 ${a} Z`} /><path d={`M${a} 0 L${a + dx} ${-dy} L${a + dx} ${a - dy} L${a} ${a}`} /><path d={`M0 0 L${dx} ${-dy} L${a + dx} ${-dy}`} />
        {[1, 2, 3].map((k) => <path key={k} d={`M${(a * k) / 4} 0 V${a}`} strokeWidth="2.5" opacity="0.4" />)}
        {[1, 2, 3].map((k) => <path key={'h' + k} d={`M0 ${(a * k) / 4} H${a}`} strokeWidth="2.5" opacity="0.4" />)}
      </g>
      <text x={a / 2} y={a / 2 + 24} textAnchor="middle" fontFamily={F.mono} fontSize={a * 0.13} fill={C.ink} opacity="0.85">1.000 L</text>
    </g>
  );
};

/* 0 — hook */
const S0: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tQ = c.at('e', 3.5);
  const bS = useS(-6, {damping: 12, stiffness: 120}), gS = useS(2, {damping: 12, stiffness: 120});
  const x90 = useS(c.at('novanta') - 2, {damping: 8, stiffness: 220});
  return (
    <AbsoluteFill>
      <At top={290}><Pop text="L’acqua in bottiglia costa" size={68} weight={600} at={-30} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(0,${(1 - bS) * 700})`}><Bottle x={130} y={700} s={1.0} /></g>
        <g transform={`translate(0,${(1 - gS) * 700})`}><TapGlass x={660} y={780} s={1.0} /></g>
      </svg>
      <div style={{position: 'absolute', top: 360, width: '100%', textAlign: 'center', transform: `scale(${0.3 + 0.7 * x90}) rotate(${(1 - x90) * -20}deg)`, opacity: Math.min(1, x90 * 2)}}>
        <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 190, color: C.red, letterSpacing: -6}}>×90</span>
        <div style={{fontFamily: F.serif, fontWeight: 600, fontSize: 56, color: C.ink, marginTop: -20}}>quella del rubinetto</div>
      </div>
      <At top={1380}><Pop text={'E chi la imbottiglia,\nquanto la *paga?*'} size={84} at={tQ} /></At>
    </AbsoluteFill>
  );
};

/* 1 — 24 cents a litre */
const S1: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tP = c.at('ventiquattro');
  const shelf = interpolate(f, [0, 24], [0, 1], {...cl, easing: ease});
  const tag = useS(c.at('litro') - 4, {damping: 7, stiffness: 120});
  return (
    <AbsoluteFill>
      <At top={290}><Pop text="Al supermercato, 1 litro" size={76} weight={600} at={2} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(${(1 - shelf) * -600},0)`}>
          {[0, 1, 2, 3].map((k) => <Bottle key={k} x={40 + k * 260} y={800} s={0.8} fill={0.9} />)}
          <rect x="0" y="1300" width="1080" height="30" fill="#8C7B65" />
        </g>
      </svg>
      <div style={{position: 'absolute', top: 470, left: 340, width: 400, transformOrigin: '200px 0px', transform: `rotate(${(1 - tag) * 35 + Math.sin(f * 0.15) * 2.5 * tag}deg)`, opacity: Math.min(1, tag * 2)}}>
        <div style={{width: 4, height: 70, background: C.ink, margin: '0 auto'}} />
        <div style={{background: '#FFF6D6', border: `6px solid ${C.ink}`, borderRadius: 24, padding: '22px 0 12px', textAlign: 'center', boxShadow: '0 16px 30px rgba(0,0,0,0.12)'}}>
          <Roll value="0,24 €" size={120} at={tP - 14} />
          <div style={{fontFamily: F.mono, fontSize: 28, color: C.ink}}>al litro</div>
        </div>
      </div>
      <At top={1470}><Pop text="prezzo medio · Mineracqua, via Altreconomia 2026" size={26} weight={500} font={F.mono} at={tP + 4} stagger={0.25} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

/* 2 — tap: 1000 litres for 2,75 € */
const S2: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tP = c.at('due'), tM = c.at('meno');
  const fill = interpolate(f, [6, tP], [0, 1], {...cl, easing: ease});
  return (
    <AbsoluteFill>
      <At top={290}><Pop text="Dal rubinetto," size={84} weight={600} at={2} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <rect x="480" y="640" width="20" height={180 + 440 * (1 - fill) * 0.6} fill={WATER} opacity="0.8" /><rect x="440" y="610" width="100" height="34" rx="10" fill="#B8B2A6" stroke={C.ink} strokeWidth="6" />
        <Cube x={210} y={820} size={440} fill={fill} />
      </svg>
      <div style={{position: 'absolute', top: 400, width: '100%', textAlign: 'center'}}><Roll value="2,75 €" size={170} at={tP - 6} color={BLUE} /></div>
      <At top={1400}><Pop text="meno di *0,3 centesimi* al litro" size={62} at={tM} /></At>
      <At top={1490}><Pop text="spesa media 500 €/anno per 182 m³ · Cittadinanzattiva 2025" size={24} weight={500} font={F.mono} at={tM + 6} stagger={0.2} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

/* 3 — companies pay the Regions < 2 € per 1000 litres */
const S3: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tR = c.at('regioni'), tD = c.at('due');
  const pipe = interpolate(f, [8, 40], [0, 1], {...cl, easing: ease});
  const fill = interpolate(f, [tR - 10, tD + 6], [0, 1], {...cl, easing: ease});
  return (
    <AbsoluteFill>
      <At top={290}><Pop text={'Le aziende pagano\nalle *Regioni*'} size={84} at={2} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        {/* mountain spring */}
        <path d="M60 900 L230 620 L320 760 L400 680 L560 900 Z" fill="#CFC6B4" stroke={C.ink} strokeWidth="6" strokeLinejoin="round" />
        <path d="M230 620 L270 690 L200 700 Z" fill="#fff" />
        <path d={`M300 860 C 420 860, 480 960, 600 960`} fill="none" stroke={WATER} strokeWidth="18" strokeDasharray="420" strokeDashoffset={420 * (1 - pipe)} strokeLinecap="round" />
        <Cube x={600} y={760} size={300} fill={fill} />
      </svg>
      <div style={{position: 'absolute', top: 1180, width: '100%', textAlign: 'center'}}>
        <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 90, color: C.red, opacity: f > tD - 6 ? 1 : 0}}>meno di </span>
        <Roll value="2 €" size={190} at={tD - 4} />
      </div>
      <At top={1440}><Pop text="ogni 1.000 litri · canone medio regionale" size={30} weight={500} font={F.mono} at={tD + 6} stagger={0.3} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

/* 4 — they pay less than you */
const S4: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tT = c.at('te');
  const b1 = interpolate(f, [8, 30], [0, 1], {...cl, easing: ease}), b2 = interpolate(f, [tT - 6, tT + 16], [0, 1], {...cl, easing: ease});
  const max = 600;
  return (
    <AbsoluteFill>
      <At top={290}><Slam at={0} from={2}><div style={{textAlign: 'center', fontFamily: F.serif, fontWeight: 800, fontSize: 150, color: C.red}}>Sì.</div></Slam></At>
      <At top={480}><Pop text={'L’azienda la paga\nmeno di *te.*'} size={88} at={c.at('chi')} /></At>
      {[['AZIENDA', 2.0, C.ink, b1, '< 2 €'], ['TU', 2.75, BLUE, b2, '2,75 €']].map(([lab, v, col, p, txt]: any, i) => (
        <div key={i} style={{position: 'absolute', left: 120, top: 850 + i * 230}}>
          <div style={{fontFamily: F.mono, fontSize: 34, color: C.mute, marginBottom: 10}}>{lab} · 1.000 litri</div>
          <div style={{display: 'flex', alignItems: 'center', gap: 24}}>
            <div style={{width: (max * v / 2.75) * p, height: 110, background: col, borderRadius: 16}} />
            <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 80, color: col, opacity: p, whiteSpace: 'nowrap'}}>{txt}</span>
          </div>
        </div>
      ))}
    </AbsoluteFill>
  );
};

/* 5 — the rest of the price */
const Chip: React.FC<{at: number; label: string; i: number}> = ({at, label, i}) => {
  const s = useS(at, {damping: 11, stiffness: 170});
  return <div style={{position: 'absolute', left: 560, top: 720 + i * 150, transform: `translateX(${(1 - s) * 400}px) scale(${0.6 + 0.4 * s})`, opacity: Math.min(1, s * 1.5),
    background: i === 3 ? C.red : '#FFFDF8', color: i === 3 ? '#fff' : C.ink, borderRadius: 60, padding: '22px 44px', boxShadow: '0 10px 24px rgba(0,0,0,0.10)', fontFamily: F.serif, fontWeight: 700, fontSize: 56}}>{label}</div>;
};
const S5: React.FC<{c: Ctx}> = ({c}) => {
  const items = [['plastica', 'plastica'], ['trasporto', 'trasporto'], ['pubblicita', 'pubblicità'], ['margine', 'margine']];
  return (
    <AbsoluteFill>
      <At top={290}><Pop text={'Il resto\ndel prezzo?'} size={110} at={2} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}><Bottle x={140} y={700} s={1} fill={0.8} /></svg>
      {items.map(([tok, lab], i) => <Chip key={tok} at={c.at(tok) - 3} label={lab} i={i} />)}
    </AbsoluteFill>
  );
};

export const N003 = makeEpisode('n003', 3, timing as any, words as any, [S0, S1, S2, S3, S4, S5, SignOff]);

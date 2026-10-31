import React from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C, F, ease} from './kit';
import {Pop, Roll, Float, Slam} from './motion';
import {Coin} from './props';
import {makeEpisode, Ctx, At, SignOff} from './episode';
import timing from '../public/n004/timing.json';
import words from '../public/n004/words.json';

const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const useS = (at: number, cfg = {damping: 14, stiffness: 130}) => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return spring({frame: f - at, fps, config: cfg}); };
const GREY = '#B9B2A5';

/* generic music player (no brand) */
const Player: React.FC<{p: number}> = ({p}) => {
  const f = useCurrentFrame();
  return (
    <div style={{width: 560, margin: '0 auto', background: '#1E1E1C', borderRadius: 48, padding: 40, boxShadow: '0 30px 60px rgba(0,0,0,0.25)'}}>
      <div style={{height: 400, borderRadius: 28, background: `linear-gradient(135deg, ${C.red}, #F2A65A)`, display: 'flex', alignItems: 'flex-end', padding: 24, gap: 10}}>
        {Array.from({length: 14}).map((_, k) => <div key={k} style={{flex: 1, background: 'rgba(255,255,255,0.85)', borderRadius: 6, height: 40 + 140 * Math.abs(noise2D('eq' + k, f * 0.08, 0))}} />)}
      </div>
      <div style={{fontFamily: F.serif, fontWeight: 700, fontSize: 44, color: '#fff', marginTop: 26}}>La tua canzone</div>
      <div style={{fontFamily: F.sans, fontSize: 28, color: '#A8A8A2'}}>Artista</div>
      <div style={{height: 8, background: '#3A3A38', borderRadius: 4, marginTop: 26}}><div style={{height: 8, width: `${p * 100}%`, background: '#fff', borderRadius: 4}} /></div>
      <div style={{display: 'flex', justifyContent: 'center', gap: 60, marginTop: 24}}>
        <svg width="40" height="40" viewBox="0 0 40 40"><path d="M30 6 L12 20 L30 34 Z M8 6 h4 v28 h-4z" fill="#fff" /></svg>
        <svg width="56" height="56" viewBox="0 0 56 56"><circle cx="28" cy="28" r="28" fill="#fff" /><rect x="19" y="16" width="6" height="24" fill="#1E1E1C" /><rect x="31" y="16" width="6" height="24" fill="#1E1E1C" /></svg>
        <svg width="40" height="40" viewBox="0 0 40 40"><path d="M10 6 L28 20 L10 34 Z M28 6 h4 v28 h-4z" fill="#fff" /></svg>
      </div>
    </div>
  );
};

/* 0 — hook */
const S0: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tQ = c.at('quanto'), tM = c.at('meno');
  const pl = useS(-8, {damping: 14, stiffness: 110}); const shrink = interpolate(f, [tQ - 6, tQ + 10], [0, 1], {...cl, easing: ease});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: interpolate(shrink, [0, 1], [380, 300]), width: '100%', transform: `scale(${(0.7 + 0.3 * pl) * (1 - shrink * 0.42)})`, transformOrigin: 'center top'}}>
        <Float seed="pl" amp={4}><Player p={(f % 150) / 150} /></Float>
      </div>
      <At top={900}><Pop text="Quanto guadagna" size={90} at={tQ} /></At>
      <At top={1000}><Pop text="l’*artista?*" size={110} at={tQ + 8} /></At>
      <div style={{position: 'absolute', top: 1170, width: '100%', textAlign: 'center', opacity: f > tM - 2 ? 1 : 0}}>
        <span style={{fontFamily: F.serif, fontWeight: 600, fontSize: 70, color: C.ink}}>meno di </span>
        <Roll value="0,5 cent" size={150} at={tM} />
      </div>
    </AbsoluteFill>
  );
};

/* 1 — one big pot */
const S1: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tN = c.at('non'), tA = c.at('abbonamenti'), tP = c.at('pubblicita'), tC = c.at('cassa');
  const jar = useS(tC - 30);
  return (
    <AbsoluteFill>
      <At top={290}><div style={{textAlign: 'center'}}><Slam at={tN - 2} from={1.8}><span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 96, color: C.ink}}>Non paga <span style={{color: C.red}}>ad ascolto.</span></span></Slam></div></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(540,${980 + (1 - jar) * 700}) scale(0.85)`}>
          <path d="M-260 -260 C -270 -180, -280 140, -240 200 C -200 250, 200 250, 240 200 C 280 140, 270 -180, 260 -260 Z" fill="#FFFDF8" stroke={C.ink} strokeWidth="9" />
          <rect x="-280" y="-300" width="560" height="50" rx="16" fill={C.ink} />
          <text x="0" y="40" textAnchor="middle" fontFamily={F.mono} fontSize="56" fill={C.ink}>CASSA</text>
        </g>
        {Array.from({length: 18}).map((_, k) => {
          const t0 = (k % 2 ? tP : tA) + Math.floor(k / 2) * 3; const p = interpolate(f, [t0, t0 + 18], [0, 1], cl);
          if (p <= 0) return null;
          const x0 = k % 2 ? 900 : 180, x1 = 440 + random('cx' + k) * 200, y1 = 960 + random('cy' + k) * 120;
          const x = x0 + (x1 - x0) * p, y = 560 + (y1 - 560) * p * p;
          return <g key={k} opacity={p < 1 ? 1 : 0.9}><Coin x={x} y={y} r={36} /></g>;
        })}
      </svg>
      <div style={{position: 'absolute', left: 60, top: 470, opacity: f > tA - 4 ? 1 : 0}}><Pop text="abbonamenti" size={52} weight={600} at={tA - 4} /></div>
      <div style={{position: 'absolute', right: 60, top: 470, opacity: f > tP - 4 ? 1 : 0}}><Pop text="pubblicità" size={52} weight={600} at={tP - 4} /></div>
    </AbsoluteFill>
  );
};

/* 2 — two thirds to rights holders */
const S2: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tT = c.at('terzi'), tR = c.at('resto');
  const a = interpolate(f, [tT - 8, tT + 18], [0, 2 / 3], {...cl, easing: ease});
  const R = 260, cx = 540, cy = 860;
  const arc = (from: number, to: number) => { const p = (t: number) => [cx + R * Math.sin(t * 2 * Math.PI), cy - R * Math.cos(t * 2 * Math.PI)]; const [x0, y0] = p(from), [x1, y1] = p(to);
    return `M${cx} ${cy} L${x0} ${y0} A ${R} ${R} 0 ${to - from > 0.5 ? 1 : 0} 1 ${x1} ${y1} Z`; };
  const items = [['etichette', 'etichette'], ['distributori', 'distributori'], ['autori', 'autori']];
  return (
    <AbsoluteFill>
      <At top={290}><Pop text={'Circa *2/3* a chi\nha i diritti'} size={88} at={2} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <circle cx={cx} cy={cy} r={R} fill={GREY} />
        {a > 0.001 && <path d={arc(0, a)} fill={C.red} />}
        <circle cx={cx} cy={cy} r={R} fill="none" stroke={C.ink} strokeWidth="8" />
      </svg>
      <div style={{position: 'absolute', top: 1170, width: '100%', display: 'flex', justifyContent: 'center', gap: 22}}>
        {items.map(([tok, lab], i) => { const s = spring({frame: f - c.at(tok) + 3, fps: 30, config: {damping: 11, stiffness: 170}});
          return <div key={tok} style={{transform: `scale(${s})`, background: C.red, color: '#fff', borderRadius: 40, padding: '14px 30px', fontFamily: F.serif, fontWeight: 700, fontSize: 44}}>{lab}</div>; })}
      </div>
      <div style={{position: 'absolute', top: 1320, width: '100%', textAlign: 'center', opacity: interpolate(f, [tR, tR + 10], [0, 1], cl)}}>
        <span style={{display: 'inline-block', width: 34, height: 34, background: GREY, borderRadius: 8, marginRight: 14, verticalAlign: 'middle'}} />
        <span style={{fontFamily: F.serif, fontWeight: 700, fontSize: 52, color: C.ink, verticalAlign: 'middle'}}>il resto resta a Spotify</span>
      </div>
    </AbsoluteFill>
  );
};

/* 3 — split by stream share */
const S3: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tB = c.at('base'), tT = c.at('tra');
  const heights = [0.95, 0.55, 0.32, 0.18, 0.08, 0.04];
  return (
    <AbsoluteFill>
      <At top={290}><Pop text={'Si divide in base\nagli *ascolti.*'} size={88} at={2} /></At>
      <div style={{position: 'absolute', top: 600, left: 140, right: 140, height: 520, display: 'flex', alignItems: 'flex-end', gap: 26, borderBottom: `6px solid ${C.ink}`}}>
        {heights.map((h, k) => { const p = interpolate(f, [tB - 10 + k * 3, tB + 10 + k * 3], [0, 1], {...cl, easing: ease});
          return <div key={k} style={{flex: 1, height: 500 * h * p, background: k === 3 ? C.red : C.ink, borderRadius: '12px 12px 0 0'}} />; })}
      </div>
      <div style={{position: 'absolute', top: 1140, left: 140, right: 140, display: 'flex', justifyContent: 'space-between', fontFamily: F.mono, fontSize: 26, color: C.mute}}>
        <span>più ascolti</span><span>meno ascolti</span>
      </div>
      <div style={{position: 'absolute', top: 1230, width: '100%', textAlign: 'center', opacity: f > tT - 2 ? 1 : 0}}>
        <Roll value="0,003–0,005 $" size={110} at={tT} />
        <div style={{fontFamily: F.mono, fontSize: 32, color: C.ink, marginTop: 10}}>in media ad ascolto</div>
      </div>
      <At top={1470}><Pop text="Spotify non ha una tariffa fissa · stime TuneCore 2026" size={26} weight={500} font={F.mono} at={tT + 8} stagger={0.25} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

/* 4 — the label takes its cut */
const S4: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tE = c.at('etichetta'), tP = c.at('prende');
  const flow = interpolate(f, [tE - 10, tP + 20], [0, 1], cl);
  const cut = useS(tP, {damping: 9, stiffness: 200});
  return (
    <AbsoluteFill>
      <At top={290}><Pop text={'Prima di arrivare\nall’artista…'} size={88} at={2} /></At>
      {[['ETICHETTA', 260], ['ARTISTA', 880]].map(([lab, y]: any, i) => (
        <div key={i} style={{position: 'absolute', top: y + 300, left: 290, width: 500, height: 160, borderRadius: 30, background: i ? '#FFFDF8' : C.ink, border: `7px solid ${C.ink}`,
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: F.mono, fontSize: 52, color: i ? C.ink : '#fff'}}>{lab}</div>
      ))}
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        {Array.from({length: 8}).map((_, k) => { const p = (flow * 1.6 - k * 0.1); if (p <= 0) return null; if (p >= 1 && !(k % 2 === 0)) return null;
          const kept = k % 2 === 0 && p > 0.45; // half the coins stay at the label
          const y = kept ? 600 - k * 6 : 400 + p * 820; const x = kept ? 820 : 540 + (k % 3 - 1) * 60; return <g key={k}><Coin x={x} y={y} r={34} /></g>; })}
      </svg>
      <div style={{position: 'absolute', top: 820, width: '100%', textAlign: 'center', transform: `scale(${cut}) rotate(${(1 - cut) * -30}deg)`, opacity: Math.min(1, cut * 2)}}>
        <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 90, color: C.red}}>✂ la sua parte</span>
      </div>
    </AbsoluteFill>
  );
};

/* 5 — 200,000 streams for 1,000 €, and the 1,000-stream floor */
const S5: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const tD = c.at('duecentomila'), tS = c.at('sotto'), tN = c.at('niente');
  const n = interpolate(f, [4, tD + 6], [0, 200000], {...cl, easing: ease});
  const zero = useS(tN - 4, {damping: 8, stiffness: 220});
  const phase2 = f > tS - 6;
  return (
    <AbsoluteFill>
      <div style={{opacity: phase2 ? 0.15 : 1, transition: 'none'}}>
        <At top={300}><Pop text="Per guadagnare *1.000 €*" size={84} at={2} /></At>
        <div style={{position: 'absolute', top: 520, width: '100%', textAlign: 'center', fontFamily: F.serif, fontWeight: 800, fontSize: 200, color: C.ink, fontVariantNumeric: 'tabular-nums'}}>
          {Math.round(n).toLocaleString('it-IT')}</div>
        <At top={760}><Pop text="ascolti (e più)" size={56} weight={600} at={tD} /></At>
      </div>
      {phase2 && <>
        <At top={980}><Pop text={'Sotto i *1.000* ascolti\nin un anno:'} size={78} at={tS - 4} /></At>
        <div style={{position: 'absolute', top: 1200, width: '100%', textAlign: 'center', transform: `scale(${2 - zero}) rotate(-8deg)`, opacity: Math.min(1, zero * 2)}}>
          <span style={{display: 'inline-block', border: `12px solid ${C.red}`, color: C.red, fontFamily: F.serif, fontWeight: 800, fontSize: 150, padding: '0 50px', borderRadius: 26}}>0 €</span>
        </div>
      </>}
      <At top={1490}><Pop text="regola Spotify in vigore dal 2024" size={26} weight={500} font={F.mono} at={tS} stagger={0.3} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

export const N004 = makeEpisode('n004', 4, timing as any, words as any, [S0, S1, S2, S3, S4, S5, SignOff]);

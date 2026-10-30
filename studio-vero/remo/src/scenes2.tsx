import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {evolvePath} from '@remotion/paths';
import {C, F, Mark, ease} from './kit';
import {Bean} from './props';
import {Pop, Roll, Float, Marker, Slam} from './motion';
import italy from '../italy.json';

const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const At: React.FC<{top: number; children: React.ReactNode}> = ({top, children}) => <div style={{position: 'absolute', top, left: 0, width: '100%'}}>{children}</div>;
const useS = (at: number, cfg = {damping: 14, stiffness: 130}) => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return spring({frame: f - at, fps, config: cfg}); };

/* D — receipt: of 1,29 € twelve cents go to the State */
export const D: React.FC<{r: (s: number) => number; segs: number[][]}> = ({r, segs}) => {
  const f = useCurrentFrame();
  const t1 = r(segs[1][0]), t2 = r(segs[2][0]);
  const unroll = interpolate(f, [t1 - 10, t1 + 20], [0, 1], {...cl, easing: ease});
  const stamp = useS(t2, {damping: 9, stiffness: 220});
  const H = 560 * unroll;
  const rows: [string, string, number][] = [['CAFFÈ', '1,29', t1 - 4], ['di cui IVA 10%', '0,12', t1 + 10], ['', '', 0]];
  return (
    <AbsoluteFill>
      <At top={280}><Pop text="E il *resto?*" size={150} at={2} stagger={1.3} /></At>
      <div style={{position: 'absolute', top: 560, left: 290, width: 500, height: 640, overflow: 'hidden'}}>
        <div style={{position: 'absolute', top: 0, width: 500, height: H, background: '#FFFDF8', boxShadow: '0 20px 40px rgba(0,0,0,0.12)',
          WebkitMaskImage: 'linear-gradient(#000 0 0)', clipPath: `polygon(0 0,100% 0,100% calc(100% - 14px),${Array.from({length: 20}).map((_, i) => `${100 - i * 5 - 2.5}% 100%, ${100 - (i + 1) * 5}% calc(100% - 14px)`).join(',')})`}}>
          <div style={{padding: '40px 44px', fontFamily: F.mono, color: C.ink}}>
            <div style={{textAlign: 'center', fontSize: 30, letterSpacing: 4}}>BAR · SCONTRINO</div>
            <div style={{borderTop: '3px dashed #999', margin: '26px 0'}} />
            {rows.slice(0, 2).map(([a, b, at], i) => {
              const p = interpolate(f, [at, at + 8], [0, 1], cl);
              return <div key={i} style={{display: 'flex', justifyContent: 'space-between', fontSize: i ? 32 : 40, margin: '18px 0', opacity: p,
                color: i ? C.red : C.ink, fontWeight: i ? 700 : 500}}><span>{a}</span><span>{b} €</span></div>;
            })}
            <div style={{borderTop: '3px dashed #999', margin: '26px 0'}} />
          </div>
        </div>
        <div style={{position: 'absolute', top: 360, left: 120, transform: `rotate(-14deg) scale(${2.4 - 1.4 * stamp})`, opacity: Math.min(1, stamp * 2),
          border: `8px solid ${C.red}`, color: C.red, fontFamily: F.serif, fontWeight: 800, fontSize: 64, padding: '6px 26px', borderRadius: 14, mixBlendMode: 'multiply'}}>ALLO STATO</div>
      </div>
      <At top={1270}><div style={{textAlign: 'center'}}><Roll value="0,12 €" size={170} at={t1 + 12} /></div></At>
    </AbsoluteFill>
  );
};

/* icons for the costs */
const Icon: React.FC<{k: string}> = ({k}) => {
  const s = {stroke: C.ink, strokeWidth: 7, fill: 'none', strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  if (k === 'affitto') return <svg viewBox="0 0 100 100" width="90"><path d="M15 50 L50 20 L85 50 M25 42 V82 H75 V42" {...s} /><rect x="42" y="58" width="16" height="24" {...s} /></svg>;
  if (k === 'personale') return <svg viewBox="0 0 100 100" width="90"><circle cx="50" cy="34" r="15" {...s} /><path d="M22 84 C 24 60, 76 60, 78 84" {...s} /></svg>;
  if (k === 'energia') return <svg viewBox="0 0 100 100" width="90"><path d="M56 12 L28 56 H50 L42 88 L72 42 H50 Z" {...s} fill={C.red} stroke={C.ink} /></svg>;
  return <svg viewBox="0 0 100 100" width="90"><rect x="18" y="16" width="64" height="30" rx="6" {...s} /><path d="M30 46 V60 H70 V46 M42 60 V70 H58 V60" {...s} /><path d="M24 84 H76" {...s} /></svg>;
};

/* E — the bar pays the rest */
export const E: React.FC<{r: (s: number) => number; segs: number[][]}> = ({r, segs}) => {
  const f = useCurrentFrame();
  const items = ['affitto', 'personale', 'energia', 'macchina'];
  const tb = r(segs[1][0]);
  const bar = interpolate(f, [4, 30], [0, 1], {...cl, easing: ease});
  const total = 1.29, H = 700, x0 = 120, y0 = 600;
  const parts: [number, string, string][] = [[0.04, C.red, 'caffè'], [0.12, C.ink, 'IVA'], [1.13, '#B9B2A5', 'bar']];
  let y = y0 + H;
  return (
    <AbsoluteFill>
      <At top={280}><Pop text="Tutto il resto" size={96} weight={600} at={2} /></At>
      <At top={385}><Pop text="paga il *bar.*" size={120} at={tb} stagger={1.3} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        {parts.map(([v, col, lab], i) => {
          const g = interpolate(f, [4 + i * 7, 22 + i * 7], [0, 1], {...cl, easing: ease});
          const h = Math.max(i === 0 ? 14 : 0, (H * v) / total) * g; y -= h;
          return <g key={i}><rect x={x0} y={y} width={190} height={h} fill={col} />
            <text x={x0 + 215} y={i === 2 ? y + 50 : y + h / 2 + (i === 0 ? 30 : 14)} fontFamily={F.mono} fontSize="30" fill={i === 0 ? C.red : C.ink} opacity={g}>
              {lab} · {v.toFixed(2).replace('.', ',')} €</text></g>;
        })}
        <rect x={x0} y={y0} width={190} height={H} fill="none" stroke={C.ink} strokeWidth="5" opacity={bar} />
      </svg>
      {items.map((k, i) => {
        const at = r(segs[2 + i][0]) - 3;
        const s = useS(at, {damping: 11, stiffness: 170});
        return (
          <div key={k} style={{position: 'absolute', left: 560, top: 700 + i * 150, display: 'flex', alignItems: 'center', gap: 24,
            transform: `translateX(${(1 - s) * 400}px) scale(${0.6 + 0.4 * s})`, opacity: Math.min(1, s * 1.5)}}>
            <div style={{width: 120, height: 120, borderRadius: 60, background: '#FFFDF8', boxShadow: '0 10px 24px rgba(0,0,0,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Icon k={k} /></div>
            <span style={{fontFamily: F.serif, fontWeight: 600, fontSize: 56, color: C.ink}}>{k}</span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/* F — map: Messina vs Bolzano */
const MAP = {x: 140, y: 470, s: 1.3};          // map placement: 610x793 viewBox scaled
const pt = (x: number, y: number) => [MAP.x + x * MAP.s, MAP.y + y * MAP.s];
export const Fm: React.FC<{r: (s: number) => number; segs: number[][]}> = ({r, segs}) => {
  const f = useCurrentFrame();
  const draw = interpolate(f, [0, 40], [0, 1], {...cl, easing: ease});
  const tM = r(segs[1][0]), tB = r(segs[2][0]);
  const pins: [string, number[], string, number, string][] = [['MESSINA', pt(444, 612), '1,06 €', tM, C.ink], ['BOLZANO', pt(250, 48), '1,51 €', tB, C.red]];
  return (
    <AbsoluteFill>
      <At top={270}><Pop text="Ecco perché" size={90} weight={600} at={2} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(${MAP.x},${MAP.y}) scale(${MAP.s})`}>
          {(italy as any).locations.map((l: any, i: number) => {
            const ev = evolvePath(Math.min(1, Math.max(0, draw * 1.3 - i * 0.015)), l.path);
            const hi = (l.id === 'sicily' && f > tM) || (l.id === 'trentino-south-tyrol' && f > tB);
            return <path key={l.id} d={l.path} fill={hi ? (l.id === 'sicily' ? '#D9D2C4' : '#F2C4B8') : '#E9E3D6'} fillOpacity={draw}
              stroke={C.ink} strokeWidth={1.6} strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
          })}
        </g>
        {pins.map(([name, [x, y], price, at, col], i) => {
          const s = spring({frame: f - at, fps: 30, config: {damping: 9, stiffness: 160}});
          if (f < at) return null;
          return <g key={i} transform={`translate(${x},${y - (1 - s) * 200})`}>
            <circle r={20 + 30 * (1 - Math.min(1, (f - at) / 20))} fill={col} opacity={0.25 * (1 - Math.min(1, (f - at) / 20))} />
            <path d="M0 0 C -26 -30, -26 -62, 0 -62 C 26 -62, 26 -30, 0 0 Z" fill={col} /><circle cy="-42" r="9" fill="#fff" />
          </g>;
        })}
      </svg>
      {pins.map(([name, [x, y], price, at, col], i) => (
        <div key={'l' + i} style={{position: 'absolute', left: i === 0 ? 110 : 600, top: i === 0 ? 1310 : 470, textAlign: 'left'}}>
          <div style={{fontFamily: F.mono, fontSize: 32, color: C.mute, opacity: f > at ? 1 : 0}}>{name}</div>
          <Roll value={price} size={130} at={at + 4} color={col} />
        </div>
      ))}
    </AbsoluteFill>
  );
};

/* G — same bean, you pay the counter */
export const G: React.FC<{r: (s: number) => number; segs: number[][]}> = ({r, segs}) => {
  const f = useCurrentFrame();
  const t2 = r(segs[1][0]);
  const beanS = useS(0, {damping: 12, stiffness: 120});
  const shrink = interpolate(f, [t2 - 6, t2 + 8], [0, 1], {...cl, easing: ease});
  const counter = useS(t2 - 2, {damping: 15, stiffness: 110});
  return (
    <AbsoluteFill>
      <At top={290}><Pop text={'Il chicco è\nlo *stesso.*'} size={120} at={2} /></At>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(540,${interpolate(shrink, [0, 1], [930, 760])}) scale(${beanS * interpolate(shrink, [0, 1], [1, 0.4])}) rotate(${f * 1.2})`}>
          <Bean x={0} y={0} r={150} rot={-20} />
        </g>
        {/* bar counter */}
        <g transform={`translate(0,${(1 - counter) * 900})`}>
          <rect x="90" y="980" width="900" height="44" rx="12" fill="#2A2A28" />
          <rect x="120" y="1024" width="840" height="300" fill="#6B4A33" />
          {[0, 1, 2, 3, 4, 5].map((i) => <rect key={i} x={140 + i * 140} y={1044} width={120} height={260} rx="6" fill="none" stroke="#4E3524" strokeWidth="5" />)}
          <g transform="translate(700,900)"><rect x="-80" y="-10" width="160" height="90" rx="14" fill="#B8B2A6" stroke={C.ink} strokeWidth="5" /><rect x="-20" y="80" width="40" height="20" fill={C.ink} /></g>
        </g>
      </svg>
      <At top={1390}><Pop text="Paghi il *bancone.*" size={100} at={t2} stagger={1.2} /></At>
    </AbsoluteFill>
  );
};

/* H — sign-off */
export const Hs: React.FC<{r: (s: number) => number; segs: number[][]}> = ({r, segs}) => {
  const f = useCurrentFrame();
  const draw = interpolate(f, [0, 22], [0, 1], {...cl, easing: ease});
  const dot = useS(16, {damping: 8, stiffness: 200});
  const tN = r(segs[2][0]);
  const arrow = Math.sin(f * 0.25) * 14;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 380, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Float seed="mark" amp={4}><Mark size={300} draw={draw} dot={dot} /></Float>
      </div>
      <At top={740}><Pop text="Sono *Vero*" size={130} at={6} /></At>
      <At top={900}><Pop text="un’AI che ti spiega cosa c’è dietro le cose" size={34} weight={500} font={F.mono} at={r(segs[1][0])} stagger={0.4} tracking={0} color={C.mute} /></At>
      <At top={1130}><Pop text={'Il prossimo perché\nlo scegli *tu.*'} size={92} at={tN} /></At>
      <div style={{position: 'absolute', top: 1400 + arrow, width: '100%', textAlign: 'center', opacity: f > tN + 20 ? 1 : 0, fontFamily: F.sans, fontWeight: 700, fontSize: 40, color: C.red}}>
        scrivilo nei commenti ↓</div>
    </AbsoluteFill>
  );
};

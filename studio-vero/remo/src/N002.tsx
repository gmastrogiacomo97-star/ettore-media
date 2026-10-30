import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C, F, ease} from './kit';
import {Pop, Roll, Float, Marker, Slam} from './motion';
import {makeEpisode, Ctx, At, SignOff} from './episode';
import timing from '../public/n002/timing.json';
import words from '../public/n002/words.json';

const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const AMBER = '#E8A93A', AMBER_D = '#C9862A';
const useS = (at: number, cfg = {damping: 14, stiffness: 130}) => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return spring({frame: f - at, fps, config: cfg}); };
const eur = (v: number, d = 2) => v.toFixed(d).replace('.', ',');

/* fuel pump display */
const Pump: React.FC<{euro: number; litri: number; scale?: number}> = ({euro, litri, scale = 1}) => (
  <div style={{transform: `scale(${scale})`, width: 620, margin: '0 auto', background: '#1E1E1C', borderRadius: 40, padding: '34px 40px', boxShadow: '0 30px 60px rgba(0,0,0,0.25)'}}>
    {[['EURO', eur(euro)], ['LITRI', eur(litri)]].map(([k, v], i) => (
      <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#C9D9B8', borderRadius: 16, padding: '10px 26px', marginBottom: i ? 0 : 18}}>
        <span style={{fontFamily: F.mono, fontSize: 30, color: '#3B4A2E'}}>{k}</span>
        <span style={{fontFamily: F.mono, fontWeight: 500, fontSize: i ? 70 : 110, color: '#1C2A12', fontVariantNumeric: 'tabular-nums'}}>{v}</span>
      </div>
    ))}
  </div>
);

/* the litre jar: layers from bottom; each [value, colour, label] grows with its own progress */
const Jar: React.FC<{layers: [number, string, number][]; total?: number; wave?: boolean; x?: number; y?: number; w?: number; h?: number}> =
  ({layers, total = 2.015, wave = true, x = 300, y = 560, w = 480, h = 860}) => {
  const f = useCurrentFrame(); let acc = 0;
  return (
    <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
      <defs><clipPath id="jar"><rect x={x} y={y} width={w} height={h} rx="50" /></clipPath></defs>
      <rect x={x + 8} y={y + 14} width={w} height={h} rx="50" fill="#000" opacity="0.08" />
      <rect x={x} y={y} width={w} height={h} rx="50" fill="#FFFDF8" />
      <g clipPath="url(#jar)">
        {layers.map(([v, col, p], i) => {
          const hh = (h * v / total) * p; const top = y + h - acc - hh; acc += hh;
          const isTop = i === layers.length - 1 && wave;
          const d = isTop ? `M${x} ${top} ` + Array.from({length: 13}).map((_, k) => `L${x + k * w / 12} ${top + noise2D('w', k * 0.4, f * 0.04) * 10}`).join(' ') + ` L${x + w} ${top + hh} L${x} ${top + hh} Z`
            : `M${x} ${top} H${x + w} V${top + hh} H${x} Z`;
          return <path key={i} d={d} fill={col} />;
        })}
        <rect x={x + 40} y={y + 40} width="26" height={h - 80} rx="13" fill="#fff" opacity="0.35" />
      </g>
      <rect x={x} y={y} width={w} height={h} rx="50" fill="none" stroke={C.ink} strokeWidth="8" />
      <text x={x + w / 2} y={y - 24} textAnchor="middle" fontFamily={F.mono} fontSize="34" fill={C.ink}>1 LITRO</text>
    </svg>
  );
};

/* 0 — hook */
const S0: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame();
  const tQ = c.at('quanti');
  const euro = interpolate(f, [0, 40], [37.4, 100], {...cl, easing: ease});
  const pumpY = interpolate(f, [tQ - 4, tQ + 10], [0, 1], {...cl, easing: ease});
  return (
    <AbsoluteFill>
      <At top={300}><Pop text="Fai il pieno da" size={80} weight={600} at={-30} /></At>
      <At top={400}><div style={{textAlign: 'center'}}><Slam at={-3} from={1.8}><span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 230, color: C.red, letterSpacing: -5}}>100 €</span></Slam></div></At>
      <div style={{position: 'absolute', top: interpolate(pumpY, [0, 1], [820, 1000]), width: '100%', transform: `scale(${1 - pumpY * 0.25})`}}>
        <Float seed="pump" amp={4}><Pump euro={euro} litri={euro / 2.015} /></Float>
      </div>
      <At top={1330}><Pop text="Quanti vanno" size={92} at={tQ} /></At>
      <At top={1430}><Pop text="allo *Stato?*" size={110} at={tQ + 8} /></At>
    </AbsoluteFill>
  );
};

/* 1 — a litre costs about 2 € */
const S1: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame();
  const fill = interpolate(f, [4, 40], [0, 1], {...cl, easing: ease});
  const tDue = c.at('due');
  return (
    <AbsoluteFill>
      <At top={290}><Pop text="Un litro di benzina" size={84} weight={600} at={2} /></At>
      <At top={410}><div style={{textAlign: 'center'}}><Roll value="2,015 €" size={190} at={10} /></div></At>
      <Jar layers={[[2.015, AMBER, fill]]} y={700} h={720} />
      <At top={1470}><Pop text="media self · Mimit, 28 ottobre 2026" size={28} weight={500} font={F.mono} at={tDue} stagger={0.3} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

/* 2 — excise */
const S2: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame();
  const g = interpolate(f, [c.at('accise') - 14, c.at('accise') + 10], [0, 1], {...cl, easing: ease});
  const tF = c.at('fissa'); const stamp = useS(tF, {damping: 9, stiffness: 220});
  return (
    <AbsoluteFill>
      <Jar layers={[[0.6729, C.ink, g], [2.015 - 0.6729, AMBER, 1]]} x={120} y={560} w={420} h={860} />
      <div style={{position: 'absolute', left: 590, top: 1120}}>
        <Roll value="0,67 €" size={150} at={2} color={C.ink} />
        <div style={{fontFamily: F.mono, fontSize: 40, color: C.ink, marginTop: 10, opacity: g}}>ACCISE</div>
      </div>
      <div style={{position: 'absolute', left: 600, top: 1330, transform: `rotate(-10deg) scale(${2.2 - 1.2 * stamp})`, opacity: Math.min(1, stamp * 2),
        border: `7px solid ${C.red}`, color: C.red, fontFamily: F.serif, fontWeight: 800, fontSize: 54, padding: '4px 22px', borderRadius: 12}}>FISSA</div>
      <At top={300}><Pop text={'Sessantasette centesimi\nsono *accise.*'} size={86} at={2} /></At>
    </AbsoluteFill>
  );
};

/* 3 — VAT, also on the excise */
const S3: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame();
  const tI = c.at('iva'); const tA = c.at('anche');
  const g = interpolate(f, [tI - 6, tI + 16], [0, 1], {...cl, easing: ease});
  const arrow = interpolate(f, [tA, tA + 16], [0, 1], {...cl, easing: ease});
  const H = 860, y = 560, total = 2.015; const yI = y + H - H * (0.6729 + 0.9787) / total - (H * 0.3634 / total) / 2; const yA = y + H - (H * 0.6729 / total) / 2;
  return (
    <AbsoluteFill>
      <Jar layers={[[0.6729, C.ink, 1], [0.9787, AMBER, 1], [0.3634, C.red, g]]} x={120} y={y} w={420} h={H} wave={false} />
      <div style={{position: 'absolute', left: 590, top: yI - 90}}>
        <Roll value="0,36 €" size={130} at={tI} />
        <div style={{fontFamily: F.mono, fontSize: 36, color: C.red, opacity: g}}>IVA 22%</div>
      </div>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <path d={`M560 ${yI + 60} C 700 ${yI + 220}, 700 ${yA - 100}, 560 ${yA}`} fill="none" stroke={C.red} strokeWidth="8" strokeDasharray="900" strokeDashoffset={900 * (1 - arrow)} strokeLinecap="round" />
        <path d={`M560 ${yA} l 26 -6 l -12 24 z`} fill={C.red} opacity={arrow > 0.95 ? 1 : 0} />
      </svg>
      <div style={{position: 'absolute', left: 720, top: (yI + yA) / 2 - 20, opacity: arrow, transform: `translateX(${(1 - arrow) * 60}px)`}}>
        <div style={{fontFamily: F.serif, fontWeight: 800, fontSize: 80, color: C.red}}>+0,15 €</div>
        <div style={{fontFamily: F.mono, fontSize: 28, color: C.ink, width: 300}}>di IVA calcolata<br />sulle accise</div>
      </div>
      <At top={300}><Pop text={'Poi c’è l’*IVA*,\nil 22%.'} size={92} at={2} /></At>
    </AbsoluteFill>
  );
};

/* 4 — a tax on a tax */
const Stamp: React.FC<{at: number; y: number; rot: number; label: string; color: string}> = ({at, y, rot, label, color}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - at, fps, config: {damping: 8, stiffness: 200}});
  return <div style={{position: 'absolute', top: y, width: '100%', display: 'flex', justifyContent: 'center', transform: `translateY(${(1 - s) * -900}px) rotate(${rot + noise2D(label, f * 0.03, 0) * 2}deg)`}}>
    <div style={{border: `12px solid ${color}`, color, fontFamily: F.serif, fontWeight: 800, fontSize: 150, padding: '0 60px', borderRadius: 26, background: C.paper}}>{label}</div>
  </div>;
};
const S4: React.FC<{c: Ctx}> = ({c}) => {
  const tS = c.at('sopra');
  return (
    <AbsoluteFill>
      <Stamp at={2} y={1020} rot={4} label="TASSA" color={C.ink} />
      <Stamp at={tS - 4} y={820} rot={-6} label="TASSA" color={C.red} />
      <At top={300}><Pop text={'Una tassa *sopra*\nun’altra tassa.'} size={100} at={c.at('una')} /></At>
    </AbsoluteFill>
  );
};

/* 5 — total to the State vs the actual fuel */
const S5: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame();
  const tP = c.at('piu'), tB = c.at('benzina'), tM = c.at('meno');
  const b1 = interpolate(f, [tP, tP + 14], [0, 1], {...cl, easing: ease}), b2 = interpolate(f, [tB, tB + 14], [0, 1], {...cl, easing: ease});
  const H = 860, y = 560, total = 2.015;
  const yAmb = [y + H - H * (0.6729 + 0.9787) / total, y + H - H * 0.6729 / total];
  return (
    <AbsoluteFill>
      <Jar layers={[[0.6729, C.ink, 1], [0.9787, AMBER, 1], [0.3634, C.red, 1]]} x={120} y={y} w={420} h={H} wave={false} />
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        {/* bracket for taxes: red top + ink bottom (two pieces) */}
        <path d={`M570 ${y} h30 V${yAmb[0]} h-30`} fill="none" stroke={C.red} strokeWidth="6" opacity={b1} />
        <path d={`M570 ${yAmb[1]} h30 V${y + H} h-30`} fill="none" stroke={C.red} strokeWidth="6" opacity={b1} />
        <path d={`M560 ${yAmb[0] + 8} h40 V${yAmb[1] - 8} h-40`} fill="none" stroke={AMBER_D} strokeWidth="6" opacity={b2} />
      </svg>
      <div style={{position: 'absolute', left: 630, top: y + 20, opacity: b1, transform: `translateX(${(1 - b1) * 80}px)`}}>
        <Roll value="1,04 €" size={120} at={tP} color={C.red} />
        <div style={{fontFamily: F.mono, fontSize: 32, color: C.red}}>ALLO STATO</div>
      </div>
      <div style={{position: 'absolute', left: 630, top: (yAmb[0] + yAmb[1]) / 2 - 60, opacity: b2, transform: `translateX(${(1 - b2) * 80}px)`}}>
        <Roll value="0,98 €" size={110} at={tB} color={AMBER_D} />
        <div style={{fontFamily: F.mono, fontSize: 28, color: C.ink, width: 360}}>benzina, trasporto<br />e guadagno</div>
      </div>
      <At top={1440}><div style={{textAlign: 'center', opacity: f > tM ? 1 : 0}}><Pop text="meno della *metà*" size={64} at={tM} /></div></At>
      <At top={300}><Pop text={'Totale: più di *1 €*\nal litro allo Stato.'} size={84} at={2} /></At>
    </AbsoluteFill>
  );
};

/* 6 — your 100 € fill-up */
const S6: React.FC<{c: Ctx}> = ({c}) => {
  const f = useCurrentFrame(); const t51 = c.at('cinquantuno');
  const split = interpolate(f, [t51 - 6, t51 + 16], [0, 1], {...cl, easing: ease});
  const pumpS = useS(0);
  return (
    <AbsoluteFill>
      <At top={300}><Pop text="Sul tuo pieno da 100 €" size={80} weight={600} at={2} /></At>
      <div style={{position: 'absolute', top: 470, width: '100%', transform: `scale(${0.6 + 0.4 * pumpS})`}}><Pump euro={100} litri={49.63} scale={0.85} /></div>
      <div style={{position: 'absolute', top: 900, left: 90, width: 900, height: 160, display: 'flex', gap: 14 * split}}>
        <div style={{flex: 51, background: C.red, borderRadius: 18, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `translateX(${-split * 10}px)`}}>
          <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 80, color: '#fff', opacity: split}}>51 €</span></div>
        <div style={{flex: 49, background: AMBER, borderRadius: 18, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `translateX(${split * 10}px)`}}>
          <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 80, color: C.ink, opacity: split}}>49 €</span></div>
      </div>
      <div style={{position: 'absolute', top: 1080, left: 90, width: 900, display: 'flex', fontFamily: F.mono, fontSize: 32, opacity: split}}>
        <div style={{flex: 51, color: C.red}}>tasse</div><div style={{flex: 49, color: C.ink}}>benzina e il resto</div>
      </div>
      <At top={1260}><div style={{textAlign: 'center'}}><Slam at={t51}><span style={{fontFamily: F.serif, fontWeight: 800, fontSize: 120, color: C.ink}}>sono <span style={{color: C.red}}>tasse.</span></span></Slam></div></At>
      <At top={1470}><Pop text="accisa 0,6729 €/l · IVA 22% · prezzo Mimit 2,015 €/l" size={26} weight={500} font={F.mono} at={t51 + 10} stagger={0.25} tracking={0} color={C.mute} /></At>
    </AbsoluteFill>
  );
};

export const N002 = makeEpisode('n002', 2, timing as any, words as any, [S0, S1, S2, S3, S4, S5, S6, SignOff]);

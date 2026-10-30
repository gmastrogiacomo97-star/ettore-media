import React from 'react';
import {random, useCurrentFrame, interpolate} from 'remotion';
import {C, F, ease} from './kit';

const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

/* single coffee bean */
export const Bean: React.FC<{x: number; y: number; r: number; rot: number; s?: number}> = ({x, y, r, rot, s = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <ellipse cx="0" cy="0" rx={r} ry={r * 0.72} fill="#4A2A17" />
    <ellipse cx={-r * 0.25} cy={-r * 0.25} rx={r * 0.45} ry={r * 0.25} fill="#7A4A2A" opacity="0.55" />
    <path d={`M${-r * 0.75},0 C ${-r * 0.3},${-r * 0.25} ${r * 0.3},${r * 0.25} ${r * 0.75},0`} stroke="#22120A" strokeWidth={r * 0.14} fill="none" strokeLinecap="round" />
  </g>
);

/* beans pouring from (sx,sy) into a pile centred at (px,py); t0..t1 = pour window (frames) */
export const BeanPour: React.FC<{n: number; sx: number; sy: number; px: number; py: number; t0: number; t1: number; w?: number}> =
  ({n, sx, sy, px, py, t0, t1, w = 150}) => {
  const f = useCurrentFrame();
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const start = t0 + (i / n) * (t1 - t0);
        const tf = (f - start) / 30; if (tf < 0) return null;
        // final resting spot: rows of a mound
        const row = Math.floor(Math.sqrt(i * 1.6)); const k = i - Math.floor(row * row / 1.6);
        const restX = px + (random('bx' + i) - 0.5) * w * (1 - row * 0.12) ;
        const restY = py - row * 13 - random('by' + i) * 6;
        const fall = Math.min(1, tf / 0.45);
        const x = sx + (restX - sx) * fall + (random('jx' + i) - 0.5) * 30 * Math.sin(fall * Math.PI);
        const y = sy + (restY - sy) * (fall * fall);
        const bounce = fall >= 1 ? Math.max(0, Math.sin(Math.min(1, (tf - 0.45) / 0.2) * Math.PI)) * 8 : 0;
        return <Bean key={i} x={x} y={y - bounce} r={13} rot={random('r' + i) * 360 + tf * 200 * (1 - fall)} />;
      })}
    </g>
  );
};

/* kitchen scale with LCD; value shown in grams */
export const Scale: React.FC<{x: number; y: number; grams: number; children?: React.ReactNode}> = ({x, y, grams, children}) => (
  <g transform={`translate(${x},${y})`}>
    <ellipse cx="0" cy="96" rx="230" ry="18" fill="#000" opacity="0.10" />
    <rect x="-210" y="-10" width="420" height="100" rx="26" fill="#2A2A28" />
    <rect x="-200" y="-4" width="400" height="12" rx="6" fill="#3B3B38" />
    <rect x="-90" y="26" width="180" height="50" rx="10" fill="#C9D9B8" />
    <text x="60" y="64" textAnchor="end" fontFamily={F.mono} fontSize="40" fontWeight="500" fill="#1C2A12">{grams.toFixed(1)}</text>
    <text x="66" y="64" fontFamily={F.mono} fontSize="20" fill="#1C2A12">g</text>
    {/* pan */}
    <ellipse cx="0" cy="-16" rx="180" ry="22" fill="#D8D2C6" stroke={C.ink} strokeWidth="4" />
    {children}
  </g>
);

/* 1-cent coin */
export const Coin: React.FC<{x: number; y: number; r?: number; tilt?: number}> = ({x, y, r = 46, tilt = 0.32}) => (
  <g transform={`translate(${x},${y})`}>
    <ellipse cx="0" cy={r * tilt * 0.35} rx={r} ry={r * tilt} fill="#8C4A22" />
    <ellipse cx="0" cy="0" rx={r} ry={r * tilt} fill="#C46F3A" stroke="#7A3D1A" strokeWidth="3" />
    <ellipse cx="0" cy="0" rx={r * 0.78} ry={r * tilt * 0.78} fill="none" stroke="#E39A62" strokeWidth="3" />
  </g>
);

/* coins dropping and stacking */
export const CoinStack: React.FC<{x: number; y: number; n: number; t0: number; gap?: number}> = ({x, y, n, t0, gap = 7}) => {
  const f = useCurrentFrame();
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const p = interpolate(f, [t0 + i * gap, t0 + i * gap + 12], [0, 1], clamp);
        if (p <= 0) return null;
        const yy = y - i * 17 - (1 - Math.pow(p, 2)) * 520;
        const sq = p >= 1 ? 1 - 0.12 * Math.max(0, Math.sin(Math.min(1, (f - t0 - i * gap - 12) / 5) * Math.PI)) : 1;
        return <g key={i} transform={`translate(0,${(1 - sq) * 6})`}><Coin x={x} y={yy} /></g>;
      })}
    </g>
  );
};

/* number counting with tabular digits */
export const Count: React.FC<{from: number; to: number; t0: number; t1: number; dec?: number; suffix?: string; size: number; color?: string}> =
  ({from, to, t0, t1, dec = 2, suffix = ' €', size, color = C.red}) => {
  const f = useCurrentFrame();
  const v = interpolate(f, [t0, t1], [from, to], {...clamp, easing: ease});
  return <span style={{fontFamily: F.serif, fontWeight: 800, fontSize: size, color, fontVariantNumeric: 'tabular-nums', letterSpacing: -size * 0.015}}>
    {v.toFixed(dec).replace('.', ',')}{suffix}</span>;
};

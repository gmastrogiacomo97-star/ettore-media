import React from 'react';
import {useCurrentFrame} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C} from './kit';

/* espresso cup, side view, ink outline + soft shading; steam driven by noise */
export const Cup: React.FC<{size?: number; steam?: number; fill?: number}> = ({size = 620, steam = 1, fill = 1}) => {
  const f = useCurrentFrame();
  const steamPath = (k: number) => {
    const pts: string[] = [];
    for (let i = 0; i <= 24; i++) {
      const y = 130 - i * 7;
      const x = 200 + (k - 1) * 46 + noise2D('s' + k, i * 0.12, f * 0.018) * (8 + i * 1.6);
      pts.push(`${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`);
    }
    return pts.join(' ');
  };
  return (
    <svg width={size} height={size * 0.82} viewBox="0 0 400 330">
      <defs>
        <linearGradient id="cer" x1="0" x2="1">
          <stop offset="0" stopColor="#FFFFFF" /><stop offset="0.55" stopColor="#F6F2EA" /><stop offset="1" stopColor="#D9D1C2" />
        </linearGradient>
        <radialGradient id="crema" cx="0.42" cy="0.4" r="0.7">
          <stop offset="0" stopColor="#D9A066" /><stop offset="0.55" stopColor={C.crema} /><stop offset="1" stopColor="#6B3F22" />
        </radialGradient>
        <linearGradient id="sau" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#FFFFFF" /><stop offset="1" stopColor="#DCD4C5" /></linearGradient>
        <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" /></filter>
        <linearGradient id="sfade" x1="0" x2="0" y1="1" y2="0"><stop offset="0" stopColor="#fff" stopOpacity="0" /><stop offset="0.25" stopColor="#fff" stopOpacity="1" /><stop offset="1" stopColor="#fff" stopOpacity="0" /></linearGradient>
        <mask id="sm"><rect x="0" y="0" width="400" height="140" fill="url(#sfade)" /></mask>
      </defs>
      {/* steam */}
      <g mask="url(#sm)">{[0, 1, 2].map((k) => (
        <path key={k} d={steamPath(k)} fill="none" stroke="#9C9284" strokeOpacity={0.35 * steam} strokeWidth={14} strokeLinecap="round"
          filter="url(#blur)" style={{maskImage: 'none'}} />
      ))}</g>
      {/* shadow */}
      <ellipse cx="200" cy="300" rx="170" ry="16" fill="#000" opacity="0.10" />
      {/* saucer */}
      <ellipse cx="200" cy="284" rx="172" ry="30" fill="url(#sau)" stroke={C.ink} strokeWidth="5" />
      <ellipse cx="200" cy="278" rx="100" ry="14" fill="none" stroke={C.ink} strokeOpacity="0.18" strokeWidth="3" />
      {/* handle */}
      <path d="M300 170 C 350 160, 360 230, 300 236" fill="none" stroke={C.ink} strokeWidth="14" strokeLinecap="round" />
      <path d="M300 170 C 350 160, 360 230, 300 236" fill="none" stroke="#F6F2EA" strokeWidth="5" strokeLinecap="round" />
      {/* body */}
      <path d="M96 150 L 112 250 C 118 282, 282 282, 288 250 L 304 150 Z" fill="url(#cer)" stroke={C.ink} strokeWidth="5" strokeLinejoin="round" />
      <path d="M124 170 L 134 238" stroke="#fff" strokeWidth="8" strokeLinecap="round" opacity="0.9" />
      {/* rim + crema */}
      <ellipse cx="200" cy="150" rx="104" ry="20" fill="#F6F2EA" stroke={C.ink} strokeWidth="5" />
      <ellipse cx="200" cy="152" rx="90" ry="14" fill="url(#crema)" opacity={fill} />
      <path d="M150 150 C 175 141, 215 160, 245 148" fill="none" stroke="#E8BC86" strokeWidth="3" opacity={0.8 * fill} />
    </svg>
  );
};

/* a small heap of ground coffee */
export const Grounds: React.FC<{size?: number; k?: number}> = ({size = 220, k = 1}) => (
  <svg width={size} height={size * 0.6} viewBox="0 0 200 120" style={{overflow: 'visible'}}>
    <ellipse cx="100" cy="104" rx="90" ry="10" fill="#000" opacity="0.1" />
    <path d={`M10 104 C 40 ${104 - 70 * k}, 160 ${104 - 70 * k}, 190 104 Z`} fill={C.coffee} />
    {Array.from({length: 40}).map((_, i) => {
      const x = 20 + ((i * 37) % 160), y = 100 - ((i * 53) % 60) * k * Math.sin((x - 10) / 180 * Math.PI);
      return <circle key={i} cx={x} cy={y} r={1.8 + (i % 3)} fill={i % 2 ? '#5A3A24' : '#2A170C'} />;
    })}
  </svg>
);

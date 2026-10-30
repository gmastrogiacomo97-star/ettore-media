import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, Paper} from './kit';
export const Avatar: React.FC = () => (
  <Paper>
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <svg width="820" height="820" viewBox="0 0 100 100">
        <defs>
          <radialGradient id="dot" cx="0.38" cy="0.35" r="0.7"><stop offset="0" stopColor="#FF7A5C" /><stop offset="1" stopColor={C.red} /></radialGradient>
        </defs>
        <g transform="translate(-4,-4)">
          <line x1="62" y1="62" x2="80" y2="80" stroke="#000" strokeOpacity="0.10" strokeWidth="13" strokeLinecap="round" transform="translate(1.2,1.6)" />
          <circle cx="45.2" cy="45.6" r="27" fill="none" stroke="#000" strokeOpacity="0.10" strokeWidth="8" />
          <line x1="64" y1="64" x2="80" y2="80" stroke={C.ink} strokeWidth="12" strokeLinecap="round" />
          <circle cx="80" cy="80" r="4.2" fill={C.red} />
          <circle cx="44" cy="44" r="27" fill={C.paper} stroke={C.ink} strokeWidth="8" />
          <path d="M26 36 A 20 20 0 0 1 36 25" stroke="#fff" strokeOpacity="0.6" strokeWidth="2.4" fill="none" strokeLinecap="round" />
          <circle cx="44" cy="44" r="9.5" fill="url(#dot)" />
        </g>
      </svg>
    </AbsoluteFill>
  </Paper>
);

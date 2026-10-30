import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, F, Paper, Masthead} from './kit';
import {Cup, Grounds} from './Cup';
export const Cover001: React.FC = () => {
  const lx = 600, ly = 1080, LR = 230;
  return (
    <Paper>
      <Masthead num={1} />
      <div style={{position: 'absolute', top: 330, width: '100%', textAlign: 'center', fontFamily: F.serif, fontWeight: 800, color: C.ink}}>
        <div style={{fontSize: 96, lineHeight: 1}}>Perché un caffè</div>
        <div style={{fontSize: 96, lineHeight: 1.1}}>costa</div>
        <div style={{fontSize: 250, lineHeight: 1, color: C.red, letterSpacing: -5}}>1,29 €<span style={{color: C.ink}}>?</span></div>
      </div>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <defs><clipPath id="cl"><circle cx={lx} cy={ly} r={LR - 20} /></clipPath></defs>
        <g transform="translate(200,850)"><Cup size={600} /></g>
        <g clipPath="url(#cl)">
          <rect width="1080" height="1920" fill={C.paper2} />
          <g transform={`translate(${lx - 150},${ly - 30})`}><Grounds size={300} k={1} /></g>
          <text x={lx} y={ly - 60} textAnchor="middle" fontFamily={F.serif} fontWeight="800" fontSize="100" fill={C.red}>0,04 €</text>
        </g>
        <circle cx={lx} cy={ly} r={LR - 10} fill="none" stroke={C.ink} strokeWidth="22" />
        <line x1={lx + LR * 0.7} y1={ly + LR * 0.7} x2={lx + LR * 1.15} y2={ly + LR * 1.15} stroke={C.ink} strokeWidth="34" strokeLinecap="round" />
        <circle cx={lx + LR * 1.15} cy={ly + LR * 1.15} r="14" fill={C.red} />
      </svg>
      <div style={{position: 'absolute', top: 1500, width: '100%', textAlign: 'center', fontFamily: F.mono, fontSize: 34, color: C.mute, letterSpacing: 2}}>DOVE VANNO I TUOI SOLDI</div>
    </Paper>
  );
};

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

export const Cover002: React.FC = () => {
  const x = 300, y = 820, w = 480, h = 640, total = 2.015;
  const L: [number, string][] = [[0.6729, C.ink], [0.9787, '#E8A93A'], [0.3634, C.red]];
  let acc = 0;
  return (
    <Paper>
      <Masthead num={2} />
      <div style={{position: 'absolute', top: 320, width: '100%', textAlign: 'center', fontFamily: F.serif, fontWeight: 800, color: C.ink}}>
        <div style={{fontSize: 92, lineHeight: 1.05}}>Pieno da <span style={{color: C.red}}>100 €</span>.</div>
        <div style={{fontSize: 92, lineHeight: 1.05}}>Quanti vanno</div>
        <div style={{fontSize: 92, lineHeight: 1.05}}>allo <span style={{color: C.red}}>Stato?</span></div>
      </div>
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
        <defs><clipPath id="j2"><rect x={x} y={y} width={w} height={h} rx="50" /></clipPath></defs>
        <rect x={x + 8} y={y + 14} width={w} height={h} rx="50" fill="#000" opacity="0.08" />
        <g clipPath="url(#j2)">{L.map(([v, col], i) => { const hh = h * v / total; const top = y + h - acc - hh; acc += hh; return <rect key={i} x={x} y={top} width={w} height={hh} fill={col} />; })}
          <rect x={x + 40} y={y + 40} width="26" height={h - 80} rx="13" fill="#fff" opacity="0.35" /></g>
        <rect x={x} y={y} width={w} height={h} rx="50" fill="none" stroke={C.ink} strokeWidth="8" />
        <text x={x + w / 2} y={y - 24} textAnchor="middle" fontFamily={F.mono} fontSize="34" fill={C.ink}>1 LITRO</text>
      </svg>
      <div style={{position: 'absolute', top: 1520, width: '100%', textAlign: 'center', fontFamily: F.mono, fontSize: 34, color: C.mute, letterSpacing: 2}}>BENZINA · I CONTI VERI</div>
    </Paper>
  );
};

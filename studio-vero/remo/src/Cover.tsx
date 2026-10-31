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

export const Cover003: React.FC = () => (
  <Paper>
    <Masthead num={3} />
    <div style={{position: 'absolute', top: 320, width: '100%', textAlign: 'center', fontFamily: F.serif, fontWeight: 800, color: C.ink}}>
      <div style={{fontSize: 88, lineHeight: 1.05}}>L’acqua in bottiglia</div>
      <div style={{fontSize: 88, lineHeight: 1.05}}>costa</div>
      <div style={{fontSize: 260, lineHeight: 1, color: C.red, letterSpacing: -6}}>×90</div>
      <div style={{fontSize: 70, lineHeight: 1.05}}>quella del rubinetto.</div>
    </div>
    <svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
      <g transform="translate(250,880) scale(0.9)">
        <path d="M80 0 h40 v40 c0 30 70 50 70 110 v420 c0 30 -20 40 -40 40 h-100 c-20 0 -40 -10 -40 -40 v-420 c0 -60 70 -80 70 -110 z" fill="#9FD0EC" stroke={C.ink} strokeWidth="7" />
        <rect x="72" y="-22" width="56" height="30" rx="6" fill="#2F6FA0" stroke={C.ink} strokeWidth="6" />
        <rect x="10" y="260" width="180" height="110" fill={C.red} />
        <text x="100" y="328" textAnchor="middle" fontFamily={F.serif} fontWeight="800" fontSize="40" fill="#fff">0,24 €</text>
      </g>
      <g transform="translate(560,1120) scale(0.9)">
        <path d="M80 160 L260 160 L245 380 L95 380 Z" fill="#9FD0EC" opacity="0.8" />
        <path d="M70 80 L270 80 L250 385 L90 385 Z" fill="none" stroke={C.ink} strokeWidth="7" strokeLinejoin="round" />
        <text x="170" y="290" textAnchor="middle" fontFamily={F.serif} fontWeight="800" fontSize="34" fill={C.ink}>0,003 €</text>
      </g>
    </svg>
    <div style={{position: 'absolute', top: 1560, width: '100%', textAlign: 'center', fontFamily: F.mono, fontSize: 32, color: C.mute, letterSpacing: 2}}>AL LITRO · E CHI LA IMBOTTIGLIA?</div>
  </Paper>
);

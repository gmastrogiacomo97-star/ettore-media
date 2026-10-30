import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import '@fontsource/fraunces/600.css';
import '@fontsource/fraunces/800.css';
import '@fontsource/fraunces/600-italic.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/700.css';
import '@fontsource/jetbrains-mono/500.css';

export const C = {
  paper: '#F3EFE6', paper2: '#E9E3D6', ink: '#141414', red: '#E8452C', mute: '#7A7368',
  coffee: '#3B2416', crema: '#B9814A',
};
export const F = {
  serif: '"Fraunces", serif', sans: '"Inter", sans-serif', mono: '"JetBrains Mono", monospace',
};
export const ease = Easing.bezier(0.16, 1, 0.3, 1);       // expo-out
export const easeIO = Easing.bezier(0.65, 0, 0.35, 1);

export const useSpring = (delay = 0, cfg = {damping: 14, stiffness: 120, mass: 0.8}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return spring({frame: f - delay, fps, config: cfg});
};
export const fade = (f: number, a: number, b: number) =>
  interpolate(f, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

/* paper with grain + soft vignette */
export const Paper: React.FC<{children?: React.ReactNode}> = ({children}) => (
  <AbsoluteFill style={{background: C.paper}}>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 40%, rgba(255,255,255,0.55), rgba(0,0,0,0) 60%), radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(60,40,20,0.16) 100%)'}} />
    {children}
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'multiply', opacity: 0.55}}>
      <svg width="100%" height="100%">
        <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" stitchTiles="stitch" />
          <feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.3  0 0 0 0.22 0" /></filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  </AbsoluteFill>
);

/* Vero mark: ring + red dot */
export const Mark: React.FC<{size: number; draw?: number; dot?: number}> = ({size, draw = 1, dot = 1}) => {
  const r = 40, sw = 9, circ = 2 * Math.PI * r;
  return (
    <svg width={size} height={size} viewBox="0 0 100 100">
      <circle cx="50" cy="50" r={r} fill="none" stroke={C.ink} strokeWidth={sw} strokeLinecap="round"
        strokeDasharray={circ} strokeDashoffset={circ * (1 - draw)} transform="rotate(-90 50 50)" />
      <circle cx="50" cy="50" r={12 * dot} fill={C.red} />
    </svg>
  );
};

export const Masthead: React.FC<{num: number}> = ({num}) => {
  const f = useCurrentFrame();
  const line = interpolate(f, [-1, 0], [1, 1], {extrapolateRight: 'clamp', easing: ease});
  return (
    <div style={{position: 'absolute', top: 150, left: 90, right: 90}}>
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontFamily: F.mono, fontSize: 30, color: C.ink, letterSpacing: 2}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 16}}><Mark size={40} />DIETRO LE COSE</div>
        <div style={{color: C.mute}}>N. {String(num).padStart(3, '0')}</div>
      </div>
      <div style={{height: 3, background: C.ink, marginTop: 22, transformOrigin: 'left', transform: `scaleX(${line})`}} />
    </div>
  );
};

/* word-by-word kinetic headline; *word* = red */
export const Kinetic: React.FC<{text: string; size: number; delay?: number; stagger?: number; color?: string; italic?: boolean; weight?: number; lh?: number}> =
  ({text, size, delay = 0, stagger = 3, color = C.ink, italic = false, weight = 800, lh = 1.05}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  let red = false, wi = 0;
  return (
    <div style={{fontFamily: F.serif, fontWeight: weight, fontSize: size, lineHeight: lh, color, textAlign: 'center', fontStyle: italic ? 'italic' : 'normal', letterSpacing: -size * 0.02}}>
      {text.split('\n').map((line, li) => (
        <div key={li} style={{display: 'block'}}>
          {line.split(' ').map((w, i) => {
            if (w.startsWith('*')) red = true;
            const isRed = red; if (w.endsWith('*') || /\*[.,!?]$/.test(w)) red = false;
            const s = spring({frame: f - delay - wi++ * stagger, fps, config: {damping: 16, stiffness: 140, mass: 0.7}});
            return (
              <span key={i} style={{display: 'inline-block', overflow: 'hidden', verticalAlign: 'top', padding: '0 0.12em', margin: '0 -0.04em'}}>
                <span style={{display: 'inline-block', transform: `translateY(${(1 - s) * 105}%)`, color: isRed ? C.red : undefined}}>{w.replace(/\*/g, '')}</span>
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export const Note: React.FC<{children: React.ReactNode; delay?: number; y?: number}> = ({children, delay = 10, y = 1570}) => {
  const f = useCurrentFrame();
  return <div style={{position: 'absolute', top: y, width: '100%', textAlign: 'center', fontFamily: F.mono, fontSize: 28, color: C.mute, opacity: fade(f, delay, delay + 12), letterSpacing: 1}}>{children}</div>;
};

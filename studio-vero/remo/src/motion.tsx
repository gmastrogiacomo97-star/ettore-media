import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {C, F, ease} from './kit';

const cl = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

/* per-letter pop: rises, scales and un-blurs; *word* red; optional exit */
export const Pop: React.FC<{text: string; size: number; at?: number; stagger?: number; weight?: number; font?: string; color?: string;
  lh?: number; exitAt?: number; align?: 'center' | 'left'; tracking?: number}> =
  ({text, size, at = 0, stagger = 1.1, weight = 800, font = F.serif, color = C.ink, lh = 1.05, exitAt, align = 'center', tracking = -0.02}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  let red = false, n = 0;
  const ex = exitAt !== undefined ? interpolate(f, [exitAt, exitAt + 8], [0, 1], {...cl, easing: ease}) : 0;
  return (
    <div style={{fontFamily: font, fontWeight: weight, fontSize: size, lineHeight: lh, color, textAlign: align, letterSpacing: size * tracking}}>
      {text.split('\n').map((line, li) => (
        <div key={li} style={{whiteSpace: 'nowrap'}}>
          {line.split(' ').map((w, wi) => {
            if (w.startsWith('*')) red = true;
            const isRed = red; if (/\*[.,!?…]?$/.test(w)) red = false;
            const chars = w.replace(/\*/g, '').split('');
            return (
              <span key={wi} style={{display: 'inline-block', marginRight: '0.24em'}}>
                {chars.map((ch, ci) => {
                  const k = n++;
                  const s = spring({frame: f - at - k * stagger, fps, config: {damping: 13, stiffness: 160, mass: 0.6}});
                  const e2 = ex > 0 ? interpolate(ex, [0, 1], [0, 1]) : 0;
                  return <span key={ci} style={{display: 'inline-block', color: isRed ? C.red : undefined,
                    transform: `translateY(${(1 - s) * 0.6 - e2 * 0.5}em) scale(${0.3 + 0.7 * s}) rotate(${(1 - s) * (k % 2 ? 12 : -12)}deg)`,
                    opacity: Math.min(1, s * 1.5) * (1 - e2), filter: `blur(${(1 - Math.min(1, s)) * 10 + e2 * 8}px)`}}>{ch}</span>;
                })}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

/* slot-machine number: each digit rolls to its target */
export const Roll: React.FC<{value: string; size: number; at?: number; dur?: number; color?: string; stagger?: number}> =
  ({value, size, at = 0, dur = 24, color = C.red, stagger = 3}) => {
  const f = useCurrentFrame(); let d = 0;
  const vis = interpolate(f, [at - 1, at + 4], [0, 1], cl);
  return (
    <span style={{opacity: vis, display: 'inline-flex', fontFamily: F.serif, fontWeight: 800, fontSize: size, color, lineHeight: 1, letterSpacing: -size * 0.015}}>
      {value.split('').map((ch, i) => {
        if (!/[0-9]/.test(ch)) {
          const p = interpolate(f, [at + i * stagger, at + i * stagger + 10], [0, 1], {...cl, easing: ease});
          return <span key={i} style={{display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 0.4}em)`}}>{ch === ' ' ? ' ' : ch}</span>;
        }
        const k = d++; const target = +ch + 10 * (2 + k);
        const p = interpolate(f, [at + k * stagger, at + k * stagger + dur], [0, 1], {...cl, easing: ease});
        const pos = p * target; const blur = Math.min(8, Math.abs(interpolate(f, [at + k * stagger, at + k * stagger + dur * 0.6, at + k * stagger + dur], [0, 1, 0], cl)) * 8);
        return (
          <span key={i} style={{display: 'inline-block', height: '1em', overflow: 'hidden', position: 'relative', width: '0.62em'}}>
            <span style={{position: 'absolute', left: 0, right: 0, textAlign: 'center', transform: `translateY(${-pos}em)`, filter: `blur(${blur}px)`}}>
              {Array.from({length: target + 1}).map((_, j) => <div key={j} style={{height: '1em'}}>{j % 10}</div>)}
            </span>
          </span>
        );
      })}
    </span>
  );
};

/* gentle perpetual drift so nothing is ever frozen */
export const Float: React.FC<{seed: string; amp?: number; rot?: number; children: React.ReactNode; style?: React.CSSProperties}> =
  ({seed, amp = 6, rot = 0.6, children, style}) => {
  const f = useCurrentFrame();
  const x = noise2D(seed + 'x', f * 0.012, 0) * amp, y = noise2D(seed + 'y', 0, f * 0.012) * amp, r = noise2D(seed + 'r', f * 0.01, 1) * rot;
  return <div style={{...style, transform: `${style?.transform ?? ''} translate(${x}px,${y}px) rotate(${r}deg)`}}>{children}</div>;
};

/* marker swipe behind/under text */
export const Marker: React.FC<{at: number; width: number; height?: number; color?: string; opacity?: number}> =
  ({at, width, height = 22, color = C.red, opacity = 0.9}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at, at + 10], [0, 1], {...cl, easing: ease});
  return <div style={{width, height, background: color, opacity, transformOrigin: 'left', transform: `scaleX(${p}) skewX(-12deg)`, borderRadius: 4, margin: '0 auto'}} />;
};

/* slam: big entrance from scale>1 with blur and a short shake */
export const Slam: React.FC<{at?: number; children: React.ReactNode; from?: number}> = ({at = 0, children, from = 2.4}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - at, fps, config: {damping: 11, stiffness: 200, mass: 0.7}});
  const sc = from + (1 - from) * s; const shake = f - at > 3 && f - at < 12 ? Math.sin((f - at) * 2.6) * (12 - (f - at)) * 1.4 : 0;
  return <div style={{transform: `translateX(${shake}px) scale(${sc})`, filter: `blur(${(1 - Math.min(1, s)) * 14}px)`, opacity: Math.min(1, s * 2)}}>{children}</div>;
};

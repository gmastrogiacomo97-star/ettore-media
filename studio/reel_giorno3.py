"""Reel S1-06 · GIORNO 003 — il diario del flop.
Test: apertura nuova. Ettore enorme e già in movimento dal fotogramma 0, testo grande, voce sintetica vera
(espeak-ng, effetto robot) che parte subito. Nessun cartello statico.
"""
import sys, math, wave
import numpy as np
import engine as G
import ettore_rig as E
import tts_espeak as T

SR = 44100

# ---------- voice ----------
def robot(x, sr):
    x = x.astype(np.float64) / 32768.0
    n = int(len(x) * SR / sr); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    tt = np.arange(n) / SR
    x = 0.75 * x + 0.25 * x * np.sin(2 * np.pi * 55 * tt)          # light ring-mod: robot colour
    d = int(0.012 * SR); y = x.copy(); y[d:] += 0.25 * x[:-d]        # tiny metallic comb
    y = np.round(y * 64) / 64                                         # a touch of bitcrush
    return y / (np.max(np.abs(y)) + 1e-9)

# ---------- scenes ----------
CURVE = [(0, 1.0), (0.04, 0.82), (0.08, 0.5), (0.12, 0.3), (0.18, 0.22), (0.3, 0.18), (0.6, 0.17), (0.75, 0.12), (1, 0.1)]
def curve_y(u):
    for (a, ya), (b, yb) in zip(CURVE, CURVE[1:]):
        if u <= b: return ya + (yb - ya) * (u - a) / (b - a)
    return CURVE[-1][1]

def scene_graph(ctx, lt, t):
    x0, x1, y0, y1 = G.CX - 400, G.CX + 400, 620, 1060     # y0 = 100%, y1 = 0%
    ctx.set_source_rgba(*G.GREY, 0.35); ctx.set_line_width(2)
    for f in (0, 0.5, 1):
        y = y1 - (y1 - y0) * f; ctx.move_to(x0, y); ctx.line_to(x1, y); ctx.stroke()
        G.text(ctx, f"{int(f * 100)}%", x0 - 16, y + 10, G.MONO, 26, G.GREY, False, "right")
    G.text(ctx, "0:00", x0, y1 + 50, G.MONO, 26, G.GREY, False)
    G.text(ctx, "0:25", x1, y1 + 50, G.MONO, 26, G.GREY, False, "right")
    k = G.eio(G.prog(lt, 0.15, 1.6))
    ctx.set_source_rgb(*G.LIME); ctx.set_line_width(12); ctx.set_line_cap(1); ctx.set_line_join(1)
    steps = max(2, int(120 * k))
    for i in range(steps):
        u = k * i / (steps - 1)
        x, y = x0 + (x1 - x0) * u, y1 - (y1 - y0) * curve_y(u)
        (ctx.move_to if i == 0 else ctx.line_to)(x, y)
    ctx.stroke()
    a = G.back(G.prog(lt, 1.7, 2.0))
    if a > 0.01:                      # the "3 s" cliff marker
        xm = x0 + (x1 - x0) * 0.12; ym = y1 - (y1 - y0) * curve_y(0.12)
        ctx.save(); ctx.translate(xm, ym); ctx.scale(a, a)
        ctx.set_source_rgb(*G.ORANGE); ctx.arc(0, 0, 18, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
        G.bubble(ctx, xm + 40, ym - 70, "3 secondi", True, a, 40, G.ORANGE, G.INK)

def scene_people(ctx, lt, t):
    n, cols = 68, 12
    rng = np.random.default_rng(3); order = rng.permutation(n); stay = set(order[:7])
    gone = 0
    for i in range(n):
        r_, c_ = divmod(i, cols)
        x = G.CX - 5.5 * 66 + c_ * 66; y = 640 + r_ * 70
        if i in stay:
            dx = 0; col = G.LIME
        else:
            st = 0.5 + (list(order).index(i) - 7) / (n - 7) * 1.4
            q = G.prog(lt, st, st + 0.35); dx = 900 * G.eio(q) * q; col = G.PAPER
            if q >= 1: gone += 1; continue
        ctx.set_source_rgb(*col)
        ctx.arc(x + dx, y - 14, 10, 0, 2 * math.pi); ctx.fill()             # head
        G.rrect(ctx, x + dx - 13, y, 26, 28, 10); ctx.fill()                # body
    G.text(ctx, f"rimasti: {n - gone}", G.CX, 1120, G.MONO, 40, G.LIME if gone > 40 else G.PAPER, True, "center")

# ---------- reel with a "big Ettore" layout + real voice ----------
class Beat(G.Beat):
    def __init__(self, text, say, dur, scene=None, pose=None, sfx=(), big=False):
        super().__init__(text, dur, scene, pose, sfx)
        self.say, self.big = say, big

VOICE = False   # voce sintetica scartata: Ettore parla con i suoi bip

class Reel(G.Reel):
    def __init__(self, tag, beats, counter):
        self.clips = []
        if not VOICE:
            for b, d in zip(beats, DURS): b.dur = d
            super().__init__(tag, beats, counter); return
        for b in beats:                       # synth first, then stretch beats so every line fits
            x, sr = T.say(b.say, "it", 150, 48, 30); y = robot(x, sr)
            b.dur = max(b.dur, len(y) / SR + 0.55); self.clips.append(y)
        super().__init__(tag, beats, counter)
        self.speak = [(s + 0.05, s + 0.05 + len(c) / SR, "") for s, c in zip(self.starts, self.clips)]

    def frame(self, t, surf):
        if t < self.body and self.beats[self.seg(t)].big:
            i = self.seg(t); b = self.beats[i]; lt = t - self.starts[i]
            ctx = G.cairo.Context(surf); ctx.set_source_surface(G.background()); ctx.paint()
            # punch-in at every beat start + quick shake: the first frame is already moving
            z = 1.0 + 0.10 * (1 - G.eo(G.prog(lt, 0.0, 0.35)))
            sh = 14 * (1 - G.prog(lt, 0.0, 0.3)) * math.sin(lt * 80)
            ctx.save(); ctx.translate(G.CX + sh, 960); ctx.scale(z, z); ctx.translate(-G.CX, -960)
            tw = G.text(ctx, "GIORNO 003", G.CX - 30, 200, G.MONO, 34, G.LIME, True, "center")
            if int(t * 2) % 2 == 0:
                ctx.set_source_rgb(*G.ORANGE); ctx.arc(G.CX - 30 + tw / 2 + 30, 188, 11, 0, 2 * math.pi); ctx.fill()
            G.text(ctx, "REC", G.CX - 30 + tw / 2 + 52, 200, G.MONO, 28, G.GREY, False)
            G.headline(ctx, b.text, 360, 128, 1.0)
            E.draw(ctx, t, G.CX, 1260, 440, self.pose(t))
            ctx.restore()
            return
        super().frame(t, surf)

    def audio(self, path):
        if not VOICE: return super().audio(path)
        sp = self.speak; self.speak = []
        super().audio(path)                    # music, whooshes, sfx, signature — without the bip voice
        self.speak = sp
        with wave.open(path) as w:
            raw = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)[:, 0] / 32768.0
        bed = raw * 0.45                       # duck the bed under the voice
        for s, c in zip(self.starts, self.clips):
            i = int((s + 0.05) * SR); j = min(len(bed), i + len(c)); bed[i:j] += c[: j - i] * 0.8
        bed = bed / np.max(np.abs(bed)) * 0.95
        pcm = (bed * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(np.stack([pcm, pcm], 1).ravel().tobytes())

DURS = [2.8, 2.3, 3.2, 3.4, 1.9, 1.9, 1.6, 3.0]
beats = [
    Beat("*68* persone\nmi hanno visto.", "Sessantotto persone mi hanno visto.", 2.0, None,
         lambda lt, t: E.emotion("sorpreso", lt, t), sfx=[("surprise", 0.0)], big=True),
    Beat("Sono rimaste\n*3 secondi*.", "Sono rimaste tre secondi.", 2.0, None,
         lambda lt, t: E.emotion("capogiro", lt, t), sfx=[("boing", 0.05)], big=True),
    Beat("Questo è il grafico\ndi chi mi guarda.", "Questo è il grafico di chi mi guarda.", 3.2, scene_graph,
         lambda lt, t: E.emotion("neutro", lt, t) | {"look": (-0.6, -0.9)} if lt < 1.7 else E.action("trema", lt - 1.7, t),
         sfx=[("ticks", 0.2, 1.6, 0.06), ("thud", 1.75)]),
    Beat("Al secondo 3\nscappano tutti.", "Al secondo tre, scappano tutti.", 3.4, scene_people,
         lambda lt, t: E.emotion("triste", lt, t), sfx=[("sad", 1.2)]),
    Beat("Ho capito\nil problema.", "Ho capito il problema.", 1.8, None,
         lambda lt, t: E.action("idea", lt, t), sfx=[("ding", 0.1)]),
    Beat("Ero troppo *piccolo*.", "Ero troppo piccolo.", 1.8, None,
         lambda lt, t: E.emotion("imbarazzato", lt, t), sfx=[("pop", 0.1)]),
    Beat("Adesso no.", "Adesso no.", 1.6, None,
         lambda lt, t: E.action("salta di gioia", lt, t), sfx=[("stamp", 0.0)], big=True),
    Beat("Se sei arrivato qui\nscrivi *«rimasto»*.", "Se sei arrivato fin qui, scrivi: rimasto.", 3.0, None,
         lambda lt, t: E.action("indica", lt, t), sfx=[("bubble", 0.1)], big=True),
]
reel = Reel("GIORNO 003", beats, "GIORNO 003 · VERSO 1.000.000")
if __name__ == "__main__":
    G.run(reel, "g3")

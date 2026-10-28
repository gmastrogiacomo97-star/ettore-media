"""Ettore reel engine.
A reel = list of Beat(text, dur, scene, pose, sfx). The engine handles: tag line, big centered headline
(words in *...* or «...» are lime), scene band, expressive Ettore, voice bips, whooshes, light beat,
closing signature «Annotato.», cover-ready frames, MP4 render.
"""
import math, subprocess, zlib, wave, sys
import cairo
import numpy as np
import ettore_rig as E

W, H, FPS = 1080, 1920, 30
BG = (0x0E/255,) * 3
LIME, INK, PAPER, ORANGE = E.LIME, E.INK, E.PAPER, E.ORANGE
GREY = (0xA8/255, 0xA8/255, 0xA2/255)
DARK = (0x1A/255,) * 3
WATER = E.WATER
SANS, MONO = "Space Grotesk Light", "JetBrains Mono"
CX = 540
SCENE_Y = 840          # centre of the scene band
ETT_Y, ETT_R = 1378, 190
SIG = 1.7

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)

# ---------- drawing helpers ----------
def rrect(ctx, x, y, w, h, r):
    E.rrect(ctx, x, y, w, h, r)

def font(ctx, fam, size, bold=True):
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text(ctx, s, x, y, fam=SANS, size=60, color=PAPER, bold=True, align="left", alpha=1.0):
    font(ctx, fam, size, bold)
    adv = ctx.text_extents(s).x_advance
    if align == "center": x -= adv / 2
    elif align == "right": x -= adv
    ctx.set_source_rgba(*color, alpha); ctx.move_to(x, y); ctx.show_text(s)
    return adv

def typed(s, lt, start, cps=20):
    return s[: int(max(0.0, lt - start) * cps)]

def paper(ctx, w, h):
    rrect(ctx, -w / 2, -h / 2, w, h, 14); ctx.set_source_rgb(*PAPER); ctx.fill()
    ctx.set_source_rgba(0.55, 0.75, 0.95, 0.35); ctx.set_line_width(2)
    for i in range(1, int(h / 56)):
        yy = -h / 2 + i * 56 + 10; ctx.move_to(-w / 2 + 24, yy); ctx.line_to(w / 2 - 24, yy); ctx.stroke()
    ctx.set_source_rgba(*ORANGE, 0.5); ctx.move_to(-w / 2 + 70, -h / 2); ctx.line_to(-w / 2 + 70, h / 2); ctx.stroke()

def bubble(ctx, x, y, s, left, k=1.0, size=40, fill=None, tcol=None):
    """chat bubble anchored at (x,y): left bubbles grow right from x, right bubbles grow left."""
    if k <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k)
    font(ctx, SANS, size, True); tw = ctx.text_extents(s).x_advance
    bw = tw + size * 1.3; bh = size * 1.9
    bx = 0 if left else -bw
    rrect(ctx, bx, -bh / 2, bw, bh, bh * 0.38)
    ctx.set_source_rgb(*(fill or ((0.22, 0.22, 0.22) if left else LIME))); ctx.fill()
    text(ctx, s, bx + size * 0.65, size * 0.35, SANS, size, tcol or (PAPER if left else INK), True)
    ctx.restore()

_BG = None
def background():
    global _BG
    if _BG is None:
        _BG = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); b = cairo.Context(_BG)
        b.set_source_rgb(*BG); b.paint(); b.set_source_rgba(1, 1, 1, 0.05)
        for gx in range(30, W, 60):
            for gy in range(30, H, 60):
                b.arc(gx, gy, 2, 0, 2 * math.pi); b.fill()
    return _BG

def headline(ctx, s, y, size, alpha, dy=0.0):
    font(ctx, SANS, size, True)
    lines = s.split("\n")
    widest = max(ctx.text_extents(l.replace("*", "")).x_advance for l in lines)
    if widest > 900: size *= 900 / widest; font(ctx, SANS, size, True)
    sp = ctx.text_extents(" ").x_advance
    quote = s.startswith("«")          # a whole spoken line: all lime
    for i, line in enumerate(lines):
        words = line.split(" "); clean = [w.replace("*", "") for w in words]
        lw = sum(ctx.text_extents(w).x_advance for w in clean) + sp * (len(words) - 1)
        x = CX - lw / 2
        for w, c in zip(words, clean):
            hl = quote or w.startswith("*") or "«" in w or "»" in w
            ctx.set_source_rgba(*(LIME if hl else PAPER), alpha)
            ctx.move_to(x, y + dy + i * size * 1.12); ctx.show_text(c)
            x += ctx.text_extents(c).x_advance + sp

def hook_headline(ctx, s, y, size):
    """giant ink text on lime; *words* go in an ink box with lime text."""
    font(ctx, SANS, size, True)
    lines = s.split("\n")
    widest = max(ctx.text_extents(l.replace("*", "")).x_advance for l in lines)
    if widest > 880: size *= 880 / widest; font(ctx, SANS, size, True)
    sp = ctx.text_extents(" ").x_advance
    for i, line in enumerate(lines):
        words = line.split(" "); clean = [w.replace("*", "") for w in words]
        lw = sum(ctx.text_extents(w).x_advance for w in clean) + sp * (len(words) - 1)
        x = CX - lw / 2; yy = y + i * size * 1.08
        for w, c in zip(words, clean):
            adv = ctx.text_extents(c).x_advance
            if w.startswith("*"):
                rrect(ctx, x - 14, yy - size * 0.82, adv + 28, size * 1.05, 16); ctx.set_source_rgb(*INK); ctx.fill()
                ctx.set_source_rgb(*LIME)
            else:
                ctx.set_source_rgb(*INK)
            ctx.move_to(x, yy); ctx.show_text(c); x += adv + sp

# ---------- reel ----------
class Beat:
    def __init__(self, text, dur, scene=None, pose=None, sfx=(), scale=1.0, tag=None, speak=True, hook=False):
        self.text, self.dur, self.scene, self.pose, self.hook = text, dur, scene, pose, hook
        self.sfx, self.scale, self.tag, self.speak = list(sfx), scale, tag, speak

class Reel:
    def __init__(self, tag, beats, counter, quiet=()):
        self.tag, self.beats, self.counter = tag, beats, counter
        self.starts = []; t = 0.0
        for b in beats: self.starts.append(t); t += b.dur
        self.body = t; self.dur = t + SIG; self.quiet = list(quiet)   # quiet = (start,end) with no music
        self.speak = []
        for b, s in zip(beats, self.starts):
            if b.speak and b.text:
                n = len(b.text.replace("\n", " ").replace("*", ""))
                self.speak.append((s + 0.08, s + 0.08 + min(n * 0.062, b.dur - 0.6), b.text.replace("*", "")))

    def seg(self, t):
        for i, b in enumerate(self.beats):
            if t < self.starts[i] + b.dur: return i
        return len(self.beats) - 1

    def talking(self, t):
        return any(a <= t < b for a, b, _ in self.speak) or (self.body + 0.47 <= t < self.body + 0.87)

    def pose(self, t):
        if t >= self.body:
            p = E.action("prende appunti", t - self.body, t); p["pen"] = 0
            p["dy"] = -4 * math.sin(clamp((t - self.body) / 0.15) * math.pi)
        else:
            i = self.seg(t); b = self.beats[i]; lt = t - self.starts[i]
            p = b.pose(lt, t) if b.pose else E.emotion("neutro", lt, t)
        if self.talking(t) and p["mouth"] not in ("o", "open_big", "grin"):
            p["mouth"] = "o" if int(t * 11) % 2 == 0 else "flat"
        return p

    def frame(self, t, surf):
        ctx = cairo.Context(surf)
        ctx.set_source_surface(background()); ctx.paint()
        if t < self.body and self.beats[self.seg(t)].hook:
            i = self.seg(t); b = self.beats[i]; lt = t - self.starts[i]
            ctx.set_source_rgb(*LIME); ctx.paint()
            z = 1.0 + 0.06 * (1 - eo(prog(lt, 0.0, 0.3)))
            sh = 10 * (1 - prog(lt, 0.0, 0.35)) * math.sin(lt * 90)
            ctx.save(); ctx.translate(CX + sh, 960); ctx.scale(z, z); ctx.translate(-CX, -960)
            hook_headline(ctx, b.text, 470, 150)
            p = self.pose(t); p["halo_col"] = PAPER
            E.draw(ctx, t, CX, 1360, 300, p)
            ctx.restore()
            return
        if t < self.body:
            i = self.seg(t); b = self.beats[i]; A = self.starts[i]; lt = t - A
            tag = b.tag or self.tag
            tw = text(ctx, tag, CX - 30, 300, MONO, 32, LIME, True, "center")
            if int(t * 2) % 2 == 0:
                ctx.set_source_rgb(*ORANGE); ctx.arc(CX - 30 + tw / 2 + 30, 289, 10, 0, 2 * math.pi); ctx.fill()
            text(ctx, "REC", CX - 30 + tw / 2 + 50, 300, MONO, 26, GREY, False)
            inn = 1.0 if i == 0 else eo(prog(t, A, A + 0.3))
            out = eio(prog(t, A + b.dur - 0.25, A + b.dur))
            al = inn * (1 - out)
            if al > 0.01:
                if b.text: headline(ctx, b.text, 430, 92, al, (1 - inn) * 40 - out * 30)
                if b.scene:
                    sc = (0.95 + 0.05 * inn) * b.scale
                    ctx.push_group()
                    ctx.translate(CX, SCENE_Y); ctx.scale(sc, sc); ctx.translate(-CX, -SCENE_Y)
                    b.scene(ctx, lt, t)
                    ctx.pop_group_to_source(); ctx.paint_with_alpha(al)
        else:
            lt = t - self.body
            k = back(prog(lt, 0.12, 0.3)); a = clamp(lt / 0.12)
            ctx.save(); ctx.translate(CX, 700); ctx.rotate(math.radians(-5)); ctx.scale(1.35 - 0.35 * k, 1.35 - 0.35 * k)
            ctx.set_source_rgba(*LIME, a); ctx.set_line_width(10)
            rrect(ctx, -330, -95, 660, 190, 22); ctx.stroke()
            text(ctx, "Annotato.", 0, 38, SANS, 118, LIME, True, "center", alpha=a)
            ctx.restore()
            text(ctx, self.counter, CX, 960, MONO, 38, PAPER, True, "center", alpha=eo(prog(lt, 0.35, 0.6)))
        h0 = self.starts[1] if self.beats[0].hook else 0.0
        r = ETT_R * (0.6 + 0.4 * back(prog(t, h0, h0 + 0.3)))
        E.draw(ctx, t, CX, ETT_Y, r, self.pose(t))

    # ---------- audio ----------
    def audio(self, path):
        SR = 44100; out = np.zeros(int(SR * self.dur) + SR); rng = np.random.default_rng(11)
        def add(sig, t0, g=1.0):
            i = int(t0 * SR); j = min(len(out), i + len(sig))
            if 0 <= i < len(out): out[i:j] += sig[: j - i] * g
        def env(n, a=0.004, r=0.6):
            e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
            nr = int(n * r); e[n - nr:] *= np.linspace(1, 0, nr) ** 1.5; return e
        def tone(f, d, kind="sine", glide=0.0):
            n = int(d * SR); tt = np.arange(n) / SR
            ph = 2 * np.pi * np.cumsum(f * (1 + glide * tt / max(d, 1e-6))) / SR
            return np.tanh(3 * np.sin(ph)) if kind == "square" else np.sin(ph)
        def noise(d, sm=1):
            x = rng.standard_normal(int(d * SR))
            return np.convolve(x, np.ones(sm) / sm, mode="same") if sm > 1 else x
        def click(t0, g=0.12): add(noise(0.01) * env(int(0.01 * SR), 0.0005, 0.9), t0, g)
        SC = [0, 2, 4, 7, 9, 12]; VOW = set("aeiouàèéìòù")
        def voice(s, a, b, base=300):
            ch = list(s.replace("\n", " ")); dt = (b - a) / max(1, len(ch))
            for k, c in enumerate(ch):
                if not c.isalpha(): continue
                f = base * 2 ** (SC[zlib.crc32(c.lower().encode()) % 6] / 12) * (1.06 if c.lower() in VOW else 1)
                sg = 0.55 * tone(f, dt * 0.85, "square", -0.04) + 0.45 * tone(2 * f, dt * 0.85)
                add(np.round(sg * 24) / 24 * env(len(sg), 0.003, 0.5), a + k * dt, 0.22)
        for a, b, s in self.speak: voice(s, a, b)
        for s in self.starts[1:]:
            w = noise(0.26, 30); add(w * np.sin(np.linspace(0, np.pi, len(w))) ** 2, s - 0.08, 0.3)
        lib = {
            "pop": lambda t0: add(tone(420, 0.09, glide=1.2) * env(int(0.09 * SR), 0.002, 0.7), t0, 0.32),
            "bubble": lambda t0: add(tone(500, 0.08, glide=1.0) * env(int(0.08 * SR), 0.002, 0.7), t0, 0.28),
            "ding": lambda t0: add((tone(1320, 0.7) + 0.6 * tone(1760, 0.7)) * env(int(0.7 * SR), 0.002, 0.95), t0, 0.18),
            "stamp": lambda t0: add((tone(90, 0.28, glide=-0.5) + 0.35 * noise(0.28, 4)) * env(int(0.28 * SR), 0.002, 0.9), t0, 0.6),
            "glitch": lambda t0: (add(np.round(noise(0.45, 2) * env(int(0.45 * SR), 0.002, 0.4) * 4) / 4, t0, 0.22),
                                  add(tone(140, 0.4, "square", -0.6) * env(int(0.4 * SR), 0.002, 0.8), t0, 0.22)),
            "boing": lambda t0: add(tone(180, 0.35, glide=2.5) * env(int(0.35 * SR), 0.003, 0.7), t0, 0.3),
            "thud": lambda t0: add((tone(70, 0.3, glide=-0.4) + 0.2 * noise(0.3, 6)) * env(int(0.3 * SR), 0.002, 0.9), t0, 0.55),
            "surprise": lambda t0: [add(tone(1100 + 300 * k, 0.05, "square") * env(int(0.05 * SR)), t0 + k * 0.06, 0.12) for k in range(3)],
            "sad": lambda t0: add(tone(330, 0.6, "square", glide=-0.35) * env(int(0.6 * SR), 0.01, 0.8), t0, 0.1),
            "alarm": lambda t0: add(tone(880, 0.07, "square") * env(int(0.07 * SR)), t0, 0.1),
            "tick": lambda t0: add(tone(1800, 0.012) * env(int(0.012 * SR), 0.001, 0.8), t0, 0.1),
            "click": lambda t0: click(t0),
        }
        for b, s in zip(self.beats, self.starts):
            for item in b.sfx:
                kind, t0 = item[0], item[1]
                if kind == "type":   # ("type", t0, text, cps)
                    for k, c in enumerate(item[2]):
                        if c != " ": click(s + t0 + k / item[3])
                elif kind == "ticks":  # ("ticks", t0, t1, interval)
                    tt = t0
                    while tt < item[2]: lib["tick"](s + tt); tt += item[3]
                else:
                    lib[kind](s + t0)
        lib["stamp"](self.body + 0.15)
        for k, f in enumerate([392, 494, 440, 587]):
            sg = 0.55 * tone(f, 0.075, "square", -0.04) + 0.45 * tone(2 * f, 0.075)
            add(np.round(sg * 24) / 24 * env(len(sg), 0.003, 0.5), self.body + 0.47 + k * 0.1, 0.24)
        beat = 0.6; t = 0.0; k = 0
        while t < self.dur:
            if not any(a <= t < b for a, b in self.quiet):
                if k % 2 == 0: add(tone(65, 0.18, glide=-0.4) * env(int(0.18 * SR), 0.002, 0.9), t, 0.3)
                add(noise(0.03) * env(int(0.03 * SR), 0.001, 0.9), t + beat / 2, 0.035)
            t += beat; k += 1
        mix = out[: int(SR * self.dur)]
        mix[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))
        mix = mix / np.max(np.abs(mix)) * 0.89
        pcm = (mix * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(np.stack([pcm, pcm], 1).ravel().tobytes())

    def stills(self, times, prefix):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for t in times:
            self.frame(t, surf); surf.write_to_png(f"{prefix}_{t:05.2f}.png")

    def render(self, outp):
        wav = outp.replace(".mp4", ".wav"); self.audio(wav)
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav, "-shortest",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                              "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", outp], stdin=subprocess.PIPE)
        for k in range(int(self.dur * FPS)):
            self.frame(k / FPS, surf); surf.flush(); p.stdin.write(bytes(surf.get_data()))
        p.stdin.close(); p.wait()
        return self.dur

def run(reel, prefix):
    mode = sys.argv[1] if len(sys.argv) > 1 else "video"
    if mode == "stills":
        reel.stills([float(x) for x in sys.argv[2:]], prefix)
    else:
        print("done", reel.render(sys.argv[2]))

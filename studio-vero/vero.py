"""Vero · Dietro le cose — video engine (editorial style: paper, ink, one red)."""
import math, subprocess, wave, os, sys, json
import cairo
import numpy as np

W, H, FPS = 1080, 1920, 30
PAPER = (0xF3/255, 0xEF/255, 0xE6/255)
INK = (0x14/255,) * 3
RED = (0xE8/255, 0x45/255, 0x2C/255)
MUTE = (0x6B/255, 0x66/255, 0x5E/255)
SERIF, SANS, MONO = "Fraunces", "Inter", "JetBrains Mono"
CX = W / 2
HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.join(HERE, "../voice/ric/it-riccardo_fasol-x-low.onnx")

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)

def font(ctx, fam, size, weight=cairo.FONT_WEIGHT_BOLD):
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL, weight); ctx.set_font_size(size)

def text(ctx, s, x, y, fam=SANS, size=48, col=INK, align="center", alpha=1.0, bold=True):
    font(ctx, fam, size, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    adv = ctx.text_extents(s).x_advance
    if align == "center": x -= adv / 2
    elif align == "right": x -= adv
    ctx.set_source_rgba(*col, alpha); ctx.move_to(x, y); ctx.show_text(s)
    return adv

def rich(ctx, s, y, size, alpha=1.0, maxw=920, fam=SERIF, lh=1.1):
    """multi-line centred serif; *words* in red."""
    font(ctx, fam, size)
    lines = s.split("\n")
    widest = max(ctx.text_extents(l.replace("*", "")).x_advance for l in lines)
    if widest > maxw: size *= maxw / widest; font(ctx, fam, size)
    sp = ctx.text_extents(" ").x_advance
    red = False
    for i, line in enumerate(lines):
        words = line.split(" "); clean = [w.replace("*", "") for w in words]
        lw = sum(ctx.text_extents(c).x_advance for c in clean) + sp * (len(words) - 1)
        x = CX - lw / 2
        for w, c in zip(words, clean):
            if w.startswith("*"): red = True
            ctx.set_source_rgba(*(RED if red else INK), alpha)
            ctx.move_to(x, y + i * size * lh); ctx.show_text(c)
            if w.endswith("*") or w.endswith("*.") or w.endswith("*,"): red = False
            x += ctx.text_extents(c).x_advance + sp
    return size

def mark(ctx, cx, cy, r, k=1.0, col=INK, dot=RED):
    """the Vero mark: a ring (the lens) with a dot (what's behind)."""
    ctx.set_source_rgb(*col); ctx.set_line_width(r * 0.22)
    ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * k); ctx.stroke()
    if k > 0.6:
        ctx.set_source_rgb(*dot); ctx.arc(cx, cy, r * 0.3 * back((k - 0.6) / 0.4), 0, 2 * math.pi); ctx.fill()

def paper_bg():
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    c.set_source_rgb(*PAPER); c.paint()
    rng = np.random.default_rng(3)
    for _ in range(9000):                      # faint paper grain
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        c.set_source_rgba(0, 0, 0, rng.uniform(0.01, 0.035)); c.rectangle(x, y, 1.6, 1.6); c.fill()
    return s

def tts(line, path):
    if not os.path.exists(path):
        p = subprocess.run([sys.executable, "-m", "piper", "-m", VOICE, "-f", path, "--length-scale", "0.84"],
                           input=line.encode(), capture_output=True)
        if p.returncode: raise RuntimeError(p.stderr.decode()[-400:])
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()

class Beat:
    def __init__(self, say, draw, pad=0.55, min_dur=2.6):
        self.say, self.draw, self.pad, self.min_dur = say, draw, pad, min_dur

class Video:
    def __init__(self, num, beats, slug):
        self.num, self.beats, self.slug = num, beats, slug
        os.makedirs(os.path.join(HERE, "tts", slug), exist_ok=True)
        self.starts, self.vdur = [], []; t = 0.0
        for i, b in enumerate(beats):
            d = tts(b.say, self.wav(i)) if b.say else 0.0
            self.vdur.append(d); self.starts.append(t)
            t += max(b.min_dur, d + b.pad)
        self.dur = t
        self.bg = paper_bg()

    def wav(self, i): return os.path.join(HERE, "tts", self.slug, f"{i:02d}.wav")

    def seg(self, t):
        for i in range(len(self.beats) - 1, -1, -1):
            if t >= self.starts[i]: return i
        return 0

    def frame(self, t, surf):
        ctx = cairo.Context(surf); ctx.set_source_surface(self.bg); ctx.paint()
        # masthead
        ctx.set_source_rgb(*INK); ctx.rectangle(90, 214, W - 180, 3); ctx.fill()
        mark(ctx, 112, 180, 16)
        text(ctx, "DIETRO LE COSE", 144, 192, MONO, 30, INK, "left")
        text(ctx, f"N. {self.num:03d}", W - 90, 192, MONO, 30, MUTE, "right", bold=False)
        i = self.seg(t); b = self.beats[i]; lt = t - self.starts[i]
        end = (self.starts[i + 1] if i + 1 < len(self.beats) else self.dur) - self.starts[i]
        a_in = 1.0 if i == 0 else eo(prog(lt, 0, 0.25))
        a_out = 1 - prog(lt, end - 0.18, end) if i + 1 < len(self.beats) else 1.0
        ctx.push_group()
        b.draw(ctx, lt, end, t)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a_in * a_out)
        # progress rule at the bottom
        ctx.set_source_rgba(*INK, 0.15); ctx.rectangle(90, 1740, W - 180, 4); ctx.fill()
        ctx.set_source_rgb(*RED); ctx.rectangle(90, 1740, (W - 180) * t / self.dur, 4); ctx.fill()

    def audio(self, path):
        SR = 44100; out = np.zeros(int(SR * (self.dur + 1)))
        def add(sig, t0, g=1.0):
            i = int(t0 * SR); j = min(len(out), i + len(sig))
            if i < len(out): out[i:j] += sig[: j - i] * g
        for i, b in enumerate(self.beats):
            if not b.say: continue
            with wave.open(self.wav(i)) as w:
                sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
            x = np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x)   # resample to 44.1k
            add(x, self.starts[i] + 0.12, 1.0)
        # soft music bed: warm pad chords + light pulse
        tt = np.arange(len(out)) / SR
        chords = [(220.0, 277.18, 329.63), (196.0, 246.94, 293.66), (174.61, 220.0, 261.63), (196.0, 246.94, 329.63)]
        bed = np.zeros_like(out)
        for k, ch in enumerate(chords * 10):
            a, z = k * 3.2, k * 3.2 + 3.4
            m = (tt >= a) & (tt < z)
            env = np.sin(np.pi * np.clip((tt[m] - a) / 3.4, 0, 1)) ** 0.6
            for f in ch: bed[m] += np.sin(2 * np.pi * f * tt[m]) * env * 0.33 + np.sin(2 * np.pi * 2 * f * tt[m]) * env * 0.05
        pulse = (np.sin(2 * np.pi * tt / 0.6) > 0.995).astype(float)
        bed += np.convolve(pulse, np.exp(-np.arange(2000) / 300), "same") * 0.15
        out += bed * 0.055
        for s in self.starts[1:]:   # tiny paper-swipe on cuts
            n = int(0.18 * SR); nz = np.random.default_rng(int(s * 10)).standard_normal(n)
            nz = np.convolve(nz, np.ones(25) / 25, "same") * np.sin(np.linspace(0, np.pi, n)) ** 2
            add(nz, s - 0.06, 0.25)
        out = out[: int(SR * self.dur)]
        out[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))
        out = out / np.max(np.abs(out)) * 0.9
        pcm = (out * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(np.stack([pcm, pcm], 1).ravel().tobytes())

    def stills(self, times, prefix):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for t in times: self.frame(t, s); s.write_to_png(f"{prefix}_{t:05.2f}.png")

    def render(self, outp):
        wav = outp[:-4] + ".wav"; self.audio(wav)
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "veryfast",
                              "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", outp],
                             stdin=subprocess.PIPE)
        for k in range(int(self.dur * FPS)):
            self.frame(k / FPS, s); s.flush(); p.stdin.write(bytes(s.get_data()))
        p.stdin.close(); p.wait(); os.remove(wav)
        return self.dur

def run(v):
    if len(sys.argv) > 1 and sys.argv[1] == "stills": v.stills([float(x) for x in sys.argv[3:]], sys.argv[2])
    else: print("dur", v.render(sys.argv[2] if len(sys.argv) > 2 else f"{v.slug}.mp4"))

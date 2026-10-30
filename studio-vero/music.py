"""music.py <timing.json> <gaps comma> <out.wav> [sfx json]: piano lo-fi bed + sfx, ducked under voice."""
import sys, json, subprocess, numpy as np, os
SR = 44100
SF = os.path.dirname(os.path.abspath(__file__)) + "/../sf/node_modules"
def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(float)
timing = json.load(open(sys.argv[1])); gaps = [float(g) for g in sys.argv[2].split(",")]
starts = []; acc = 0
for t, g in zip(timing, gaps): starts.append(round(acc * 30) / 30); acc += t["dur"] + g
total = round(acc * 30) / 30
out = np.zeros(int(SR * (total + 2)))
def add(x, t0, g=1.0):
    i = int(t0 * SR); j = min(len(out), i + len(x))
    if 0 <= i < len(out): out[i:j] += x[: j - i] * g
# --- piano: Salamander samples, pitch-shift from nearest A/C/D#/F# ---
NOTES = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]
cache = {}
def piano(midi, vel=0.5):
    names = {0: "C", 3: "Ds", 6: "Fs", 9: "A"}
    base = min(names, key=lambda b: min(abs((midi % 12) - b), 12 - abs((midi % 12) - b)))
    octv = midi // 12 - 1; diff = (midi % 12) - base
    if diff > 6: diff -= 12; octv += 0
    if diff < -6: diff += 12
    key = f"{names[base]}{octv}"
    if key not in cache: cache[key] = load(f"{SF}/@audio-samples/piano-mp3-velocity8/audio/{key}v8.mp3")
    x = cache[key]; r = 2 ** (diff / 12)
    y = np.interp(np.arange(0, len(x), r), np.arange(len(x)), x)[: int(SR * 3.5)]
    y *= np.linspace(1, 0, len(y)) ** 1.5
    return y * vel
def samp(name): return load(f"{SF}/supersonic-scsynth-samples/samples/{name}.flac")
kick, hat, snap, hiss = samp("drum_bass_soft"), samp("hat_snap"), samp("perc_snap"), samp("vinyl_hiss")
bpm = 88; beat = 60 / bpm; bar = beat * 4
# Am9 - Fmaj7 - Cmaj7 - G6  (warm, curious)
prog = [[45, 60, 64, 67, 71], [41, 57, 60, 64, 69], [48, 55, 59, 64, 67], [43, 55, 59, 62, 64]]
music = np.zeros_like(out); saved = out; out = music
nb = int(total / bar) + 2
for b in range(nb):
    ch = prog[b % 4]; t0 = b * bar
    add(piano(ch[0], 0.35), t0)
    for k, n in enumerate(ch[1:]): add(piano(n, 0.18), t0 + 0.012 * k)
    add(piano(ch[2] + 12, 0.10), t0 + beat * 2.5)            # little answer note
    for q in range(4):
        add(kick, t0 + q * beat, 0.32 if q in (0, 2) else 0.0)
        add(hat, t0 + q * beat + beat / 2, 0.06)
    add(snap, t0 + beat * 1, 0.05); add(snap, t0 + beat * 3, 0.05)
h = np.tile(hiss, int(len(out) / max(1, len(hiss))) + 1)[: len(out)]; out += h * 0.03
out = saved
# --- ducking under the voice ---
env = np.ones(len(music))
for s, t in zip(starts, timing):
    a, b = int((s + 0.1) * SR), int((s + 0.1 + t["dur"]) * SR)
    env[a:b] = 0.45
env = np.convolve(env, np.ones(int(0.15 * SR)) / int(0.15 * SR), "same")
out += music * env * 0.55
# --- sfx ---
swoosh, pop, tick, impact, coin = samp("perc_swoosh"), samp("elec_pop"), samp("elec_tick"), samp("perc_impact1"), samp("elec_ping")
for s in starts[1:]: add(swoosh, s - 0.12, 0.22)
if len(sys.argv) > 4:
    for kind, t in json.load(open(sys.argv[4])): add({"pop": pop, "tick": tick, "swoosh": swoosh, "impact": impact, "coin": coin}[kind], t, {"impact": 0.5, "coin": 0.18}.get(kind, 0.25))
out = out[: int(SR * total)]
f = int(0.5 * SR); out[-f:] *= np.linspace(1, 0, f); out[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
out = out / np.max(np.abs(out)) * 0.5
import soundfile as sf; sf.write(sys.argv[3], np.stack([out, out], 1), SR)
print("music", total)

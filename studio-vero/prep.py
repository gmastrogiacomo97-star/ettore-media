"""prep.py <ep> : from ettore-media/audio-in/<ep>/{full.mp3,lines.json} build remo/public/<ep>/{voice.wav,words.json,timing.json}
- trims silence, speeds up 1.08x, aligns with faster-whisper, maps script lines to time ranges.
"""
import sys, json, subprocess, re, os, unicodedata
import numpy as np, soundfile as sf
ep = sys.argv[1]
SP = "/tmp/claude-0/-home-claude/e89a2476-daf8-5499-a945-14c713cc7d6b/scratchpad"
src = f"/home/claude/ettore-media/audio-in/{ep}"
out = f"{SP}/remo/public/{ep}"; os.makedirs(out, exist_ok=True)
lines = json.load(open(f"{src}/lines.json"))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{src}/full.mp3", "-f", "f32le", "-ac", "1", "-ar", "44100", "-"], capture_output=True).stdout
s = np.frombuffer(raw, np.float32).copy(); idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0] - 1500): idx[-1] + 6000]
sf.write(f"{out}/_v.wav", s, 44100)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{out}/_v.wav", "-af", "atempo=1.08", f"{out}/voice.wav"]); os.remove(f"{out}/_v.wav")
from faster_whisper import WhisperModel
m = WhisperModel(f"{SP}/fwb", device="cpu", compute_type="int8", cpu_threads=2)
x, sr = sf.read(f"{out}/voice.wav", dtype="float32")
x16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
segs, _ = m.transcribe(x16, language="it", word_timestamps=True, beam_size=5, initial_prompt=" ".join(lines))
W = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for sg in segs for w in sg.words]
json.dump(W, open(f"{out}/words.json", "w"), ensure_ascii=False)
norm = lambda t: re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", t.lower()).encode("ascii", "ignore").decode())
# line starts: first script word of each line, matched in order
starts = []; pos = 0
for li, l in enumerate(lines):
    first = norm(l.split()[0])
    if li == 0: starts.append(0); continue
    exp = len(" ".join(lines[:li])) / len(" ".join(lines))          # expected fraction
    best = None
    for k in range(pos + 1, len(W)):
        if norm(W[k][0]).startswith(first[:4]) or first.startswith(norm(W[k][0])[:4] or "#"):
            score = abs(W[k][1] / W[-1][2] - exp)
            if best is None or score < best[0]: best = (score, k)
            if W[k][1] / W[-1][2] > exp + 0.12: break
    k = best[1] if best else pos + 1
    starts.append(k); pos = k
T = []
for li, l in enumerate(lines):
    a = starts[li]; b = starts[li + 1] if li + 1 < len(lines) else len(W)
    ws = W[a:b]; sw = l.split(); n = len(ws)
    words = [[w, ws[min(n - 1, round(k * n / len(sw)))][1]] for k, w in enumerate(sw)]
    T.append({"text": l, "start": ws[0][1], "end": ws[-1][2], "words": words})
json.dump(T, open(f"{out}/timing.json", "w"), ensure_ascii=False, indent=1)
print(" ".join(f"{w}@{a}" for w, a, b in W))
for t in T: print(round(t["start"], 2), round(t["end"], 2), t["text"][:50])
# music + sfx inputs
conv = [{"text": t["text"], "dur": t["end"] - t["start"]} for t in T]
gaps = [T[i + 1]["start"] - T[i]["end"] for i in range(len(T) - 1)] + [1.4]
json.dump(conv, open(f"{out}/conv.json", "w")); open(f"{out}/gaps.txt", "w").write(",".join(f"{g:.3f}" for g in gaps))

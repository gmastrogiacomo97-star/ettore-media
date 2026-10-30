"""align.py <model_dir> <wav> <out.json>: word timestamps with faster-whisper"""
import sys, json, soundfile as sf, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[1], device="cpu", compute_type="int8", cpu_threads=2)
x, sr = sf.read(sys.argv[2], dtype="float32")
if x.ndim > 1: x = x.mean(1)
if sr != 16000:
    x = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
segs, info = m.transcribe(x, language="it", word_timestamps=True, beam_size=5)
words = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in s.words]
json.dump(words, open(sys.argv[3], "w"), ensure_ascii=False)
print(" ".join(f"{w}@{a}" for w, a, b in words))

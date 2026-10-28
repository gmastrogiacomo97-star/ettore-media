"""Minimal espeak-ng synth via ctypes (bundled espeakng_loader). say(text, path, voice, rate, pitch)."""
import ctypes, wave, numpy as np, espeakng_loader as L
_lib = ctypes.cdll.LoadLibrary(L.get_library_path())
_CB = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)
_buf = []
def _cb(wav, n, ev):
    if wav and n > 0: _buf.append(np.ctypeslib.as_array(wav, shape=(n,)).copy())
    return 0
_cbf = _CB(_cb)
SR = _lib.espeak_Initialize(1, 0, L.get_data_path().encode(), 0)
_lib.espeak_SetSynthCallback(_cbf)
def say(text, voice="it", rate=165, pitch=55, rng=40):
    _buf.clear()
    _lib.espeak_SetVoiceByName(voice.encode())
    _lib.espeak_SetParameter(1, rate, 0); _lib.espeak_SetParameter(3, pitch, 0); _lib.espeak_SetParameter(4, rng, 0)
    b = text.encode("utf-8")
    _lib.espeak_Synth(b, len(b) + 1, 0, 0, 0, 0x10, None, None)  # espeakCHARS_UTF8
    _lib.espeak_Synchronize()
    return (np.concatenate(_buf) if _buf else np.zeros(1, np.int16)), SR
if __name__ == "__main__":
    import sys
    x, sr = say(sys.argv[1], *sys.argv[3:4])
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.astype(np.int16).tobytes())
    print(sr, len(x) / sr)

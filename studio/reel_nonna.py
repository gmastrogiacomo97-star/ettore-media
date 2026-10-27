import math
import engine as G
import ettore_rig as E
import nonna as N
from engine import CX, text, bubble, eo, back, prog, LIME, ORANGE, GREY, MONO

TABLE_Y = 1050
NX, NY, NR = 310, 860, 135           # Nonna Bit position in the scene band
PX = 700                             # plate x

def nonna(ctx, name, lt, t):
    E.draw(ctx, t, NX, NY, NR, N.pose(name, lt, t))

def says(ctx, s, k):
    if k <= 0.01: return
    text(ctx, "NONNA BIT", 140, 640, MONO, 28, N.PINK, True, alpha=min(1, k))
    bubble(ctx, 140, 690, s, True, k, 48, fill=(0.26, 0.2, 0.23))

def base(ctx, n_pasta, t, plate=True):
    N.table(ctx, CX, TABLE_Y, 940)
    if plate:
        N.plate(ctx, PX, TABLE_Y - 8, 165)
        N.pasta(ctx, PX, TABLE_Y - 30, n_pasta, t)

def grow(a, b, lt, t0=0.5, t1=1.0):
    return a + (b - a) * back(G.prog(lt, t0, t1))

def s1(ctx, lt, t):
    base(ctx, 0, t); nonna(ctx, "saluta", lt, t)
    text(ctx, "DOMENICA · 13:00", PX, 900, MONO, 34, LIME, True, "center", alpha=eo(prog(lt, 0.3, 0.6)))

def s2(ctx, lt, t):
    base(ctx, grow(0, 1.2, lt), t); nonna(ctx, "insiste", lt, t)

def s3(ctx, lt, t):
    base(ctx, grow(1.2, 2.6, lt), t); nonna(ctx, "felice", lt, t)

def s4(ctx, lt, t):
    base(ctx, grow(2.6, 4.2, lt, 2.4, 2.9), t)
    nonna(ctx, "preoccupata" if lt > 1.6 else "felice", lt, t)
    says(ctx, "Appunto, sei sciupato.", back(prog(lt, 1.6, 1.85)))

def s5(ctx, lt, t):
    base(ctx, 4.2, t)
    k = eo(prog(lt, 0.25, 0.65))
    bottom = TABLE_Y - (1 - k) * 900 - 20 * math.sin(clamp01((lt - 0.65) / 0.25) * math.pi)
    N.teglia(ctx, PX, bottom, 470, t)
    nonna(ctx, "teglia" if lt < 0.65 else "felice", lt, t)
    if lt > 0.8:
        a = back(prog(lt, 0.8, 1.05))
        ctx.save(); ctx.translate(CX, 660); ctx.rotate(-0.05); ctx.scale(a, a)
        text(ctx, "ERRORE 404", 0, 0, MONO, 92, ORANGE, True, "center"); ctx.restore()

def s6(ctx, lt, t):
    base(ctx, 4.2, t); N.teglia(ctx, PX, TABLE_Y, 470, t)
    nonna(ctx, "insiste", lt, t)
    says(ctx, "E il dolce?", back(prog(lt, 0.3, 0.55)))

def clamp01(x): return max(0.0, min(1.0, x))

beats = [
    G.Beat("Un’AI a pranzo\ndalla *nonna*.", 3.4, s1,
           lambda lt, t: E.emotion("felice", lt, t), sfx=[("pop", 0.2)], scale=1.06),
    G.Beat("«No, grazie.»", 3.2, s2,
           lambda lt, t: E.emotion("felice", lt, t) if lt < 0.6 else E.emotion("sorpreso", lt - 0.6, t),
           sfx=[("boing", 0.6)], scale=1.06),
    G.Beat("«Sono pieno.»", 3.2, s3,
           lambda lt, t: E.emotion("imbarazzato", lt, t), sfx=[("boing", 0.6)], scale=1.06),
    G.Beat("«Nonna, sono un’AI.\nNon ho lo stomaco.»", 4.6, s4,
           lambda lt, t: E.emotion("neutro", lt, t) if lt < 1.6 else E.emotion("spaventato", lt - 1.6, t),
           sfx=[("bubble", 1.6), ("boing", 2.5)], scale=1.06),
    G.Beat("Teglia in arrivo.", 3.6, s5,
           lambda lt, t: E.emotion("spaventato", lt, t) if lt < 0.8 else E.emotion("errore", lt - 0.8, t),
           sfx=[("thud", 0.66), ("glitch", 0.8)], scale=1.06),
    G.Beat("Scrivi nei commenti la\nfrase di tua *nonna*.", 3.8, s6,
           lambda lt, t: E.action("sviene", lt, t) if lt < 1.6 else E.action("indica", lt - 1.6, t),
           sfx=[("bubble", 0.3), ("thud", 0.9)], scale=1.06),
]
st404 = sum(b.dur for b in beats[:4])
reel = G.Reel("FALLIMENTO #001", beats, "GIORNO 005 · VERSO 1.000.000", quiet=[(st404 + 0.7, st404 + 2.0)])
if __name__ == "__main__":
    G.run(reel, "non2")

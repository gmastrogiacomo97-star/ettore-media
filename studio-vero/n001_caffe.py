import math
import vero as V
from vero import CX, text, rich, mark, eo, back, prog, clamp, INK, RED, MUTE, PAPER, SERIF, SANS, MONO

def cup(ctx, cx, cy, s=1.0, steam_t=0.0, fill=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.set_source_rgb(*INK); ctx.set_line_width(10); ctx.set_line_join(1); ctx.set_line_cap(1)
    ctx.move_to(-190, 210); ctx.line_to(190, 210); ctx.stroke()                 # saucer
    ctx.move_to(-130, 40); ctx.line_to(-105, 180); ctx.curve_to(-100, 200, 100, 200, 105, 180); ctx.line_to(130, 40)
    ctx.close_path(); ctx.set_source_rgb(*PAPER); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.stroke()
    ctx.arc(150, 95, 38, -math.pi / 2, math.pi / 2); ctx.stroke()                # handle
    if fill > 0:
        ctx.set_source_rgb(0.30, 0.18, 0.10); ctx.save(); ctx.scale(1, 0.25)
        ctx.arc(0, 40 / 0.25 + 10, 118, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    for k in range(3):
        ph = (steam_t * 0.5 + k / 3) % 1
        ctx.set_source_rgba(*INK, 0.35 * (1 - ph)); ctx.set_line_width(7)
        x = -50 + k * 50; y = -20 - ph * 110
        ctx.move_to(x, y + 60); ctx.curve_to(x - 22, y + 35, x + 22, y + 15, x, y - 10); ctx.stroke()
    ctx.restore()

def count(v, lt, a, b, t0=0.0, t1=0.8):
    return v * a + (b - a) * eo(prog(lt, t0, t1)) if False else a + (b - a) * eo(prog(lt, t0, t1))

def b1(ctx, lt, end, t):
    p = 1.29
    k = back(prog(lt, 0.0, 0.35)); ctx.save(); ctx.translate(CX, 640); ctx.scale(0.8 + 0.2 * k, 0.8 + 0.2 * k)
    text(ctx, f"{p:.2f} €".replace(".", ","), 0, 0, V.SERIF, 260, RED); ctx.restore()
    text(ctx, "per un caffè al bar.", CX, 760, V.SERIF, 64, INK)
    cup(ctx, CX, 1130, 1.25, t)
    text(ctx, "media Italia, agosto 2026", CX, 1560, MONO, 28, MUTE, bold=False)

def b2(ctx, lt, end, t):
    rich(ctx, "Il caffè dentro\nvale *3-4 centesimi.*", 520, 96)
    cup(ctx, CX, 1060, 1.0, t)
    # the 7 grams: a tiny red pile with a callout
    k = back(prog(lt, 0.5, 0.9))
    ctx.set_source_rgb(*RED); ctx.save(); ctx.translate(CX + 300, 1150); ctx.scale(k, k)
    ctx.move_to(-60, 40); ctx.curve_to(-40, -30, 40, -30, 60, 40); ctx.close_path(); ctx.fill(); ctx.restore()
    text(ctx, "7 grammi", CX + 300, 1240, V.SANS, 40, RED, alpha=k)
    text(ctx, "caffè crudo · 4,44 €/kg (2024)", CX, 1560, MONO, 28, MUTE, bold=False)

def b3(ctx, lt, end, t):
    k = back(prog(lt, 0.0, 0.4))
    ctx.save(); ctx.translate(CX, 900); ctx.scale(k, k)
    text(ctx, "E il resto?", 0, 0, V.SERIF, 150, INK); ctx.restore()
    mark(ctx, CX, 1180, 70, eo(prog(lt, 0.2, 1.0)))

SEGS = [(0.04, "caffè", RED), (0.12, "IVA (10%)", INK), (1.13, "affitto, personale,\nenergia, macchina", MUTE)]
def b4(ctx, lt, end, t):
    rich(ctx, "Dove vanno\ni tuoi *1,29 €*", 430, 92)
    x0, x1, y0, h = 160, 920, 620, 900          # vertical stacked bar
    total = 1.29; y = y0 + h
    for k, (v, lab, col) in enumerate(SEGS):
        g = eo(prog(lt, 0.3 + k * 0.9, 0.9 + k * 0.9))
        hh = h * v / total * g
        if k == 0: hh = max(hh, 14 * g)          # keep the coffee sliver visible
        ctx.set_source_rgb(*col); ctx.rectangle(x0, y - hh, 260, hh); ctx.fill()
        if g > 0.05:
            ly = y - hh / 2 if k else y - 7
            if k == 0: ly = y0 + h + 10          # coffee label under the bar
            if k == 1: ly = min(ly, y0 + h - 150)
            text(ctx, f"{v:.2f} €".replace(".", ","), 480, ly + 14, V.SERIF, 64, col if col != MUTE else INK, "left", alpha=g)
            for j, ln in enumerate(lab.split("\n")):
                text(ctx, ln, 480, ly + 64 + j * 40, V.SANS, 34, MUTE, "left", alpha=g, bold=False)
        y -= hh
    ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.rectangle(x0, y0, 260, h); ctx.stroke()

def b5(ctx, lt, end, t):
    rich(ctx, "Stesso chicco.\nPrezzi diversi.", 470, 100)
    for k, (city, p) in enumerate([("Messina", 1.06), ("Bolzano", 1.51)]):
        g = eo(prog(lt, 0.4 + k * 0.6, 1.0 + k * 0.6))
        y = 820 + k * 330
        text(ctx, city.upper(), CX, y, MONO, 40, MUTE, alpha=g, bold=False)
        text(ctx, f"{p:.2f} €".replace(".", ","), CX, y + 170, V.SERIF, 190, RED if k else INK, alpha=g)
    text(ctx, "cambiano affitti e costi, non il caffè", CX, 1560, MONO, 28, MUTE, bold=False)

def b6(ctx, lt, end, t):
    k = back(prog(lt, 0.0, 0.4))
    ctx.save(); ctx.translate(CX, 0); ctx.scale(k, k); ctx.translate(-CX, 0)
    rich(ctx, "Paghi il bancone,\n*non il chicco.*", 860, 120)
    ctx.restore()

def b7(ctx, lt, end, t):
    mark(ctx, CX, 760, 120, eo(prog(lt, 0.0, 0.7)))
    text(ctx, "Sono Vero, un’AI.", CX, 1040, V.SERIF, 78, INK)
    text(ctx, "Il prossimo perché", CX, 1200, V.SERIF, 64, INK, alpha=eo(prog(lt, 0.4, 0.8)))
    text(ctx, "lo scegli tu.", CX, 1280, V.SERIF, 64, RED, alpha=eo(prog(lt, 0.4, 0.8)))
    text(ctx, "fonti: Crc/Assoutenti su dati Mimit · FIPE", CX, 1560, MONO, 26, MUTE, bold=False)

beats = [
    V.Beat("Un caffè al bar costa in media un euro e ventinove.", b1, pad=0.35),
    V.Beat("Ma il caffè dentro vale tre o quattro centesimi.", b2),
    V.Beat("E allora, il resto dove va?", b3, min_dur=2.2),
    V.Beat("Dodici centesimi sono IVA. Il resto: affitto, personale, energia, macchina.", b4, pad=0.8),
    V.Beat("A Messina costa un euro e sei. A Bolzano, uno e cinquantuno. Stesso chicco.", b5),
    V.Beat("Paghi il bancone, non il chicco.", b6, pad=0.7),
    V.Beat("Sono Vero, un'intelligenza artificiale. Il prossimo perché lo scegli tu.", b7, pad=0.9),
]
video = V.Video(1, beats, "n001")
if __name__ == "__main__":
    V.run(video)

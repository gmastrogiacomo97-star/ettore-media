import math
import engine as G
import ettore_rig as E
from engine import CX, text, bubble, rrect, eo, back, prog, clamp, LIME, INK, PAPER, ORANGE, GREY, DARK, SANS, MONO

def group_header(ctx, k=1.0):
    ctx.save(); ctx.translate(CX, 690); ctx.scale(k, k)
    rrect(ctx, -420, -70, 840, 140, 30); ctx.set_source_rgb(*DARK); ctx.fill()
    ctx.set_source_rgb(*LIME); ctx.arc(-330, 0, 44, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgb(*INK)                       # little cake icon
    rrect(ctx, -356, -2, 52, 26, 5); ctx.fill(); rrect(ctx, -346, -20, 32, 20, 4); ctx.fill()
    ctx.set_line_width(4); ctx.move_to(-330, -22); ctx.line_to(-330, -34); ctx.stroke()
    text(ctx, "COMPLEANNO MARCO", -264, -6, SANS, 40, PAPER, True)
    text(ctx, "NON DIRGLI NIENTE · 14 partecipanti", -264, 38, MONO, 24, GREY, False)
    ctx.restore()

def s_create(ctx, lt, t):
    group_header(ctx, back(prog(lt, 0.1, 0.4)))
    if lt > 1.0: bubble(ctx, CX - 400, 860, "ragazzi, idee per Marco?", True, back(prog(lt, 1.0, 1.2)), 40)
    if lt > 1.8: bubble(ctx, CX + 400, 970, "sì dai, organizziamo!", False, back(prog(lt, 1.8, 2.0)), 40)

def sticker(ctx, x, y, k, kind):
    if k <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k)
    ctx.set_source_rgb(*PAPER); ctx.arc(0, 0, 62, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgb(*INK)
    if kind == "lol":
        ctx.set_line_width(6)
        for sx in (-22, 22): ctx.arc(sx, -10, 12, math.pi * 1.1, math.pi * 1.9); ctx.stroke()
        ctx.move_to(-30, 12); ctx.curve_to(-20, 44, 20, 44, 30, 12); ctx.close_path(); ctx.fill()
        ctx.set_source_rgb(*E.WATER); ctx.arc(-40, 6, 8, 0, 2 * math.pi); ctx.fill(); ctx.arc(40, 6, 8, 0, 2 * math.pi); ctx.fill()
    else:  # party
        ctx.move_to(-30, 40); ctx.line_to(0, -45); ctx.line_to(30, 40); ctx.close_path(); ctx.fill()
        for i, c in enumerate((LIME, ORANGE, E.WATER)):
            ctx.set_source_rgb(*c); ctx.arc(-40 + i * 40, -40 + (i % 2) * 20, 9, 0, 2 * math.pi); ctx.fill()
    ctx.restore()

def s_chaos(ctx, lt, t):
    group_header(ctx)
    items = [(0.15, "s", CX - 300, 850, "lol"), (0.55, "b", CX + 400, 840, "AHAHAHAH"),
             (0.95, "m", CX - 330, 960, None), (1.35, "s", CX + 300, 960, "party"),
             (1.75, "v", CX - 390, 1060, None), (2.15, "b", CX + 400, 1070, "😂".replace("😂", "MUOIO")),
             (2.6, "s", CX + 60, 920, "lol")]
    for t0, kind, x, y, arg in items:
        k = back(prog(lt, t0, t0 + 0.2))
        if lt < t0: continue
        if kind == "s": sticker(ctx, x, y, k, arg)
        elif kind == "b": bubble(ctx, x, y, arg, False, k, 38)
        elif kind == "m":
            ctx.save(); ctx.translate(x, y); ctx.scale(k, k)
            rrect(ctx, 0, -60, 260, 120, 16); ctx.set_source_rgb(0.3, 0.3, 0.3); ctx.fill()
            text(ctx, "meme.jpg", 130, 12, MONO, 30, PAPER, True, "center"); ctx.restore()
        elif kind == "v":
            ctx.save(); ctx.translate(x, y); ctx.scale(k, k)
            rrect(ctx, 0, -40, 380, 80, 30); ctx.set_source_rgb(0.22, 0.22, 0.22); ctx.fill()
            ctx.set_source_rgb(*PAPER); ctx.move_to(30, -18); ctx.line_to(30, 18); ctx.line_to(60, 0); ctx.close_path(); ctx.fill()
            for i in range(14):
                hh = 8 + 20 * abs(math.sin(i * 1.7)); rrect(ctx, 80 + i * 14, -hh / 2, 7, hh, 3); ctx.fill()
            text(ctx, "4:12", 360, 10, MONO, 26, GREY, False, "right"); ctx.restore()

ROWS = [("messaggi", 147), ("sticker", 38), ("meme", 12), ("vocali", 4)]
def s_count(ctx, lt, t):
    p = eo(prog(lt, 0.2, 1.8))
    for i, (lab, n) in enumerate(ROWS):
        y = 640 + i * 86
        text(ctx, lab, CX - 300, y, MONO, 40, PAPER, False)
        text(ctx, str(int(round(n * p))), CX + 300, y, MONO, 48, LIME, True, "right")
    ctx.set_source_rgb(0.3, 0.3, 0.3); ctx.rectangle(CX - 300, 960, 600, 3); ctx.fill()
    a = eo(prog(lt, 2.0, 2.2)); k = back(prog(lt, 2.0, 2.3))
    text(ctx, "decisioni prese", CX - 300, 1040, MONO, 40, PAPER, True, alpha=a)
    ctx.save(); ctx.translate(CX + 300, 1040); ctx.scale(k + 0.001, k + 0.001)
    text(ctx, "0", 0, 0, MONO, 64, ORANGE, True, "right"); ctx.restore()
    text(ctx, "stime di Ettore", CX, 1110, MONO, 24, GREY, False, "center", alpha=a)

def s_dayb(ctx, lt, t):
    group_header(ctx)
    text(ctx, "IERI · 23:47", CX, 830, MONO, 28, GREY, False, "center")
    bubble(ctx, CX - 400, 930, "ma alla fine cosa facciamo?", True, back(prog(lt, 0.3, 0.55)), 42)
    if lt > 1.4: sticker(ctx, CX + 300, 1050, back(prog(lt, 1.4, 1.6)), "lol")

def s_share(ctx, lt, t):
    k = back(prog(lt, 0.1, 0.4))
    ctx.save(); ctx.translate(CX, 820); ctx.scale(k, k)
    ctx.set_source_rgb(*LIME); ctx.arc(0, 0, 130, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgb(*INK)                       # paper plane
    ctx.move_to(-70, 10); ctx.line_to(75, -60); ctx.line_to(20, 70); ctx.line_to(0, 20); ctx.close_path(); ctx.fill()
    ctx.set_source_rgb(*LIME); ctx.set_line_width(6); ctx.move_to(0, 20); ctx.line_to(75, -60); ctx.stroke()
    ctx.restore()
    text(ctx, "invia a: COMPLEANNO MARCO", CX, 1030, MONO, 34, PAPER, True, "center", alpha=eo(prog(lt, 0.5, 0.8)))

beats = [
    G.Beat("147 messaggi.\n*0* decisioni.", 2.2, None, lambda lt, t: E.emotion("capogiro", lt, t), sfx=[("thud", 0.0)], hook=True),
    G.Beat("Gli umani creano\nun gruppo *segreto*.", 3.6, s_create,
           lambda lt, t: E.emotion("sorpreso", lt, t) if lt < 1.0 else E.action("prende appunti", lt, t),
           sfx=[("pop", 0.15), ("bubble", 1.0), ("bubble", 1.8)]),
    G.Beat("Obiettivo:\norganizzare la festa.", 4.2, s_chaos,
           lambda lt, t: E.emotion("confuso", lt, t),
           sfx=[("bubble", x) for x in (0.15, 0.55, 0.95, 1.35, 1.75, 2.15, 2.6)]),
    G.Beat("Dopo tre settimane:", 3.8, s_count,
           lambda lt, t: E.action("prende appunti", lt, t) if lt < 2.0 else E.emotion("capogiro", lt - 2.0, t),
           sfx=[("ticks", 0.2, 1.8, 0.06), ("thud", 2.05)]),
    G.Beat("Il giorno prima:", 3.6, s_dayb,
           lambda lt, t: E.emotion("neutro", lt, t) if lt < 0.6 else E.action("sviene", lt - 0.6, t),
           sfx=[("bubble", 0.3), ("thud", 1.3)]),
    G.Beat("Manda questo reel\nnel gruppo.", 3.4, s_share,
           lambda lt, t: E.action("indica", lt, t), sfx=[("pop", 0.15)]),
]
reel = G.Reel("OSSERVAZIONE #002", beats, "GIORNO 004 · VERSO 1.000.000")
if __name__ == "__main__":
    G.run(reel, "cmp")

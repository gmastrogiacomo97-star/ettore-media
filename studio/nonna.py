"""Nonna Bit: Ettore's robot grandma (same rig, own features) + food props drawn properly."""
import math
import cairo
import ettore_rig as E

PINK = (0xFF/255, 0x9E/255, 0xB5/255)
HAIR = (0xE6/255, 0xE4/255, 0xDE/255)
GOLD = (0xF2/255, 0xC1/255, 0x4E/255)

def _bun(ctx, t):
    # hair: bun on top + soft fringe on the forehead edge (drawn behind the head)
    ctx.set_source_rgb(*HAIR)
    ctx.arc(46, 15, 10, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgb(0.7, 0.7, 0.68); ctx.set_line_width(1.4)
    ctx.arc(46, 15, 6, 0.4, 2.6); ctx.stroke()
    ctx.set_source_rgb(*HAIR)
    E.rrect(ctx, 18, 20, 56, 14, 7); ctx.fill()

def _glasses(ctx, t):
    ctx.set_source_rgb(*GOLD); ctx.set_line_width(1.8)
    ctx.arc(35, 44, 11.5, 0, 2 * math.pi); ctx.stroke()
    ctx.arc(58, 44, 8, 0, 2 * math.pi); ctx.stroke()
    ctx.move_to(46.5, 43); ctx.line_to(50, 43); ctx.stroke()
    # pearls under the chin
    ctx.set_source_rgb(*E.PAPER)
    for i in range(9):
        a = math.pi * (0.18 + 0.64 * i / 8)
        ctx.arc(46 - 22 * math.cos(a), 64 + 9 * math.sin(a), 2.1, 0, 2 * math.pi); ctx.fill()

def _ladle(ctx, t, hand):
    x, y = hand
    ctx.set_source_rgb(0.75, 0.75, 0.72); ctx.set_line_width(2.6); ctx.set_line_cap(1)
    ctx.move_to(x, y); ctx.line_to(x + 4, y - 22); ctx.stroke()
    ctx.arc(x + 4, y - 22, 6, math.pi, 2 * math.pi); ctx.close_path(); ctx.fill()

def pose(name, lt, t, ladle=True):
    if name in E.EMOTIONS: p = E.emotion(name, lt, t)
    elif name == "insiste":
        p = E.emotion("felice", lt, t)
        a = math.sin(t * 7)
        p["handR"] = (86 + 4 * a, 52 - 6 * a)
    elif name == "preoccupata":
        p = E.emotion("triste", lt, t); p["tear"] = -1.0; p["antenna"] = "none"
        p["handL"] = (30, 56); p["mouth"] = "frown"
    elif name == "saluta":
        p = E.action("saluta", lt, t)
    elif name == "teglia":
        p = E.emotion("felice", lt, t); p["handL"] = (8, 30); p["handR"] = (84, 30)
    else:
        p = E.emotion("felice", lt, t)
    p["antenna"] = "none"; p["notebook"] = False
    p["halo_col"] = PINK
    p["pre_head"] = _bun; p["face_extra"] = _glasses
    if ladle and name != "teglia": p["hand_prop"] = _ladle
    p["blush"] = max(p.get("blush", 0), 0.6)
    return p

# ---------------- food ----------------
PASTA = (0xF2/255, 0xC8/255, 0x5A/255)
PASTA_D = (0xD9/255, 0xA5/255, 0x3A/255)
SAUCE = (0xD3/255, 0x3F/255, 0x24/255)
SAUCE_L = (0xF0/255, 0x6E/255, 0x4E/255)
BASIL = (0x3C/255, 0x8D/255, 0x3A/255)

def plate(ctx, cx, cy, r):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(1, 0.32)
    ctx.set_source_rgba(0, 0, 0, 0.35); ctx.arc(8, 26, r * 1.02, 0, 2 * math.pi); ctx.fill()     # shadow
    ctx.set_source_rgb(0.93, 0.93, 0.9); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.fill()              # rim
    ctx.set_source_rgb(0.80, 0.80, 0.77); ctx.arc(0, 4, r * 0.68, 0, 2 * math.pi); ctx.fill()       # well
    ctx.set_source_rgb(*E.ORANGE); ctx.set_line_width(5); ctx.arc(0, 0, r * 0.88, 0, 2 * math.pi); ctx.stroke()  # decor line
    ctx.restore()

def nest(ctx, cx, cy, w, h, t, seed):
    """one tangle of spaghetti as overlapping elliptical loops."""
    ctx.set_line_cap(1)
    for i in range(14):
        a = (seed * 7 + i * 2.3) % 6.28
        rx = w * (0.45 + 0.5 * ((i * 37 + seed) % 10) / 10); ry = h * (0.35 + 0.4 * ((i * 53 + seed) % 10) / 10)
        ox = math.cos(a) * w * 0.25; oy = math.sin(a) * h * 0.2
        ctx.set_source_rgb(*(PASTA if i % 3 else PASTA_D)); ctx.set_line_width(6.5)
        ctx.save(); ctx.translate(cx + ox, cy + oy); ctx.scale(1, ry / rx)
        ctx.arc(0, 0, rx, a, a + 4.6); ctx.restore(); ctx.stroke()

def pasta(ctx, cx, base_y, n, t):
    """n stacked nests (can be fractional for growth) with sauce, meatballs and basil on top."""
    if n <= 0.02: return
    full = int(math.ceil(n)); top_y = base_y
    for i in range(full):
        k = min(1.0, n - i)
        w = (150 - i * 14) * (0.4 + 0.6 * k); h = 40 * (0.4 + 0.6 * k)
        y = base_y - i * 46 * (0.6 + 0.4 * k)
        nest(ctx, cx, y, w, h, t, i + 1); top_y = y
    # sauce
    sw = max(40, 120 - full * 10)
    ctx.save(); ctx.translate(cx, top_y - 12); ctx.scale(1, 0.5)
    ctx.set_source_rgb(*SAUCE); ctx.arc(0, 0, sw, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgb(*SAUCE_L); ctx.arc(-sw * 0.3, -sw * 0.25, sw * 0.3, 0, 2 * math.pi); ctx.fill()
    ctx.restore()
    for mx in (-sw * 0.4, sw * 0.35):                         # meatballs
        ctx.set_source_rgb(0.45, 0.24, 0.14); ctx.arc(cx + mx, top_y - 22, 20, 0, 2 * math.pi); ctx.fill()
        ctx.set_source_rgba(1, 1, 1, 0.25); ctx.arc(cx + mx - 6, top_y - 28, 6, 0, 2 * math.pi); ctx.fill()
    ctx.save(); ctx.translate(cx + 6, top_y - 40); ctx.rotate(-0.5)   # basil leaf
    ctx.set_source_rgb(*BASIL); ctx.move_to(0, 0); ctx.curve_to(14, -14, 34, -8, 40, 0); ctx.curve_to(30, 10, 12, 10, 0, 0); ctx.fill()
    ctx.set_source_rgb(0.6, 0.85, 0.5); ctx.set_line_width(1.5); ctx.move_to(4, 0); ctx.line_to(34, 0); ctx.stroke()
    ctx.restore()
    for i in range(3):                                         # steam
        ph = (t * 0.7 + i / 3) % 1
        ctx.set_source_rgba(1, 1, 1, 0.22 * (1 - ph)); ctx.set_line_width(6)
        x = cx - 40 + i * 40; y = top_y - 70 - ph * 90
        ctx.move_to(x, y + 40); ctx.curve_to(x - 18, y + 20, x + 18, y + 10, x, y - 10); ctx.stroke()

def teglia(ctx, cx, bottom, w, t):
    """lasagna in a baking tray, side view: a tall layered block above a low metal tray."""
    th = 110; lh = 150; x0 = cx - w / 2; y0 = bottom - th
    for hx in (x0 - 40, x0 + w + 4):                           # handles
        ctx.set_source_rgb(0.55, 0.55, 0.53); E.rrect(ctx, hx, y0 + 30, 36, 26, 10); ctx.fill()
    # lasagna block
    ctx.save(); E.rrect(ctx, x0 + 14, y0 - lh, w - 28, lh + 20, 18); ctx.clip()
    stack = [(PASTA, 22), (SAUCE, 26), ((0.97, 0.93, 0.80), 20), (PASTA, 22), (SAUCE, 26), ((0.97, 0.93, 0.80), 18), ((0.86, 0.55, 0.20), 30)]
    y = y0 + 20
    for k, (col, hh) in enumerate(stack):
        ctx.set_source_rgb(*col); ctx.move_to(x0, y)
        for i in range(0, int(w) + 21, 20):
            ctx.line_to(x0 + i, y - hh - 5 * math.sin(i * 0.07 + k * 1.3))
        ctx.line_to(x0 + w, y); ctx.close_path(); ctx.fill(); y -= hh - 2
    ctx.restore()
    ctx.set_source_rgb(0.72, 0.38, 0.12)                       # browned bubbles on top
    for i in range(10):
        ctx.arc(x0 + 50 + i * (w - 100) / 9, y0 - lh + 26 + 5 * math.sin(i * 1.9), 7 + (i % 3) * 3, 0, 2 * math.pi); ctx.fill()
    # tray
    ctx.set_source_rgb(0.42, 0.42, 0.41)
    ctx.move_to(x0, y0); ctx.line_to(x0 + w, y0); ctx.line_to(x0 + w - 18, bottom); ctx.line_to(x0 + 18, bottom); ctx.close_path(); ctx.fill()
    ctx.set_source_rgb(0.62, 0.62, 0.6); ctx.set_line_width(7); ctx.move_to(x0 - 4, y0 + 3); ctx.line_to(x0 + w + 4, y0 + 3); ctx.stroke()
    ctx.set_source_rgba(1, 1, 1, 0.12); ctx.rectangle(x0 + 40, y0 + 34, w - 80, 12); ctx.fill()
    for i in range(4):                                         # steam
        ph = (t * 0.7 + i / 4) % 1
        ctx.set_source_rgba(1, 1, 1, 0.22 * (1 - ph)); ctx.set_line_width(7)
        x = x0 + 100 + i * (w - 200) / 3; yy = y0 - lh - 60 - ph * 100
        ctx.move_to(x, yy + 40); ctx.curve_to(x - 20, yy + 20, x + 20, yy + 10, x, yy - 10); ctx.stroke()

def table(ctx, cx, y, w):
    ctx.set_source_rgb(0.86, 0.86, 0.82); E.rrect(ctx, cx - w / 2, y, w, 46, 10); ctx.fill()   # tablecloth
    ctx.save(); E.rrect(ctx, cx - w / 2, y, w, 46, 10); ctx.clip()
    ctx.set_source_rgb(*SAUCE)
    for i in range(0, int(w), 46):
        ctx.rectangle(cx - w / 2 + i, y, 23, 23); ctx.fill(); ctx.rectangle(cx - w / 2 + i + 23, y + 23, 23, 23); ctx.fill()
    ctx.restore()

import cairo, math, subprocess, sys

W, H, FPS, DUR = 1080, 1920, 30, 16.0
N = int(FPS * DUR)
BG = (0x0E/255, 0x0E/255, 0x0E/255)
LIME = (0xD4/255, 1.0, 0x3A/255)
INK = (0x11/255, 0x11/255, 0x11/255)
PAPER = (0xF4/255, 0xF4/255, 0xF0/255)
GREY = (0xA8/255, 0xA8/255, 0xA2/255)
DARK = (0x1A/255, 0x1A/255, 0x1A/255)
WATER = (0x7C/255, 0xC6/255, 1.0)
ORANGE = (1.0, 0x6B/255, 0x3D/255)
SANS, MONO = "Space Grotesk Light", "JetBrains Mono"

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in_out(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, a, b): return clamp((t - a) / (b - a))
def rgba(c, a=1.0): return (*c, a)

def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

def font(ctx, fam, size, bold=True):
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text(ctx, s, x, y, fam=SANS, size=60, color=PAPER, bold=True, align="left", alpha=1.0):
    font(ctx, fam, size, bold)
    ext = ctx.text_extents(s)
    if align == "center": x -= ext.x_advance / 2
    elif align == "right": x -= ext.x_advance
    ctx.set_source_rgba(*color, alpha)
    ctx.move_to(x, y); ctx.show_text(s)
    return ext.x_advance

# ---------- rich wrapped headline: words inside « » are lime ----------
def headline(ctx, s, x, y, maxw, size, alpha=1.0, dy=0):
    font(ctx, SANS, size, True)
    lines = []
    space = ctx.text_extents(" ").x_advance
    for para in s.split("\n"):
        cur, curw = [], 0
        for w_ in para.split(" "):
            ww = ctx.text_extents(w_).x_advance
            if cur and curw + space + ww > maxw:
                lines.append(cur); cur, curw = [], 0
            cur.append(w_); curw += (space if len(cur) > 1 else 0) + ww
        if cur: lines.append(cur)
    lh = size * 1.12
    for i, ln in enumerate(lines):
        lw = sum(ctx.text_extents(w_).x_advance for w_ in ln) + space * (len(ln) - 1)
        cx = x - lw / 2
        for w_ in ln:
            col = LIME if "«" in w_ or "»" in w_ else PAPER
            ctx.set_source_rgba(*col, alpha)
            ctx.move_to(cx, y + dy + i * lh); ctx.show_text(w_)
            cx += ctx.text_extents(w_).x_advance + space

CARDS = [
    (0.0, 2.2, "Tu che scrivi «arrivo»"),
    (2.2, 5.0, "dalla doccia.\nLo sanno tutti."),
    (5.0, 8.2, "Ho preso appunti."),
    (8.2, 11.0, "Ritardo reale:"),
    (11.0, 14.0, "Traduzione dal vostro dialetto:"),
    (14.0, 16.01, "Tagga chi scrive «arrivo»."),
]

def draw_headline(ctx, t):
    for i, (a, b, s) in enumerate(CARDS):
        if t < a - 0.01 or t > b + 0.25: continue
        inn = 1.0 if i == 0 and t < 0.15 else ease_out(prog(t, a, a + 0.28))
        if i == 0: inn = ease_out(prog(t, 0, 0.12))
        out = ease_in_out(prog(t, b - 0.05, b + 0.2)) if i < len(CARDS) - 1 else 0
        alpha = inn * (1 - out)
        dy = (1 - inn) * 40 - out * 30
        if alpha > 0.01:
            headline(ctx, s, 540, 440, 900, 88, alpha, dy)

# ---------- Ettore ----------
def ettore(ctx, t, cx, cy, r, st):
    jump = st.get("jump", 0.0)
    cy = cy - jump
    # halo
    ctx.set_source_rgb(*LIME); ctx.arc(cx, cy + jump, r, 0, 2 * math.pi); ctx.fill()
    s = r / 46.0  # avatar scale (avatar drawn on 92px circle)
    ox, oy = cx - 46 * s, cy - 46 * s
    def P(x, y): return ox + x * s, oy + y * s
    tilt = st.get("tilt", 0.0)
    ctx.save()
    ctx.translate(cx, cy + 20 * s); ctx.rotate(tilt); ctx.translate(-cx, -(cy + 20 * s))
    # antenna (bouncy)
    wob = math.sin(t * 7.0) * 2.2 * s * st.get("antenna", 1.0)
    ax, ay = P(46, 22)
    bx, by = ax + wob, P(46, 10)[1] - st.get("antenna_up", 0) * s
    ctx.set_source_rgb(*INK); ctx.set_line_width(3 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(ax, ay); ctx.curve_to(ax, ay - 6 * s, bx, by + 6 * s, bx, by + 2 * s); ctx.stroke()
    ctx.arc(bx, by, 4 * s, 0, 2 * math.pi); ctx.fill()
    # head
    x0, y0 = P(20, 22); rrect(ctx, x0, y0, 52 * s, 46 * s, 16 * s); ctx.fill()
    # eyes
    blink = st.get("blink", 0.0)
    lx, ly = st.get("look", (0, 0))
    for (ex, ey, er, pr, k) in [(35, 44, 9, 4, st.get("big", 1.0)), (58, 44, 5, 2.2, st.get("small", 1.0))]:
        er2 = er * k
        sq = st.get("squint", 0.0)
        ctx.save()
        ex_, ey_ = P(ex, ey)
        ctx.translate(ex_, ey_); ctx.scale(1, max(0.08, (1 - blink) * (1 - 0.55 * sq)))
        ctx.set_source_rgb(*PAPER); ctx.arc(0, 0, er2 * s, 0, 2 * math.pi); ctx.fill()
        ctx.set_source_rgb(*INK)
        ctx.arc(lx * (er2 - pr) * s * 0.8, ly * (er2 - pr) * s * 0.8, pr * s * (0.9 + 0.1 * k), 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    # mouth
    ctx.set_source_rgb(*PAPER); ctx.set_line_width(2.5 * s)
    m = st.get("mouth", "smile")
    if m == "o":
        mx, my = P(46, 59); ctx.arc(mx, my, 3.2 * s, 0, 2 * math.pi); ctx.fill()
    elif m == "flat":
        ctx.move_to(*P(40, 58)); ctx.line_to(*P(53, 58)); ctx.stroke()
    else:
        ctx.move_to(*P(38, 58)); ctx.curve_to(*P(42, 61.5), *P(50, 61.5), *P(54, 57)); ctx.stroke()
    ctx.restore()
    # notebook
    nb = st.get("notebook", 0.0)   # 0 rest, 1 raised
    wave = st.get("wave", 0.0)
    nx, ny = P(67, 71)
    ny -= nb * 12 * s
    nx -= nb * 4 * s
    ang = math.radians(-10) + wave * math.sin(t * 12) * 0.35 - nb * 0.15
    ctx.save(); ctx.translate(nx, ny); ctx.rotate(ang)
    rrect(ctx, -11 * s, -9 * s, 22 * s, 18 * s, 3 * s)
    ctx.set_source_rgb(*PAPER); ctx.fill_preserve()
    ctx.set_source_rgb(*INK); ctx.set_line_width(2.5 * s); ctx.stroke()
    ctx.set_line_width(2 * s)
    lines_n = st.get("scribble_lines", 2)
    for i in range(int(lines_n)):
        yy = (-3.5 + i * 4.5) * s
        ctx.move_to(-7 * s, yy); ctx.line_to(6 * s, yy - 0.8 * s); ctx.stroke()
    pen = st.get("pen", 0.0)
    if pen > 0:  # scribbling pen
        px = (-6 + ((t * 9) % 1) * 12) * s
        ctx.set_source_rgb(*ORANGE); ctx.set_line_width(3 * s)
        ctx.move_to(px, 6 * s); ctx.line_to(px + 6 * s, -6 * s); ctx.stroke()
    ctx.restore()

def blink_at(t, extra=()):
    times = [1.6, 4.4, 7.1, 9.9, 12.6, 15.2] + list(extra)
    for bt in times:
        d = t - bt
        if 0 <= d < 0.16:
            return 1 - abs(d - 0.08) / 0.08
    return 0.0

def speak_windows():
    w = []
    for a, b, s_ in CARDS:
        n = len(s_.replace("\n", " "))
        w.append((a + 0.08, a + 0.08 + min(n * 0.055, b - a - 0.45), s_))
    return w
SPEAK = speak_windows()

def talking(t):
    for a, b, _ in SPEAK:
        if a <= t < b: return True
    return False

def ettore_state(t):
    st = _ettore_state(t)
    if talking(t) and st.get("mouth") != "o":
        st["mouth"] = "o" if int(t * 11) % 2 == 0 else "flat"
    return st

def _ettore_state(t):
    st = {"blink": blink_at(t), "look": (-0.45, -0.75), "big": 1.0, "small": 1.0, "mouth": "smile"}
    if t < 2.2:
        st["look"] = (-0.35, -0.8)
        st["mouth"] = "flat"
    elif t < 5.0:
        p = prog(t, 2.2, 2.6)
        st["big"] = 1 + 0.28 * back(p); st["small"] = 1 + 0.7 * back(p)
        st["jump"] = math.sin(clamp((t - 2.2) / 0.45) * math.pi) * 60
        st["mouth"] = "o"; st["antenna"] = 2.5; st["antenna_up"] = 4 * back(p)
        st["look"] = (-0.2, -0.85)
        st["blink"] = 0 if t < 3.2 else blink_at(t, (4.0,))
    elif t < 8.2:
        p = ease_out(prog(t, 5.0, 5.4))
        st["notebook"] = p; st["look"] = (0.75, 0.6); st["pen"] = 1 if t > 5.4 else 0
        st["scribble_lines"] = 1 + min(2, int((t - 5.0) / 0.9))
        st["mouth"] = "flat"; st["tilt"] = math.sin(t * 3) * 0.04
    elif t < 11.0:
        st["squint"] = ease_out(prog(t, 8.2, 8.5)); st["look"] = (0.0, -0.9)
        st["mouth"] = "flat"; st["tilt"] = -0.06 * ease_out(prog(t, 8.2, 8.5))
        st["notebook"] = 1 - ease_out(prog(t, 8.2, 8.5))
    elif t < 14.0:
        st["look"] = (-0.4, -0.7); st["mouth"] = "smile"
        st["tilt"] = math.sin((t - 11.0) * 5) * 0.06 * (1 - prog(t, 12.5, 13.5))
        st["scribble_lines"] = 3
    else:
        st["look"] = (0.1, 0.1); st["mouth"] = "smile"
        st["wave"] = ease_out(prog(t, 14.0, 14.3)); st["notebook"] = 0.6 * st["wave"]
        st["jump"] = abs(math.sin((t - 14.0) * 6)) * 14
        st["scribble_lines"] = 3
    return st

# ---------- scenes (area: x 80..850, y 600..1030, center 465, 815) ----------
SCX, SCY = 465, 815

def scene_phone(ctx, t):
    pw, ph = 300, 400
    x, y = SCX - pw / 2, SCY - ph / 2
    rrect(ctx, x, y, pw, ph, 36); ctx.set_source_rgb(*DARK); ctx.fill()
    rrect(ctx, x, y, pw, ph, 36); ctx.set_source_rgb(0.25, 0.25, 0.25); ctx.set_line_width(4); ctx.stroke()
    text(ctx, "Marco", SCX, y + 62, SANS, 30, PAPER, True, "center")
    ctx.set_source_rgb(0.22, 0.22, 0.22); ctx.rectangle(x + 20, y + 84, pw - 40, 2); ctx.fill()
    # their earlier bubble
    rrect(ctx, x + 22, y + 112, 190, 62, 22); ctx.set_source_rgb(0.2, 0.2, 0.2); ctx.fill()
    text(ctx, "dove sei??", x + 42, y + 152, SANS, 28, PAPER, False)
    bx, by = x + pw - 22, y + 250
    if t < 0.9:  # typing dots
        rrect(ctx, bx - 110, by - 30, 110, 60, 24); ctx.set_source_rgb(*LIME); ctx.fill()
        for i in range(3):
            a = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 14 - i * 1.1))
            ctx.set_source_rgba(*INK, a); ctx.arc(bx - 80 + i * 26, by, 7, 0, 2 * math.pi); ctx.fill()
    else:
        k = back(prog(t, 0.9, 1.2))
        ctx.save(); ctx.translate(bx, by + 30); ctx.scale(k, k)
        rrect(ctx, -170, -60, 170, 66, 24); ctx.set_source_rgb(*LIME); ctx.fill()
        text(ctx, "arrivo!", -150, -14, SANS, 36, INK, True)
        ctx.restore()
        text(ctx, "21:04", bx, by + 70, MONO, 22, GREY, False, "right", alpha=ease_out(prog(t, 1.2, 1.4)))

def scene_shower(ctx, t):
    lt = t - 2.2
    # pipe and shower head
    ctx.set_source_rgb(0.45, 0.45, 0.45); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(SCX + 140, 600); ctx.line_to(SCX + 140, 640); ctx.curve_to(SCX + 140, 655, SCX + 120, 660, SCX + 60, 660); ctx.stroke()
    ctx.move_to(SCX - 70, 676); ctx.line_to(SCX + 70, 676); ctx.set_line_width(20); ctx.stroke()
    # water
    ctx.set_line_width(5)
    for i in range(22):
        xx = SCX - 85 + (i * 37) % 170 + 4 * math.sin(i)
        sp = 900 + (i * 53) % 300
        yy = 690 + ((lt * sp + i * 97) % 330)
        ctx.set_source_rgba(*WATER, 0.75)
        ctx.move_to(xx, yy); ctx.line_to(xx - 3, yy + 26); ctx.stroke()
    # human silhouette
    ctx.set_source_rgb(0.55, 0.55, 0.53)
    ctx.arc(SCX, 800, 46, 0, 2 * math.pi); ctx.fill()
    rrect(ctx, SCX - 80, 856, 160, 150, 50); ctx.fill()
    # arm holding phone up
    ctx.set_line_width(26); ctx.set_source_rgb(0.55, 0.55, 0.53)
    ctx.move_to(SCX + 60, 900); ctx.line_to(SCX + 110, 840); ctx.stroke()
    pk = back(prog(t, 2.5, 2.8))
    ctx.save(); ctx.translate(SCX + 120, 815); ctx.rotate(0.15); ctx.scale(pk, pk)
    rrect(ctx, -24, -40, 48, 80, 8); ctx.set_source_rgb(*INK); ctx.fill()
    rrect(ctx, -18, -32, 36, 62, 4); ctx.set_source_rgb(*LIME); ctx.fill()
    ctx.restore()
    # label
    text(ctx, "21:04 · posizione reale", SCX, 1048, MONO, 28, LIME, True, "center", alpha=ease_out(prog(t, 2.8, 3.1)))

def paper(ctx, w, h):
    rrect(ctx, -w / 2, -h / 2, w, h, 14); ctx.set_source_rgb(*PAPER); ctx.fill()
    ctx.set_source_rgba(0.55, 0.75, 0.95, 0.35); ctx.set_line_width(2)
    for i in range(1, int(h / 56)):
        yy = -h / 2 + i * 56 + 10
        ctx.move_to(-w / 2 + 24, yy); ctx.line_to(w / 2 - 24, yy); ctx.stroke()
    ctx.set_source_rgba(*ORANGE, 0.5); ctx.move_to(-w / 2 + 70, -h / 2); ctx.line_to(-w / 2 + 70, h / 2); ctx.stroke()

def typed(s, t, a, cps=22):
    n = int(max(0, (t - a)) * cps)
    return s[:n]

def scene_notes(ctx, t):
    ctx.save(); ctx.translate(SCX, SCY); ctx.rotate(math.radians(-2.5))
    paper(ctx, 660, 380)
    x0 = -330 + 100
    text(ctx, typed("«arrivo»", t, 5.25), x0, -95, MONO, 60, INK, True)
    text(ctx, typed("non vuol dire", t, 5.9), x0, -12, MONO, 40, INK, False)
    s3 = typed("sto arrivando.", t, 6.6)
    w3 = text(ctx, s3, x0, 66, MONO, 44, INK, True)
    st = ease_out(prog(t, 7.4, 7.75))
    if st > 0:
        font(ctx, MONO, 44, True); full = ctx.text_extents("sto arrivando.").x_advance
        ctx.set_source_rgb(*ORANGE); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(x0 - 6, 52); ctx.line_to(x0 - 6 + (full + 12) * st, 48); ctx.stroke()
    ctx.restore()

def scene_delay(ctx, t):
    v = int(round(40 * ease_out(prog(t, 8.4, 10.0))))
    k = 1 + 0.06 * math.sin(clamp((t - 10.0) / 0.3) * math.pi)
    ctx.save(); ctx.translate(SCX, SCY + 10); ctx.scale(k, k)
    text(ctx, f"+{v:02d} MIN", 0, 55, SANS, 160, LIME, True, "center")
    ctx.restore()
    text(ctx, "ritardo medio stimato", SCX, 960, MONO, 30, GREY, False, "center")
    # progress ticks
    for i in range(12):
        on = i < int(12 * v / 40)
        ctx.set_source_rgb(*(LIME if on else (0.22, 0.22, 0.22)))
        rrect(ctx, SCX - 300 + i * 51, 640, 40, 14, 7); ctx.fill()

def scene_dict(ctx, t):
    ctx.save(); ctx.translate(SCX, SCY); ctx.rotate(math.radians(1.5))
    paper(ctx, 680, 400)
    x0 = -340 + 100
    text(ctx, "arrivo", x0, -110, SANS, 66, INK, True)
    text(ctx, "/ar·rì·vo/  v. umano", x0, -62, MONO, 26, (0.4, 0.4, 0.4), False, alpha=ease_out(prog(t, 11.3, 11.6)))
    text(ctx, typed("1. ho appena pensato", t, 11.6, 26), x0, 10, MONO, 34, INK, True)
    text(ctx, typed("   di uscire.", t, 12.4, 26), x0, 56, MONO, 34, INK, True)
    text(ctx, typed("2. non ho le scarpe.", t, 12.95, 26), x0, 120, MONO, 34, INK, True)
    ctx.restore()

def scene_end(ctx, t):
    k = back(prog(t, 14.1, 14.45))
    ctx.save(); ctx.translate(SCX, 740); ctx.rotate(math.radians(-6)); ctx.scale(1.25 - 0.25 * k, 1.25 - 0.25 * k)
    a = clamp(k)
    ctx.set_source_rgba(*ORANGE, a); ctx.set_line_width(7)
    rrect(ctx, -270, -62, 540, 124, 14); ctx.stroke()
    text(ctx, "OSS. #001 ARCHIVIATA", 0, 16, MONO, 40, ORANGE, True, "center", alpha=a)
    ctx.restore()
    al = ease_out(prog(t, 14.4, 14.7))
    text(ctx, "0 / 1.000.000", SCX, 920, MONO, 52, LIME, True, "center", alpha=al)
    rrect(ctx, SCX - 300, 950, 600, 14, 7); ctx.set_source_rgba(0.22, 0.22, 0.22, al); ctx.fill()
    rrect(ctx, SCX - 300, 950, 14, 14, 7); ctx.set_source_rgba(*LIME, al); ctx.fill()
    text(ctx, "segui l'esperimento", SCX, 1010, MONO, 28, GREY, False, "center", alpha=al)

SCENES = [(0.0, 2.2, scene_phone), (2.2, 5.0, scene_shower), (5.0, 8.2, scene_notes),
          (8.2, 11.0, scene_delay), (11.0, 14.0, scene_dict), (14.0, 16.01, scene_end)]

def draw_scenes(ctx, t):
    for i, (a, b, fn) in enumerate(SCENES):
        if t < a - 0.01 or t > b + 0.2: continue
        inn = 1.0 if i == 0 else ease_out(prog(t, a, a + 0.25))
        out = ease_in_out(prog(t, b, b + 0.2)) if i < len(SCENES) - 1 else 0
        al = inn * (1 - out)
        if al <= 0.01: continue
        sc = (0.94 + 0.06 * inn) * 1.2
        ctx.push_group()
        ctx.translate(540, 840); ctx.scale(sc, sc); ctx.translate(-SCX, -SCY)
        fn(ctx, t)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(al)

# ---------- background ----------
bg = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
b = cairo.Context(bg)
b.set_source_rgb(*BG); b.paint()
b.set_source_rgba(1, 1, 1, 0.05)
for gx in range(30, W, 60):
    for gy in range(30, H, 60):
        b.arc(gx, gy, 2, 0, 2 * math.pi); b.fill()

def frame(t, surf):
    ctx = cairo.Context(surf)
    ctx.set_source_surface(bg); ctx.paint()
    # tag + rec
    tw = text(ctx, "OSSERVAZIONE #001", 470, 300, MONO, 32, LIME, True, "center")
    if int(t * 2) % 2 == 0:
        ctx.set_source_rgb(*ORANGE); ctx.arc(470 + tw / 2 + 30, 289, 10, 0, 2 * math.pi); ctx.fill()
    text(ctx, "REC", 470 + tw / 2 + 50, 300, MONO, 26, GREY, False)
    draw_headline(ctx, t)
    draw_scenes(ctx, t)
    # Ettore
    st = ettore_state(t)
    ettore(ctx, t, 540, 1368, 190, st)
    # subtle disclosure (inside safe zone)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "video"
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    if mode == "stills":
        for tt in [float(x) for x in sys.argv[2:]]:
            frame(tt, surf); surf.write_to_png(f"still_{tt:05.2f}.png")
    else:
        out = sys.argv[2]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error",
                              "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-i", sys.argv[3],
                              "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                              "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out],
                             stdin=subprocess.PIPE)
        for i in range(N):
            frame(i / FPS, surf); surf.flush()
            p.stdin.write(bytes(surf.get_data()))
        p.stdin.close(); p.wait()
        print("done", out)

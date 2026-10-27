"""Ettore's expressive rig: emotions + actions. Coordinates are in 'avatar units' (head sits in a 92x92 box)."""
import cairo, math

LIME = (0xD4/255, 1.0, 0x3A/255)
INK = (0x11/255, 0x11/255, 0x11/255)
PAPER = (0xF4/255, 0xF4/255, 0xF0/255)
ORANGE = (1.0, 0x6B/255, 0x3D/255)
WATER = (0x7C/255, 0xC6/255, 1.0)
GREY = (0.6, 0.6, 0.58)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, k): return a + (b - a) * k

def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

REST_L, REST_R = (13, 74), (77, 72)

def base_pose():
    return {"eyeL": "open", "eyeR": "open", "kL": 1.0, "kR": 1.0, "look": (0.0, -0.3), "blink": 0.0, "squint": 0.0,
            "brows": (0.0, 0.0, 0.0), "mouth": "smile", "antenna": "normal",
            "blush": 0.0, "tear": -1.0, "sweat": 0.0, "steam": 0.0, "question": 0.0, "exclaim": 0.0, "stars": 0.0,
            "hearts": 0.0, "handL": REST_L, "handR": REST_R, "notebook": True, "nb_angle": -0.17, "pen": 0.0,
            "dx": 0.0, "dy": 0.0, "tilt": 0.0, "sx": 1.0, "sy": 1.0, "halo": 1.0, "glitch": 0.0}

# ---------------- drawing ----------------
def _star(ctx, x, y, r, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.move_to(0, -r)
    for i in range(1, 8):
        a = i * math.pi / 4; rr = r if i % 2 == 0 else r * 0.38
        ctx.line_to(rr * math.sin(a), -rr * math.cos(a))
    ctx.close_path(); ctx.restore()

def _heart(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 3); ctx.curve_to(-6, -1, -4, -6, 0, -3); ctx.curve_to(4, -6, 6, -1, 0, 3)
    ctx.close_path(); ctx.restore()

def _eye(ctx, t, x, y, r, pr, kind, k, p):
    ctx.save(); ctx.translate(x, y)
    if kind == "open":
        sy = max(0.08, (1 - p["blink"]) * (1 - 0.6 * p["squint"]))
        ctx.save(); ctx.scale(1, sy)
        ctx.set_source_rgb(*PAPER); ctx.arc(0, 0, r * k, 0, 2 * math.pi); ctx.fill()
        lx, ly = p["look"]; pk = 1.0 if k <= 1.2 else 0.75   # wide eyes -> smaller pupils (fear)
        ctx.set_source_rgb(*INK); ctx.arc(lx * (r * k - pr) * 0.8, ly * (r * k - pr) * 0.8, pr * pk, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    else:
        ctx.set_source_rgb(*PAPER); ctx.set_line_width(2.4); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        rr = r * k
        if kind == "happy":    # ^ shaped
            ctx.arc(0, rr * 0.5, rr * 0.8, math.pi * 1.15, math.pi * 1.85); ctx.stroke()
        elif kind == "sad":    # closed, drooping
            ctx.arc(0, -rr * 0.2, rr * 0.75, math.pi * 0.2, math.pi * 0.8); ctx.stroke()
        elif kind == "closed":
            ctx.move_to(-rr * 0.8, 0); ctx.line_to(rr * 0.8, 0); ctx.stroke()
        elif kind == "x":
            d = rr * 0.7
            ctx.move_to(-d, -d); ctx.line_to(d, d); ctx.move_to(d, -d); ctx.line_to(-d, d); ctx.stroke()
        elif kind == "spiral":
            ctx.set_line_width(1.6); rot = t * 8
            for i in range(60):
                a = i * 0.32 + rot; rad = rr * i / 60
                (ctx.move_to if i == 0 else ctx.line_to)(rad * math.cos(a), rad * math.sin(a))
            ctx.stroke()
        elif kind == "heart":
            ctx.set_source_rgb(*ORANGE); _heart(ctx, 0, 0, rr / 5.5 * (1 + 0.12 * math.sin(t * 14))); ctx.fill()
        elif kind == "star":
            _star(ctx, 0, 0, rr * 1.1, t * 3); ctx.fill()
    ctx.restore()

def _mouth(ctx, t, kind):
    ctx.set_source_rgb(*PAPER); ctx.set_line_width(2.5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if kind == "smile":
        ctx.move_to(38, 57); ctx.curve_to(42, 61.5, 50, 61.5, 54, 57); ctx.stroke()
    elif kind == "grin":
        ctx.move_to(37, 55.5); ctx.line_to(55, 55.5); ctx.curve_to(54, 64, 38, 64, 37, 55.5); ctx.close_path(); ctx.fill()
        ctx.set_source_rgb(*ORANGE); ctx.arc(46, 61, 2.6, 0, math.pi); ctx.fill()
    elif kind == "flat":
        ctx.move_to(40, 58); ctx.line_to(53, 58); ctx.stroke()
    elif kind == "o":
        ctx.arc(46, 59, 3.2, 0, 2 * math.pi); ctx.fill()
    elif kind == "open_big":
        ctx.save(); ctx.translate(46, 59.5); ctx.scale(1, 1.3); ctx.arc(0, 0, 4.6, 0, 2 * math.pi); ctx.restore(); ctx.fill()
        ctx.set_source_rgb(*INK); ctx.save(); ctx.translate(46, 60); ctx.scale(1, 1.3); ctx.arc(0, 0, 2.8, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    elif kind == "frown":
        ctx.move_to(39, 61); ctx.curve_to(43, 56.5, 49, 56.5, 53, 61); ctx.stroke()
    elif kind == "wavy":
        ctx.set_line_width(2.0)
        for i in range(25):
            x = 38 + i * 16 / 24; y = 58.5 + 1.6 * math.sin(i * 0.9 + t * 20)
            (ctx.move_to if i == 0 else ctx.line_to)(x, y)
        ctx.stroke()
    elif kind == "grit":
        rrect(ctx, 38, 55, 16, 7, 2); ctx.fill()
        ctx.set_source_rgb(*INK); ctx.set_line_width(1.1)
        for x in (42, 46, 50): ctx.move_to(x, 55.5); ctx.line_to(x, 61.5); ctx.stroke()
        ctx.move_to(38.5, 58.5); ctx.line_to(53.5, 58.5); ctx.stroke()
    elif kind == "tongue":
        ctx.move_to(38, 57); ctx.curve_to(42, 61.5, 50, 61.5, 54, 57); ctx.stroke()
        ctx.set_source_rgb(*ORANGE); ctx.arc(49, 60.5, 2.8, 0, math.pi); ctx.fill()

def _arm(ctx, sh, hand, side):
    ex = (sh[0] + hand[0]) / 2 + side * 5; ey = (sh[1] + hand[1]) / 2 + 3
    for col, w in ((PAPER, 6.2), (INK, 3.6)):
        ctx.set_source_rgb(*col); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(*sh); ctx.curve_to(ex, ey, ex, ey, *hand); ctx.stroke()

def _hand(ctx, hand, pinch=False):
    x, y = hand
    ctx.set_source_rgb(*PAPER); ctx.arc(x, y, 5.6, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgb(*INK); ctx.arc(x, y, 4.4, 0, 2 * math.pi); ctx.fill()
    if pinch:   # fingers bunched pointing up: the Italian 'ma che vuoi'
        ctx.move_to(x - 5, y - 1); ctx.curve_to(x - 5, y - 9, x - 1.5, y - 15, x, y - 17)
        ctx.curve_to(x + 1.5, y - 15, x + 5, y - 9, x + 5, y - 1); ctx.close_path()
        ctx.set_source_rgb(*INK); ctx.fill_preserve(); ctx.set_source_rgb(*PAPER); ctx.set_line_width(1.3); ctx.stroke()
        ctx.set_line_width(0.9)
        for dx in (-1.8, 0, 1.8):
            ctx.move_to(x + dx, y - 4); ctx.line_to(x + dx * 0.3, y - 13); ctx.stroke()

def _notebook(ctx, t, hand, ang, pen):
    ctx.save(); ctx.translate(hand[0] - 2, hand[1] - 4); ctx.rotate(ang)
    rrect(ctx, -11, -9, 22, 18, 3); ctx.set_source_rgb(*PAPER); ctx.fill_preserve()
    ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    ctx.set_line_width(2)
    for i in range(3):
        yy = -3.5 + i * 4.5; ctx.move_to(-7, yy); ctx.line_to(6, yy - 0.8); ctx.stroke()
    if pen > 0:
        px = -6 + ((t * 9) % 1) * 12
        ctx.set_source_rgb(*ORANGE); ctx.set_line_width(3); ctx.move_to(px, 6); ctx.line_to(px + 6, -6); ctx.stroke()
    ctx.restore()

def draw(ctx, t, cx, cy, r, p):
    s = r / 46.0
    # halo
    if p["halo"] > 0:
        ctx.set_source_rgb(*p.get("halo_col", LIME)); ctx.arc(cx, cy, r * p["halo"], 0, 2 * math.pi); ctx.fill()
    ctx.save()
    ctx.translate(cx - 46 * s, cy - 46 * s); ctx.scale(s, s)
    gx = (math.sin(t * 90) * 3 if p["glitch"] > 0 and int(t * 20) % 3 == 0 else 0) * p["glitch"]
    ctx.translate(46 + p["dx"] + gx, 68 + p["dy"]); ctx.rotate(p["tilt"]); ctx.scale(p["sx"], p["sy"]); ctx.translate(-46, -68)
    # arms behind head when raised above shoulders
    shL, shR = (22, 58), (70, 58)
    # antenna
    ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    an = p["antenna"]
    wob = math.sin(t * 7.0) * 2.0
    if an == "none":
        bx, by = None, None
    elif an == "droop":
        ctx.move_to(46, 22); ctx.curve_to(46, 14, 52, 11, 57, 15); ctx.stroke(); bx, by = 57, 16
    elif an == "spin":
        a = t * 18; bx, by = 46 + 6 * math.cos(a), 11 + 2 * math.sin(a)
        ctx.move_to(46, 22); ctx.line_to(46, 13); ctx.stroke()
    elif an == "stiff":
        ctx.move_to(46, 22); ctx.line_to(46, 6); ctx.stroke(); bx, by = 46, 5
    else:
        bx, by = 46 + wob, 10
        ctx.move_to(46, 22); ctx.curve_to(46, 16, bx, 16, bx, by + 2); ctx.stroke()
    if bx is not None:
        ctx.arc(bx, by, 4, 0, 2 * math.pi); ctx.fill()
    if p.get("pre_head"): p["pre_head"](ctx, t)
    if an == "spark":
        ctx.set_source_rgb(*LIME if p["halo"] == 0 else PAPER)
        for i in range(6):
            a = i * math.pi / 3 + t * 2; l0, l1 = 6, 9 + 2 * math.sin(t * 20 + i)
            ctx.set_line_width(1.6); ctx.move_to(bx + l0 * math.cos(a), by + l0 * math.sin(a))
            ctx.line_to(bx + l1 * math.cos(a), by + l1 * math.sin(a)); ctx.stroke()
    # head
    ctx.set_source_rgb(*INK); rrect(ctx, 20, 22, 52, 46, 16); ctx.fill()
    # blush
    if p["blush"] > 0:
        ctx.set_source_rgba(*ORANGE, 0.55 * p["blush"])
        for x in (30, 61):
            ctx.save(); ctx.translate(x, 54); ctx.scale(1, 0.5); ctx.arc(0, 0, 4.5, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    # eyes
    _eye(ctx, t, 35, 44, 9, 4, p["eyeL"], p["kL"], p)
    _eye(ctx, t, 58, 44, 5, 2.2, p["eyeR"], p["kR"], p)
    # brows: (angle, angle, raise)
    bl, br, bh = p["brows"]
    ctx.set_source_rgb(*PAPER); ctx.set_line_width(2.4); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for (x, y, half, ang) in ((35, 31.5 - bh - 9 * (p["kL"] - 1), 6, bl), (58, 34 - bh - 5 * (p["kR"] - 1), 4.5, -br)):
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.move_to(-half, 0); ctx.line_to(half, 0); ctx.stroke(); ctx.restore()
    # mouth
    _mouth(ctx, t, p["mouth"])
    if p.get("face_extra"): p["face_extra"](ctx, t)
    # tear
    if p["tear"] >= 0:
        ty = 50 + (p["tear"] % 1) * 18
        ctx.set_source_rgb(*WATER); ctx.move_to(29, ty - 4); ctx.curve_to(31.5, ty, 31.5, ty + 3, 29, ty + 3)
        ctx.curve_to(26.5, ty + 3, 26.5, ty, 29, ty - 4); ctx.fill()
    # sweat
    if p["sweat"] > 0:
        sy = 24 + 3 * math.sin(t * 6)
        ctx.set_source_rgba(*WATER, p["sweat"]); ctx.move_to(74, sy - 5); ctx.curve_to(77.5, sy, 77.5, sy + 4, 74, sy + 4)
        ctx.curve_to(70.5, sy + 4, 70.5, sy, 74, sy - 5); ctx.fill()
    # arms + hands + notebook
    hL, hR = p["handL"], p["handR"]
    _arm(ctx, shL, hL, -1); _hand(ctx, hL, p.get("pinchL", False))
    _arm(ctx, shR, hR, 1)
    _hand(ctx, hR, p.get("pinchR", False))
    if p["notebook"]: _notebook(ctx, t, hR, p["nb_angle"], p["pen"])
    if p.get("hand_prop"): p["hand_prop"](ctx, t, hR)
    ctx.restore()
    # effects in screen space around the head (unaffected by squash)
    def U(x, y): return cx + (x - 46) * s, cy + (y - 46) * s
    ctx.save()
    if p["steam"] > 0:
        for i in range(3):
            ph = (t * 1.6 + i / 3) % 1
            x, y = U(30 + i * 16, 14 - ph * 16)
            ctx.set_source_rgba(0.85, 0.85, 0.85, 0.7 * (1 - ph) * p["steam"]); ctx.arc(x, y, (3 + ph * 4) * s, 0, 2 * math.pi); ctx.fill()
    if p["question"] > 0:
        k = back(p["question"]); x, y = U(80, 18 + 2 * math.sin(t * 5))
        ctx.select_font_face("Space Grotesk Light", 0, 1); ctx.set_font_size(26 * s * k)
        ctx.set_source_rgb(*PAPER); ctx.move_to(x, y); ctx.show_text("?")
    if p["exclaim"] > 0:
        k = back(p["exclaim"]); x, y = U(80, 18)
        ctx.select_font_face("Space Grotesk Light", 0, 1); ctx.set_font_size(28 * s * k)
        ctx.set_source_rgb(*ORANGE); ctx.move_to(x, y); ctx.show_text("!")
    if p["stars"] > 0:
        for i in range(3):
            a = t * 4 + i * 2 * math.pi / 3
            x, y = U(46 + 26 * math.cos(a), 12 + 6 * math.sin(a))
            ctx.set_source_rgba(*PAPER, p["stars"]); _star(ctx, x, y, 4 * s, t * 5); ctx.fill()
    if p["hearts"] > 0:
        for i in range(3):
            ph = (t * 0.8 + i / 3) % 1
            x, y = U(30 + i * 16 + 3 * math.sin(t * 3 + i), 16 - ph * 20)
            ctx.set_source_rgba(*ORANGE, (1 - ph) * p["hearts"]); _heart(ctx, x, y, 0.6 * s); ctx.fill()
    ctx.restore()

# ---------------- library ----------------
def blink_cycle(t, period=2.8, off=0.0):
    d = (t + off) % period
    return 1 - abs(d - 0.08) / 0.08 if d < 0.16 else 0.0

def emotion(name, lt, t=None):
    """lt = seconds since the emotion started."""
    t = lt if t is None else t
    p = base_pose(); k = eo(lt / 0.25); p["blink"] = blink_cycle(t)
    if name == "neutro":
        p["look"] = (math.sin(t * 1.3) * 0.5, -0.3)
    elif name == "felice":
        p["eyeL"] = p["eyeR"] = "happy"; p["mouth"] = "grin"; p["brows"] = (0, 0, 2 * k)
        p["dy"] = -abs(math.sin(t * 6)) * 3
    elif name == "ridere":
        p["eyeL"] = p["eyeR"] = "happy"; p["mouth"] = "open_big"; p["brows"] = (0.2, 0.2, 2)
        p["dy"] = -abs(math.sin(t * 14)) * 3; p["tilt"] = -0.15 * k; p["handL"] = (22, 66)
        p["tear"] = (lt * 1.5) % 1
    elif name == "sorpreso":
        p["kL"] = 1 + 0.3 * back(lt / 0.3); p["kR"] = 1 + 0.7 * back(lt / 0.3); p["mouth"] = "o"
        p["brows"] = (0, 0, 4 * k); p["antenna"] = "stiff"; p["exclaim"] = clamp(lt / 0.3)
        p["dy"] = -math.sin(clamp(lt / 0.4) * math.pi) * 10; p["blink"] = 0
    elif name == "spaventato":
        p["kL"] = p["kR"] = 1.35; p["look"] = (0, 0); p["mouth"] = "wavy"; p["brows"] = (-0.35, -0.35, 4)
        p["sweat"] = k; p["dx"] = math.sin(t * 70) * 1.2 * k; p["sy"] = 1 - 0.08 * k; p["sx"] = 1 - 0.05 * k
        p["handL"] = (30, 62); p["handR"] = (64, 62); p["notebook"] = False; p["antenna"] = "stiff"; p["blink"] = 0
    elif name == "triste":
        p["eyeL"] = "open"; p["look"] = (0, 0.7); p["mouth"] = "frown"; p["brows"] = (-0.4, -0.4, 1)
        p["antenna"] = "droop"; p["tear"] = (lt * 0.7) % 1; p["dy"] = 3 * k; p["sy"] = 1 - 0.05 * k
        p["handL"] = (16, 80); p["handR"] = (76, 80); p["nb_angle"] = 0.4
    elif name == "confuso":
        p["look"] = (0.5, -0.7); p["mouth"] = "wavy"; p["brows"] = (0.3, 0.0, 0) ; p["question"] = clamp(lt / 0.3)
        p["tilt"] = 0.18 * k; p["kL"] = 1.1; p["kR"] = 0.8; p["handL"] = (10, 40)
    elif name == "capogiro":
        p["eyeL"] = p["eyeR"] = "spiral"; p["mouth"] = "wavy"; p["stars"] = k
        p["tilt"] = 0.16 * math.sin(t * 4); p["dx"] = 3 * math.sin(t * 4); p["antenna"] = "spin"
        p["handL"] = (12, 64 + 4 * math.sin(t * 4)); p["handR"] = (80, 64 - 4 * math.sin(t * 4))
    elif name == "arrabbiato":
        p["squint"] = 0.4; p["mouth"] = "grit"; p["brows"] = (0.45, 0.45, -2); p["steam"] = k
        p["dx"] = math.sin(t * 40) * 0.8; p["handL"] = (16, 70); p["handR"] = (76, 70)
    elif name == "innamorato":
        p["eyeL"] = p["eyeR"] = "heart"; p["mouth"] = "smile"; p["hearts"] = k; p["blush"] = k
        p["tilt"] = 0.08 * math.sin(t * 2); p["handL"] = (30, 66); p["handR"] = (62, 66); p["notebook"] = False
    elif name == "imbarazzato":
        p["look"] = (-0.8, 0.5); p["mouth"] = "wavy"; p["blush"] = k; p["brows"] = (-0.25, -0.25, 1)
        p["sweat"] = 0.8 * k; p["handL"] = (36, 58); p["handR"] = (56, 58); p["notebook"] = False; p["sy"] = 0.97
    elif name == "errore":
        p["eyeL"] = p["eyeR"] = "x"; p["mouth"] = "flat"; p["glitch"] = 1; p["antenna"] = "spark"
        p["tilt"] = math.sin(t * 50) * 0.04
    return p

def action(name, lt, t=None):
    t = lt if t is None else t
    p = base_pose(); p["blink"] = blink_cycle(t)
    if name == "saluta":
        p["mouth"] = "grin"; p["eyeL"] = p["eyeR"] = "happy"
        a = math.sin(t * 12); p["handL"] = (6 + 3 * a, 34); p["tilt"] = 0.05 * a
    elif name == "prende appunti":
        p["look"] = (0.8, 0.7); p["mouth"] = "flat"; p["handR"] = (68, 60); p["nb_angle"] = -0.4; p["pen"] = 1
        p["handL"] = (52, 66); p["brows"] = (0.15, 0, 0)
    elif name == "facepalm":
        k = eo(lt / 0.3); p["handL"] = (lerp(13, 36, k), lerp(74, 44, k)); p["mouth"] = "frown"
        p["eyeR"] = "closed"; p["tilt"] = 0.12 * k; p["dy"] = 2 * k; p["antenna"] = "droop"
    elif name == "spallucce":
        k = math.sin(clamp(lt / 0.6) * math.pi); p["handL"] = (6, 58 - 6 * k); p["handR"] = (86, 58 - 6 * k)
        p["mouth"] = "flat"; p["brows"] = (-0.3, -0.3, 3 * k); p["dy"] = -3 * k; p["look"] = (0.5, -0.5); p["notebook"] = False
    elif name == "indica":
        k = eo(lt / 0.25); p["handR"] = (lerp(77, 92, k), lerp(72, 40, k)); p["notebook"] = False
        p["look"] = (0.9, -0.6); p["mouth"] = "o"; p["brows"] = (0, 0, 3); p["exclaim"] = k
    elif name == "ma che vuoi":
        a = math.sin(t * 9); p["handR"] = (84, 46 + 4 * a); p["pinchR"] = True; p["notebook"] = False
        p["mouth"] = "flat"; p["brows"] = (0.35, 0.35, 0); p["squint"] = 0.25; p["tilt"] = -0.06
    elif name == "salta di gioia":
        ph = (lt * 2.2) % 1; j = math.sin(ph * math.pi)
        p["dy"] = -18 * j; p["sy"] = 1 - 0.12 * (1 - j) * (ph < 0.15 or ph > 0.85); p["sx"] = 2 - p["sy"]
        p["handL"] = (6, 30); p["handR"] = (86, 30); p["notebook"] = False
        p["eyeL"] = p["eyeR"] = "happy"; p["mouth"] = "open_big"; p["antenna"] = "spark"
    elif name == "trema":
        p["kL"] = p["kR"] = 1.3; p["mouth"] = "grit"; p["dx"] = math.sin(t * 80) * 1.5; p["sweat"] = 1
        p["handL"] = (32, 66); p["handR"] = (60, 66); p["notebook"] = False; p["sy"] = 0.93; p["blink"] = 0
        p["brows"] = (-0.35, -0.35, 4); p["look"] = (0, 0)
    elif name == "sviene":
        k = eio(lt / 0.8); p["tilt"] = 1.45 * k; p["dy"] = 6 * k; p["eyeL"] = p["eyeR"] = "x" if lt > 0.3 else "open"
        p["mouth"] = "o"; p["antenna"] = "droop"; p["handL"] = (lerp(13, 4, k), lerp(74, 50, k)); p["notebook"] = False
        p["stars"] = clamp((lt - 0.8) / 0.3)
    elif name == "applaude":
        a = abs(math.sin(t * 10)); p["handL"] = (40 - 6 * a, 70); p["handR"] = (52 + 6 * a, 70); p["notebook"] = False
        p["eyeL"] = p["eyeR"] = "happy"; p["mouth"] = "grin"; p["dy"] = -2 * a
    elif name == "idea":
        p["antenna"] = "spark"; p["kL"] = 1.15; p["kR"] = 1.3; p["mouth"] = "grin"; p["brows"] = (0, 0, 4)
        p["handL"] = (10, 36); p["look"] = (0, -0.9); p["exclaim"] = clamp(lt / 0.3)
    return p

EMOTIONS = ["neutro", "felice", "ridere", "sorpreso", "spaventato", "triste", "confuso", "capogiro",
            "arrabbiato", "innamorato", "imbarazzato", "errore"]
ACTIONS = ["saluta", "prende appunti", "facepalm", "spallucce", "indica", "ma che vuoi", "salta di gioia",
           "trema", "sviene", "applaude", "idea"]

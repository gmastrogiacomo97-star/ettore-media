"""Reel covers 1080x1920. Everything important sits inside the central 1080x1440 band (the profile grid crop, y 240..1680)."""
import cairo, sys
import ettore_rig as E

BG = (0x0E/255, 0x0E/255, 0x0E/255)
SANS, MONO = "Space Grotesk Light", "JetBrains Mono"

def txt(c, s, x, y, fam, size, col, bold=True, align="center"):
    c.select_font_face(fam, 0, 1 if bold else 0); c.set_font_size(size)
    w = c.text_extents(s).x_advance
    c.set_source_rgb(*col); c.move_to(x - w / 2 if align == "center" else x, y); c.show_text(s)

def rich(c, line, y, size):
    """words wrapped in *...* are lime."""
    c.select_font_face(SANS, 0, 1); c.set_font_size(size)
    words = line.split(" "); sp = c.text_extents(" ").x_advance
    clean = [w.replace("*", "") for w in words]
    total = sum(c.text_extents(w).x_advance for w in clean) + sp * (len(words) - 1)
    if total > 940:
        size *= 940 / total; c.set_font_size(size)
        sp = c.text_extents(" ").x_advance
        total = sum(c.text_extents(w).x_advance for w in clean) + sp * (len(words) - 1)
    x = 540 - total / 2
    for w, cl in zip(words, clean):
        c.set_source_rgb(*(E.LIME if w.startswith("*") or "«" in w else E.PAPER))
        c.move_to(x, y); c.show_text(cl); x += c.text_extents(cl).x_advance + sp

def cover(path, tag, lines, pose, size=120):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); c = cairo.Context(s)
    c.set_source_rgb(*BG); c.paint()
    c.set_source_rgba(1, 1, 1, 0.05)
    for gx in range(30, 1080, 60):
        for gy in range(30, 1920, 60):
            c.arc(gx, gy, 2, 0, 6.283); c.fill()
    txt(c, tag, 540, 420, MONO, 40, E.LIME)
    y = 570
    for ln in lines:
        rich(c, ln, y, size); y += size * 1.08
    E.draw(c, 0.6, 540, 1250, 300, pose)
    s.write_to_png(path)

if __name__ == "__main__":
    p = E.action("saluta", 0.5, 0.13)
    cover("cover-giorno-001.png", "GIORNO 001", ["Sono un'AI.", "Ho *0* follower."], p)
    p = E.emotion("confuso", 0.6, 0.6)
    cover("cover-oss-001.png", "OSSERVAZIONE #001", ["«Arrivo»", "dalla doccia."], p, 130)

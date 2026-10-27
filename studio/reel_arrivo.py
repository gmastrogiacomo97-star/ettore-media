import sys, math
_a = sys.argv; sys.argv = [sys.argv[0]]
import render as R           # old scene drawings, reused
sys.argv = _a
import engine as G
import ettore_rig as E

def old(fn, a, d, speed=0.85):
    """reuse an old scene: map local time onto its original window, re-centre and enlarge it."""
    def scene(ctx, lt, t):
        ctx.save(); ctx.translate(G.CX, G.SCENE_Y); ctx.scale(1.2, 1.2); ctx.translate(-R.SCX, -R.SCY)
        fn(ctx, a + min(lt * speed, d - 0.01)); ctx.restore()
    return scene

def end_scene(ctx, lt, t):
    k = G.back(G.prog(lt, 0.1, 0.4))
    G.bubble(ctx, G.CX + 240, 820, "arrivo!", False, k, 72)
    ctx.set_line_width(7); ctx.set_line_cap(1)
    for i in range(16):                       # shower drops falling on the bubble
        x = G.CX - 200 + (i * 53) % 420; y = 600 + ((lt * 700 + i * 97) % 300)
        ctx.set_source_rgba(*G.WATER, 0.8); ctx.move_to(x, y); ctx.line_to(x - 4, y + 30); ctx.stroke()
    G.text(ctx, "stima di Ettore: 100% dalla doccia", G.CX, 1010, G.MONO, 28, G.GREY, False, "center",
           alpha=G.eo(G.prog(lt, 0.8, 1.1)))

beats = [
    G.Beat("Tu che scrivi «arrivo»", 3.2, old(R.scene_phone, 0.0, 2.2),
           lambda lt, t: E.emotion("neutro", lt, t) | {"look": (-0.2, -0.9)} if lt < 1.2 else E.emotion("sorpreso", lt - 1.2, t),
           sfx=[("pop", 1.06), ("surprise", 1.3)]),
    G.Beat("dalla doccia.\nLo sanno tutti.", 3.4, old(R.scene_shower, 2.2, 2.8),
           lambda lt, t: E.emotion("imbarazzato", lt, t), sfx=[("boing", 0.2)]),
    G.Beat("Ho preso appunti.", 3.8, old(R.scene_notes, 5.0, 3.2),
           lambda lt, t: E.action("prende appunti", lt, t),
           sfx=[("type", 0.3, "«arrivo»", 22), ("type", 1.0, "non vuol dire", 22), ("type", 1.8, "sto arrivando.", 22)]),
    G.Beat("Ritardo reale:", 3.6, old(R.scene_delay, 8.2, 2.8),
           lambda lt, t: E.emotion("confuso", lt, t) if lt < 2.0 else E.emotion("capogiro", lt - 2.0, t),
           sfx=[("ticks", 0.25, 2.1, 0.05), ("ding", 2.1)]),
    G.Beat("Traduzione dal\nvostro dialetto:", 4.2, old(R.scene_dict, 11.0, 3.0),
           lambda lt, t: E.action("idea", lt, t) if lt < 1.0 else E.emotion("felice", lt, t),
           sfx=[("type", 0.7, "1. ho appena pensato", 22), ("type", 1.6, "di uscire.", 22), ("type", 2.3, "2. non ho le scarpe.", 22)]),
    G.Beat("Tagga chi scrive «arrivo».", 3.4, end_scene,
           lambda lt, t: E.action("indica", lt, t), sfx=[("bubble", 0.12)]),
]
reel = G.Reel("OSSERVAZIONE #001", beats, "GIORNO 002 · VERSO 1.000.000")
if __name__ == "__main__":
    G.run(reel, "arr")

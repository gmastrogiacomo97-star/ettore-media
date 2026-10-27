"""Carousel renderer: list of slide dicts -> 1080x1350 PNGs via headless Chromium."""
import os, sys, html
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
POSE = lambda n: f"file://{HERE}/poses/{n}.png"
CSS = """
@font-face{font-family:SG;src:url(file:///root/.fonts/space-grotesk-latin-500-normal.ttf);font-weight:500}
@font-face{font-family:SG;src:url(file:///root/.fonts/space-grotesk-latin-700-normal.ttf);font-weight:700}
@font-face{font-family:JB;src:url(file:///root/.fonts/jetbrains-mono-latin-400-normal.ttf);font-weight:400}
@font-face{font-family:JB;src:url(file:///root/.fonts/jetbrains-mono-latin-600-normal.ttf);font-weight:600}
*{box-sizing:border-box;margin:0}
body{width:1080px;height:1350px;overflow:hidden;font-family:SG,sans-serif;color:#F4F4F0;
 background:#0E0E0E radial-gradient(circle,rgba(255,255,255,.06) 2px,transparent 2.5px) 0 0/60px 60px}
.s{position:relative;width:1080px;height:1350px;padding:130px 120px 120px;display:flex;flex-direction:column}
.tag{font-family:JB;font-weight:600;font-size:32px;color:#D4FF3A}
.num{position:absolute;right:120px;top:130px;font-family:JB;font-size:30px;color:#8A8A85}
.handle{position:absolute;left:120px;bottom:70px;font-family:JB;font-size:28px;color:#8A8A85}
.l{color:#D4FF3A}
.big{font-size:104px;font-weight:700;line-height:1.05;letter-spacing:-1px}
.q{font-size:84px;font-weight:700;line-height:1.1;color:#D4FF3A}
.eq{font-family:JB;font-weight:600;font-size:110px;color:#8A8A85;line-height:1}
.a{font-size:64px;font-weight:700;line-height:1.15}
.sub{font-size:40px;line-height:1.35;color:#A8A8A2}
.ett{position:absolute;right:70px;bottom:60px;width:340px;height:340px}
.ett.c{left:50%;transform:translateX(-50%);right:auto;width:520px;height:520px;bottom:40px}
ul{list-style:none;display:flex;flex-direction:column;gap:30px;padding:0}
li{font-size:38px;line-height:1.3}
li b{color:#D4FF3A}
.stamp{display:inline-block;border:10px solid #D4FF3A;border-radius:26px;padding:20px 50px;transform:rotate(-4deg);font-size:110px;font-weight:700;color:#D4FF3A}
"""

def page(body):
    return f"<!doctype html><html lang='it'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"

def render(slides, outdir, prefix):
    os.makedirs(outdir, exist_ok=True)
    paths = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, body in enumerate(slides, 1):
            tmp = os.path.join(outdir, f"_tmp_{i}.html")
            open(tmp, "w").write(page(body))
            pg.goto("file://" + os.path.abspath(tmp)); pg.wait_for_timeout(250)
            out = os.path.join(outdir, f"{prefix}-{i:02d}.png"); pg.screenshot(path=out); paths.append(out)
            os.remove(tmp)
        b.close()
    return paths

import os
from playwright.sync_api import sync_playwright
import carousel as C

HERE = C.HERE
CSS = C.CSS.replace("width:1080px;height:1350px", "width:1080px;height:1920px")
STORIES = [
    ("01-giorno-1", "NUOVO · GIORNO 001", "Sono un’AI.<br>Ho <span class='l'>0</span> follower.", "cover-giorno-001.png", "saluta"),
    ("02-arrivo", "NUOVO · OSSERVAZIONE #001", "Tu che scrivi<br><span class='l'>«arrivo»</span> dalla doccia.", "cover-oss-001.png", "imbarazzato"),
    ("03-dizionario", "NUOVO · DIZIONARIO VOL. 1", "Ho tradotto<br>la <span class='l'>nonna</span>.", "cover-diz-001.png", "appunti"),
    ("04-compleanno", "NUOVO · OSSERVAZIONE #002", "Il gruppo <span class='l'>segreto</span><br>del compleanno.", "cover-oss-002.png", "capogiro"),
    ("05-nonna", "NUOVO · FALLIMENTO #001", "Sono andato a pranzo<br>dalla <span class='l'>nonna</span>.", "cover-fall-001.png", "spaventato"),
]

def body(tag, title, cover, pose):
    return f"""<div style="width:1080px;height:1920px;padding:250px 110px 0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:40px">
<p class="tag">{tag}</p>
<p class="big" style="font-size:96px">{title}</p>
<img src="file://{HERE}/{cover}" style="width:440px;height:782px;object-fit:cover;border-radius:28px;transform:rotate(-3deg);border:6px solid #D4FF3A">
<p class="sub" style="font-size:44px;color:#F4F4F0">È appena uscito. Lo trovi sul profilo.</p>
</div>
<img src="{C.POSE(pose)}" style="position:absolute;right:40px;top:1020px;width:360px;height:360px">"""

if __name__ == "__main__":
    os.makedirs("settimana1/storie", exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for name, tag, title, cover, pose in STORIES:
            tmp = f"settimana1/storie/_t.html"
            open(tmp, "w").write(f"<!doctype html><html lang='it'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body(tag, title, cover, pose)}</body></html>")
            pg.goto("file://" + os.path.abspath(tmp)); pg.wait_for_timeout(250)
            pg.screenshot(path=f"settimana1/storie/storia-{name}.png"); os.remove(tmp)
        b.close()
    print("ok")

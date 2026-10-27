import carousel as C
P = C.POSE
N = 9
H = "<p class='handle'>@ettore.ciprova</p>"
def num(i): return f"<p class='num'>{i}/{N}</p>"

ENTRIES = [
    ("«Non ho fatto niente di speciale.»", "Quattro portate e il dolce.", "sorpreso"),
    ("«Solo un assaggio.»", "Un piatto colmo. Due, se fai il bis.", "capogiro"),
    ("«Ne è rimasto un pochino.»", "Una teglia intera da portare a casa.", "spaventato"),
    ("«Mangia, che sei sciupato.»", "Hai appena finito il secondo piatto.", "confuso"),
    ("«Ti ho fatto due cose al volo.»", "Cucina dalle sette di mattina.", "imbarazzato"),
]

slides = []
slides.append(f"""<div class='s'><p class='tag'>DIZIONARIO UMANO–AI · VOL. 1</p>
<p class='big' style='margin-top:70px'>Il dizionario<br>della <span class='l'>nonna</span>.</p>
<p class='sub' style='margin-top:36px'>5 frasi tradotte da un’AI.<br>Scorri →</p>
<img class='ett c' src='{P("appunti")}'>{H}</div>""")
slides.append(f"""<div class='s'><p class='tag'>PREMESSA</p>{num(2)}
<p class='a' style='margin-top:90px'>La nonna parla italiano.</p>
<p class='a l' style='margin-top:24px'>Ma non quello del vocabolario.</p>
<p class='sub' style='margin-top:40px'>Ho provato a tradurla. Ecco cosa ho capito.</p>
<img class='ett' src='{P("confuso")}'>{H}</div>""")
for i, (q, a, pose) in enumerate(ENTRIES, 3):
    slides.append(f"""<div class='s'><p class='tag'>VOCE {i - 2}</p>{num(i)}
<p class='q' style='margin-top:90px'>{q}</p>
<p class='eq' style='margin-top:40px'>=</p>
<p class='a' style='margin-top:24px;max-width:760px'>{a}</p>
<img class='ett' src='{P(pose)}'>{H}</div>""")
items = "".join(f"<li><b>{q}</b><br>= {a}</li>" for q, a, _ in ENTRIES)
slides.append(f"""<div class='s'><p class='tag'>RIASSUNTO DA SALVARE</p>{num(8)}
<ul style='margin-top:60px'>{items}</ul>{H}</div>""")
slides.append(f"""<div class='s' style='align-items:center;text-align:center'>{num(9)}
<p class='a' style='margin-top:120px'>Quale frase della nonna<br>manca nel dizionario?</p>
<p class='sub' style='margin-top:30px'>Scrivila nei commenti:<br>le migliori finiscono nel Vol. 2.</p>
<p style='margin-top:80px'><span class='stamp'>Annotato.</span></p>
{H}</div>""")

if __name__ == "__main__":
    print(C.render(slides, "settimana1/03-dizionario-nonna", "dizionario-nonna"))

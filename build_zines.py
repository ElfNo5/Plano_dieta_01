#!/usr/bin/env python3
"""
Builds the 4 FREEZER FUEL zine fragments into ./zines/00X.html
Each fragment = SVG filter defs + a <div class="zine"> body.
The Streamlit app wraps them with <head> (fonts + base.css) at render time,
so downloads are fully self-contained. Re-run this after editing content.
"""
import os, html
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "zines")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- svg toolkit
DEFS = '''<svg class="fx" aria-hidden="true"><defs>
<filter id="wob"><feTurbulence type="turbulence" baseFrequency="0.013 0.02" numOctaves="3" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="6"/></filter>
<filter id="wob2"><feTurbulence type="turbulence" baseFrequency="0.02 0.03" numOctaves="3" seed="21" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>
<filter id="wob3"><feTurbulence type="turbulence" baseFrequency="0.016" numOctaves="3" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="7"/></filter>
</defs></svg>'''

# tiny hand-drawn doodles (bold ink stroke). color via currentColor.
def _svg(inner, vb="0 0 100 100"):
    return (f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round" style="width:100%;height:100%">{inner}</svg>')
DOODLE = {
 "egg":     _svg('<path d="M50 12c16 0 28 26 28 44a28 28 0 0 1-56 0c0-18 12-44 28-44Z"/>'),
 "drum":    _svg('<path d="M30 70 18 82"/><circle cx="24" cy="76" r="7"/><path d="M34 66c-12-12-8-34 8-42s34 4 38 18c3 10-3 16-10 15 3 8-3 15-12 15-8 0-16-3-24-6Z"/>'),
 "beef":    _svg('<path d="M22 40c-4-16 14-26 30-22 18 4 30 20 26 36-3 12-18 20-34 16C30 66 25 54 22 40Z"/><circle cx="46" cy="46" r="9"/>'),
 "liver":   _svg('<path d="M20 46c0-16 16-26 34-22 16 4 28 14 26 30-2 14-18 22-34 18-14-4-26-12-26-26Z"/><path d="M40 34c6 10 6 24 2 34"/>'),
 "flame":   _svg('<path d="M50 12c4 14-10 18-10 32 0 12 8 20 10 20s10-8 10-20c0-6-2-10-4-14 8 4 14 12 14 24a20 20 0 0 1-40 0c0-22 16-30 20-42Z"/>'),
 "leaf":    _svg('<path d="M26 74C22 42 46 22 78 22c2 30-18 54-52 52Z"/><path d="M40 60c10-10 20-16 30-20"/>'),
 "star":    _svg('<path d="M50 14 60 40l28 2-22 18 8 27-24-15-24 15 8-27-22-18 28-2Z"/>'),
 "snow":    _svg('<path d="M50 12v76M18 31l64 38M82 31 18 69M50 24l-9 9 9 9 9-9zM24 40l1 12 12 1M76 40l-1 12-12 1"/>'),
 "bolt":    _svg('<path d="M56 10 26 56h20l-8 34 34-50H50Z"/>'),
 "banana":  _svg('<path d="M20 40c6 30 34 44 62 34 4-2 4-8-1-8-24 6-44-8-49-30-2-6-14-2-12 4Z"/>'),
 "choco":   _svg('<rect x="24" y="24" width="52" height="52" rx="3"/><path d="M50 24v52M24 50h52"/>'),
 "pepper":  _svg('<path d="M62 30c8-14 20-14 20-14s-4 12-14 16"/><path d="M60 34c-16-6-34 4-38 22-3 14 8 26 22 24 16-2 26-16 24-34-1-6-3-9-8-12Z"/>'),
 "clock":   _svg('<circle cx="50" cy="52" r="34"/><path d="M50 34v18l12 8M50 12v6M32 16l3 6M68 16l-3 6"/>'),
 "arrowdn": _svg('<path d="M50 16v56M30 52l20 22 20-22"/>'),
 "whisk":   _svg('<path d="M40 20 66 78M52 22c14 6 20 22 14 40M60 20c10 10 12 26 4 44M46 20c8 4 12 14 12 26"/>'),
 "check":   _svg('<path d="M22 52l18 20 40-46"/>'),
 "spoon":   _svg('<ellipse cx="42" cy="30" rx="16" ry="20"/><path d="M46 48 60 84"/>'),
 "cup":     _svg('<path d="M26 34h44v20a22 22 0 0 1-44 0Z"/><path d="M70 38h10a8 8 0 0 1 0 16h-8"/><path d="M34 20c0 6-4 6-4 10M50 18c0 6-4 6-4 10"/>'),
}
def doodle(name, size=64, color="var(--ink)", cls="", style=""):
    return (f'<span class="{cls}" style="display:inline-block;width:{size}px;height:{size}px;'
            f'color:{color};{style}">{DOODLE[name]}</span>')

def esc(s): return html.escape(str(s))

# ------------------------------------------------------------- section pieces
def masthead(no, kicker, title_lines, tag, stats, band, title_color=None,
             stat_shapes=None):
    tc = f"color:{title_color};" if title_color else ""
    title_html = "<br>".join(f'<span>{esc(t)}</span>' for t in title_lines)
    shapes = stat_shapes or ["burst","burst blue","burst red","blob"]
    chips = ""
    for i,(num,lab) in enumerate(stats):
        sh = shapes[i % len(shapes)]
        rot = [-6,5,-3,7][i % 4]
        chips += (f'<div class="{sh}" style="width:150px;height:150px;transform:rotate({rot}deg)">'
                  f'<div style="width:80px;line-height:.9">'
                  f'<span class="stat" style="font-size:20px;display:block;white-space:nowrap">{esc(num)}</span>'
                  f'<span class="tag" style="font-size:8.5px">{esc(lab)}</span></div></div>')
    return f'''
<section class="band {band} slash-bot">
  <div class="dotfield" style="opacity:.10"></div>
  <div class="wrap center">
    <div class="stampbox t-r" style="margin-bottom:14px">ZINE Nº {esc(no)} · {esc(kicker)}</div>
    <h1 class="mega txt-sh" style="font-size:clamp(44px,10vw,94px);letter-spacing:-.015em;{tc}margin:.04em 0 .12em">{title_html}</h1>
    <p class="melt" style="font-size:clamp(19px,3.4vw,29px);max-width:640px;margin:0 auto;transform:rotate(-.6deg)">{tag}</p>
    <div class="row" style="justify-content:center;gap:18px;margin-top:32px">{chips}</div>
  </div>
</section>'''

def seclabel(text, sub=None, hl=True):
    inner = f'<span class="hl">{esc(text)}</span>' if hl else esc(text)
    s = f'<p class="kick" style="margin:0 0 6px">{esc(sub)}</p>' if sub else ""
    return f'<div style="margin:0 0 26px">{s}<h2 class="seclbl">{inner}</h2></div>'

MEAL_STYLES = [
  # (background, textcolor, shadowclass, tilt, accent)
  ("var(--cream)","var(--ink)","sh","t-l","var(--blue)"),
  ("var(--blue)","var(--cream)","sh-y","t-r","var(--yellow)"),
  ("var(--yellow)","var(--ink)","sh","t-l2","var(--red)"),
  ("var(--cream)","var(--ink)","sh-r","t-r2","var(--pink)"),
]
def meal_card(slot, name_pt, name_en, ings, kcal, prot, note, icon, i, sweet=False):
    bg,tc,sh,tilt,acc = MEAL_STYLES[i % 4]
    lis = "".join(f"<li>{esc(x)}</li>" for x in ings)
    slotfont = "var(--f-melt)" if sweet else "var(--f-cond)"
    namecls = "melt" if sweet else "cond"
    badge = ('<span class="chip pink" style="position:absolute;top:-14px;left:18px;transform:rotate(-4deg)">'
             'THE SWEET ONE ✦</span>') if sweet else ""
    return f'''
  <article class="card {sh} {tilt}" style="background:{bg};color:{tc};border-color:var(--ink)">
    {badge}
    <div style="position:absolute;top:14px;right:14px;width:60px;height:60px;color:{acc};opacity:.9">{DOODLE[icon]}</div>
    <p class="tag" style="color:{acc};margin:0 0 2px">{esc(slot)}</p>
    <h3 class="{namecls}" style="font-size:30px;line-height:1;margin:2px 0 0">{esc(name_en)}</h3>
    <p class="body" style="font-style:italic;opacity:.72;margin:2px 0 10px;font-size:15px">{esc(name_pt)}</p>
    <ul class="clean" style="margin-bottom:12px">{lis}</ul>
    <div class="row" style="gap:9px;margin:0 0 10px">
      <span class="chip" style="background:{acc};color:{'var(--cream)' if acc in ('var(--blue)','var(--red)') else 'var(--ink)'}">≈{esc(kcal)} kcal</span>
      <span class="chip">{esc(prot)} g protein</span>
    </div>
    <p style="font-size:15px;margin:0"><b>↳</b> {note}</p>
  </article>'''

def plates(title_sub, intro, meals, cols=2):
    cards = "".join(meal_card(**m, i=i) for i,m in enumerate(meals))
    return f'''
<section class="band paper2 slash-bot">
  <div class="wrap">
    {seclabel("THE 4 PLATES", sub=title_sub)}
    <p class="body" style="max-width:640px;margin:-10px 0 26px;font-size:18px">{intro}</p>
    <div class="grid{cols}">{cards}</div>
  </div>
</section>'''

def mixups(swaps):
    """swaps = list of (mealname, [alt,alt,alt]); rendered as scattered sticky chips."""
    cols = ["var(--yellow)","var(--pink)","var(--cream)","var(--blue)"]
    blocks = ""
    for j,(meal,alts) in enumerate(swaps):
        rot = [-2,2,-1.5,1.5][j%4]
        chiprow = ""
        for k,a in enumerate(alts):
            c = cols[k % len(cols)]
            fg = "var(--cream)" if c=="var(--blue)" else "var(--ink)"
            rr = [-3,2,-2,3][k%4]
            chiprow += (f'<span class="sticker" style="background:{c};color:{fg};transform:rotate({rr}deg);'
                        f'font-size:16px;margin:6px 8px 6px 0">{esc(a)}</span>')
        blocks += f'''
      <div style="transform:rotate({rot}deg);margin:0 0 22px">
        <h3 class="gothic" style="font-size:30px;color:var(--cream)">{esc(meal)}</h3>
        <div class="row" style="gap:0">{chiprow}</div>
      </div>'''
    return f'''
<section class="band navy slash-bot">
  <div class="dotfield" style="opacity:.08"></div>
  <div class="wrap">
    <div style="margin:0 0 22px"><p class="kick" style="color:var(--yellow)">stop eating the same thing</p>
      <h2 class="seclbl" style="color:var(--cream)"><span class="hl" style="background:var(--red);color:var(--cream)">MIX IT UP</span></h2></div>
    <p class="body" style="color:var(--cream);max-width:620px;margin:-8px 0 24px">
      Same macros, different plate. Swap any meal for one of these — all nut-free, all freeze-friendly. Rotate them so no two weeks taste alike.</p>
    {blocks}
  </div>
</section>'''

def sunday(steps, minutes):
    items = ""
    for i,(h,b) in enumerate(steps):
        rot = [-1.5,1.5,-1,1][i%4]
        arrow = ('<div style="width:52px;height:52px;color:var(--red);margin:0 auto -6px;transform:rotate('
                 f'{[0,180,0,180][i%4]}deg)">{DOODLE["arrowdn"]}</div>') if i>0 else ""
        items += f'''
    {arrow}
    <div class="card sh {'t-l' if i%2 else 't-r'}" style="max-width:720px;margin:0 auto;transform:rotate({rot}deg);display:flex;gap:18px;align-items:flex-start">
      <span class="mega" style="font-size:64px;color:var(--blue);line-height:.8">{i+1}</span>
      <div><h3 class="cond" style="font-size:24px;margin:2px 0 4px">{esc(h)}</h3>
      <p style="margin:0;font-size:16px">{b}</p></div>
    </div>'''
    return f'''
<section class="band yellow slash-bot">
  <div class="wrap">
    {seclabel("THE SUNDAY BATCH", sub=f"one session · ≈{minutes} min · the whole week done")}
    <div style="display:flex;flex-direction:column;gap:8px">{items}</div>
  </div>
</section>'''

def freeze(rules):
    tiles = ""
    ic = ["snow","choco","arrowdn","clock"]
    cols = ["var(--blue)","var(--red)","var(--yellow)","var(--cream)"]
    for i,(h,b) in enumerate(rules):
        c = cols[i%4]; fg = "var(--cream)" if c in("var(--blue)","var(--red)") else "var(--ink)"
        rot=[-3,2,-2,3][i%4]
        tiles += f'''
      <div class="panel {'sh' if fg=='var(--ink)' else 'sh'}" style="background:{c};color:{fg};transform:rotate({rot}deg)">
        <div style="width:46px;height:46px;margin-bottom:10px;color:{fg}">{DOODLE[ic[i%4]]}</div>
        <h4 class="cond" style="font-size:21px;margin:0 0 4px">{esc(h)}</h4>
        <p style="margin:0;font-size:15px">{b}</p>
      </div>'''
    return f'''
<section class="band paper2 slash-bot">
  <div class="wrap">
    {seclabel("FREEZE &amp; REHEAT", hl=True)}
    <div class="grid4" style="margin-top:6px">{tiles}</div>
  </div>
</section>'''

def shopping(total_line, cats, foot):
    blocks = ""
    for cat,items in cats:
        rows=""
        for name,detail,price in items:
            det = f'<span style="opacity:.62;font-size:14px"> · {esc(detail)}</span>' if detail else ""
            rows += f'''
        <label class="ff-item" style="display:flex;align-items:center;gap:12px;padding:9px 4px;cursor:pointer">
          <span class="ff-box" style="flex:0 0 auto;width:26px;height:26px;border:3px solid var(--ink);background:var(--cream)"></span>
          <span class="ff-name" style="flex:1;font-size:17px">{esc(name)}{det}</span>
          <span class="chip yellow" style="box-shadow:3px 3px 0 var(--ink)">{esc(price)}</span>
        </label>'''
        blocks += f'''
      <div style="margin:0 0 18px">
        <h3 class="gothic" style="font-size:26px;transform:rotate(-1.4deg);display:inline-block;
          background:var(--ink);color:var(--yellow);padding:2px 12px;box-shadow:5px 5px 0 var(--blue)">{esc(cat)}</h3>
        <div style="margin-top:10px">{rows}</div>
      </div>'''
    return f'''
<section class="band red slash-bot">
  <div class="wrap">
    <div style="margin:0 0 20px"><p class="kick">tap an item to cross it off</p>
      <h2 class="seclbl" style="color:var(--cream)"><span class="hl" style="background:var(--yellow)">★ MERCADO ★</span></h2></div>
    <div class="panel" style="background:var(--cream);color:var(--ink);border-width:4px;box-shadow:12px 12px 0 var(--ink)">
      <p class="cond" style="font-size:22px;margin:0 0 14px">{total_line}</p>
      {blocks}
      <div class="zig" style="margin:8px 0 14px"></div>
      <p style="margin:0;font-size:15px;opacity:.8">{foot}</p>
    </div>
  </div>
  <script>
    (function(){{
      document.querySelectorAll('.ff-item').forEach(function(el){{
        el.addEventListener('click',function(){{
          var on=el.getAttribute('data-on')==='1';
          el.setAttribute('data-on',on?'0':'1');
          var box=el.querySelector('.ff-box'), nm=el.querySelector('.ff-name');
          box.style.background=on?'var(--cream)':'var(--blue)';
          box.innerHTML=on?'':'<svg viewBox="0 0 100 100" style="width:100%;height:100%" fill="none" stroke="#fbf4e2" stroke-width="14" stroke-linecap="round"><path d="M20 52l18 22 42-48"/></svg>';
          nm.style.textDecoration=on?'none':'line-through';
          nm.style.opacity=on?'1':'.5';
        }});
      }});
    }})();
  </script>
</section>'''

def realtalk(text, band="navy"):
    return f'''
<section class="band {band}">
  <div class="wrap center">
    <div class="sticker t-l2" style="background:var(--yellow);font-size:15px;letter-spacing:.2em;padding:6px 14px">REAL TALK</div>
    <p class="melt" style="font-size:clamp(20px,3.6vw,30px);max-width:720px;margin:20px auto 0;color:var(--cream);line-height:1.25">{text}</p>
    <div style="width:60px;height:60px;margin:22px auto 0;color:var(--yellow)">{DOODLE["bolt"]}</div>
  </div>
</section>'''

def wrap_zine(sections):
    return DEFS + '<div class="zine">' + "".join(sections) + '</div>'

# ============================================================ ZINE 001
z001 = wrap_zine([
  masthead("001","freezer fuel",["FREEZER","FUEL"],
    "cook once on sunday → eat like a king all week. cheap, high-protein, sweet-tooth-approved.",
    [("1.5k","kcal/day"),("136g","protein"),("4","meals/day"),("R$166","/ week")],
    "band blue", stat_shapes=["burst","burst red","burst navy","blob"]),
  plates("same four every day — that's the trick",
    "Make a big batch of each on Sunday, portion, freeze. Weekday-you just reheats and eats.",
    [
      dict(slot="Meal 1 · Breakfast", name_en="EGG BAKE TRAY", name_pt="omelete de forno",
           ings=["4 eggs (ovos)","handful chopped repolho + cebola","20 g cheap cheese (muçarela / minas)","salt · pepper · garlic"],
           kcal="340", prot="29", icon="egg",
           note="Whisk → pour in a tray → bake 200 graus ~20 min → slice into 7. The crusty cheese edge is the flavour bomb."),
      dict(slot="Meal 2 · Lunch", name_en="SHREDDED CHICKEN", name_pt="frango desfiado com legumes",
           ings=["170 g cooked chicken breast (peito)","cabbage + carrot + onion","1 tsp oil · paprika · garlic"],
           kcal="370", prot="52", icon="drum",
           note="Pressure-cook the breast, shred with two forks, sauté with the veg. A pressure cooker is your best friend."),
      dict(slot="Meal 3 · Dinner", name_en="BEEF &amp; CABBAGE SKILLET", name_pt="carne moída com repolho",
           ings=["120 g cheap ground beef (carne moída de 2ª)","shredded cabbage + 1 egg to bind","tomato · onion · 1 tsp oil"],
           kcal="340", prot="30", icon="beef",
           note="Brown the beef, wilt the cabbage, fold a beaten egg in to bind. No beef? → 2 eggs + cheese, or leftover chicken."),
      dict(slot="Meal 4 · The Sweet One", name_en="CHOCO-BANANA BAKE", name_pt="bolo proteico de chocolate",
           ings=["2 eggs + 1 banana","40 g powdered milk (leite em pó)","20 g cocoa + 20 g oats (aveia)","sweetener + pinch of fermento"],
           kcal="330", prot="25", icon="choco", sweet=True,
           note="Blend everything → bake 180 graus ~18 min → slice into 7. Dessert that loves you back."),
    ]),
  mixups([
    ("Breakfast", ["Egg bake tray","Ham + egg muffins","Oat-banana protein pancakes","Savoury omelette rolls"]),
    ("Lunch", ["Shredded chicken","Chicken meatballs","Frango à parmegiana lite","Chicken & cabbage bowl"]),
    ("Dinner", ["Beef & cabbage skillet","Cheap picadinho + veg","Egg & cheese quiche muffins","Chicken drumstick + roast veg"]),
    ("The sweet one", ["Choco-banana bake","Banana-cinnamon pudim","Cocoa pudim","Oat-banana cookies"]),
  ]),
  sunday([
    ("Cook all the chicken","Pressure-cook the full 1.3 kg of breast (~25 min), then shred while the oven preheats."),
    ("Oven does double duty","Bake the egg tray and the choco-banana bake at the same time — different trays, same heat."),
    ("One big cabbage base","Sauté a giant batch of cabbage + onion. Split it: half with beef (dinner), the rest stays loose for lunch."),
    ("Portion into 28 + freeze","7 of each meal, flat containers, labelled by day. Fridge 2 days, freeze the other 5. Done till next Sunday."),
  ], minutes=90),
  freeze([
    ("Cool first","Let everything cool fully before it hits the freezer — warm food makes ice crystals and soggy meals."),
    ("Freeze flat","Single portions, packed flat. They stack better and thaw way faster than a frozen brick."),
    ("Thaw ahead","Move tomorrow's meals to the fridge tonight, or microwave from frozen 3–4 min, stirring halfway."),
    ("~1 month","Eat within about a month frozen. Cover the egg bake with a damp paper towel so it doesn't dry out."),
  ]),
  shopping("★ full 7 days · ≈ R$166 total · ~R$24 / day",
    [
      ("PROTEINS",[
        ("Ovos","≈ 4 dúzias (49 un)","R$45"),
        ("Peito de frango","1,3 kg · sobrecoxa = cheaper","R$24"),
        ("Carne moída de 2ª","≈ 900 g · patinho/acém em promo","R$22"),
      ]),
      ("PRODUCE",[
        ("Repolho","1 cabeça grande","R$6"),("Cenoura","500 g","R$3"),
        ("Cebola","700 g","R$4"),("Tomate","500 g","R$4"),("Banana","8 un (≈1 kg)","R$5"),
      ]),
      ("PANTRY",[
        ("Cacau em pó","100 g","R$10"),("Leite em pó","300 g","R$18"),
        ("Aveia","200 g","R$5"),("Queijo barato","muçarela ou minas · 150 g","R$8"),
        ("Óleo · sal · alho · temperos","básicos + adoçante + fermento","R$12"),
      ]),
    ],
    "Rough small-city estimates — they'll swing with the season and your market. No fish, no nuts, all freezer-friendly."),
  realtalk("1,500 kcal is a lean, steady cut. Eat all four plates, keep the water up, lift heavy — the abs show up in the kitchen, not the gym.",
    band="blue"),
])
open(os.path.join(OUT,"001.html"),"w").write(z001)

# ============================================================ ZINE 002
z002 = wrap_zine([
  masthead("002","the broke edition",["DIRT CHEAP","DELUXE"],
    "soy-meat, eggs &amp; liver doing all the heavy lifting. same protein, half the price — still a sweet at the end.",
    [("1.5k","kcal/day"),("132g","protein"),("0","nuts"),("R$121","/ week")],
    "band red", stat_shapes=["burst blue","burst","burst navy","blob"]),
  plates("four cheap, filling plates a day",
    "The whole week runs on soy protein (PTS), eggs, chicken liver and a little powdered milk. Chicken breast is out — PTS + liver are in, for about R$60 less a week.",
    [
      dict(slot="Meal 1 · Breakfast", name_en="SOY + EGG SCRAMBLE", name_pt="ovos mexidos com PTS",
           ings=["3 eggs (ovos)","35 g dry PTS, rehydrated","onion + tomato + 1 tsp oil","garlic · salt · pepper"],
           kcal="370", prot="35", icon="egg",
           note="Soak the PTS in hot water 10 min, squeeze dry, scramble right into the eggs. Soak in stock = way more flavour."),
      dict(slot="Meal 2 · Lunch", name_en='SOY "GROUND BEEF"', name_pt="PTS temperada com legumes",
           ings=["60 g dry PTS, rehydrated","1 egg (to bind + protein)","tomato · onion · cabbage · carrot","1 tsp oil · paprika · cumin"],
           kcal="310", prot="36", icon="pepper",
           note="Cook it exactly like carne moída — brown the onion, add drained PTS, tomato, simmer. Tastes like meat sauce, costs like nothing."),
      dict(slot="Meal 3 · Dinner", name_en="LIVER &amp; ONIONS", name_pt="fígado de frango acebolado",
           ings=["200 g chicken liver (fígado)","lots of onion + abobrinha / chuchu","1 tsp oil · garlic · bay leaf"],
           kcal="270", prot="36", icon="liver",
           note="Sear the liver hot &amp; fast so it stays tender, pile on soft onions. Iron-packed, insanely cheap. Not into liver? → swap for coxa/sobrecoxa."),
      dict(slot="Meal 4 · The Sweet One", name_en="BANANA-CINNAMON PUDIM", name_pt="pudim proteico de banana",
           ings=["2 eggs + ½ banana","45 g powdered milk (leite em pó)","cinnamon (canela) + sweetener"],
           kcal="360", prot="25", icon="banana", sweet=True,
           note="Blend, pour into cups, water-bath bake 180 graus ~25 min. Sets like a flan — cheap dessert, real protein, zero nuts."),
    ]),
  mixups([
    ("Breakfast", ["Soy + egg scramble","Egg & tomato bake","PTS breakfast hash","Cheesy egg cups"]),
    ("Lunch", ['Soy "ground beef"',"PTS chili","Soy & egg picadinho","PTS-stuffed cabbage"]),
    ("Dinner", ["Liver & onions","Coxa/sobrecoxa acebolada","PTS stroganoff","Liver & tomato ragu"]),
    ("The sweet one", ["Banana-cinnamon pudim","Cocoa pudim","Coffee pudim","Milk-powder brigadeiro cups"]),
  ]),
  sunday([
    ("Soak all the PTS","Cover the full week's soy protein in hot water (or stock) for 10 min, then squeeze it dry. Do this first so it's ready."),
    ("Two PTS pans","One scramble base for breakfast, one 'ground beef' tomato base for lunch. Season them differently."),
    ("Sear the liver","Hot pan, quick sear, then a mountain of soft onions. Don't overcook it or it turns rubbery."),
    ("Bake the pudins + portion","Water-bath bake while everything cools. Portion 28, freeze flat, labelled by day."),
  ], minutes=75),
  freeze([
    ("Cool first","Fully cool everything before freezing — the liver especially hates a slow refreeze."),
    ("Flat packs","Single portions, flat. PTS reheats perfectly; it soaked up all that sauce."),
    ("Thaw ahead","Fridge overnight, or microwave from frozen ~3 min. Liver: reheat gently, don't nuke it dry."),
    ("~1 month","Eat within a month. Pudins thaw sweetest in the fridge overnight."),
  ]),
  shopping("★ full 7 days · ≈ R$121 total · ~R$4 / meal",
    [
      ("PROTEINS",[
        ("Proteína de soja (PTS)","700 g · the MVP","R$14"),
        ("Ovos","≈ 3½ dúzias (42 un)","R$38"),
        ("Fígado de frango","1,4 kg · dirt cheap","R$14"),
      ]),
      ("PRODUCE",[
        ("Cebola","1 kg · you'll use a lot","R$6"),("Tomate","600 g","R$5"),
        ("Repolho + cenoura","1 cabeça + 400 g","R$8"),("Abobrinha ou chuchu","500 g","R$4"),
        ("Banana","4 un","R$3"),
      ]),
      ("PANTRY",[
        ("Leite em pó","300 g","R$18"),("Canela + cacau","para os pudins","R$8"),
        ("Óleo · alho · louro · temperos","básicos + adoçante","R$3"),
      ]),
    ],
    "Rough small-city prices — they move with the season. Nut-free and fish-free from top to bottom."),
  realtalk("Cheap food isn't punishment food. Season the PTS like you mean it, keep a sweet at the end of every day, and this is a week you'll actually repeat.",
    band="navy"),
])
open(os.path.join(OUT,"002.html"),"w").write(z002)

# ============================================================ ZINE 003
z003 = wrap_zine([
  masthead("003","the lean cut",["GRIT"],
    "1,300 kcal, 132 g protein, dirt cheap. lean protein, big piles of veg for volume, almost no added fat.",
    [("1.3k","kcal/day"),("132g","protein"),("0","nuts"),("R$127","/ week")],
    "band navy", title_color="var(--yellow)", stat_shapes=["burst","burst blue","burst red","blob"]),
  realtalk("1,300 is an aggressive cut and you'll feel it. Eat all four meals, drink water, and treat this as a short lean stretch — not forever.",
    band="red"),
  plates("lean protein does the whole job",
    "Chicken breast, soy protein and eggs, almost no added fat, big piles of veg for volume. Cooked once Sunday, frozen, done. Nut-free top to bottom.",
    [
      dict(slot="Meal 1 · Breakfast", name_en="EGG + SOY SCRAMBLE", name_pt="ovos mexidos com PTS",
           ings=["2 eggs (ovos)","45 g dry PTS, rehydrated","onion + tomato, barely any oil","garlic · salt · pepper"],
           kcal="270", prot="35", icon="egg",
           note="Soak PTS in hot stock 10 min, squeeze dry, scramble straight into the eggs. The stock makes it taste like more than it costs."),
      dict(slot="Meal 2 · Lunch", name_en="CHICKEN &amp; GREENS", name_pt="peito de frango com verdura",
           ings=["150 g cooked chicken breast","big pile of cabbage + greens","½ tsp oil · paprika · garlic"],
           kcal="290", prot="46", icon="leaf",
           note="The leanest cheap protein there is — shred it into the greens so it stays juicy. Volume is your friend on a lean day."),
      dict(slot="Meal 3 · Dinner", name_en="SOY CHILI BOWL", name_pt="chili de proteína de soja",
           ings=["55 g dry PTS, rehydrated","tomato · onion · cabbage","cumin · paprika · ½ tsp oil"],
           kcal="190", prot="27", icon="pepper",
           note="Cook it like a chili minus the beans — keeps carbs down. Make it properly spicy so a lean week never gets boring."),
      dict(slot="Meal 4 · The Sweet One", name_en="COCOA PUDIM", name_pt="pudim proteico de cacau",
           ings=["2 eggs + ½ banana","40 g skim milk powder (desnatado)","cocoa (cacau) + sweetener"],
           kcal="290", prot="26", icon="cup", sweet=True,
           note="Blend, pour into cups, water-bath bake 180 graus ~25 min. Chocolate that actually fits inside 1,300. No nuts, all protein."),
    ]),
  mixups([
    ("Breakfast", ["Egg + soy scramble","Egg-white veggie bake","Cottage-cheese egg cups","Tomato shakshuka lite"]),
    ("Lunch", ["Chicken & greens","Chicken zucchini bowl","Shredded chicken salad","Chicken & cabbage stir-fry"]),
    ("Dinner", ["Soy chili bowl","Soy & tomato stew","PTS lettuce wraps","Spicy soy & pepper skillet"]),
    ("The sweet one", ["Cocoa pudim","Cinnamon pudim","Coffee gelatina","Cocoa-banana mug bake"]),
  ]),
  sunday([
    ("Soak the PTS","Cover the full week's soy protein in hot stock, 10 min, squeeze dry. First job, so it's ready when you need it."),
    ("Cook the chicken","Pressure-cook or poach the 1.3 kg of breast, shred it. Keep it moist — lean meat dries out fast."),
    ("Two soy pans","One scramble base, one spicy chili base. Season them apart so the week doesn't taste identical."),
    ("Bake the pudins + portion","Water-bath bake while everything cools. 28 servings, flat, labelled by day."),
  ], minutes=75),
  freeze([
    ("Cool first","Fully cool before freezing so nothing turns to slush."),
    ("Flat packs","Single portions, flat. Faster thaw, easier stack."),
    ("Thaw ahead","Fridge overnight, or microwave from frozen ~3 min. Reheat lean chicken gently so it doesn't dry out."),
    ("~1 month","Eat within a month. Pudins thaw sweetest overnight in the fridge."),
  ]),
  shopping("★ full 7 days · ≈ R$127 total · ~R$4.50 / meal",
    [
      ("PROTEIN",[
        ("Peito de frango","1,3 kg · lean workhorse","R$22"),
        ("Proteína de soja (PTS)","700 g","R$14"),
        ("Ovos","≈ 2½ dúzias (28 un)","R$25"),
      ]),
      ("PRODUCE",[
        ("Repolho + verduras","1 cabeça + 1 maço","R$7"),("Cebola","700 g","R$4"),
        ("Tomate","500 g","R$4"),("Cenoura","400 g","R$3"),("Banana","4 un","R$3"),
      ]),
      ("PANTRY",[
        ("Leite em pó desnatado","300 g · keeps the pudim lean","R$20"),
        ("Cacau em pó","100 g","R$10"),
        ("Óleo · alho · temperos · adoçante","basics","R$12"),
      ]),
    ],
    "Rough small-city prices. Strip it further: cinnamon over cocoa, full-fat milk powder if it's cheaper that week."),
  realtalk("Aggressive cuts work in short bursts, not marathons. Run this a few weeks, then step back up. If you feel wrecked, eat more — see a nutritionist before you push it.",
    band="navy"),
])
open(os.path.join(OUT,"003.html"),"w").write(z003)

# ============================================================ ZINE 004  (NEW — the variety one)
def weekgrid(days):
    cells=""
    cols=["var(--blue)","var(--red)","var(--yellow)","var(--pink)","var(--cream)","var(--blue)","var(--red)"]
    for i,(day,dinner,sweet) in enumerate(days):
        c=cols[i%len(cols)]; fg="var(--cream)" if c in("var(--blue)","var(--red)") else "var(--ink)"
        rot=[-2,1.5,-1,2,-1.5,1,-2][i%7]
        cells+=f'''
      <div class="panel sh" style="background:{c};color:{fg};transform:rotate({rot}deg)">
        <p class="tag" style="margin:0 0 6px;font-size:12px">{esc(day)}</p>
        <h4 class="cond" style="font-size:20px;line-height:1.05;margin:0 0 6px">{esc(dinner)}</h4>
        <p class="melt" style="margin:0;font-size:16px;opacity:.9">↳ {esc(sweet)}</p>
      </div>'''
    return f'''
<section class="band paper2 slash-bot">
  <div class="wrap">
    {seclabel("7 NIGHTS, 7 DINNERS", sub="a different plate every single day")}
    <p class="body" style="max-width:640px;margin:-10px 0 24px">Breakfast &amp; lunch stay easy (pick from the pools below). The <b>dinner + sweet</b> rotate all week so nothing repeats.</p>
    <div class="grid4" style="gap:16px">{cells}</div>
  </div>
</section>'''

def pools(title, groups):
    blocks=""
    for name,icon,opts in groups:
        chips="".join(
          f'<span class="sticker" style="transform:rotate({[-2,2,-1,1][k%4]}deg);margin:6px 8px 6px 0;font-size:16px;'
          f'background:{["var(--yellow)","var(--cream)","var(--pink)","var(--blue)"][k%4]};'
          f'color:{"var(--cream)" if ["var(--yellow)","var(--cream)","var(--pink)","var(--blue)"][k%4]=="var(--blue)" else "var(--ink)"}">{esc(o)}</span>'
          for k,o in enumerate(opts))
        blocks+=f'''
      <div class="card sh t-l" style="margin:0 0 22px">
        <div style="position:absolute;top:14px;right:14px;width:52px;height:52px;color:var(--blue)">{DOODLE[icon]}</div>
        <h3 class="gothic" style="font-size:26px">{esc(name)}</h3>
        <div class="row" style="gap:0;margin-top:8px">{chips}</div>
      </div>'''
    return f'''
<section class="band blue slash-bot">
  <div class="dotfield" style="opacity:.08"></div>
  <div class="wrap">
    <div style="margin:0 0 22px"><p class="kick" style="color:var(--yellow)">{esc(title)}</p>
      <h2 class="seclbl" style="color:var(--cream)"><span class="hl" style="background:var(--yellow)">BUILD YOUR DAY</span></h2></div>
    {blocks}
  </div>
</section>'''

z004 = wrap_zine([
  masthead("004","no-repeat mode",["SEM","REPETIR"],
    "the anti-boredom plan. rotate a different dinner &amp; dessert every night — same cheap shopping list, zero monotony.",
    [("~1.5k","kcal/day"),("~130g","protein"),("7","dinners"),("0","nuts"),],
    "band navy", title_color="var(--pink)", stat_shapes=["burst pink","burst","burst blue","blob"]),
  weekgrid([
    ("SEG","Beef & cabbage skillet","Choco-banana bake"),
    ("TER","Liver & onions","Banana-cinnamon pudim"),
    ("QUA","Soy chili bowl","Cocoa pudim"),
    ("QUI","Chicken & peppers (xadrez)","Oat-banana cookies"),
    ("SEX","Egg & cheese quiche muffins","Coffee pudim"),
    ("SÁB","Soy stroganoff (PTS)","Brigadeiro de leite em pó"),
    ("DOM","Drumstick + roast veg","Cocoa-banana mug bake"),
  ]),
  pools("mix & match, all freeze-friendly", [
    ("BREAKFAST","egg", ["Egg bake tray","Soy + egg scramble","Oat-banana pancakes","Ham & egg muffins"]),
    ("LUNCH","drum", ["Shredded chicken + veg",'Soy "ground beef"',"Chicken & greens","Chicken meatballs"]),
  ]),
  mixups([
    ("Swap a dinner", ["Beef & cabbage","Liver & onions","Soy chili","Chicken & peppers","Quiche muffins","Soy stroganoff","Drumstick + veg"]),
    ("Swap a sweet", ["Choco-banana bake","Banana-cinnamon pudim","Cocoa pudim","Oat-banana cookies","Coffee pudim","Brigadeiro cups"]),
  ]),
  sunday([
    ("Cook the two big proteins","Pressure-cook the chicken and brown the beef. Shred / portion both while the oven runs."),
    ("Soak PTS, sear liver","Soy protein for chili &amp; stroganoff soaks in stock; sear the liver hot and fast, then onions."),
    ("Oven runs the sweets","Egg muffins, quiche muffins and the week's pudins/bakes go in together — same heat, different trays."),
    ("Label by NIGHT, not just meal","Because dinners differ, write the weekday on each dinner pack so future-you grabs the right one."),
  ], minutes=110),
  freeze([
    ("Cool first","Everything fully cool before freezing — a rotating week means more variety to keep straight, so label hard."),
    ("Flat packs","Single portions, flat. Group by weekday if you want to just grab-and-go."),
    ("Thaw ahead","Fridge overnight is best for the rotation — pull tomorrow's dinner + sweet the night before."),
    ("~1 month","Everything keeps ~a month. Cookies and bakes thaw fastest; pudins thaw sweetest overnight."),
  ]),
  shopping("★ full 7 days · ≈ R$180 total · the variety tax is tiny",
    [
      ("PROTEINS",[
        ("Ovos","≈ 4 dúzias","R$45"),
        ("Peito + coxa de frango","1,4 kg misto","R$26"),
        ("Carne moída de 2ª","500 g","R$12"),
        ("Fígado de frango","400 g","R$4"),
        ("Proteína de soja (PTS)","500 g","R$10"),
      ]),
      ("PRODUCE",[
        ("Repolho + verduras","1 cabeça + 1 maço","R$8"),("Pimentão + cebola","500 g + 700 g","R$9"),
        ("Tomate","600 g","R$5"),("Cenoura + abobrinha","600 g","R$6"),("Banana","10 un","R$6"),
      ]),
      ("PANTRY",[
        ("Leite em pó","400 g","R$22"),("Cacau + café + canela","para a rotação de doces","R$14"),
        ("Aveia","250 g","R$6"),("Queijo barato","200 g","R$10"),
        ("Óleo · alho · temperos · adoçante","básicos","R$12"),
      ]),
    ],
    "One shopping list, seven different nights. Rough small-city prices — fish-free, nut-free, boredom-free."),
  realtalk("Variety is the reason people actually finish a cut. If eating the same four plates was breaking you, this is your plan — rotate, freeze, repeat the week (never the day).",
    band="red"),
])
open(os.path.join(OUT,"004.html"),"w").write(z004)

print("built:", sorted(os.listdir(OUT)))
for f in sorted(os.listdir(OUT)):
    print(f, os.path.getsize(os.path.join(OUT,f)), "bytes")

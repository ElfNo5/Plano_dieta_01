# FREEZER FUEL · meal-prep zines

Four 7-day meal-prep zines in a grunge / neo-brutalist style, served by a small
Streamlit app. Every zine is high-protein, freeze-friendly, dirt cheap — and
**nut-free & sardine-free** top to bottom.

## The four plans

| # | Zine | Base | kcal/day | ~Cost/week |
|---|------|------|----------|-----------|
| 001 | Freezer Fuel | chicken · ground beef · eggs | 1,500 | R$166 |
| 002 | Dirt Cheap Deluxe | soy protein (PTS) · liver · eggs | 1,450 | R$121 |
| 003 | GRIT (lean cut) | chicken · soy · eggs | 1,300 | R$127 |
| 004 | Sem Repetir (no-repeat) | 7 rotating dinners + 7 sweets | ~1,500 | ~R$180 |

Every zine also has a **MIX IT UP** section with drop-in swaps, so no two weeks
have to taste the same. 004 goes further: a different dinner and dessert every
night of the week, plus breakfast/lunch pools you assemble yourself.

> Note: 003 (GRIT) is an aggressive 1,300 kcal cut — eat all four meals, keep
> water up, and treat it as a short stretch, not a lifestyle.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

Push this whole folder to a GitHub repo and point Streamlit Cloud at
`streamlit_app.py`. No secrets, no extra config — the app only reads local
files.

## How it's put together

```
streamlit_app.py    app: zine picker, inline render, .html download
build_zines.py      generator — edit meal data here, run to regenerate zines/
_preview.py         writes standalone preview HTML (same composition as the app)
assets/base.css     shared neo-brutalist design system
zines/00X.html      generated zine bodies (HTML fragments)
fonts/              the 7 provided fonts + their licenses
```

At run time the app inlines all seven fonts as base64 `@font-face` rules and
prepends the shared CSS, so the **downloaded .html files are fully
self-contained** — they work offline, no font files needed.

One quirk handled for you: Courbe Sans ships *empty* glyphs for `—`, `–`, `•`
and `·`, so a supplemental `@font-face` with a `unicode-range` serves just
those four codepoints from Comangs (also a provided font). Only the seven
provided fonts are ever used.

### Design system (rules.txt)

- Vibrant blue / yellow / red palette on aged paper, grain + xerox noise
- Sharp offset shadows only — no soft shadows anywhere
- Every section has its own layout: starburst stat badges, tilted cards,
  torn-edge panels, week grids, checklists — not a "document"
- No ruled lines inside writing areas; clean diamond bullets instead
- Grunge section labels (Violent Brave) + heavy mastheads (Superglue)
- Hand-drawn SVG doodles throughout

### Editing the meal plans

All meal data lives as plain Python structures in `build_zines.py`. Change
what you want, then:

```bash
python3 build_zines.py
```

and the zines regenerate. The app picks them up on next reload.

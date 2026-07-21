import base64
import pathlib

import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# FREEZER FUEL · meal-prep zines
# Neo-brutalist / grunge redesign. Fonts, CSS and zine bodies live as real
# files next to this script, so the whole thing launches on Streamlit as-is.
# Each zine is composed at run time: base64 @font-face + shared CSS + body,
# which also makes every downloaded .html fully self-contained.
# ---------------------------------------------------------------------------
ROOT   = pathlib.Path(__file__).parent
FONTS  = ROOT / "fonts"
ASSETS = ROOT / "assets"
ZINES_DIR = ROOT / "zines"

st.set_page_config(
    page_title="Freezer Fuel · Meal-Prep Zines",
    page_icon="🥩",
    layout="wide",
)

# --- zine registry --------------------------------------------------------
ZINES = {
    "001": {"label": "001 · Freezer Fuel",
            "blurb": "Chicken · beef · eggs — 1,500 kcal · ~R$166/wk",
            "file": "freezer-fuel-001.html", "src": "001.html", "height": 5650},
    "002": {"label": "002 · Dirt Cheap Deluxe",
            "blurb": "Soy protein · liver · eggs — 1,450 kcal · ~R$121/wk",
            "file": "freezer-fuel-002.html", "src": "002.html", "height": 5500},
    "003": {"label": "003 · GRIT (lean cut)",
            "blurb": "Chicken · soy · eggs — 1,300 kcal · ~R$127/wk",
            "file": "freezer-fuel-003.html", "src": "003.html", "height": 5750},
    "004": {"label": "004 · Sem Repetir (no-repeat)",
            "blurb": "7 rotating dinners — ~1,500 kcal · ~R$180/wk",
            "file": "freezer-fuel-004.html", "src": "004.html", "height": 5650},
}
ORDER = ["001", "002", "003", "004"]

# --- fonts: build one shared @font-face block (base64, cached) -------------
FONT_FACES = [
    # (css family name, filename, format)
    ("Superglue",     "Superglue.otf",     "opentype"),
    ("Courbe Sans",   "CourbeSans.ttf",    "truetype"),
    ("Violent Brave", "ViolentBrave.ttf",  "truetype"),
    ("Comangs",       "Comangs.ttf",       "truetype"),
    ("Messy Melted",  "MessyMelted.ttf",   "truetype"),
    ("Cyasren",       "Cyasren.otf",       "opentype"),
    ("Ophium",        "Ophium.ttf",        "truetype"),
]

@st.cache_data(show_spinner=False)
def build_fontface_css() -> str:
    css = []
    b64_by_family = {}
    for family, fname, fmt in FONT_FACES:
        data = (FONTS / fname).read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        b64_by_family[family] = b64
        css.append(
            f"@font-face{{font-family:'{family}';font-style:normal;font-weight:400;"
            f"font-display:swap;src:url(data:font/{'otf' if fmt=='opentype' else 'ttf'};"
            f"base64,{b64}) format('{fmt}');}}"
        )
    # Courbe Sans ships empty glyphs for em/en-dash, bullet and middot, so they
    # render blank. Serve just those codepoints from Comangs (a provided font
    # that has real outlines) under the same family name — no copy edits needed.
    css.append(
        "@font-face{font-family:'Courbe Sans';font-display:swap;"
        f"src:url(data:font/ttf;base64,{b64_by_family['Comangs']}) format('truetype');"
        "unicode-range:U+2013,U+2014,U+2022,U+00B7;}"
    )
    return "\n".join(css)

@st.cache_data(show_spinner=False)
def load_base_css() -> str:
    return (ASSETS / "base.css").read_text(encoding="utf-8")

@st.cache_data(show_spinner=False)
def load_zine_body(src: str) -> str:
    return (ZINES_DIR / src).read_text(encoding="utf-8")

def compose(zine_key: str) -> str:
    """Full standalone HTML document for a zine (used to render AND to download)."""
    body = load_zine_body(ZINES[zine_key]["src"])
    return (
        "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
        f"<title>FREEZER FUEL — {ZINES[zine_key]['label']}</title>"
        f"<style>{build_fontface_css()}</style>"
        f"<style>{load_base_css()}</style>"
        "</head><body>"
        f"{body}"
        "</body></html>"
    )

# --- startup check: fail with a clear message if repo files are missing ----
_required = (
    [ASSETS / "base.css"]
    + [ZINES_DIR / z["src"] for z in ZINES.values()]
    + [FONTS / fname for _, fname, _ in FONT_FACES]
)
_missing = [p for p in _required if not p.exists()]
if _missing:
    st.error(
        "**Arquivos faltando no deploy** — o app precisa das pastas "
        "`zines/`, `assets/` e `fonts/` junto com o `streamlit_app.py` "
        "no repositório:\n\n"
        + "\n".join(f"- `{p.relative_to(ROOT)}`" for p in _missing)
    )
    st.stop()

# --- trim Streamlit chrome so the zine sits near full-bleed ---------------
st.markdown(
    """
    <style>
      .block-container {padding: 0.4rem 0.8rem 2rem 0.8rem; max-width: 100%;}
      header[data-testid="stHeader"] {background: transparent;}
      #MainMenu, footer {visibility: hidden;}
      iframe {border: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🥩 Freezer Fuel")
    st.caption(
        "Four 7-day meal-prep zines. Same rules: high protein, freeze-friendly, "
        "**nut-free & fish-free**, dirt cheap. Grunge / neo-brutalist, built in the provided fonts."
    )
    key = st.radio("Pick a plan", ORDER, format_func=lambda k: ZINES[k]["label"])
    st.caption(ZINES[key]["blurb"])

    doc = compose(key)
    st.download_button(
        "⬇️  Download this zine (.html)",
        data=doc.encode("utf-8"),
        file_name=ZINES[key]["file"],
        mime="text/html",
        use_container_width=True,
    )
    st.divider()
    st.caption(
        "New to the collection: **004 · Sem Repetir** rotates a different dinner and "
        "dessert every night, so no two days taste the same."
    )
    st.caption(
        "Heads up: the 1,300-kcal plan (GRIT) is an aggressive cut. Eat all four meals, "
        "keep water up, and see a nutritionist if you run it more than a few weeks."
    )

components.html(compose(key), height=ZINES[key]["height"], scrolling=True)

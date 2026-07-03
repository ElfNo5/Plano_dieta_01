# Freezer Fuel — Meal-Prep Zines

A single Streamlit app that bundles three 7-day meal-prep zines and lets you
switch between them from the sidebar. All three share the same rules:
high-protein, freeze-friendly, nut-free, and dirt cheap with ingredients you
can find in small Brazilian cities.

| # | Plan | Calories | Cost |
|---|------|----------|------|
| 001 | Freezer Fuel (chicken · sardine · eggs) | ~1,600 kcal/day | ~R$185/wk |
| 002 | Dirt Cheap Deluxe (soy protein · liver · eggs) | ~1,450 kcal/day | ~R$121/wk |
| 003 | GRIT — the lean cut (chicken · soy · eggs) | ~1,300 kcal/day | ~R$127/wk |

Each zine is embedded in `streamlit_app.py` as base64-encoded HTML, so the app
is fully self-contained — no extra files are required to run it.

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy to Streamlit Community Cloud
1. Push this repo to GitHub (at minimum `streamlit_app.py` and `requirements.txt`).
2. Go to https://share.streamlit.io , connect the repo, and set the main file to
   `streamlit_app.py`.
3. Deploy.

## Tweaks
- Each plan's render height is set by its `"height"` value in the `ZINES` dict
  inside `streamlit_app.py` — raise or lower it if a zine shows a gap or an
  inner scrollbar on your screen.
- The sidebar has a **Download** button that saves the selected zine as a
  standalone `.html` file.

> Note: the 1,300-kcal plan (GRIT) is an aggressive cut. Eat all four meals,
> keep water up, and check in with a nutritionist if you run it more than a few
> weeks.

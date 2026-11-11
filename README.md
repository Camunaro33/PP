# Beam-Column Design Tool — CSA S16-24

Interactive educational web app for beam-column design per CSA S16-24 Clause 13.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud (free)

1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Click **New app** → connect your GitHub repo → set **Main file** to `app.py`
4. Click **Deploy** — your app is live in ~60 seconds

## Features

- Interactive section selector (W310 family, CSA G40.21 350W)
- Live sliders for Cf, Mfx, Mfy, L, k-ratio
- Step 1: Section classification with bar charts
- Step 2: Cross-section capacity with stacked interaction bar
- Step 3a: Member, no LTB — column curve + interaction
- Step 3b: Member, with LTB — weak-axis curve + Lb vs Lu check
- Sensitivity analysis: how ratios vary with load
- Full formula derivation with numerical substitution for every step

"""
Beam-Column Design — CSA S16-24  (Clause 13)
Section data sourced directly from CISC HSC Tables T1 · T2 · T3
"""
import math, numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="GCI 2011 — Conception de Structures I  |  Université Laval",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global ────────────────────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.main { background: #F4F7FB; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem !important;
                   max-width: 1400px !important; }
section[data-testid="stSidebar"] { background: #0D1F3C !important; }
section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stMarkdown p { color: #94A3B8 !important; font-size:.82rem !important; }
section[data-testid="stSidebar"] strong { color: #E2E8F0 !important; }
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: #1E3A5F !important; border-color: #334E6F !important; color: #E2E8F0 !important; }
section[data-testid="stSidebar"] hr { border-color: #1E3A5F !important; }

/* ── Tab bar ───────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 12px 12px 0 0;
    padding: 6px 10px 0;
    border-bottom: 2px solid #1565C0;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: #EEF2FF;
    border-radius: 8px 8px 0 0;
    padding: 8px 16px;
    font-size: .82rem;
    font-weight: 600;
    color: #475569;
    border: 1px solid #CBD5E1;
    border-bottom: none;
}
.stTabs [aria-selected="true"] {
    background: #1565C0 !important;
    color: white !important;
    border-color: #1565C0 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: white;
    border-radius: 0 0 12px 12px;
    padding: 20px 24px;
    border: 1px solid #E2E8F0;
    border-top: none;
}

/* ── KPI cards ─────────────────────────────────────────────────────────── */
.kpi {
    background: white;
    border-radius: 12px;
    padding: 14px 10px 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,.07);
    border-top: 4px solid #1565C0;
    transition: transform .15s;
}
.kpi:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,.12); }
.kpi-l { font-size: .68rem; color: #64748B; font-weight: 600;
          text-transform: uppercase; letter-spacing: .06em; margin-bottom: 4px; }
.kpi-v { font-size: 1.35rem; font-weight: 800; color: #1565C0; line-height: 1.1; }

/* ── Formula box ───────────────────────────────────────────────────────── */
.fbox {
    background: #F8FAFF;
    border-left: 5px solid #1565C0;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .82rem;
    color: #1E293B;
    line-height: 2.0;
    margin: 10px 0;
    box-shadow: 0 2px 6px rgba(21,101,192,.08);
}

/* ── Result boxes ──────────────────────────────────────────────────────── */
.rok {
    background: linear-gradient(135deg, #DCFCE7, #F0FDF4);
    border-left: 6px solid #16A34A;
    border-radius: 0 10px 10px 0;
    padding: 12px 18px;
    font-weight: 700;
    font-size: 1.05rem;
    color: #15803D;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(22,163,74,.12);
}
.rwarn {
    background: linear-gradient(135deg, #FFFBEB, #FEF9C3);
    border-left: 6px solid #D97706;
    border-radius: 0 10px 10px 0;
    padding: 12px 18px;
    font-weight: 700;
    font-size: 1.05rem;
    color: #92400E;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(217,119,6,.12);
}
.rfail {
    background: linear-gradient(135deg, #FEF2F2, #FFE4E6);
    border-left: 6px solid #DC2626;
    border-radius: 0 10px 10px 0;
    padding: 12px 18px;
    font-weight: 700;
    font-size: 1.05rem;
    color: #991B1B;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(220,38,38,.12);
}

/* ── Info box ──────────────────────────────────────────────────────────── */
.ibox {
    background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
    border: 1px solid #93C5FD;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: .85rem;
    color: #1E3A5F;
    margin: 8px 0;
    line-height: 1.6;
}

/* ── Section heading ───────────────────────────────────────────────────── */
h2 {
    color: #0F172A !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding-bottom: 6px !important;
    margin-top: 0 !important;
    border-bottom: 2px solid #1565C0 !important;
}

/* ── Disclaimer gate ───────────────────────────────────────────────────── */
.disc-gate {
    background: white;
    border-radius: 20px;
    padding: 0;
    max-width: 820px;
    margin: 40px auto 0;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,.15);
}
.disc-gate-header {
    background: linear-gradient(135deg, #0D1F3C 0%, #1565C0 100%);
    padding: 32px 36px 28px;
    text-align: center;
}
.disc-gate-body {
    padding: 28px 36px 32px;
}
.disc-gate h2 {
    color: #DC2626 !important;
    font-size: 1.15rem !important;
    border-bottom: none !important;
    margin: 0 0 10px !important;
}
.disc-gate p { color: #374151; font-size: .92rem; line-height: 1.7; }
.disc-gate ul { color: #374151; font-size: .90rem; line-height: 1.85;
                margin: 0 0 14px; padding-left: 1.4em; }
.disc-gate .sign {
    font-size: .80rem; color: #6B7280;
    border-top: 1px solid #E5E7EB;
    padding-top: 12px; margin-top: 18px;
}

/* ── Edu banner ────────────────────────────────────────────────────────── */
.edu-banner {
    background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
    border: 1.5px solid #FCD34D;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: .82rem;
    color: #78350F;
    margin-bottom: 12px;
}

/* ── App header ────────────────────────────────────────────────────────── */
.app-header {
    background: linear-gradient(135deg, #0D1F3C 0%, #1565C0 60%, #1976D2 100%);
    border-radius: 0 0 16px 16px;
    padding: 20px 28px 18px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(21,101,192,.25);
}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  DISCLAIMER GATE  — must be accepted before any content is shown
# ═══════════════════════════════════════════════════════════════════════════════

if "accepted" not in st.session_state:
    st.session_state["accepted"] = False

if not st.session_state["accepted"]:
    st.markdown("""
<div class="disc-gate">
  <div class="disc-gate-header">
    <div style="font-size:2.8rem;margin-bottom:8px">🏗️</div>
    <div style="font-size:1.5rem;font-weight:800;color:white;letter-spacing:.02em;margin-bottom:6px">
      GCI 2011 — Conception de Structures I
    </div>
    <div style="font-size:1.0rem;color:#93C5FD;margin-bottom:3px">
      Université Laval &nbsp;·&nbsp; Département de génie civil et de génie des eaux
    </div>
    <div style="font-size:.92rem;color:#BAD4F5">
      Professeur : <strong style="color:white">Luca Sorelli</strong>, ing., Ph.D.
    </div>
    <div style="margin-top:12px;display:inline-block;background:rgba(255,255,255,.15);
                border-radius:20px;padding:4px 16px;font-size:.8rem;color:#E0F2FE;
                border:1px solid rgba(255,255,255,.25)">
      Outil pédagogique — Vérification d'un poteau-poutre en acier — CSA S16-24 Cl. 13
    </div>
  </div>
  <div class="disc-gate-body">

  <h2>⚠️  Educational Use Only — Disclaimer &amp; Terms of Use</h2>
  <p><strong>Please read carefully before proceeding. You must accept these terms to access this tool.</strong></p>

  <p>This application was developed exclusively for <strong>academic and educational purposes</strong>
  as a teaching aid for <strong>GCI 2011 — Conception de Structures I</strong> at <strong>Université Laval</strong>,
  under the supervision of <strong>Prof. Luca Sorelli</strong>.
  It is intended to help students understand the beam-column design methodology described in
  <strong>CSA S16-24 — Design of Steel Structures, Clause 13</strong>, using section property data
  sourced from the <strong>CISC Handbook of Steel Construction, 13th edition (Tables T1, T2, T3)</strong>.</p>

  <ul>
    <li>This tool <strong>must not be used</strong> for the design, verification, or assessment
        of any real structure, construction project, or professional engineering work.</li>
    <li>Results produced by this tool are <strong>not certified, validated, or approved</strong>
        by any professional or regulatory body.</li>
    <li>The tool may contain errors, simplifications, or approximations that are
        acceptable for teaching but <strong>unacceptable in professional practice</strong>.</li>
    <li>Any use of this tool outside the classroom is <strong>entirely at the user's own risk</strong>.</li>
    <li>Prof. Luca Sorelli, Université Laval, and all contributors accept
        <strong>no liability whatsoever</strong> for any loss, damage, injury, or consequence
        arising from the use or misuse of this tool.</li>
    <li>This tool does not replace the judgement of a licensed professional engineer.
        All structural designs must be reviewed and stamped by a qualified engineer
        in accordance with applicable codes and regulations.</li>
  </ul>

  <p>By clicking <strong>"I understand and accept — open the tool"</strong> below, you confirm that:</p>
  <ul>
    <li>You are using this tool solely for educational and learning purposes in GCI 2011.</li>
    <li>You will <strong>not</strong> use, cite, or rely on any result from this tool
        in any professional engineering context.</li>
    <li>You understand that the tool may contain inaccuracies and that you bear
        full responsibility for any use you make of its output.</li>
  </ul>

  <div class="sign">
    GCI 2011 — Conception de Structures I &nbsp;|&nbsp; Université Laval &nbsp;|&nbsp;
    Prof. Luca Sorelli, ing., Ph.D.<br>
    Référence : CSA S16-24 Cl. 13 &nbsp;|&nbsp; CISC HSC 13th éd. &nbsp;|&nbsp;
    φ = 0.90 &nbsp;|&nbsp; n = 1.34
  </div>
  </div><!-- end disc-gate-body -->
</div>
""", unsafe_allow_html=True)

    col_l, col_btn, col_r = st.columns([1, 2, 1])
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅  I understand and accept — open the tool",
                     use_container_width=True, type="primary"):
            st.session_state["accepted"] = True
            st.rerun()
        st.markdown(
            "<p style='text-align:center;font-size:.78rem;color:#888;margin-top:6px'>"
            "If you do not accept these terms, close this page.</p>",
            unsafe_allow_html=True)
    st.stop()   # block all content below until accepted

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION DATABASE  — values read directly from HSC Tables T1 (pages 6-44 to 6-55)
#  Keys: A[mm²] d[mm] bf[mm] tf[mm] tw[mm]
#        Ix[10⁶mm⁴] Sx[10³mm³] Zx[10³mm³] rx[mm]
#        Iy[10⁶mm⁴] Sy[10³mm³] Zy[10³mm³] ry[mm]
#        J[10³mm⁴]  Cw[10⁹mm⁶]  Lu[mm]  Fy[MPa]
# ═══════════════════════════════════════════════════════════════════════════════
RAW = {
# ── W690 (page 6-44) ──────────────────────────────────────────────────────
"W690×802":(102000,835,329,22.0,15.0, 10600,25400,30900, 322, 875,4520,7150,92.5,  206000,119000, 5490, 345),
"W690×548": (69900,730,17400,310,20.0,15.0,  6730,17400,20400, 310, 543,2920,4570,88.1,   68200, 66200, 5280, 345),
"W690×500": (63800,720,16000,308,30.0,24.0,  5700,15200,18500, 299, 530,2500,3920,88.0,   53900, 53600, 5080, 345),
"W690×419": (53400,710,296,13.1,8.4,  4950,13300,15300,305,395,2170,3370,86.0,  54600,53600, 4920, 345),
"W690×265": (33800,678,254,15.7,10.9, 2890, 8080, 9330,292,266,1640,2530,88.1,  26400,23400, 3900, 345),
"W690×217": (27600,695,255,11.7,8.5,  2630, 6700, 7760,292,206,1300,2010,86.4,  14600,20800, 3810, 345),
# ── W610 (page 6-46) ──────────────────────────────────────────────────────
"W610×300": (38200,641,230,19.0,14.9, 2940, 7550, 8820,241, 225,1410,2180,76.4,  17000,16600, 4600, 345),
"W610×272": (34600,620,319,20.6,15.4, 2520, 6840, 7810,238, 180,1270,1960,76.4,  11000,14700, 4500, 345),
"W610×241": (30800,620,318,22.9,14.9, 2560, 6220, 7050,238, 157,1180,1740,76.4,  13000,11000, 4000, 345),
"W610×174": (22100,616,325,19.0,10.6, 1540, 4810, 5540,235, 112, 760,1140,71.1,   7030, 9640, 3900, 345),
"W610×155": (19700,611,324,19.0,9.9,  1530, 4830, 5370,235,  101,793,1200,71.6,   6900, 8420, 3700, 345),
"W610×125": (15900,612,229,19.6,11.9, 1710, 4600, 5300,328,   49,431, 650,55.5,   1100, 4800, 2700, 345),
"W610×101": (12900,603,228,14.9,10.5, 1120, 3720, 4310,295,   34,281, 420,51.3,    595, 3480, 2200, 345),
"W610×82":  (10400,599,178,12.8,10.0,  564, 2290, 2690,232,   18,187, 275,41.6,    340, 1780, 1900, 345),
# ── W530 (page 6-46) ──────────────────────────────────────────────────────
"W530×300": (38200,560,220,25.4,16.5, 2210, 6240, 7340,241, 225,1410,2180,76.4,  38200,30800, 5800, 345),
"W530×272": (34600,544,212,22.9,14.0, 1970, 5640, 6460,236, 180,1270,1960,76.4,  29000,27600, 5400, 345),
"W530×182": (23200,528,213,27.6,14.5, 1860, 4810, 5550,235,  112, 760,1140,69.6,  11200,16500, 4200, 345),
"W530×165": (21000,524,183,24.0,12.4, 1500, 4210, 4860,220,   49,431, 650,52.9,   8420, 9700, 3300, 345),
"W530×101": (12900,537,214,17.4,10.9, 1600, 4380, 5050,235,   34,281, 420,51.3,   8420, 9640, 3900, 345),
"W530×92":  (11700,533,209,15.6,10.2, 1360, 4040, 4640,233,   30,250, 374,50.8,   5990, 7880, 3700, 345),
"W530×85":  (10800,535,166,13.6,10.3,  746, 2740, 3200,218,   16,169, 249,37.6,   1620, 4140, 2200, 345),
"W530×74":  ( 9480,529,166,13.6,9.7,  1370, 3650, 4210,220,   13,145, 215,37.1,   1290, 3600, 2000, 345),
"W530×66":  ( 8370,525,165,11.4,8.9,   350, 1670, 1970,205,    8.4,129,189,31.6,    840, 2680, 1800, 345),
# ── W460 (page 6-48) ──────────────────────────────────────────────────────
"W460×260": (33100,480,282,24.4,15.3, 2550, 7030, 7720,278, 163,1130,1740,70.3,  13900, 8950, 5500, 345),
"W460×213": (27100,474,280,21.3,13.1, 1770, 5560, 6410,256, 101, 816,1250,61.1,   7030, 6530, 5000, 345),
"W460×177": (22600,482,286,26.9,16.6, 2090, 5600, 6590,275,  83, 643, 983,56.0,   5020, 5990, 4600, 345),
"W460×158": (20100,476,284,23.9,15.0, 1760, 5150, 6000,268,  72, 578, 884,55.7,   3600, 5260, 4200, 345),
"W460×144": (18400,472,283,22.1,13.6, 2920, 5080, 5940,280,  66, 509, 779,55.4,   2850, 4720, 4000, 345),
"W460×128": (16300,467,282,19.7,12.2, 2460, 4620, 5410,264,  57, 452, 692,55.2,   2010, 4140, 3800, 345),
"W460×113": (14400,463,280,17.3,10.8, 2090, 4160, 4870,257,  47, 385, 589,54.8,   1370, 3580, 3600, 345),
"W460×97":  (12300,466,193,19.0,11.4, 1960, 3760, 4400,239,  36, 290, 441,49.6,   1550, 1870, 3100, 345),
"W460×82":  (10400,460,191,16.0, 9.9, 1030, 3600, 4000,228,  28, 236, 357,49.1,    929, 1540, 2800, 345),
"W460×74":  ( 9480,457,190,14.5, 9.0, 1680, 3250, 3800,233,  24, 218, 331,49.0,    694, 1370, 2600, 345),
"W460×68":  ( 8730,459,154,15.4, 9.1, 1240, 2800, 3310,225,  17, 190, 288,41.4,    662,  718, 2000, 345),
"W460×52":  ( 6630,450,152,10.8, 7.6,  212, 1310, 1550,179,   8.6,113,170,36.0,    190,  422, 1600, 345),
# ── W410 (page 6-48) ──────────────────────────────────────────────────────
"W410×149": (19000,431,264,25.0,14.9, 1850, 3840, 4410,312,   97, 583, 886,71.4,   3420, 3200, 5500, 345),
"W410×132": (16800,425,263,22.2,12.8, 1650, 3700, 4290,281,   76, 476, 723,67.3,   2730, 2650, 5200, 345),
"W410×100": (12700,415,260,16.9, 9.4, 1690, 3140, 3700,247,   47, 320, 487,60.9,   1370, 1680, 4800, 345),
"W410×85":  (10800,417,181,18.2,10.9, 1250, 2560, 2990,232,   30, 234, 356,52.7,    887,  843, 3600, 345),
"W410×74":  ( 9480,413,180,16.0, 9.7,  985, 2380, 2770,229,   24, 196, 299,50.4,    628,  703, 3200, 345),
"W410×67":  ( 8580,410,179,14.4, 8.8,  716, 2000, 2340,220,   19, 160, 244,47.3,    419,  540, 2800, 345),
"W410×53":  ( 6760,403,177,10.9, 7.5,  785, 1810, 2120,220,   11, 125, 190,40.4,    242,  375, 2400, 345),
"W410×46":  ( 5890,403,140,11.2, 7.0,  154, 1130, 1310,162,    5.1, 73,110,29.5,    154,  138, 1700, 345),
"W410×39":  ( 4990,399,140, 8.8, 6.4,  126,  997, 1150,159,    4.0, 57, 86,28.4,    100,  107, 1500, 345),
# ── W360 (page 6-50) ──────────────────────────────────────────────────────
"W360×677": (86300,569,448,67.6,42.5, 7120,19700,27200,288, 1960,8650,13400,151, 101000, 98700, 9000, 345),
"W360×551": (70100,550,441,56.4,34.6, 5810,16500,22200,288, 1360,6200, 9560,139,  82000, 97000, 8500, 345),
"W360×421": (53600,531,432,45.0,26.8, 4160,13000,17300,278,  812,4620,7120,123,  31000, 62000, 7500, 345),
"W360×314": (40000,517,422,36.0,20.8, 3240,10100,13500,257,  504,3580,5520,112,  13900, 47800, 7000, 345),
"W360×262": (33400,508,418,30.4,17.4, 2620, 8470,11300,249,  375,2990,4620,106,   8820, 38800, 6500, 345),
"W360×237": (30200,502,395,27.2,15.9, 2160, 7460, 9910,245,  283,2390,3700,96.8,  5810, 32900, 6200, 345),
"W360×216": (27600,498,394,24.4,14.3, 1980, 6900, 9140,245,  243,2120,3250,93.9,  4440, 29500, 6000, 345),
"W360×196": (25100,372,374,26.2,16.4, 3420, 3840, 4490,369, 229,1220,1860,95.5,  5140, 6830, 5800, 345),
"W360×179": (22800,368,373,23.9,15.0, 3120, 3480, 4070,330, 207,1110,1680,95.2,  3910, 6120, 5500, 345),
"W360×162": (20600,364,371,21.8,13.3, 2560, 3120, 3660,316, 185, 997,1510,94.9,  2830, 5430, 5300, 345),
"W360×147": (18800,360,370,19.8,12.3, 2380, 2960, 3470,308, 165, 894,1350,93.6,  2200, 4820, 5000, 345),
"W360×134": (17000,356,369,18.0,11.2, 2100, 2720, 3200,302, 148, 803,1210,93.3,  1680, 4310, 4800, 345),
"W360×122": (15500,363,257,21.7,13.0, 1670, 2050, 2420,304, 61.5, 479, 724,63.0, 2340, 1960, 3700, 345),
"W360×110": (14100,360,256,19.9,11.4, 1760, 1900, 2240,310, 54.3, 424, 639,62.0, 1810, 1700, 3400, 345),
"W360×101": (12900,357,255,18.3,10.8, 1990, 1650, 1950,296, 46.2, 362, 545,59.9, 1370, 1550, 3200, 345),
"W360×91":  (11600,353,254,16.4, 9.5, 1680, 1510, 1780,297, 38.3, 302, 455,57.5, 1000, 1360, 3000, 345),
"W360×79":  (10100,354,205,16.8, 9.4, 1830, 1210, 1430,297, 24.8, 242, 365,49.6,  855,  712, 2600, 345),
"W360×72":  ( 9100,350,204,15.1, 8.6, 1960, 1090, 1280,286, 21.5, 211, 318,48.6,  600,  600, 2400, 345),
"W360×64":  ( 8130,347,203,13.5, 7.7, 1560,  989, 1170,281, 18.7, 184, 278,47.9,  434,  542, 2200, 345),
"W360×57":  ( 7230,358,172,13.1, 7.9,  947,  804,  947,278, 10.4, 121, 182,37.9,  330,  301, 1700, 345),
"W360×51":  ( 6450,355,171,11.6, 7.2,  809,  704,  832,275,  8.9, 104, 157,37.2,  228,  256, 1600, 345),
"W360×45":  ( 5700,352,171,  9.8, 6.9,  696,  630,  735,274,  7.3,  85, 128,35.8,  151,  207, 1400, 345),
"W360×39":  ( 4990,353,128,10.7, 6.5,  490,  540,  631,273,  3.76, 59,  88,27.5,   110,   96, 1300, 345),
"W360×33":  ( 4170,349,127, 8.5, 5.8,  379,  455,  527,255,  2.91, 46,  69,26.4,    57,   73, 1100, 345),
# ── W310 (pages 6-50/6-51) ────────────────────────────────────────────────
"W310×500": (63800,500,427,75.1,45.1,20400,20400,16900,281,1392,4490,6900,147.0,101000,15300, 7000, 345),
"W310×454": (57800,479,420,68.7,41.3,16900,19100,15400,275,1130,4000,6240,145.0, 77200,13100, 6700, 345),
"W310×415": (52800,468,415,62.7,38.9,14900,17600,14200,268, 865,3610,5610,144.0, 59500,11300, 6500, 345),
"W310×375": (47800,457,409,57.2,35.4,13700,16000,13300,255, 755,3270,5090,144.0, 44900, 9570, 6200, 345),
"W310×342": (43700,453,407,52.6,32.6,12400,14600,12000,255, 619,2910,4530,143.0, 34900, 8420, 6100, 345),
"W310×313": (39900,449,403,48.3,30.0,11000,13300,11000,254, 504,2620,4070,143.0, 27000, 7350, 5900, 345),
"W310×283": (36100,365,322,44.1,26.9, 9880,10200, 8820,244, 419,2340,3610,110.0, 20400, 6330, 5600, 345),
"W310×253": (32200,356,319,39.6,24.4, 8450, 9270, 8030,243, 342,2080,3220,107.0, 14800, 5370, 5300, 345),
"W310×226": (28800,348,316,35.6,22.1, 7560, 8140, 7080,234, 283,1830,2840,105.0, 10800, 4620, 5100, 345),
"W310×202": (25800,341,315,31.8,20.1, 6620, 7140, 6230,228, 229,1610,2500,104.0,  7740, 3960, 4900, 345),
"W310×179": (22800,333,313,28.1,18.0, 5780, 6230, 5440,224, 180,1400,2170,104.0,  5360, 3340, 4800, 345),
"W310×158": (20100,327,310,25.0,15.5, 4750, 5460, 4760,222, 143,1220,1900,  87.0,  3780, 2840, 5490, 345),
"W310×143": (18200,323,309,22.9,14.0, 4160, 4950, 4320,218, 110, 991,1540,  79.0,  2870, 2540, 5280, 345),
"W310×129": (16500,318,308,20.6,13.1, 3690, 4360, 3810,214,  86, 834,1300,  72.0,  2130, 2220, 5080, 345),
"W310×118": (15000,314,307,18.7,11.9, 3340, 3980, 3480,210,  70, 673,1050,  68.0,  1600, 1970, 4920, 345),
"W310×107": (13600,311,306,17.0,10.9, 2990, 3570, 3120,206,  55, 560, 870,  63.0,  1220, 1760, 4790, 345),
"W310×97":  (12300,308,305,15.4, 9.9, 2650, 3140, 2740,204,  43, 478, 744,  59.0,  1010, 1560, 4970, 345),
"W310×86":  (11000,310,254,16.3, 9.1, 2200, 2800, 2440,195,  33, 351, 547,  55.0,   877,  961, 3900, 345),
"W310×79":  (10100,306,254,14.6, 8.8, 1950, 2520, 2200,194,  27, 314, 490,  52.0,   657,  847, 3810, 345),
"W310×74":  ( 9430,310,205,16.3, 9.4, 1570, 2160, 1880,185,  18, 229, 357,  44.0,   718,  522, 3000, 345),
"W310×67":  ( 8450,306,204,14.6, 8.5, 1340, 1960, 1710,182,  14, 203, 316,  41.0,   522,  439, 2800, 345),
"W310×60":  ( 7530,303,203,13.1, 7.5, 1090, 1700, 1490,180,  11, 180, 279,  38.0,   378,  384, 2500, 345),
"W310×52":  ( 6650,318,167,13.2, 7.6,  869, 1380, 1200,186,   6.3,135, 209,  38.0,   308,  191, 2200, 345),
"W310×45":  ( 5690,313,166,11.2, 6.6,  712, 1140, 1000,183,   5.0,112, 174,  37.0,   191,  126, 1900, 345),
"W310×39":  ( 4940,310,165, 9.7, 5.8,  596,  997,  869,183,   3.9, 94, 146,  36.0,   126,   84, 1600, 345),
"W310×33":  ( 4190,313,102,10.8, 6.6,  280,  707,  619,145,   1.1,  66, 102,  16.0,   122,   27, 1100, 345),
"W310×28":  ( 3590,309,102, 8.9, 6.0,  225,  607,  533,145,   0.834,56,  86,  15.0,    75,   22, 1000, 345),
"W310×24":  ( 3040,305,101, 6.7, 5.6,  164,  495,  439,142,   0.618,46,  71,  14.0,    43,   16,  900, 345),
"W310×21":  ( 2690,303,101, 5.7, 5.1,  115,  437,  379,140,   0.491,39,  60,  13.5,    29,   12,  800, 345),
# ── W250 (pages 6-52/6-53) ────────────────────────────────────────────────
"W250×167": (21300,289,265,31.8,19.2, 4610, 5530, 4870,195, 68.1,748,1140,56.6,  6310, 1630, 5500, 345),
"W250×149": (19000,282,263,28.4,17.3, 4010, 4820, 4240,194, 54.7,658,1000,53.7,  4510, 1390, 5200, 345),
"W250×131": (16700,275,261,25.1,15.4, 3330, 4240, 3730,192, 43.2,571, 870,50.9,  3120, 1160, 5000, 345),
"W250×115": (14600,269,259,22.1,13.5, 2800, 3600, 3170,190, 33.5,495, 753,47.9,  2130, 1016, 4700, 345),
"W250×101": (12900,264,257,19.6,11.9, 2360, 3200, 2810,188, 25.4,432, 656,44.4,  1490,  872, 4400, 345),
"W250×89":  (11400,260,256,17.3,10.7, 2000, 2800, 2470,186, 20.4,378, 574,42.3,  1040,  751, 4100, 345),
"W250×80":  (10200,256,255,15.6, 9.4, 1730, 2440, 2150,185, 15.9,338, 513,39.6,   757,  623, 3900, 345),
"W250×73":  ( 9280,253,254,14.2, 8.6, 1510, 2140, 1880,181, 11.8,306, 466,35.7,   575,  575, 3700, 345),
"W250×67":  ( 8550,257,204,15.7, 8.9, 1700, 1800, 1580,195,  9.42,265, 403,33.2,   524,  459, 3100, 345),
"W250×58":  ( 7420,252,203,13.5, 8.0, 1360, 1570, 1380,186,  7.64,214, 325,32.1,   337,  379, 2800, 345),
"W250×49":  ( 6250,247,202,11.0, 7.4, 1060, 1340, 1180,180,  5.56,173, 263,29.8,   188,  274, 2400, 345),
"W250×45":  ( 5720,266,148,13.0, 7.6,  875, 1340, 1180,186,  3.03,152, 231,23.0,   194,  179, 1900, 345),
"W250×39":  ( 4920,262,147,11.2, 6.6,  684, 1050,  928,182,  2.43,127, 193,22.3,   122,  144, 1700, 345),
"W250×33":  ( 4190,258,146, 9.1, 6.1,  546,  840,  742,181,  1.78, 98, 149,20.6,    75,  108, 1500, 345),
"W250×28":  ( 3630,260,102,10.0, 6.4,  391,  921,  811,174,  1.78,168, 255,22.1,   129,   98, 1700, 345),
"W250×25":  ( 3230,257,102, 8.4, 6.1,  303,  749,  660,169,  1.26, 93, 140,19.8,    82,   75, 1500, 345),
"W250×22":  ( 2850,254,102, 6.9, 5.8,  245,  703,  619,170,  0.918, 54,  83,17.9,    43,   56, 1300, 345),
"W250×18":  ( 2270,251,101, 5.3, 4.8,  177,  597,  525,166,  0.610, 37,  56,16.4,    21,   37, 1100, 345),
# ── W200 (pages 6-54/6-55) ────────────────────────────────────────────────
"W200×100": (12700,229,210,23.7,14.5, 1130, 1150,  989,145, 36.6,349, 533,53.8,  2090,  386, 4000, 345),
"W200×86":  (11000,222,209,20.6,13.0,  940,  981,  847,144, 29.1,300, 458,51.5,  1390,  318, 3600, 345),
"W200×71":  ( 9100,216,206,17.4,10.2,  749,  803,  695,142, 20.7,246, 375,47.7,   817,  250, 3200, 345),
"W200×59":  ( 7560,210,205,14.2, 9.1,  601,  653,  566,139, 15.4,199, 303,45.1,   463,  196, 2900, 345),
"W200×52":  ( 6650,206,204,12.6, 7.9,  512,  589,  512,138, 12.6,175, 266,43.5,   323,  167, 2600, 345),
"W200×46":  ( 5860,203,203,11.0, 7.2,  450,  495,  451,137,  9.98,151, 229,41.3,   220,  141, 2500, 345),
"W200×42":  ( 5310,205,166,11.8, 7.2,  396,  448,  399,133,  5.33,108, 165,31.7,   192,   84, 2000, 345),
"W200×36":  ( 4570,201,165,10.2, 6.2,  313,  380,  342,131,  4.10, 92,139,30.0,   122,   69, 1800, 345),
"W200×31":  ( 3970,210,134,10.2, 6.4,  297,  307,  299,122,  3.87, 61,  93,31.2,    61,   42, 1500, 345),
"W200×27":  ( 3440,207,133, 8.4, 5.8,  233,  256,  246,116,  3.11, 49,  76,30.0,    36,   29, 1300, 345),
"W200×22":  ( 2860,206,102, 8.0, 6.2,  165,  198,  188,105,  1.42, 42,  63,22.3,    35,   22, 1300, 345),
"W200×19":  ( 2440,203,102, 6.5, 5.8,  129,  177,  167,103,  0.976, 36, 54,20.0,    18,   16, 1200, 345),
"W200×15":  ( 1910,200,100, 5.2, 4.3,   89.9,131,  119, 97,  0.869, 28, 42,21.3,     8.24,  12, 1000, 345),
# ── W150 (page 6-54) ──────────────────────────────────────────────────────
"W150×37":  ( 4750,162,154,11.6, 8.1,  220,  311,  275, 73,  7.07, 91,140,38.6,   197,   40, 2200, 345),
"W150×30":  ( 3810,157,153, 9.3, 6.6,  165,  249,  221, 66,  5.56, 73,112,38.2,   103,   30, 2000, 345),
"W150×22":  ( 2860,152,152, 6.6, 5.8,  110,  186,  161, 62,  3.87, 51, 77,36.8,    43,   20, 1700, 345),
"W150×24":  ( 3060,160,102,10.3, 6.6,  119,  177,  167,105,  1.83, 36, 55,24.4,    93,   13, 1400, 345),
"W150×18":  ( 2290,153,102, 7.1, 5.8,   87.3,131,  119, 97,  1.26, 25, 38,23.5,    37,    9, 1200, 345),
"W150×14":  ( 1730,150,100, 5.5, 4.3,   61.5,109,   99, 95,  0.918, 20, 30,22.9,    17,    7, 1000, 345),
"W150×13":  ( 1610,148,100, 4.9, 4.3,   54.8, 95,   85, 92,  0.818, 18, 27,22.5,    13,    6,  900, 345),
"W100×19":  ( 2480,106,103, 8.8, 7.1,    4.77,96,   103,44,  1.61, 32, 48,25.5,    63,    3,  800, 345),
}

#  Unpack into a clean dict  ─────────────────────────────────────────────────
# tuple order: A d bf tf tw  Ix Sx Zx rx  Iy Sy Zy ry  J[10³mm⁴] Cw[10⁹mm⁶] Lu Fy
_K = "A d bf tf tw Ix Sx Zx rx Iy Sy Zy ry J Cw Lu Fy".split()
SECTIONS = {}
for name, row in RAW.items():
    r = dict(zip(_K, row))
    # Convert to SI base units (mm)
    r["Zx"] *= 1e3        # → mm³
    r["Sx"] *= 1e3        # → mm³
    r["Zy"] *= 1e3        # → mm³
    r["Sy"] *= 1e3        # → mm³
    r["Ix"] *= 1e6        # → mm⁴
    r["Iy"] *= 1e6        # → mm⁴
    r["J"]  *= 1e3        # → mm⁴
    r["Cw"] *= 1e9        # → mm⁶
    r["h"]   = r["d"] - 2*r["tf"]
    SECTIONS[name] = r

# Section families for grouping
FAMILIES = {
    "W690": [k for k in SECTIONS if k.startswith("W690")],
    "W610": [k for k in SECTIONS if k.startswith("W610")],
    "W530": [k for k in SECTIONS if k.startswith("W530")],
    "W460": [k for k in SECTIONS if k.startswith("W460")],
    "W410": [k for k in SECTIONS if k.startswith("W410")],
    "W360": [k for k in SECTIONS if k.startswith("W360")],
    "W310": [k for k in SECTIONS if k.startswith("W310")],
    "W250": [k for k in SECTIONS if k.startswith("W250")],
    "W200": [k for k in SECTIONS if k.startswith("W200")],
    "W150 / W100": [k for k in SECTIONS if k.startswith("W150") or k.startswith("W100")],
}

# ═══════════════════════════════════════════════════════════════════════════════
#  DESIGN EQUATIONS  —  CSA S16-24 / CISC HSC 13th ed.
#
#  PARAMETER EXPLANATION
#  ──────────────────────
#  k      : moment ratio κ = Mf1/Mf2  (|Mf1| ≤ |Mf2|)
#            +1 = double curvature (best case)   −1 = single curvature (worst case)
#            Used to compute ω1  [HSC 13.8.5]
#
#  ω1     : equivalent uniform moment factor  [HSC 13.8.5]
#            ω1 = 0.6 − 0.4·κ  ≥ 0.4
#            Accounts for moment gradient along the member.
#            Smaller ω1 → smaller amplification → less conservative.
#
#  U1x/U1y: moment amplification factor for P-δ (member bow)  [HSC 13.8.4]
#            U1 = ω1 / (1 − Cf/Ce)  applied to Mfx or Mfy
#            — For BRACED members:   U1x ≥ 0  (Step 3a, no LTB check)
#                                    U1x ≥ 1  (Step 2 section check)
#                                    U1x ≥ 1  (Step 3b, with LTB — to avoid
#                                               double-counting P-δ already in Mu)
#            — For UNBRACED members: U1x = U1y = 1.0
#              (P-Δ sway effect already included in Mf via U2·Mf analysis)
#
#  U2     : storey sway amplification factor  [HSC 13.8.4 / Cl.8.7]
#            Accounts for P-Δ (storey drift) in UNBRACED frames.
#            The user must supply U2·Mf2 as the applied moment Mf when unbraced.
#            U2 ≥ 1 / (1 − ΣCf / ΣCe_storey)   (computed by sway analysis)
#            In this tool: for UNBRACED, U1=1 and the user enters Mf already
#            amplified by U2.  A reminder is shown on screen.
#
#  β      : biaxial interaction factor  [HSC 13.8.2]
#            β = 0.6 + 0.4·λ̄y  ≤ 0.85
#            λ̄y = reduced slenderness for weak axis
#            For cross-section check (Step 2): β = 0.6 (fixed, λ̄y not needed)
#
#  n      : Perry-Robertson exponent  [HSC 13.3.1]
#            n = 1.34 for hot-rolled W shapes (Class 1–3)
#            n = 2.24 for welded (WWF) sections
#
#  Cex/Cey: elastic Euler critical force for strong / weak axis  [HSC 13.8.4]
#            Ce = π²·E·A / (KL/r)²
#            Used in U1 calculation for each axis independently.
# ═══════════════════════════════════════════════════════════════════════════════

def fl_lims(Fy):
    # Flange slenderness limits  [CSA S16-24 Table 4.1]
    s = math.sqrt(Fy)
    return {1: 145/s, 2: 170/s, 3: 200/s}

def wb_lims(Fy, Cf, pCy):
    # Web slenderness limits for beam-columns  [CSA S16-24 Table 4.2]
    # Limit depends on Cf/φCy: higher axial → tighter web limit
    s = math.sqrt(Fy)
    r = min(Cf/pCy, 1.0)
    return {1: (1100/s)*(1-0.391*r),
            2: (1700/s)*(1-0.391*r),
            3:  1900/s}

def classify(v, lm):
    # Return section class (1–4) for a given slenderness ratio and limits dict
    for c in [1,2,3]:
        if v <= lm[c]: return c
    return 4

def col_cr(phi, A, Fy, KLr, E=200000, n=1.34):
    """
    Factored compressive resistance  Cr  [HSC 13.3.1]
    Cr = φ·A·Fy·(1 + λ̄^(2n))^(-1/n)
    n = 1.34  hot-rolled W shapes
    n = 2.24  welded WWF sections
    λ̄ = √(Fy/Fe)  reduced slenderness
    Fe = π²·E / (KL/r)²  Euler elastic critical stress
    """
    Fe  = math.pi**2 * E / KLr**2
    lam = math.sqrt(Fy / Fe)
    Cr  = phi * A * Fy * (1 + lam**(2*n))**(-1/n)
    return Cr, lam, Fe

def omega1(k):
    """
    Equivalent uniform moment factor ω1  [HSC 13.8.5]
    For no lateral loads between supports:  ω1 = 0.6 − 0.4·κ  ≥ 0.4
    κ = Mf1/Mf2  (+1 = double curvature, −1 = single curvature)
    """
    return max(0.6 - 0.4*k, 0.4)

def U1_calc(w1_val, Cf, Ce):
    """
    Moment amplification factor U1  [HSC 13.8.4]
    U1 = ω1 / (1 − Cf/Ce)
    — Accounts for P-δ (member bow) effect
    — Applied independently to Mfx (using Cex) and Mfy (using Cey)
    — For BRACED frame: U1 ≥ 0 for Step 3a (no LTB),
                         U1 ≥ 1 for Step 2 (section) and Step 3b (with LTB)
    — For UNBRACED frame: U1x = U1y = 1.0
      (P-Δ sway already in Mf via U2 analysis — do not double-count)
    """
    return max(w1_val / (1 - Cf/Ce), 0.0)

def beta_biaxial(ly):
    """
    Biaxial interaction factor β  [HSC 13.8.2]
    β = 0.6 + 0.4·λ̄y  ≤ 0.85
    For cross-section check (Step 2): β = 0.6 (fixed, independent of λ̄y)
    """
    return min(0.6 + 0.4*ly, 0.85)

def Mr_section(phi, Zx, Sx, Fy, cls):
    """
    Factored bending resistance of the cross-section  [HSC 13.5]
    Class 1 & 2 → Mr = φ·Zx·Fy  (plastic moment)
    Class 3     → Mr = φ·Sx·Fy  (elastic moment)
    """
    return phi*Zx*Fy if cls <= 2 else phi*Sx*Fy

def LTB_Mu(E, G, Iy, J, Cw, L):
    """
    Elastic LTB critical moment Mu  [HSC 13.6]
    Mu = (ω2·π/Ls)·√(E·Iy·G·J + (π·E/Ls)²·Iy·Cw)
    ω2 applied outside this function.
    """
    return (math.pi/L) * math.sqrt(E*Iy*G*J + (math.pi*E/L)**2 * Iy*Cw)

def Mr_ltb_calc(phi, Zx, Sx, Fy, Mu_eff):
    """
    Factored bending resistance with LTB  [HSC 13.6]
    If Mu ≥ 0.67·Mp:  Mr = φ·min(1.15·Mp·(1 − 0.28·Mp/Mu),  Mp)
    If Mu < 0.67·Mp:  Mr = φ·Mu  (elastic LTB governs)
    """
    Mp = Fy * Zx
    if Mu_eff >= 0.67*Mp:
        return phi * min(1.15*Mp*(1 - 0.28*Mp/Mu_eff), Mp)
    return phi * Mu_eff

# ─────────────────────────────────────────────────────────────────────────────

def compute(sn, Cf_kN, Mfx_kNm, Mfy_kNm, L_mm,
            Kx=1.0, Ky=1.0, k=0.67, kwy=0.67,
            om2=1.0, braced=True, U2=1.0,
            sec_type="hot-rolled",
            E=200000, G=77000, phi=0.9):
    """
    Full beam-column verification per CSA S16-24 Cl. 13.

    Parameters
    ----------
    k       : κ = Mf1/Mf2 for STRONG axis  (+1=double curv, −1=single curv)
    kwy     : κ = Mf1/Mf2 for WEAK axis    (same convention)
    om2     : LTB moment gradient factor ω2  [HSC 13.6]
    braced  : True  = braced frame  → U1 computed, U2 not applicable
              False = unbraced frame → U1x=U1y=1.0, user enters U2·Mf
    U2      : Storey sway amplification  [HSC 8.7]
              Only used when braced=False; Mfx is multiplied by U2 before checks.
    sec_type: 'hot-rolled' → n=1.34   |   'welded' → n=2.24  [HSC 13.3.1]
    """
    s   = SECTIONS[sn]
    n   = 1.34 if sec_type == "hot-rolled" else 2.24

    # ── Applied forces (apply U2 amplification for unbraced frames) ──────────
    # For UNBRACED frames, the engineer must amplify moments by U2 to account
    # for the P-Δ (storey sway) effect.  U1 is then set to 1.0.  [HSC 13.8.4]
    Cf  = Cf_kN  * 1e3
    if braced:
        Mfx = Mfx_kNm * 1e6   # no U2 for braced
        Mfy = Mfy_kNm * 1e6
    else:
        Mfx = Mfx_kNm * 1e6 * U2   # U2·Mf for unbraced sway moments
        Mfy = Mfy_kNm * 1e6 * U2

    A,d,bf,tf,tw = s["A"],s["d"],s["bf"],s["tf"],s["tw"]
    Zx,Sx,rx     = s["Zx"],s["Sx"],s["rx"]
    Zy,Sy,ry     = s["Zy"],s["Sy"],s["ry"]
    Iy,J,Cw,Lu,Fy,h = s["Iy"],s["J"],s["Cw"],s["Lu"],s["Fy"],s["h"]

    # ── STEP 1: Section classification  [CSA S16-24 Tables 4.1, 4.2] ─────────
    pCy   = phi * A * Fy
    b2tf  = (bf/2) / tf
    htw   = h / tw
    fl    = fl_lims(Fy)
    wb    = wb_lims(Fy, Cf, pCy)
    cf    = classify(b2tf, fl)
    cw    = classify(htw,  wb)
    cls   = max(cf, cw)

    # ── Section resistances  [HSC 13.5] ──────────────────────────────────────
    Mrx_s = Mr_section(phi, Zx, Sx, Fy, cls)   # strong-axis Mr
    Mry_s = phi * Zy * Fy                        # weak-axis Mr (no LTB for weak axis)

    # ── Euler critical forces  [HSC 13.8.4] ──────────────────────────────────
    # Computed for EACH axis independently — used in U1 and Cr calculations
    KLx_rx = Kx * L_mm / rx
    KLy_ry = Ky * L_mm / ry
    Cex    = math.pi**2 * E * A / KLx_rx**2    # strong-axis Euler force
    Cey    = math.pi**2 * E * A / KLy_ry**2    # weak-axis  Euler force

    # ── ω1 moment gradient factors  [HSC 13.8.5] ─────────────────────────────
    om1x = omega1(k)     # for strong-axis amplification
    om1y = omega1(kwy)   # for weak-axis  amplification

    # ── U1 amplification factors  [HSC 13.8.4] ───────────────────────────────
    #
    #  U1 = ω1 / (1 − Cf/Ce)   accounts for P-δ (member bow between supports)
    #
    #  BRACED frame (contreventée) :
    #  ─────────────────────────────
    #  Step 2  (vérification de la section)   : U1x ≥ 1.0,  U1y ≥ 1.0
    #           → minimum 1.0 because the cross-section must carry at least
    #             the applied moment, never less.
    #
    #  Step 3a (pièce sans déversement)       : U1x ≥ 0,    U1y ≥ 0
    #           → minimum 0.0 is correct here; the in-plane member check
    #             uses the actual amplified moment.  If U1 < 0 it means
    #             the member is in double curvature and moment amplification
    #             is beneficial — but we cap at 0 (not negative).
    #           SLIDE NOTE: "si contreventé U1x ≥ 0,  U1y ≥ 0"  [HSC 13.8.4]
    #
    #  Step 3b (pièce avec déversement)       : U1x ≥ 1.0,  U1y ≥ 0
    #           → U1x ≥ 1.0 because ω2 (moment gradient in LTB) already
    #             accounts for the moment shape in Mu.  Using U1x < 1
    #             would double-count the gradient benefit.
    #           → U1y ≥ 0 (weak axis has no LTB; U1y can be < 1 for
    #             double curvature on weak axis in a braced member).
    #           SLIDE NOTE: "U1x ≥ 1 si on a considéré le déversement"  [HSC 13.8.4]
    #
    #  UNBRACED frame (non contreventée) :
    #  ─────────────────────────────────────
    #  Steps 2 and 3a are NOT REQUIRED for unbraced members [slide note].
    #  Only Step 3b (avec déversement) applies, with U1x = U1y = 1.0.
    #  The P-Δ (storey sway) effect is already captured by U2·Mf,
    #  so recalculating U1 would double-count it.
    #  SLIDE NOTE: "si pas contreventé  U1x = U1y = 1.0"  [HSC 13.8.4]
    #  SLIDE NOTE: "Step 2 pas nécessaire pour une pièce non contreventée"
    # ─────────────────────────────────────────────────────────────────────────
    U1x_raw = U1_calc(om1x, Cf, Cex)   # raw value before min clamp
    U1y_raw = U1_calc(om1y, Cf, Cey)   # raw value before min clamp

    if braced:
        # Step 2 : U1x ≥ 1.0,  U1y ≥ 1.0
        U1x_s2 = max(U1x_raw, 1.0)
        U1y_s2 = max(U1y_raw, 1.0)
        # Step 3a : U1x ≥ 0,  U1y ≥ 0
        U1x_3a = max(U1x_raw, 0.0)
        U1y_3a = max(U1y_raw, 0.0)
        # Step 3b : U1x ≥ 1.0,  U1y ≥ 0  (LTB already has ω2)
        U1x_3b = max(U1x_raw, 1.0)
        U1y_3b = max(U1y_raw, 0.0)
    else:
        # Unbraced : U1x = U1y = 1.0 everywhere (P-Δ in U2·Mf)
        U1x_s2 = U1y_s2 = 1.0
        U1x_3a = U1y_3a = 1.0
        U1x_3b = U1y_3b = 1.0

    # ── STEP 2: Cross-section capacity  [HSC 13.8.2] ─────────────────────────
    # Cr = φCy (squash load — buckling suppressed)
    # β = 0.6 (fixed for cross-section check)
    Ta  = Cf / pCy
    Tb  = 0.85 * U1x_s2 * Mfx / Mrx_s
    Tc  = 0.6  * U1y_s2 * Mfy / Mry_s
    r2  = Ta + Tb + Tc

    # ── STEP 3a: Overall member, NO LTB  [HSC 13.8.3] ────────────────────────
    # Cr = f(λ̄)  where λ̄ = λ̄_max (biaxial: use max of λ̄x, λ̄y)
    # For biaxial bending, governing λ governs Cr
    Crx, lx, Fex = col_cr(phi, A, Fy, KLx_rx, E, n)
    Cry, ly, Fey = col_cr(phi, A, Fy, KLy_ry, E, n)
    # For biaxial: use λ_max → Cr = min(Crx, Cry)
    Cr3a  = min(Crx, Cry)
    lam_max = max(lx, ly)
    bv    = beta_biaxial(ly)   # β = 0.6 + 0.4·λ̄y  [HSC 13.8.2]
    T3a_A = Cf / Cr3a
    T3a_B = 0.85 * U1x_3a * Mfx / Mrx_s
    T3a_C = bv  * U1y_3a * Mfy / Mry_s
    r3a   = T3a_A + T3a_B + T3a_C

    # ── STEP 3b: Overall member, WITH LTB  [HSC 13.8.4] ──────────────────────
    # Cr uses λ̄y (weak-axis governs out-of-plane buckling)
    # Mrx may be reduced by LTB [HSC 13.6]
    # NOTE: U1x ≥ 1.0 here — do NOT use U1x < 1 when LTB is considered,
    # because w2 (moment gradient for LTB) already accounts for moment shape.
    # Using U1x < 1 would double-count the gradient effect.
    Lb = L_mm
    if Lb <= Lu:
        Mrx_b   = Mrx_s
        ltb_ok  = True
        ltb     = f"Lb={Lb:.0f} ≤ Lu={Lu:.0f} mm → Mrx = Mp (aucun déversement)"
        Mu_eff  = None
    else:
        Mu_base = LTB_Mu(E, G, Iy, J, Cw, Lb)
        Mu_eff  = om2 * Mu_base          # ω2 amplifies resistance  [HSC 13.6]
        Mrx_b   = Mr_ltb_calc(phi, Zx, Sx, Fy, Mu_eff)
        ltb_ok  = False
        ltb     = f"Lb={Lb:.0f} > Lu={Lu:.0f} mm → déversement réduit Mrx"

    T3b_A = Cf / Cry
    T3b_B = 0.85 * U1x_3b * Mfx / Mrx_b
    T3b_C = bv  * U1y_3b * Mfy / Mry_s
    r3b   = T3b_A + T3b_B + T3b_C

    gov = max(r2, r3a, r3b)

    return dict(
        # ── inputs ────────────────────────────────────────────────────────────
        sn=sn, Cf=Cf, Mfx=Mfx, Mfy=Mfy, L=L_mm,
        Kx=Kx, Ky=Ky, k=k, kwy=kwy, om2=om2,
        braced=braced, U2=U2, sec_type=sec_type,
        E=E, G=G, phi=phi, n=n,
        # ── section properties ─────────────────────────────────────────────────
        A=A, d=d, bf=bf, tf=tf, tw=tw, h=h,
        Zx=Zx, Sx=Sx, rx=rx,
        Zy=Zy, Sy=Sy, ry=ry,
        Ix=s["Ix"], Iy=Iy, J=J, Cw=Cw, Lu=Lu, Fy=Fy,
        # ── Step 1 ────────────────────────────────────────────────────────────
        pCy=pCy, b2tf=b2tf, htw=htw, fl=fl, wb=wb, cf=cf, cw=cw, cls=cls,
        # ── applicability flags ────────────────────────────────────────────────
        # Step 2 & 3a not required for unbraced members [HSC slide note]
        step2_req=braced,
        step3a_req=braced,
        # ── Step 2 ────────────────────────────────────────────────────────────
        Mrx_s=Mrx_s, Mry_s=Mry_s,
        Cex=Cex, Cey=Cey,
        om1x=om1x, om1y=om1y,
        U1x_raw=U1x_raw, U1y_raw=U1y_raw,
        U1x_s2=U1x_s2, U1y_s2=U1y_s2,
        Ta=Ta, Tb=Tb, Tc=Tc, r2=r2,
        # ── Step 3a ───────────────────────────────────────────────────────────
        KLx_rx=KLx_rx, KLy_ry=KLy_ry,
        lx=lx, ly=ly, lam_max=lam_max,
        Fex=Fex, Fey=Fey,
        Crx=Crx, Cry=Cry, Cr3a=Cr3a,
        CrA_x=Crx/A, CrA_y=Cry/A,
        bv=bv,
        U1x_3a=U1x_3a, U1y_3a=U1y_3a,
        T3a_A=T3a_A, T3a_B=T3a_B, T3a_C=T3a_C, r3a=r3a,
        # ── Step 3b ───────────────────────────────────────────────────────────
        Mrx_b=Mrx_b, U1x_3b=U1x_3b, U1y_3b=U1y_3b,
        Mu_eff=Mu_eff, ltb=ltb, ltb_ok=ltb_ok,
        T3b_A=T3b_A, T3b_B=T3b_B, T3b_C=T3b_C, r3b=r3b,
        # ── verdict ───────────────────────────────────────────────────────────
        # For unbraced: gov = max of only applicable checks (Step 3b)
        gov=gov, ok=(gov<=1.0),
    )

# ═══════════════════════════════════════════════════════════════════════════════
#  COLOUR HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
BL="#1565C0"; TL="#0D6E6E"; OR="#C45000"; PU="#5B2D8E"
GR="#1B7E34"; RD="#B71C1C"; GO="#B8860B"

def rclr(r): return RD if r>1.0 else (GO if r>0.9 else GR)
def vt(r):
    if r>1.0:  return f"✗  {r:.4f}  INADEQUATE"
    if r>0.9:  return f"△  {r:.4f}  Marginal"
    return             f"✓  {r:.4f}  ADEQUATE"
def rhtml(r):
    cls="rfail" if r>1.0 else ("rwarn" if r>0.9 else "rok")
    return f'<div class="{cls}">{vt(r)}</div>'

# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTLY: SECTION SCHEMATIC  (real mm dimensions)
# ═══════════════════════════════════════════════════════════════════════════════
def section_fig(rv):
    d,bf,tf,tw,h = rv["d"],rv["bf"],rv["tf"],rv["tw"],rv["h"]
    hd,hbf,htw = d/2, bf/2, tw/2
    cls_col = [GR,GR,GO,RD][rv["cls"]-1]

    # steel fill colours
    FC  = "rgba(46,109,164,0.90)"   # flange – solid steel blue
    WC  = "rgba(70,140,200,0.65)"   # web   – lighter

    shapes = [
        # top flange
        dict(type="rect",x0=-hbf,y0=hd-tf,x1=hbf,y1=hd,
             fillcolor=FC,line=dict(color="#1A3A5C",width=1.3),layer="above"),
        # bottom flange
        dict(type="rect",x0=-hbf,y0=-hd,x1=hbf,y1=-hd+tf,
             fillcolor=FC,line=dict(color="#1A3A5C",width=1.3),layer="above"),
        # web
        dict(type="rect",x0=-htw,y0=-hd+tf,x1=htw,y1=hd-tf,
             fillcolor=WC,line=dict(color="#1A3A5C",width=0.8),layer="above"),
    ]

    dim_color = "#555"

    annotations = [
        # ── bf label (top) ────────────────────────────────────────────────
        dict(x=0, y=hd+d*.09, text=f"<b>bf = {bf} mm</b>",
             xanchor="center", yanchor="bottom",
             showarrow=False, font=dict(size=10, color=dim_color)),
        # ── bf arrow ──────────────────────────────────────────────────────
        dict(ax=-hbf, ay=hd+d*.05, axref="x", ayref="y",
             x=hbf, y=hd+d*.05, xref="x", yref="y",
             arrowhead=2, arrowside="end+start",
             arrowcolor=dim_color, arrowwidth=1.2,
             showarrow=True, text=""),
        # ── d label (left) ────────────────────────────────────────────────
        dict(x=-hbf-bf*.18, y=0, text=f"<b>d = {d} mm</b>",
             xanchor="center", yanchor="middle", textangle=-90,
             showarrow=False, font=dict(size=10, color=dim_color)),
        # ── d arrow ───────────────────────────────────────────────────────
        dict(ax=-hbf-bf*.12, ay=-hd, axref="x", ayref="y",
             x=-hbf-bf*.12, y=hd, xref="x", yref="y",
             arrowhead=2, arrowside="end+start",
             arrowcolor=dim_color, arrowwidth=1.2,
             showarrow=True, text=""),
        # ── tf label ──────────────────────────────────────────────────────
        dict(x=hbf+bf*.06, y=hd-tf/2, text=f"tf = {tf} mm",
             xanchor="left", yanchor="middle",
             showarrow=False, font=dict(size=9, color=dim_color)),
        # ── tf arrow ──────────────────────────────────────────────────────
        dict(ax=hbf+bf*.04, ay=hd, axref="x", ayref="y",
             x=hbf+bf*.04, y=hd-tf, xref="x", yref="y",
             arrowhead=2, arrowside="end+start",
             arrowcolor=dim_color, arrowwidth=1.0,
             showarrow=True, text=""),
        # ── tw label ──────────────────────────────────────────────────────
        dict(x=hbf+bf*.06, y=0, text=f"tw = {tw} mm",
             xanchor="left", yanchor="middle",
             showarrow=False, font=dict(size=9, color=dim_color)),
        # ── tw arrow ──────────────────────────────────────────────────────
        dict(ax=-htw, ay=0, axref="x", ayref="y",
             x=htw, y=0, xref="x", yref="y",
             arrowhead=2, arrowside="end+start",
             arrowcolor=dim_color, arrowwidth=1.0,
             showarrow=True, text=""),
        # ── h label (inner left) ──────────────────────────────────────────
        dict(x=-hbf-bf*.06, y=0, text=f"h = {h} mm",
             xanchor="right", yanchor="middle", textangle=-90,
             showarrow=False, font=dict(size=8, color="#999")),
        # ── section name ──────────────────────────────────────────────────
        dict(x=0, y=-hd-d*.16, text=f"<b>{rv['sn']}</b>",
             xanchor="center", yanchor="top",
             showarrow=False, font=dict(size=14, color=BL)),
        # ── class label ───────────────────────────────────────────────────
        dict(x=0, y=-hd-d*.28,
             text=f"<b>Class {rv['cls']}</b>  (Flange: {rv['cf']} | Web: {rv['cw']})",
             xanchor="center", yanchor="top",
             showarrow=False, font=dict(size=11, color=cls_col)),
        # ── area / Fy ─────────────────────────────────────────────────────
        dict(x=0, y=-hd-d*.40,
             text=f"A = {rv['A']:,} mm²  |  Fy = {rv['Fy']} MPa",
             xanchor="center", yanchor="top",
             showarrow=False, font=dict(size=9, color="#666")),
    ]

    fig = go.Figure()
    # invisible scatter to set axes
    fig.add_trace(go.Scatter(x=[-hbf-bf*.5, hbf+bf*.5],
                              y=[-hd-d*.55, hd+d*.22],
                              mode="markers", marker=dict(opacity=0)))
    fig.update_layout(
        shapes=shapes, annotations=annotations,
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        height=460,
        margin=dict(l=20,r=20,t=20,b=20),
        paper_bgcolor="white", plot_bgcolor="white",
        showlegend=False,
    )
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTLY: MEMBER DIAGRAM  (column with Cf, Mfx, Mfy arrows)
# ═══════════════════════════════════════════════════════════════════════════════
def column_fig(rv):
    """Left figure: column body + Cf arrows only. No moment symbols."""
    Cf_kN = rv["Cf"] / 1e3
    L_m   = rv["L"]  / 1000
    bf_mm = rv["bf"]
    W = 1.0
    H = max(W * 2 * min(rv["L"] / bf_mm, 20), 4.0)
    ext   = H * 0.22
    CF_C  = "#B71C1C"
    shapes, annotations = [], []
    shapes.append(dict(type="rect", x0=-W, y0=0, x1=W, y1=H,
        fillcolor="rgba(46,109,164,0.22)", line=dict(color="#1A3A5C", width=2.5)))
    if Cf_kN > 0:
        for ay, y, yt, ya in [(-ext,0,-ext*0.5,"top"),(H+ext,H,H+ext*0.6,"bottom")]:
            annotations.append(dict(ax=0,ay=ay,axref="x",ayref="y",
                x=0,y=y,xref="x",yref="y",
                arrowhead=2,arrowwidth=4,arrowcolor=CF_C,showarrow=True,text=""))
            annotations.append(dict(x=0,y=yt,
                text=f"<b>Cf = {Cf_kN:.0f} kN</b>",
                xanchor="center",yanchor=ya,showarrow=False,
                font=dict(size=11,color=CF_C)))
    annotations.append(dict(x=0,y=H/2,
        text=f"<b>{rv['sn']}</b><br>L = {L_m:.2f} m<br>Kx={rv['Kx']}  Ky={rv['Ky']}",
        xanchor="center",yanchor="middle",showarrow=False,
        font=dict(size=9,color="#1A3A5C"),
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#1A3A5C",borderwidth=1,borderpad=4))
    pad = ext * 2.2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[-W*2.5,W*2.5],y=[-pad,H+pad],
        mode="markers",marker=dict(opacity=0,size=1)))
    fig.update_layout(shapes=shapes,annotations=annotations,
        xaxis=dict(visible=False,scaleanchor="y",scaleratio=1),
        yaxis=dict(visible=False),height=500,
        margin=dict(l=5,r=5,t=5,b=5),
        paper_bgcolor="white",plot_bgcolor="white",showlegend=False)
    return fig


def convention_fig():
    """
    Standalone sign convention diagram — always visible above the moment diagram.
    Shows two clear examples side by side:
      LEFT:  Positive moment (+) → CCW arc, arc bulges RIGHT
      RIGHT: Negative moment (−) → CW  arc, arc bulges LEFT
    With a small I-beam sketch and the rotation arrow at each one.
    """
    POS_C = "#1565C0"
    NEG_C = "#DC2626"
    R = 1.0
    shapes, annotations, traces = [], [], []

    for cx, Mpos, color, sign, rot_lbl, side_lbl in [
        (-2.8, True,  POS_C, "+", "↺ sens anti-horaire", "arc côté droit"),
        ( 2.8, False, NEG_C, "−", "↻ sens horaire",       "arc côté gauche"),
    ]:
        # Small column stub
        shapes.append(dict(type="rect",
            x0=cx-0.18, y0=-0.5, x1=cx+0.18, y1=0.5,
            fillcolor="rgba(46,109,164,0.25)",
            line=dict(color="#1A3A5C", width=1.5)))

        # Half-circle arc
        theta = np.linspace(0, math.pi, 80)
        if Mpos:
            xs = cx + R * np.cos(theta)      # right side
            ys =      R * np.sin(theta)
            x_tip, y_tip   = cx - R, 0.0
            x_tail, y_tail = cx - R, R * 0.3
        else:
            xs = cx - R * np.cos(theta)      # left side
            ys =      R * np.sin(theta)
            x_tip, y_tip   = cx + R, 0.0
            x_tail, y_tail = cx + R, R * 0.3

        traces.append(go.Scatter(x=xs, y=ys, mode="lines",
            line=dict(color=color, width=3.5),
            showlegend=False, hoverinfo="skip"))

        # Arrowhead at arc end
        annotations.append(dict(
            ax=x_tail, ay=y_tail, axref="x", ayref="y",
            x=x_tip,   y=y_tip,   xref="x",  yref="y",
            arrowhead=3, arrowsize=1.4, arrowwidth=3.0, arrowcolor=color,
            showarrow=True, text=""))

        # Labels
        lx    = cx + R + 0.2 if Mpos else cx - R - 0.2
        anc   = "left" if Mpos else "right"
        annotations += [
            dict(x=cx, y=1.55,
                 text=f"<b style='font-size:16px;color:{color}'>{sign} M</b>",
                 xanchor="center", yanchor="bottom", showarrow=False,
                 font=dict(size=14, color=color)),
            dict(x=cx, y=-0.9,
                 text=f"<b>{rot_lbl}</b><br>{side_lbl}",
                 xanchor="center", yanchor="top", showarrow=False,
                 font=dict(size=9, color=color)),
        ]

    # Central divider
    shapes.append(dict(type="line", x0=0, y0=-1.4, x1=0, y1=1.8,
        line=dict(color="#DDDDDD", width=1, dash="dot")))

    # Title
    annotations.append(dict(x=0, y=2.1,
        text="<b>Convention de signe — Moment fléchissant</b>",
        xanchor="center", yanchor="bottom", showarrow=False,
        font=dict(size=11, color="#1E293B")))

    fig = go.Figure(data=traces)
    fig.add_trace(go.Scatter(x=[-5, 5], y=[-1.6, 2.4],
        mode="markers", marker=dict(opacity=0, size=1)))
    fig.update_layout(
        shapes=shapes, annotations=annotations,
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        height=180,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="#F0F7FF",
        plot_bgcolor="#F0F7FF",
        showlegend=False)
    return fig


def moment_diag_fig(rv):
    """
    Moment diagram figure with correct half-circle moment arc symbols.

    Layout
    ------
    - Vertical dashed grey line = member neutral axis
    - Filled area = linear moment diagram
        positive moment → filled RIGHT of axis  (blue)
        negative moment → filled LEFT  of axis  (red)
        zero crossing shown if Mf1 and Mf2 have opposite signs
    - Half-circle arc at each end, centred on the axis:
        Positive (+, CCW):  arc on the RIGHT side
                            arrowhead at the LEFT end of arc (pointing DOWN)
        Negative (−, CW):   arc on the LEFT  side
                            arrowhead at the RIGHT end of arc (pointing DOWN)
    - Arc radius scales proportionally with moment magnitude
    - kappa / omega1 summary box
    """
    Mf2x = rv.get("Mf2x", rv["Mfx"]) / 1e6
    Mf1x = rv.get("Mf1x", rv["Mfx"] * rv["k"]) / 1e6
    Mf2y = rv.get("Mf2y", rv["Mfy"]) / 1e6
    Mf1y = rv.get("Mf1y", rv["Mfy"] * rv.get("kwy", 1.0)) / 1e6
    k     = rv["k"]
    bf_mm = rv["bf"]
    H     = max(1.0 * 2 * min(rv["L"] / bf_mm, 20), 4.0)
    POS_C = "#1565C0"
    NEG_C = "#DC2626"
    shapes, annotations, traces = [], [], []

    def draw_arc(cy, Mval, R, color):
        """Half-circle moment arc centred at (0, cy).
        positive (+, CCW): arc on RIGHT, arrowhead points DOWN at left end
        negative (-, CW):  arc on LEFT,  arrowhead points DOWN at right end
        """
        positive = (Mval >= 0)
        theta = np.linspace(0, math.pi, 80)
        if positive:
            xs = R * np.cos(theta)          # +R -> 0 -> -R  (right side)
            ys = cy + R * np.sin(theta)
            x_tip, y_tip   = -R, cy         # end of arc = left point
            x_tail, y_tail = -R, cy + R*0.3 # tail above tip
        else:
            xs = -R * np.cos(theta)         # -R -> 0 -> +R  (left side)
            ys = cy + R * np.sin(theta)
            x_tip, y_tip   =  R, cy         # end of arc = right point
            x_tail, y_tail =  R, cy + R*0.3
        traces.append(go.Scatter(x=xs, y=ys, mode="lines",
            line=dict(color=color, width=3.5),
            showlegend=False, hoverinfo="skip"))
        annotations.append(dict(
            ax=x_tail, ay=y_tail, axref="x", ayref="y",
            x=x_tip,   y=y_tip,   xref="x",  yref="y",
            arrowhead=3, arrowsize=1.3, arrowwidth=2.8, arrowcolor=color,
            showarrow=True, text=""))
        sign_s = "+" if positive else "\u2212"
        rot_s  = "\u21ba CCW (+)" if positive else "\u21bb CW (\u2212)"
        lx = R + 0.25 if positive else -R - 0.25
        la = "left" if positive else "right"
        annotations.append(dict(x=lx, y=cy + R*0.6,
            text=f"<b>{sign_s}{abs(Mval):.0f} kN\u00b7m</b>",
            xanchor=la, yanchor="middle", showarrow=False,
            font=dict(size=11, color=color)))
        annotations.append(dict(x=lx, y=cy + R*0.1,
            text=rot_s, xanchor=la, yanchor="middle", showarrow=False,
            font=dict(size=9, color=color)))

    if abs(Mf2x) > 0:
        SC  = 2.0
        m2s =  SC
        m1s = (Mf1x / abs(Mf2x)) * SC
        # Neutral axis
        shapes.append(dict(type="line", x0=0, y0=0, x1=0, y1=H,
            line=dict(color="#BBBBBB", width=1.5, dash="dash")))
        # Moment diagram area
        if m1s * m2s >= 0:
            col = POS_C if m2s >= 0 else NEG_C
            fc  = "rgba(21,101,192,0.15)" if m2s >= 0 else "rgba(220,38,38,0.12)"
            shapes.append(dict(type="path",
                path=f"M 0,0 L {m1s:.3f},0 L {m2s:.3f},{H:.3f} L 0,{H:.3f} Z",
                fillcolor=fc, line=dict(color=col, width=2.0)))
        else:
            yz = H * abs(m1s) / (abs(m1s) + abs(m2s))
            shapes.append(dict(type="path",
                path=f"M 0,0 L {m1s:.3f},0 L 0,{yz:.3f} Z",
                fillcolor="rgba(220,38,38,0.12)",
                line=dict(color=NEG_C, width=2.0)))
            shapes.append(dict(type="path",
                path=f"M 0,{yz:.3f} L {m2s:.3f},{H:.3f} L 0,{H:.3f} Z",
                fillcolor="rgba(21,101,192,0.15)",
                line=dict(color=POS_C, width=2.0)))
            shapes.append(dict(type="line",
                x0=-0.15, y0=yz, x1=0.15, y1=yz,
                line=dict(color="#444", width=1.5)))
            annotations.append(dict(x=0.22, y=yz, text="M = 0",
                xanchor="left", yanchor="middle", showarrow=False,
                font=dict(size=8, color="#555")))
        # Arc symbols — radius proportional to magnitude
        R2 = min(H * 0.20, 1.4)
        R1 = max(R2 * min(abs(Mf1x) / abs(Mf2x), 1.0), 0.35) if abs(Mf1x) > 0 else 0
        draw_arc(H, Mf2x, R2, POS_C if Mf2x >= 0 else NEG_C)
        if abs(Mf1x) > 0:
            draw_arc(0, Mf1x, R1, POS_C if Mf1x >= 0 else NEG_C)
        # kappa / omega1 box
        kc  = POS_C if k >= 0 else NEG_C
        om1 = max(0.6 - 0.4*k, 0.4)
        curv = "Double courbure \u2713" if k >= 0 else "Courbure simple"
        annotations.append(dict(x=SC*0.55, y=H*0.5,
            text=f"\u03ba = {k:.2f}<br><b>{curv}</b><br>\u03c9\u2081 = {om1:.3f}",
            xanchor="left", yanchor="middle", showarrow=False,
            font=dict(size=9, color=kc),
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=kc, borderwidth=1.5, borderpad=4))

    # Mfy weak-axis arcs if biaxial
    if abs(Mf2y) > 0:
        R2y = min(H * 0.14, 1.0)
        R1y = max(R2y * min(abs(Mf1y)/abs(Mf2y),1.0), 0.25) if abs(Mf1y)>0 else 0
        draw_arc(H, Mf2y, R2y, "#C45000")
        if abs(Mf1y) > 0:
            draw_arc(0, Mf1y, R1y, "#C45000")

    # Convention legend
    annotations.append(dict(x=0, y=-min(H*0.16, 1.4),
        text="<b>Convention :</b>  + = \u21ba CCW (arc droite)   \u2212 = \u21bb CW (arc gauche)",
        xanchor="center", yanchor="top", showarrow=False,
        font=dict(size=8, color="#555")))

    R_max = min(H * 0.20, 1.4)
    pad_x = SC + R_max + 1.8
    pad_y = R_max + H * 0.18
    fig = go.Figure(data=traces)
    fig.add_trace(go.Scatter(x=[-pad_x,pad_x], y=[-pad_y,H+pad_y],
        mode="markers", marker=dict(opacity=0,size=1)))
    fig.update_layout(shapes=shapes, annotations=annotations,
        xaxis=dict(visible=False,scaleanchor="y",scaleratio=1),
        yaxis=dict(visible=False),height=500,
        margin=dict(l=5,r=5,t=5,b=5),
        paper_bgcolor="white",plot_bgcolor="white",showlegend=False)
    return fig


def member_fig(rv):
    """Backward-compat alias — returns column_fig only."""
    return column_fig(rv)


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTLY: STACKED INTERACTION BAR
# ═══════════════════════════════════════════════════════════════════════════════
def stacked_bar(terms, labels, colors, ratio, title):
    fig = go.Figure()
    left = 0
    for t, lbl, col in zip(terms, labels, colors):
        r,g,b = tuple(int(col.lstrip("#")[i:i+2],16) for i in (0,2,4))
        fig.add_trace(go.Bar(
            x=[t], y=[""], orientation="h", base=left,
            marker=dict(color=f"rgba({r},{g},{b},0.20)",
                        line=dict(color=col,width=2.0)),
            text=f"<b>{t:.4f}</b>",
            textposition="inside", insidetextanchor="middle",
            textfont=dict(color=col,size=12,family="monospace"),
            name=lbl,
            hovertemplate=f"<b>{lbl}</b><br>Value: {t:.4f}<extra></extra>"))
        left += t
    fig.add_vline(x=1.0, line=dict(color="#333",width=2.5,dash="dash"))
    fig.add_annotation(x=1.02, y=0, text=f"<b>{vt(ratio)}</b>",
        showarrow=False, xanchor="left", font=dict(size=13, color=rclr(ratio)))
    fig.add_annotation(x=1.0, y=0.42, text="Limit = 1.0",
        showarrow=False, font=dict(size=8, color="#444"))
    fig.update_layout(
        barmode="stack",
        title=dict(text=title, font=dict(size=11,color=BL)),
        xaxis=dict(range=[0,1.75], showgrid=True, gridcolor="#EEE"),
        yaxis=dict(showticklabels=False),
        legend=dict(orientation="h", y=-0.52, x=0, font=dict(size=10)),
        height=185, margin=dict(l=5,r=5,t=35,b=72),
        paper_bgcolor="white", plot_bgcolor="white")
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTLY: COLUMN CURVE
# ═══════════════════════════════════════════════════════════════════════════════
def col_curve_fig(rv, axis="x"):
    phi=rv["phi"]; A=rv["A"]; Fy=rv["Fy"]; E=rv["E"]; Cr0=phi*A*Fy
    klr_v = np.linspace(0.5, 260, 500)
    crv = [phi*A*Fy*(1+math.sqrt(Fy/(math.pi**2*E/klr**2))**2.68)**(-1/1.34)/Cr0
           for klr in klr_v]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=klr_v, y=crv, mode="lines",
        line=dict(color=BL, width=2.5),
        fill="tozeroy", fillcolor="rgba(21,101,192,0.07)",
        name="Column curve  Cr/(φAFy)"))
    if axis=="x":
        klr_pt,Cr_pt,col=rv["KLx_rx"],rv["Crx"],OR
        lbl=f"Strong-axis<br>KLx/rx={klr_pt:.1f}<br>Cr={Cr_pt/1e3:.0f} kN<br>Cr/A={rv['CrA_x']:.0f} MPa"
    else:
        klr_pt,Cr_pt,col=rv["KLy_ry"],rv["Cry"],RD
        lbl=f"Weak-axis (governs)<br>KLy/ry={klr_pt:.1f}<br>Cr={Cr_pt/1e3:.0f} kN<br>Cr/A={rv['CrA_y']:.0f} MPa"
    yr = Cr_pt/Cr0
    fig.add_trace(go.Scatter(x=[0,klr_pt,klr_pt],y=[yr,yr,0],mode="lines",
        line=dict(color=col,width=1.2,dash="dot"),showlegend=False))
    fig.add_trace(go.Scatter(x=[klr_pt],y=[yr],mode="markers+text",
        marker=dict(size=12,color=col,line=dict(color="white",width=2)),
        text=[lbl], textposition="top right",
        textfont=dict(size=9,color=col), name=lbl))
    fig.update_layout(
        xaxis=dict(title="KL/r",range=[0,260],showgrid=True,gridcolor="#EEE"),
        yaxis=dict(title="Cr/(φAFy)",range=[0,1.15],showgrid=True,gridcolor="#EEE"),
        height=310, margin=dict(l=50,r=10,t=20,b=50),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(x=0.5,y=0.98,font=dict(size=9)))
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTLY: SLENDERNESS BARS
# ═══════════════════════════════════════════════════════════════════════════════
def slender_fig(rv):
    """
    Clean classification chart:
      Left group  (x = 0,1,2,3): Actual b/(2tf) | Cl.1 limit | Cl.2 limit | Cl.3 limit
      Right group (x = 5,6,7,8): Actual h/tw    | Cl.1 limit | Cl.2 limit | Cl.3 limit
    One actual bar per group — no repetition.
    A dashed horizontal line across the limits shows where the actual value sits.
    """
    cf_col = [GR,GR,GO,RD][rv["cf"]-1]
    cw_col = [GR,GR,GO,RD][rv["cw"]-1]

    def rgba(hex_col, alpha):
        r,g,b = tuple(int(hex_col.lstrip("#")[i:i+2],16) for i in (0,2,4))
        return f"rgba({r},{g},{b},{alpha})"

    fig = go.Figure()

    # ── FLANGE group (positions 0,1,2,3) ──────────────────────────────────
    flange_data = [
        ("Actual<br>b/(2tf)", rv["b2tf"],  cf_col, 0.85),   # actual – solid
        ("Cl. 1 limit",       rv["fl"][1], GR,     0.20),   # Class 1 limit
        ("Cl. 2 limit",       rv["fl"][2], GO,     0.20),   # Class 2 limit
        ("Cl. 3 limit",       rv["fl"][3], RD,     0.20),   # Class 3 limit
    ]
    for i, (lbl, val, col, alpha) in enumerate(flange_data):
        fig.add_trace(go.Bar(
            x=[i], y=[val],
            marker=dict(color=rgba(col, alpha), line=dict(color=col, width=2.0)),
            text=[f"<b>{val:.2f}</b>"], textposition="outside",
            textfont=dict(size=10, color=col),
            name=lbl, showlegend=False,
            hovertemplate=f"<b>{lbl}</b><br>{val:.2f}<extra></extra>"))

    # Horizontal dashed line at actual b/(2tf) across the three limit bars
    fig.add_shape(type="line",
        x0=0.5, x1=3.5, y0=rv["b2tf"], y1=rv["b2tf"],
        line=dict(color=cf_col, width=1.5, dash="dot"))

    # ── WEB group (positions 5,6,7,8 — gap at 4) ──────────────────────────
    web_data = [
        ("Actual<br>h/tw",    rv["htw"],   cw_col, 0.85),
        ("Cl. 1 limit",       rv["wb"][1], GR,     0.20),
        ("Cl. 2 limit",       rv["wb"][2], GO,     0.20),
        ("Cl. 3 limit",       rv["wb"][3], RD,     0.20),
    ]
    for i, (lbl, val, col, alpha) in enumerate(web_data):
        fig.add_trace(go.Bar(
            x=[i+5], y=[val],
            marker=dict(color=rgba(col, alpha), line=dict(color=col, width=2.0)),
            text=[f"<b>{val:.2f}</b>"], textposition="outside",
            textfont=dict(size=10, color=col),
            name=lbl, showlegend=False,
            hovertemplate=f"<b>{lbl}</b><br>{val:.2f}<extra></extra>"))

    # Horizontal dashed line at actual h/tw across the three limit bars
    fig.add_shape(type="line",
        x0=5.5, x1=8.5, y0=rv["htw"], y1=rv["htw"],
        line=dict(color=cw_col, width=1.5, dash="dot"))

    # ── Separator between groups ───────────────────────────────────────────
    max_val = max(rv["fl"][3], rv["wb"][3], rv["b2tf"], rv["htw"])
    fig.add_shape(type="line",
        x0=4, x1=4, y0=0, y1=max_val*1.25,
        line=dict(color="#BBBBBB", width=1.5, dash="dash"))

    # ── Group labels ───────────────────────────────────────────────────────
    fig.add_annotation(x=1.5, y=max_val*1.22,
        text=f"<b>AILE  →  Classe {rv['cf']}</b>",
        showarrow=False, font=dict(size=12, color=cf_col))
    fig.add_annotation(x=6.5, y=max_val*1.22,
        text=f"<b>ÂME  →  Classe {rv['cw']}</b>",
        showarrow=False, font=dict(size=12, color=cw_col))

    # ── x-axis tick labels ─────────────────────────────────────────────────
    tick_vals = [0,1,2,3,  5,6,7,8]
    tick_text = ["Actual<br>b/(2tf)","Cl. 1","Cl. 2","Cl. 3",
                 "Actual<br>h/tw",   "Cl. 1","Cl. 2","Cl. 3"]

    fig.update_layout(
        xaxis=dict(tickvals=tick_vals, ticktext=tick_text,
                   tickfont=dict(size=10), showgrid=False),
        yaxis=dict(title="Rapport d'élancement", showgrid=True,
                   gridcolor="#EEE", range=[0, max_val*1.30]),
        height=320, margin=dict(l=55, r=10, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        bargap=0.25,
    )
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTLY: SENSITIVITY
# ═══════════════════════════════════════════════════════════════════════════════
def sensitivity_fig(rv):
    bCf=rv["Cf"]/1e3; bMfx=rv["Mfx"]/1e6
    Cf_v  = np.linspace(50, max(bCf*2.1,500), 70)
    Mfx_v = np.linspace(10, max(bMfx*2.1,100), 70)
    def sw(arr, is_Cf):
        r2v,r3av,r3bv=[],[],[]
        for x in arr:
            try:
                a=compute(rv["sn"],x if is_Cf else bCf,
                          bMfx if is_Cf else x,
                          rv["Mfy"]/1e6,rv["L"],rv["Kx"],rv["Ky"],rv["k"],rv["om2"])
                r2v.append(a["r2"]); r3av.append(a["r3a"]); r3bv.append(a["r3b"])
            except: r2v.append(np.nan); r3av.append(np.nan); r3bv.append(np.nan)
        return r2v,r3av,r3bv
    r2c,r3ac,r3bc=sw(Cf_v,True); r2m,r3am,r3bm=sw(Mfx_v,False)
    fig=make_subplots(1,2,subplot_titles=(
        f"vs Cf  (Mfx={bMfx:.0f} kN·m)",f"vs Mfx  (Cf={bCf:.0f} kN)"))
    for ci,(xv,r2v,r3av,r3bv,xpt,xl) in enumerate([
        (Cf_v,r2c,r3ac,r3bc,bCf,"Cf (kN)"),
        (Mfx_v,r2m,r3am,r3bm,bMfx,"Mfx (kN·m)")],1):
        sl=ci==1
        fig.add_trace(go.Scatter(x=xv,y=r2v,name="② Vérif. section",line=dict(color=TL,width=2.5),showlegend=sl),row=1,col=ci)
        fig.add_trace(go.Scatter(x=xv,y=r3av,name="③ Pièce sans dévers.",line=dict(color=OR,width=2.5),showlegend=sl),row=1,col=ci)
        fig.add_trace(go.Scatter(x=xv,y=r3bv,name="④ Pièce avec dévers.",line=dict(color=PU,width=2.5),showlegend=sl),row=1,col=ci)
        fig.add_hline(y=1.0,line=dict(color=RD,width=2,dash="dash"),row=1,col=ci)
        fig.add_vline(x=xpt,line=dict(color=GO,width=1.5,dash="dot"),row=1,col=ci)
        for yv,c in zip([rv["r2"],rv["r3a"],rv["r3b"]],[TL,OR,PU]):
            fig.add_trace(go.Scatter(x=[xpt],y=[yv],mode="markers",
                marker=dict(size=10,color=c,line=dict(color="white",width=1.5)),showlegend=False),row=1,col=ci)
    fig.update_layout(height=360,paper_bgcolor="white",plot_bgcolor="white",
        legend=dict(orientation="h",y=-0.18,x=0.3),margin=dict(l=50,r=10,t=50,b=60))
    fig.update_xaxes(showgrid=True,gridcolor="#EEE")
    fig.update_yaxes(showgrid=True,gridcolor="#EEE",range=[0,None])
    for ci,xl in enumerate(["Cf (kN)","Mfx (kN·m)"],1):
        fig.update_xaxes(title_text=xl,col=ci)
    fig.update_yaxes(title_text="Interaction ratio",col=1)
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
<div style="background:linear-gradient(135deg,#0A1628,#1565C0);border-radius:12px;
            padding:18px 16px 14px;margin-bottom:14px;text-align:center">
  <div style="font-size:2rem;margin-bottom:4px">🏗️</div>
  <div style="font-size:1.0rem;font-weight:800;color:white;line-height:1.3">
    GCI 2011
  </div>
  <div style="font-size:.78rem;color:#93C5FD;margin-top:2px">
    Conception de Structures I
  </div>
  <div style="font-size:.72rem;color:#64A5D6;margin-top:1px">
    Université Laval
  </div>
  <div style="margin-top:8px;background:rgba(255,255,255,.12);border-radius:8px;
              padding:4px 10px;font-size:.72rem;color:#BAD4F5;border:1px solid rgba(255,255,255,.2)">
    Poteau-poutre en acier · CSA S16-24 Cl. 13
  </div>
</div>
""", unsafe_allow_html=True)
    st.markdown("### Section  (Table T1 — CISC HSC)")
    fam = st.selectbox("Family", list(FAMILIES.keys()), index=6)   # W310 default
    sn  = st.selectbox("Section", FAMILIES[fam],
                       index=min(13, len(FAMILIES[fam])-1))         # W310×118 default
    s   = SECTIONS[sn]
    st.markdown(
        f'<div class="ibox">Fy = <b>{s["Fy"]} MPa</b>  |  '
        f'A = <b>{s["A"]:,} mm²</b><br>'
        f'rx = <b>{s["rx"]} mm</b>  |  ry = <b>{s["ry"]} mm</b><br>'
        f'd = <b>{s["d"]} mm</b>  |  bf = <b>{s["bf"]} mm</b>  |  '
        f'tf = <b>{s["tf"]} mm</b>  |  tw = <b>{s["tw"]} mm</b></div>',
        unsafe_allow_html=True)

    st.markdown("### Charge axiale")
    max_Cf   = max(100, int(0.9*s["A"]*s["Fy"]/1e3/50)*50)
    Cf_kN   = st.slider("Cf  (kN)", 50.0, float(max_Cf),
                         min(2000.0, max_Cf*.45), 25.0,
                         help="Force de compression axiale pondérée")

    st.markdown("### Geometry")
    L_mm = st.slider("L  (mm)", 1000.0, 15000.0, 3700.0, 100.0)
    Kx   = st.select_slider("Kx", [0.5,0.65,0.7,1.0,1.2,1.5,2.0], value=1.0)
    Ky   = st.select_slider("Ky", [0.5,0.65,0.7,1.0,1.2,1.5,2.0], value=1.0)

    st.markdown("### Diagramme de moment  [HSC 13.8.5]")
    st.markdown("""<div style="font-size:.75rem;color:#94A3B8;line-height:1.6;
                               background:rgba(255,255,255,.06);border-radius:8px;
                               padding:8px 12px;margin-bottom:8px">
<b style="color:#60A5FA">Convention de signe :</b><br>
Mf2 = moment à l'extrémité <b>plus chargée</b> (toujours &gt; 0 ici)<br>
Mf1 = moment à l'autre extrémité (même sens → négatif → double courbure)<br>
κ = Mf1/Mf2 &nbsp;→&nbsp; <b>κ &gt; 0</b> = double courbure ✓ (Mf1 et Mf2 de même signe)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>κ &lt; 0</b> = courbure simple  (Mf1 et Mf2 de signes opposés)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>κ = 0</b> = moment nul à une extrémité<br>
ω1 = 0.6 − 0.4·κ &nbsp;≥&nbsp; 0.4  [HSC 13.8.5]
</div>""", unsafe_allow_html=True)

    # Mf2 is the larger-end moment (always positive reference)
    # Mf1 is the other-end moment — can be negative (single curv) or positive (double curv)
    # κ = Mf1/Mf2  is computed automatically
    max_Mfx_val = max(50.0, float(int(0.9*s["Zx"]*s["Fy"]/1e6/10)*10))
    Mf2x = st.slider("Mf2  axe fort (kN·m)  [extrémité max]",
                     10.0, max_Mfx_val, min(300.0, max_Mfx_val*0.45), 10.0,
                     help="Moment à l'extrémité la plus sollicitée (valeur de référence, toujours positif)")
    Mf1x = st.slider("Mf1  axe fort (kN·m)  [autre extrémité]",
                     -max_Mfx_val, max_Mfx_val, Mf2x*0.67, 10.0,
                     help="Même signe que Mf2 → double courbure κ>0 (favorable)\n"
                          "Signe opposé → courbure simple κ<0 (défavorable)")
    # κ = Mf1/Mf2 — clamp to [-1, 1], ensure |Mf1| ≤ |Mf2|
    k_ratio = max(-1.0, min(1.0, Mf1x / Mf2x)) if abs(Mf2x) > 0 else 0.0

    # Visual indicator
    if k_ratio > 0.0:
        curv_note = f"κ = {Mf1x:.0f}/{Mf2x:.0f} = <b>{k_ratio:.3f}</b> &nbsp;→&nbsp; ✅ Double courbure (ω1 = {max(0.6-0.4*k_ratio,0.4):.3f} ≤ 1)"
        curv_col  = "#22C55E"
    elif k_ratio < 0.0:
        curv_note = f"κ = {Mf1x:.0f}/{Mf2x:.0f} = <b>{k_ratio:.3f}</b> &nbsp;→&nbsp; ⚠️ Courbure simple (ω1 = {max(0.6-0.4*k_ratio,0.4):.3f} = max)"
        curv_col  = "#F59E0B"
    else:
        curv_note = f"κ = 0 &nbsp;→&nbsp; Moment nul à une extrémité (ω1 = 0.6)"
        curv_col  = "#60A5FA"
    st.markdown(f'<div style="font-size:.8rem;color:{curv_col};font-weight:600;'
                f'background:rgba(255,255,255,.07);border-radius:6px;padding:5px 10px;'
                f'margin-bottom:4px">{curv_note}</div>', unsafe_allow_html=True)

    max_Mfy_val = max(10.0, float(int(0.9*s["Zy"]*s["Fy"]/1e6/5)*5))
    Mf2y = st.slider("Mf2  axe faible (kN·m)  [extrémité max]",
                     0.0, max_Mfy_val, 0.0, max(1.0, float(max_Mfy_val)//50),
                     help="Moment axe faible à l'extrémité max (biaxiale)")
    Mf1y = st.slider("Mf1  axe faible (kN·m)  [autre extrémité]",
                     -max_Mfy_val, max_Mfy_val, 0.0, max(1.0, float(max_Mfy_val)//50),
                     help="Même signe → double courbure  |  Signe opposé → courbure simple")
    kwy_ratio = max(-1.0, min(1.0, Mf1y / Mf2y)) if abs(Mf2y) > 0 else 0.0
    if Mf2y > 0:
        st.markdown(f'<div style="font-size:.78rem;color:#94A3B8;padding:3px 10px">'
                    f'κy = {Mf1y:.0f}/{Mf2y:.0f} = <b>{kwy_ratio:.3f}</b></div>',
                    unsafe_allow_html=True)

    # Mfx_kNm and Mfy_kNm for compute = Mf2 (the governing end moment)
    Mfx_kNm = Mf2x
    Mfy_kNm = Mf2y

    omega2 = st.slider("ω₂  (gradient LTB, axe fort)", 0.6, 2.5, 1.0, 0.05,
        help="Facteur de gradient de moment pour le déversement [HSC 13.6]\n"
             "1.0 = moment uniforme (conservateur)\n"
             "1.75 + 1.05κ + 0.3κ² ≤ 2.5 (calculé manuellement)")

    st.markdown("### Contreventement et U2  [HSC 13.8.4]")
    braced_choice = st.radio("Type de structure",
        ["Contreventée", "Non contreventée"],
        index=0,
        help="Contreventée : U1 calculé par axe (effet P-δ)\n"
             "Non contreventée : U1=1.0, Mf amplifié par U2 (effet P-Δ)")
    braced = (braced_choice == "Contreventée")
    U2_val = 1.0
    if not braced:
        U2_val = st.number_input(
            "U2  (amplification P-Δ de l'étage)", 1.00, 5.00, 1.00, 0.05,
            help="U2 ≥ 1/(1 − ΣCf/ΣCe_étage)  [HSC Cl. 8.7]\n"
                 "Mfx et Mfy seront multipliés par U2 avant les vérifications.")
        st.markdown(
            '<div class="ibox">⚠️ <b>Structure non contreventée</b><br>'
            'U1x = U1y = 1.0 (P-δ non re-calculé)<br>'
            f'Mf × U2 = Mf × {U2_val:.2f} appliqué dans toutes les vérifications.</div>',
            unsafe_allow_html=True)

    st.markdown("### Type de section  [HSC 13.3.1]")
    sec_type = st.radio("Fabrication",
        ["hot-rolled", "welded"],
        format_func=lambda x:
            "Laminée à chaud  (n = 1.34)" if x == "hot-rolled"
            else "Soudée / WWF       (n = 2.24)",
        help="n = 1.34  sections laminées à chaud\n"
             "n = 2.24  sections soudées (WWF)  [HSC 13.3.1]")

    st.markdown("""
<div style="margin-top:8px;background:rgba(255,255,255,.06);border-radius:10px;
            padding:12px 14px;border:1px solid rgba(255,255,255,.12)">
  <div style="font-size:.7rem;color:#94A3B8;line-height:1.9;text-align:center">
    <span style="color:#60A5FA;font-weight:700">φ = 0.90</span> &nbsp;·&nbsp;
    E = 200 000 MPa &nbsp;·&nbsp; G = 77 000 MPa<br>
    <span style="color:#60A5FA">CISC HSC 13e éd.</span> T1·T2·T3<br>
    <span style="color:#60A5FA">CSA S16-24</span> Cl. 13<br>
    <span style="color:#64748B;font-size:.65rem">Prof. Luca Sorelli, ing., Ph.D.</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  COMPUTE
# ═══════════════════════════════════════════════════════════════════════════════
rv = compute(sn, Cf_kN, Mfx_kNm, Mfy_kNm, L_mm,
             Kx=Kx, Ky=Ky, k=k_ratio, kwy=kwy_ratio,
             om2=omega2, braced=braced, U2=U2_val,
             sec_type=sec_type)
# Store Mf1 values for member diagram
rv["Mf1x"] = Mf1x * 1e6   # N·mm
rv["Mf1y"] = Mf1y * 1e6
rv["Mf2x"] = Mf2x * 1e6
rv["Mf2y"] = Mf2y * 1e6

# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER  &  KPI STRIP
# ═══════════════════════════════════════════════════════════════════════════════
# ── Course / author header ───────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
    <div>
      <div style="font-size:1.55rem;font-weight:800;color:white;line-height:1.2;letter-spacing:-.01em">
        🏗️ Vérification d'un poteau-poutre en acier
      </div>
      <div style="font-size:.95rem;color:#93C5FD;margin-top:3px;font-weight:500">
        CSA S16-24 Cl. 13 &nbsp;·&nbsp; CISC HSC T1 · T2 · T3
      </div>
    </div>
    <div style="text-align:right">
      <div style="font-size:.95rem;font-weight:700;color:white">
        GCI 2011 — Conception de Structures I
      </div>
      <div style="font-size:.82rem;color:#BAD4F5;margin-top:2px">
        Université Laval &nbsp;·&nbsp; Prof. Luca Sorelli, ing., Ph.D.
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Persistent disclaimer banner — visible on every page
st.markdown("""
<div class="edu-banner">
  ⚠️ <strong>FOR EDUCATIONAL USE ONLY — GCI 2011, Université Laval (Prof. Luca Sorelli).</strong>
  Results must not be used for the design or verification of any real structure.
  No liability is accepted for any use outside the classroom.
  Always consult a licensed professional engineer for real projects.
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4,c5,c6 = st.columns(6)
def kpi(v, lbl, col, border_col=None):
    bc = border_col or col
    return (f'<div class="kpi" style="border-top-color:{bc}">'
            f'<div class="kpi-l">{lbl}</div>'
            f'<div class="kpi-v" style="color:{col}">{v}</div></div>')
c1.markdown(kpi(f"Classe {rv['cls']}", "Classe de la section",
    [GR,GR,GO,RD][rv["cls"]-1]), unsafe_allow_html=True)
c2.markdown(kpi(f"{rv['r2']:.4f}", "② Vérif. section",
    rclr(rv["r2"])), unsafe_allow_html=True)
c3.markdown(kpi(f"{rv['r3a']:.4f}", "③ Sans déversement",
    rclr(rv["r3a"])), unsafe_allow_html=True)
c4.markdown(kpi(f"{rv['r3b']:.4f}", "④ Avec déversement",
    rclr(rv["r3b"])), unsafe_allow_html=True)
c5.markdown(kpi(f"{rv['gov']:.4f}", "GOUVERNANT",
    rclr(rv["gov"])), unsafe_allow_html=True)
c6.markdown(kpi("✓ ADÉQUAT" if rv["ok"] else "✗ INADÉQUAT", "VERDICT",
    GR if rv["ok"] else RD), unsafe_allow_html=True)
st.markdown("<div style='margin:4px 0 12px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════════════════════
t0,t1,t2,t3,t4,t5 = st.tabs([
    "📐 Propriétés de la section",
    "① Classification de la section",
    "② Vérification de la section",
    "③ Vérification de la pièce  — sans déversement",
    "④ Vérification de la pièce  — avec déversement",
    "📈 Analyse de sensibilité",
])

# ── Tab 0: Section ──────────────────────────────────────────────────────────
with t0:
    st.markdown("## Propriétés de la section  (Table T1 — CISC HSC)")
    ca, cm, cn, cb = st.columns([1, 0.75, 0.9, 1.5])
    with ca:
        st.markdown("### Section transversale")
        st.plotly_chart(section_fig(rv), use_container_width=True, key="sec0")
    with cm:
        st.markdown("### Pièce — Cf")
        st.plotly_chart(column_fig(rv), use_container_width=True, key="col0")
    with cn:
        st.markdown("### Diagramme de moment")
        st.plotly_chart(convention_fig(), use_container_width=True, key="conv0")
        st.plotly_chart(moment_diag_fig(rv), use_container_width=True, key="mdf0")
    with cb:
        st.markdown("### Propriétés — HSC T1")
        rows=[
            ("A",  f"{rv['A']:,}","mm²","Gross area → φCy = φ·A·Fy"),
            ("d",  f"{rv['d']}","mm","Overall depth"),
            ("bf", f"{rv['bf']}","mm","Flange width"),
            ("tf", f"{rv['tf']}","mm","Flange thickness  → b/(2tf) slenderness"),
            ("tw", f"{rv['tw']}","mm","Web thickness  → h/tw slenderness"),
            ("h",  f"{rv['h']}","mm","Clear web height = d − 2tf"),
            ("Ix", f"{rv['Ix']/1e6:.0f}","×10⁶ mm⁴","Strong-axis second moment"),
            ("Zx", f"{rv['Zx']/1e3:.0f}","×10³ mm³",f"Plastic mod. → Mrx = {rv['Mrx_s']/1e6:.0f} kN·m (Class {rv['cls']})"),
            ("Sx", f"{rv['Sx']/1e3:.0f}","×10³ mm³","Elastic mod. → Mrx for Class 3"),
            ("rx", f"{rv['rx']}","mm",f"r-of-gyr. strong-axis → KLx/rx = {rv['KLx_rx']:.1f}"),
            ("Iy", f"{rv['Iy']/1e6:.2f}","×10⁶ mm⁴","Weak-axis second moment"),
            ("Zy", f"{rv['Zy']/1e3:.0f}","×10³ mm³",f"Plastic mod. → Mry = {rv['Mry_s']/1e6:.0f} kN·m"),
            ("Sy", f"{rv['Sy']/1e3:.0f}","×10³ mm³","Elastic mod. weak-axis"),
            ("ry", f"{rv['ry']}","mm",f"r-of-gyr. weak-axis → KLy/ry = {rv['KLy_ry']:.1f}"),
            ("J",  f"{rv['J']/1e3:.0f}","×10³ mm⁴","St-Venant torsion → LTB resistance"),
            ("Cw", f"{rv['Cw']/1e9:.0f}","×10⁹ mm⁶","Warping constant → LTB resistance"),
            ("Lu", f"{rv['Lu']:,}","mm","Max unbraced length without LTB (Table T3)"),
            ("Fy", f"{rv['Fy']}","MPa","Yield strength (G40.21 350W / A992)"),
        ]
        st.markdown("| Prop | Value | Unit | Role in design |\n|:--|--:|:--|:--|")
        for nm,val,un,desc in rows:
            st.markdown(f"| **{nm}** | {val} | {un} | {desc} |")

    st.markdown("### Computed section capacities")
    _mrx_lbl = "Mrx = φ·Zx·Fy" if rv['cls']<=2 else "Mrx = φ·Sx·Fy"
    _mrx_mod = f"{rv['Zx']/1e3:.0f}" if rv['cls']<=2 else f"{rv['Sx']/1e3:.0f}"
    st.markdown(f"""<div class="fbox">
<b>Résistances de la section  [HSC 13.5]</b><br>
φCy = φ·A·Fy = {rv['phi']}×{rv['A']:,}×{rv['Fy']} = <b>{rv['pCy']/1e3:.1f} kN</b>  (charge d'écrasement, sans flambement)<br>
{_mrx_lbl} = {rv['phi']}×{_mrx_mod}×10³×{rv['Fy']} = <b>{rv['Mrx_s']/1e6:.1f} kN·m</b>  (Classe {rv['cls']})<br>
Mry = φ·Zy·Fy = {rv['phi']}×{rv['Zy']/1e3:.0f}×10³×{rv['Fy']} = <b>{rv['Mry_s']/1e6:.1f} kN·m</b>  (axe faible, sans déversement)<br><br>
<b>Forces d'Euler critiques  [HSC 13.8.4]</b><br>
Cex = π²·E·A/(KLx/rx)² = π²×{rv['E']:.0f}×{rv['A']:,}/{rv['KLx_rx']:.1f}² = <b>{rv['Cex']/1e3:.1f} kN</b><br>
Cey = π²·E·A/(KLy/ry)² = π²×{rv['E']:.0f}×{rv['A']:,}/{rv['KLy_ry']:.1f}² = <b>{rv['Cey']/1e3:.1f} kN</b><br><br>
<b>Élancement réduit  [HSC 13.3.1]</b><br>
λ̄x = √(Fy/Fex) = √({rv['Fy']}/{rv['Fex']:.1f}) = <b>{rv['lx']:.4f}</b>  (axe fort)<br>
λ̄y = √(Fy/Fey) = √({rv['Fy']}/{rv['Fey']:.1f}) = <b>{rv['ly']:.4f}</b>  (axe faible — gouvernant pour Cr et β)<br>
λ̄_max = <b>{rv['lam_max']:.4f}</b>  (utilisé pour Cr en flexion biaxiale)<br><br>
<b>Résistance en compression  [HSC 13.3.1]</b>  n = {rv['n']}<br>
Crx = φ·A·Fy·(1+λ̄x^(2n))^(-1/n) = <b>{rv['Crx']/1e3:.1f} kN</b>  |  Cr/A = <b>{rv['CrA_x']:.1f} MPa</b>  (Table T2)<br>
Cry = φ·A·Fy·(1+λ̄y^(2n))^(-1/n) = <b>{rv['Cry']/1e3:.1f} kN</b>  |  Cr/A = <b>{rv['CrA_y']:.1f} MPa</b>  (Table T2 — gouvernant)<br><br>
<b>Vérification du déversement  [HSC 13.6]</b><br>
Lb = {rv['L']:.0f} mm  |  Lu = {rv['Lu']:,} mm  →  {'✅ Lb ≤ Lu : Mrx* = Mp (aucun déversement)' if rv['ltb_ok'] else '⚠️ Lb > Lu : le déversement réduit Mrx*'}
</div>""", unsafe_allow_html=True)

# ── Tab 1: Classification ───────────────────────────────────────────────────
with t1:
    cls_col=[GR,GR,GO,RD][rv["cls"]-1]
    st.markdown("## ① Classification de la section  [CSA S16-24 Tables 4.1 / 4.2]")
    st.markdown('<div class="ibox"><b>Pourquoi classer la section ?</b>  La classe determine si la section peut atteindre le moment plastique Mp = φ·Fy·Zx (Classe 1&2) ou seulement le moment elastique My = φ·Fy·Sx (Classe 3) avant le voilement local. La limite de l\'ame pour les poteaux-poutres depend de Cf/φCy.</div>',unsafe_allow_html=True)
    ca,cm,cn,cb=st.columns([1,0.7,0.85,1.4])
    with ca: st.plotly_chart(section_fig(rv),use_container_width=True,key="sec1")
    with cm: st.plotly_chart(column_fig(rv),use_container_width=True,key="col1")
    with cn:
        st.plotly_chart(convention_fig(), use_container_width=True, key="conv1")
        st.plotly_chart(moment_diag_fig(rv), use_container_width=True, key="mdf1")
    with cb: st.plotly_chart(slender_fig(rv),use_container_width=True,key="slen1")
    st.markdown(f"""<div class="fbox">
<b>AILE  [HSC Table 4.1]</b>  b/(2·tf)  ≤  170/√Fy  (limite Classe 2)<br>
  b/(2·tf) = ({rv['bf']/2:.1f}) / {rv['tf']} = <b>{rv['b2tf']:.3f}</b>
  ≤  170/√{rv['Fy']} = <b>{rv['fl'][2]:.3f}</b>  → Aile <b>Classe {rv['cf']}</b><br><br>
<b>ÂME  [HSC Table 4.2]</b>  h/tw  ≤  (1700/√Fy)·(1 − 0.391·Cf/φCy)  (limite Classe 2)<br>
  φCy = {rv['pCy']/1e3:.1f} kN  |  h/tw = {rv['h']}/{rv['tw']} = <b>{rv['htw']:.3f}</b>
  ≤  (1700/√{rv['Fy']})·(1 − 0.391·{rv['Cf']/1e3:.1f}/{rv['pCy']/1e3:.1f}) = <b>{rv['wb'][2]:.3f}</b>  → Âme <b>Classe {rv['cw']}</b><br><br>
<b>CLASSE GOUVERNANTE = max(Aile {rv['cf']}, Âme {rv['cw']}) = Classe {rv['cls']}</b><br>
  → Mrx = {'φ·Zx·Fy (moment plastique)' if rv['cls']<=2 else 'φ·Sx·Fy (moment élastique)'} = <b>{rv['Mrx_s']/1e6:.1f} kN·m</b>
</div>""", unsafe_allow_html=True)

# ── Tab 2: Cross-section ────────────────────────────────────────────────────
with t2:
    st.markdown("## ② Vérification de la section  [CSA S16-24 Cl. 13.8.2]")
    if not rv["braced"]:
        st.markdown('<div class="rwarn">⚠️ <b>Structure non contreventée :</b> la vérification de la section (Step 2) n\'est PAS REQUISE pour les pièces non contreventées [HSC 13.8.2 — note de la diapositive]. Résultat affiché à titre indicatif seulement. Seule la Vérification ④ (avec déversement) est requise.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ibox"><b>Principe :</b> la pièce est traitée comme infiniment courte (Cr = φCy, sans flambement). β = 0.6 (fixe pour cette vérification). <b>U1x ≥ 1.0, U1y ≥ 1.0</b> [HSC 13.8.4].</div>', unsafe_allow_html=True)
    st.plotly_chart(stacked_bar(
        [rv["Ta"],rv["Tb"],rv["Tc"]],
        [f"Cf/φCy = {rv['Cf']/1e3:.1f}/{rv['pCy']/1e3:.1f}",
         f"0.85·U1x·Mfx/Mrx = 0.85×{rv['U1x_s2']:.3f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_s']/1e6:.1f}",
         f"β·U1y·Mfy/Mry = 0.6×{rv['U1y_s2']:.3f}×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}"],
        [TL,OR,PU], rv["r2"],
        "② Vérification de la section — contribution de chaque terme"),
        use_container_width=True, key="s2bar")
    st.markdown(f"""<div class="fbox">
<b>Équation d'interaction  [HSC 13.8.2] :</b>  Cf/φCy  +  0.85·U1x·Mfx/Mrx  +  β·U1y·Mfy/Mry  ≤ 1.0<br><br>
<b>Résistances  [HSC 13.5] :</b><br>
φCy = φ·A·Fy = {rv['phi']}×{rv['A']:,}×{rv['Fy']} = <b>{rv['pCy']/1e3:.1f} kN</b><br>
Mrx = <b>{rv['Mrx_s']/1e6:.1f} kN·m</b>   Mry = <b>{rv['Mry_s']/1e6:.1f} kN·m</b>   β = 0.6 (fixe — vérification de section)<br><br>
<b>ω1 et U1  [HSC 13.8.4, 13.8.5] — condition : U1x ≥ 1.0,  U1y ≥ 1.0 :</b><br>
ω1x = 0.6 − 0.4×{rv['k']:.2f} = <b>{rv['om1x']:.4f}</b>  (≥ 0.4)   |   ω1y = 0.6 − 0.4×{rv['kwy']:.2f} = <b>{rv['om1y']:.4f}</b>  (≥ 0.4)<br>
Cex = <b>{rv['Cex']/1e3:.1f} kN</b>   |   Cey = <b>{rv['Cey']/1e3:.1f} kN</b><br>
{'U1x brut = ω1x/(1−Cf/Cex) = '+f"{rv['om1x']:.4f}/(1−{rv['Cf']/1e3:.1f}/{rv['Cex']/1e3:.1f}) = {rv['U1x_raw']:.4f}  → appliqué = max({rv['U1x_raw']:.4f}, 1.0) = <b>{rv['U1x_s2']:.4f}</b>" if rv['braced'] else "<b>U1x = 1.0</b>  (non contreventée)"}<br>
{'U1y brut = ω1y/(1−Cf/Cey) = '+f"{rv['om1y']:.4f}/(1−{rv['Cf']/1e3:.1f}/{rv['Cey']/1e3:.1f}) = {rv['U1y_raw']:.4f}  → appliqué = max({rv['U1y_raw']:.4f}, 1.0) = <b>{rv['U1y_s2']:.4f}</b>" if rv['braced'] else "<b>U1y = 1.0</b>  (non contreventée)"}<br><br>
<b>Résultat :</b><br>
{rv['Cf']/1e3:.1f}/{rv['pCy']/1e3:.1f}  +  0.85×{rv['U1x_s2']:.4f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_s']/1e6:.1f}  +  0.6×{rv['U1y_s2']:.4f}×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}<br>
= <b>{rv['Ta']:.4f}</b>  +  <b>{rv['Tb']:.4f}</b>  +  <b>{rv['Tc']:.4f}</b>  =  <b>{rv['r2']:.4f}</b>
{'<br><br><i>⚠️ Rappel : cette vérification est indicative seulement pour une structure non contreventée.</i>' if not rv['braced'] else ''}
</div>""", unsafe_allow_html=True)
    st.markdown(rhtml(rv["r2"]),unsafe_allow_html=True)

# ── Tab 3: Step 3a ──────────────────────────────────────────────────────────
with t3:
    st.markdown("## ③ Vérification de la pièce — sans déversement  [CSA S16-24 Cl. 13.8.3]")
    if not rv["braced"]:
        st.markdown('<div class="rwarn">⚠️ <b>Structure non contreventée :</b> la vérification de la pièce sans déversement (Step 3a) n\'est PAS REQUISE pour les pièces non contreventées. Seule la Vérification ④ (avec déversement) est requise. Résultat affiché à titre indicatif seulement.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ibox"><b>Principe :</b> Cr = f(λ̄_max) — λ̄ gouvernant pour flexion biaxiale. <b>U1x ≥ 0, U1y ≥ 0</b> (contreventée, amplification peut être inférieure à 1 pour double courbure) [HSC 13.8.4]. β = 0.6 + 0.4·λ̄y ≤ 0.85  [HSC 13.8.2].</div>', unsafe_allow_html=True)
    ca,cb=st.columns([1.5,1])
    with ca: st.plotly_chart(col_curve_fig(rv,"x"),use_container_width=True,key="cc3a")
    with cb: st.plotly_chart(stacked_bar(
        [rv["T3a_A"],rv["T3a_B"],rv["T3a_C"]],
        [f"Cf/Cr(λ̄_max)","0.85·U1x·Mfx/Mrx","β·U1y·Mfy/Mry"],
        [TL,OR,PU],rv["r3a"],"③ Pièce sans déversement — contribution de chaque terme"),
        use_container_width=True,key="s3abar")
    st.markdown(f"""<div class="fbox">
<b>Équation d'interaction  [HSC 13.8.3] :</b>  Cf/Cr(λ̄_max)  +  0.85·U1x·Mfx/Mrx  +  β·U1y·Mfy/Mry  ≤ 1.0<br><br>
<b>Élancement et Cr  [HSC 13.3.1] :</b>  n = {rv['n']}<br>
KLx/rx = {rv['KLx_rx']:.1f}  →  Fex = {rv['Fex']:.1f} MPa  →  λ̄x = √(Fy/Fex) = <b>{rv['lx']:.4f}</b><br>
KLy/ry = {rv['KLy_ry']:.1f}  →  Fey = {rv['Fey']:.1f} MPa  →  λ̄y = √(Fy/Fey) = <b>{rv['ly']:.4f}</b><br>
λ̄_max = max({rv['lx']:.4f}, {rv['ly']:.4f}) = <b>{rv['lam_max']:.4f}</b>  → Cr = min(Crx, Cry) = <b>{rv['Cr3a']/1e3:.1f} kN</b><br>
Crx = <b>{rv['Crx']/1e3:.1f} kN</b>  (Cr/A = {rv['CrA_x']:.1f} MPa)   |   Cry = <b>{rv['Cry']/1e3:.1f} kN</b>  (Cr/A = {rv['CrA_y']:.1f} MPa)  [Table T2]<br><br>
<b>β  [HSC 13.8.2] :</b>  β = 0.6 + 0.4·λ̄y = 0.6 + 0.4×{rv['ly']:.4f} = <b>{rv['bv']:.4f}</b>  (≤ 0.85)<br><br>
<b>U1  [HSC 13.8.4] — condition : U1x ≥ 0,  U1y ≥ 0 :</b><br>
{'U1x brut = ω1x/(1−Cf/Cex) = '+f"{rv['om1x']:.4f}/(1−{rv['Cf']/1e3:.1f}/{rv['Cex']/1e3:.1f}) = {rv['U1x_raw']:.4f}  → appliqué = max({rv['U1x_raw']:.4f}, 0) = <b>{rv['U1x_3a']:.4f}</b>" if rv['braced'] else "<b>U1x = 1.0</b>  (non contreventée)"}<br>
{'U1y brut = ω1y/(1−Cf/Cey) = '+f"{rv['om1y']:.4f}/(1−{rv['Cf']/1e3:.1f}/{rv['Cey']/1e3:.1f}) = {rv['U1y_raw']:.4f}  → appliqué = max({rv['U1y_raw']:.4f}, 0) = <b>{rv['U1y_3a']:.4f}</b>" if rv['braced'] else "<b>U1y = 1.0</b>  (non contreventée)"}<br>
<i>Note : U1 ≥ 0 (pas ≥ 1) car la double courbure (κ > 0) peut réduire l'amplification du moment.</i><br><br>
<b>Résultat :</b><br>
{rv['Cf']/1e3:.1f}/{rv['Cr3a']/1e3:.1f}  +  0.85×{rv['U1x_3a']:.4f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_s']/1e6:.1f}  +  {rv['bv']:.4f}×{rv['U1y_3a']:.4f}×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}<br>
= <b>{rv['T3a_A']:.4f}</b>  +  <b>{rv['T3a_B']:.4f}</b>  +  <b>{rv['T3a_C']:.4f}</b>  =  <b>{rv['r3a']:.4f}</b>
</div>""", unsafe_allow_html=True)
    st.markdown(rhtml(rv["r3a"]),unsafe_allow_html=True)

# ── Tab 4: Step 3b ──────────────────────────────────────────────────────────
with t4:
    st.markdown("## ④ Vérification de la pièce — avec déversement  [CSA S16-24 Cl. 13.8.4]")
    st.markdown(f'<div class="ibox"><b>Principe :</b> Cr = f(λ̄y) — l\'axe faible gouverne le flambement hors-plan. Mrx peut être réduit par déversement si Lb > Lu. U1x ≥ 1.0 (ne pas cumuler avec ω₂ déjà dans Mu).<br><b>{rv["ltb"]}</b></div>',unsafe_allow_html=True)
    ca,cb=st.columns([1.5,1])
    with ca: st.plotly_chart(col_curve_fig(rv,"y"),use_container_width=True,key="cc3b")
    with cb: st.plotly_chart(stacked_bar(
        [rv["T3b_A"],rv["T3b_B"],rv["T3b_C"]],
        [f"Cf/Cr(λ̄y)","0.85·U1x·Mfx/Mrx*","β·U1y·Mfy/Mry"],
        [TL,OR,PU],rv["r3b"],"④ Pièce avec déversement — contribution de chaque terme"),
        use_container_width=True,key="s3bbar")
    st.markdown(f"""<div class="fbox">
<b>Équation d'interaction  [HSC 13.8.4] :</b>  Cf/Cr(λ̄y)  +  0.85·U1x·Mfx/Mrx*  +  β·U1y·Mfy/Mry  ≤ 1.0<br><br>
<b>Cr axe faible  [HSC 13.3.1] :</b>  KLy/ry = {rv['KLy_ry']:.1f}  →  λ̄y = <b>{rv['ly']:.4f}</b>  →  Cry = <b>{rv['Cry']/1e3:.1f} kN</b>  (Cr/A = {rv['CrA_y']:.1f} MPa)  [Table T2]<br><br>
<b>Résistance en flexion  [HSC 13.6] :</b>  Lb = {rv['L']:.0f} mm  |  Lu = {rv['Lu']:,} mm  |  ω₂ = {rv['om2']}<br>
{'Mrx* = Mp = <b>'+f"{rv['Mrx_b']/1e6:.1f}"+'</b> kN·m  (Lb ≤ Lu — pas de déversement)' if rv['ltb_ok'] else f"Mu = ω₂·(π/Lb)·√(E·Iy·G·J + (π·E/Lb)²·Iy·Cw) = <b>{rv['Mu_eff']/1e6:.1f} kN·m</b>  →  Mrx* = <b>{rv['Mrx_b']/1e6:.1f} kN·m</b>"}<br><br>
<b>U1  [HSC 13.8.4] — conditions : U1x ≥ 1.0,  U1y ≥ 0 :</b><br>
<i>U1x ≥ 1.0 (pas ≥ 0) : ω₂ est déjà inclus dans Mu pour le déversement — utiliser U1x &lt; 1 cumuleraient l'effet du gradient deux fois.</i><br>
<i>U1y ≥ 0 (pas ≥ 1) : l'axe faible n'est pas affecté par le déversement — la double courbure peut réduire U1y.</i><br>
{'U1x brut = '+f"{rv['U1x_raw']:.4f}  → appliqué = max({rv['U1x_raw']:.4f}, 1.0) = <b>{rv['U1x_3b']:.4f}</b>" if rv['braced'] else "<b>U1x = 1.0</b>  (non contreventée)"}<br>
{'U1y brut = '+f"{rv['U1y_raw']:.4f}  → appliqué = max({rv['U1y_raw']:.4f}, 0) = <b>{rv['U1y_3b']:.4f}</b>" if rv['braced'] else "<b>U1y = 1.0</b>  (non contreventée)"}<br><br>
<b>Résultat :</b><br>
{rv['Cf']/1e3:.1f}/{rv['Cry']/1e3:.1f}  +  0.85×{rv['U1x_3b']:.4f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_b']/1e6:.1f}  +  {rv['bv']:.4f}×{rv['U1y_3b']:.4f}×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}<br>
= <b>{rv['T3b_A']:.4f}</b>  +  <b>{rv['T3b_B']:.4f}</b>  +  <b>{rv['T3b_C']:.4f}</b>  =  <b>{rv['r3b']:.4f}</b>
</div>""", unsafe_allow_html=True)
    st.markdown(rhtml(rv["r3b"]),unsafe_allow_html=True)
    gov_step=("② Vérif. section" if rv["r2"]>=rv["r3a"] and rv["r2"]>=rv["r3b"]
              else ("③ Pièce sans dévers." if rv["r3a"]>=rv["r3b"] else "④ Pièce avec dévers."))
    st.markdown(f"""<div class="fbox">
② Vérif. section = {rv['r2']:.4f}   |   ③ Sans dévers. = {rv['r3a']:.4f}   |   ④ Avec dévers. = {rv['r3b']:.4f}<br>
<b>GOUVERNANT = {gov_step} → {rv['gov']:.4f}</b>
</div>""", unsafe_allow_html=True)
    st.markdown(rhtml(rv["gov"]),unsafe_allow_html=True)

# ── Tab 5: Sensitivity ──────────────────────────────────────────────────────
with t5:
    st.markdown("## 📈 Analyse de sensibilité")
    st.markdown('<div class="ibox">Ces courbes montrent comment les trois rapports d\'interaction varient en fonction des charges. Le point doré marque le cas courant. Modifiez les glissières pour observer l\'évolution en temps réel.</div>',unsafe_allow_html=True)
    st.plotly_chart(sensitivity_fig(rv),use_container_width=True,key="sens")
    gov_step=("② Vérif. section" if rv["r2"]>=rv["r3a"] and rv["r2"]>=rv["r3b"]
              else ("③ Pièce sans dévers." if rv["r3a"]>=rv["r3b"] else "④ Pièce avec dévers."))
    st.markdown(f"""<div class="fbox">
Vérification gouvernante : <b>{gov_step}</b>  =  <b>{rv['gov']:.4f}</b>  —  {'ADÉQUAT ✓' if rv['ok'] else 'INADÉQUAT ✗'}<br>
Sarcelle = ② Vérif. section  |  Orange = ③ Pièce sans dévers.  |  Violet = ④ Pièce avec dévers.<br>
Zone verte = adéquat (ratio &lt; 1.0)   |   Zone rouge = inadéquat (ratio &gt; 1.0)
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#FFF8E1,#FEF3C7);
            border:1.5px solid #FCD34D;border-radius:12px;
            padding:14px 20px;font-size:.81rem;color:#78350F;margin-top:16px;
            box-shadow:0 2px 8px rgba(252,211,77,.2)'>
<strong>⚠️ EDUCATIONAL USE ONLY — NO LIABILITY.</strong>
This tool is a teaching aid developed for <strong>GCI 2011 — Conception de Structures I</strong>
at <strong>Université Laval</strong> under the supervision of
<strong>Prof. Luca Sorelli, ing., Ph.D.</strong>
It must not be used for the design, verification, or assessment of any real structure or
professional engineering work. Results are not certified by any professional or regulatory body
and may contain simplifications or errors appropriate for teaching but unacceptable in practice.
Prof. Luca Sorelli, Université Laval, and all contributors accept no liability whatsoever
for any consequence of using this tool outside the classroom.
All structural designs require review and stamp by a licensed professional engineer in
accordance with applicable codes and local regulations.<br><br>
<strong>Reference:</strong> CSA S16-24 Cl. 13 &nbsp;|&nbsp;
CISC HSC 13th ed. Tables T1 · T2 · T3 &nbsp;|&nbsp;
φ = 0.90 &nbsp;|&nbsp; n = 1.34 &nbsp;|&nbsp;
GCI 2011 — Université Laval &nbsp;|&nbsp; Prof. Luca Sorelli
</div>
""", unsafe_allow_html=True)

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
.main{background:#fff}
.block-container{padding-top:1.2rem;padding-bottom:1.5rem}
h1{color:#1565C0;font-size:1.6rem;font-weight:700}
h2{color:#1565C0;font-size:1.05rem;font-weight:600;border-bottom:2px solid #1565C0;padding-bottom:3px;margin-top:1.1rem}
.fbox{background:#EBF0F8;border-left:5px solid #1565C0;padding:10px 14px;border-radius:5px;
      font-family:monospace;font-size:.86rem;color:#111;line-height:1.9;margin:7px 0}
.rok{background:#D4EDDA;border-left:5px solid #1B7E34;padding:9px 14px;border-radius:5px;
     font-weight:700;font-size:1rem;color:#1B7E34;margin:7px 0}
.rwarn{background:#FFF3CD;border-left:5px solid #8A5700;padding:9px 14px;border-radius:5px;
       font-weight:700;font-size:1rem;color:#8A5700;margin:7px 0}
.rfail{background:#FCDEDE;border-left:5px solid #B71C1C;padding:9px 14px;border-radius:5px;
       font-weight:700;font-size:1rem;color:#B71C1C;margin:7px 0}
.kpi{background:#F7F9FC;border:1px solid #AABCCC;border-radius:7px;padding:10px 12px;text-align:center}
.kpi-l{font-size:.73rem;color:#555;margin-bottom:1px}
.kpi-v{font-size:1.2rem;font-weight:700;color:#1565C0}
.ibox{background:#E6F1FB;border:1px solid #B5D4F4;padding:8px 12px;border-radius:5px;
      font-size:.83rem;color:#333;margin:6px 0}
/* disclaimer gate */
.disc-gate{background:#FFF8E1;border:2.5px solid #F57F17;border-radius:12px;
           padding:28px 32px;max-width:780px;margin:60px auto 0 auto}
.disc-gate h2{color:#B71C1C;font-size:1.25rem;border:none;margin-top:0;padding-bottom:0}
.disc-gate p{color:#333;font-size:.93rem;line-height:1.75}
.disc-gate ul{color:#333;font-size:.91rem;line-height:1.9;margin:0 0 12px 0;padding-left:1.3em}
.disc-gate .sign{font-size:.82rem;color:#666;border-top:1px solid #EEE;
                 padding-top:10px;margin-top:16px}
/* persistent top banner */
.edu-banner{background:#FFF3CD;border:1.5px solid #F57F17;border-radius:6px;
            padding:7px 14px;font-size:.82rem;color:#7B3F00;margin-bottom:10px;
            display:flex;align-items:center;gap:8px}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  DISCLAIMER GATE  — must be accepted before any content is shown
# ═══════════════════════════════════════════════════════════════════════════════

if "accepted" not in st.session_state:
    st.session_state["accepted"] = False

if not st.session_state["accepted"]:
    st.markdown("""
<div class="disc-gate">

  <!-- Course & author header -->
  <div style="text-align:center;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #E0C860">
    <div style="font-size:1.35rem;font-weight:800;color:#1565C0;letter-spacing:.03em">
      🏗️ GCI 2011 — Conception de Structures I
    </div>
    <div style="font-size:1.0rem;color:#333;margin-top:4px">
      <strong>Université Laval</strong> — Département de génie civil et de génie des eaux
    </div>
    <div style="font-size:.92rem;color:#555;margin-top:3px">
      Professeur : <strong>Luca Sorelli</strong>, ing., Ph.D.
    </div>
    <div style="font-size:.82rem;color:#888;margin-top:2px">
      Beam-Column Design Tool — CSA S16-24 Cl. 13
    </div>
  </div>

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
    Reference: CSA S16-24 Cl. 13 &nbsp;|&nbsp; CISC HSC 13th ed. &nbsp;|&nbsp;
    φ = 0.90 &nbsp;|&nbsp; n = 1.34
  </div>
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
#  DESIGN  (CSA S16-24 Cl. 13)
# ═══════════════════════════════════════════════════════════════════════════════
def fl_lims(Fy): s=math.sqrt(Fy); return {1:145/s,2:170/s,3:200/s}
def wb_lims(Fy,Cf,pCy):
    s=math.sqrt(Fy); r=min(Cf/pCy, 1.0)
    return {1:(1100/s)*(1-.391*r),2:(1700/s)*(1-.391*r),3:1900/s}
def classify(v,lm):
    for c in [1,2,3]:
        if v<=lm[c]: return c
    return 4
def col_cr(phi,A,Fy,KLr,E=200000,n=1.34):
    Fe=math.pi**2*E/KLr**2; lam=math.sqrt(Fy/Fe)
    return phi*A*Fy*(1+lam**(2*n))**(-1/n), lam, Fe
def w1(k): return max(.6-.4*k,.4)
def U1_f(w,Cf,Cex): return max(w/(1-Cf/Cex),0.0)
def beta(ly): return min(.6+.4*ly,.85)
def Mr_sect(phi,Zx,Sx,Fy,cls): return phi*Zx*Fy if cls<=2 else phi*Sx*Fy
def LTB_Mu(E,G,Iy,J,Cw,L):
    return (math.pi/L)*math.sqrt(E*Iy*G*J+(math.pi*E/L)**2*Iy*Cw)
def Mr_ltb_calc(phi,Zx,Sx,Fy,Mu):
    Mp=Fy*Zx
    if Mu>=.67*Mp: return phi*min(1.15*Mp*(1-.28*Mp/Mu),Mp)
    return phi*Mu

def compute(sn, Cf_kN, Mfx_kNm, Mfy_kNm, L_mm,
            Kx=1.0, Ky=1.0, k=0.67, om2=1.0, E=200000, G=77000, phi=0.9):
    s=SECTIONS[sn]
    Cf=Cf_kN*1e3; Mfx=Mfx_kNm*1e6; Mfy=Mfy_kNm*1e6
    A,d,bf,tf,tw = s["A"],s["d"],s["bf"],s["tf"],s["tw"]
    Zx,Sx,rx = s["Zx"],s["Sx"],s["rx"]
    Zy,Sy,ry = s["Zy"],s["Sy"],s["ry"]
    Iy,J,Cw,Lu,Fy,h = s["Iy"],s["J"],s["Cw"],s["Lu"],s["Fy"],s["h"]

    pCy=phi*A*Fy; b2tf=(bf/2)/tf; htw=h/tw
    fl=fl_lims(Fy); wb=wb_lims(Fy,Cf,pCy)
    cf=classify(b2tf,fl); cw=classify(htw,wb); cls=max(cf,cw)

    Mrx_s=Mr_sect(phi,Zx,Sx,Fy,cls); Mry_s=phi*Zy*Fy
    KLx_rx=Kx*L_mm/rx; KLy_ry=Ky*L_mm/ry
    Cex=math.pi**2*E*A/KLx_rx**2
    om1=w1(k); U1s=max(U1_f(om1,Cf,Cex),1.0)
    Ta=Cf/pCy; Tb=0.85*U1s*Mfx/Mrx_s; Tc=0.6*Mfy/Mry_s; r2=Ta+Tb+Tc

    Crx,lx,Fex=col_cr(phi,A,Fy,KLx_rx,E)
    Cry,ly,Fey=col_cr(phi,A,Fy,KLy_ry,E)
    bv=beta(ly); U1a=max(U1_f(om1,Cf,Cex),0.0)
    T3a_A=Cf/Crx; T3a_B=0.85*U1a*Mfx/Mrx_s; T3a_C=bv*Mfy/Mry_s; r3a=T3a_A+T3a_B+T3a_C

    Lb=L_mm
    if Lb<=Lu:
        Mrx_b=Mrx_s; ltb_ok=True; ltb=f"Lb={Lb:.0f} ≤ Lu={Lu:.0f} mm → no LTB, Mrx = Mp"
    else:
        Mu=om2*LTB_Mu(E,G,Iy,J,Cw,Lb)
        Mrx_b=Mr_ltb_calc(phi,Zx,Sx,Fy,Mu)
        ltb_ok=False; ltb=f"Lb={Lb:.0f} > Lu={Lu:.0f} mm → LTB reduces Mrx"
    U1b=max(U1_f(om1,Cf,Cex),1.0)
    T3b_A=Cf/Cry; T3b_B=0.85*U1b*Mfx/Mrx_b; T3b_C=bv*Mfy/Mry_s; r3b=T3b_A+T3b_B+T3b_C

    gov=max(r2,r3a,r3b)
    return dict(
        sn=sn,Cf=Cf,Mfx=Mfx,Mfy=Mfy,L=L_mm,Kx=Kx,Ky=Ky,k=k,om2=om2,E=E,G=G,phi=phi,
        A=A,d=d,bf=bf,tf=tf,tw=tw,h=h,
        Zx=Zx,Sx=Sx,rx=rx,Zy=Zy,Sy=Sy,ry=ry,Ix=s["Ix"],Iy=Iy,J=J,Cw=Cw,Lu=Lu,Fy=Fy,
        pCy=pCy,b2tf=b2tf,htw=htw,fl=fl,wb=wb,cf=cf,cw=cw,cls=cls,
        Mrx_s=Mrx_s,Mry_s=Mry_s,Cex=Cex,om1=om1,U1s=U1s,
        Ta=Ta,Tb=Tb,Tc=Tc,r2=r2,
        KLx_rx=KLx_rx,KLy_ry=KLy_ry,
        lx=lx,ly=ly,Fex=Fex,Fey=Fey,Crx=Crx,Cry=Cry,
        CrA_x=Crx/A,CrA_y=Cry/A,bv=bv,U1a=U1a,
        T3a_A=T3a_A,T3a_B=T3a_B,T3a_C=T3a_C,r3a=r3a,
        Mrx_b=Mrx_b,U1b=U1b,ltb=ltb,ltb_ok=ltb_ok,
        T3b_A=T3b_A,T3b_B=T3b_B,T3b_C=T3b_C,r3b=r3b,
        gov=gov,ok=(gov<=1.0),
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
def member_fig(rv):
    """
    Clean engineering diagram of a beam-column.
    - Column drawn with REAL proportions (bf / L ratio preserved)
    - Cf  : solid red arrows at top AND bottom, pointing inward
    - Mfx : proper moment arc symbols AT EACH END (top-end and bottom-end)
            sign: positive k (double curvature) → arcs oppose each other
                  negative k (single curvature) → arcs same direction
    - Mfy : smaller moment arcs for weak-axis biaxial bending
    Uses pure SVG via Plotly shapes + annotations for clean rendering.
    """
    import math as _math

    Cf_kN = rv["Cf"]  / 1e3
    Mfx   = rv["Mfx"] / 1e6
    Mfy   = rv["Mfy"] / 1e6
    L_m   = rv["L"]   / 1000
    k     = rv["k"]           # +1 = double curvature, −1 = single
    d_mm  = rv["d"]           # section depth   [mm]
    bf_mm = rv["bf"]          # flange width    [mm]

    # ── drawing space ────────────────────────────────────────────────────────
    # Map real section to drawing: preserve bf/L aspect ratio
    # column half-width in drawing units = 1.0  (always)
    # column height proportional to real L/bf
    W    = 1.0                        # column half-width (fixed)
    ratio = rv["L"] / bf_mm           # L/bf  (typically 10–50)
    H    = W * 2 * min(ratio, 20)     # cap at 20× for very slender columns
    H    = max(H, 4.0)                # minimum height for readability

    CF_C = "#B71C1C"   # red  – axial
    MX_C = "#1565C0"   # blue – strong-axis moment
    MY_C = "#C45000"   # orange – weak-axis moment

    shapes, annotations = [], []

    # ── 1. Column body ───────────────────────────────────────────────────────
    shapes.append(dict(
        type="rect", x0=-W, y0=0, x1=W, y1=H,
        fillcolor="rgba(46,109,164,0.22)",
        line=dict(color="#1A3A5C", width=2.0)))

    # ── 2. Cf arrows (pointing INWARD at both ends) ──────────────────────────
    ext_cf = H * 0.22
    if Cf_kN > 0:
        # bottom: tail below, head at y=0
        annotations += [
            dict(ax=0, ay=-ext_cf, axref="x", ayref="y",
                 x=0,  y=0,        xref="x",  yref="y",
                 arrowhead=2, arrowwidth=3.5, arrowcolor=CF_C,
                 showarrow=True, text=""),
            dict(x=0, y=-ext_cf*0.45,
                 text=f"<b>Cf = {Cf_kN:.0f} kN</b>",
                 xanchor="center", yanchor="top",
                 showarrow=False, font=dict(size=12, color=CF_C)),
            # top: tail above, head at y=H
            dict(ax=0, ay=H+ext_cf, axref="x", ayref="y",
                 x=0,  y=H,          xref="x",  yref="y",
                 arrowhead=2, arrowwidth=3.5, arrowcolor=CF_C,
                 showarrow=True, text=""),
            dict(x=0, y=H+ext_cf*0.55,
                 text=f"<b>Cf = {Cf_kN:.0f} kN</b>",
                 xanchor="center", yanchor="bottom",
                 showarrow=False, font=dict(size=12, color=CF_C)),
        ]

    # ── 3. Mfx moment arcs AT THE ENDS  ─────────────────────────────────────
    # A moment arc is drawn as a curved Plotly path (SVG arc).
    # At the BOTTOM end (y=0):  arc on LEFT side
    # At the TOP end   (y=H):  arc on RIGHT side
    # Sign convention:
    #   k > 0  (double curvature) → arcs point in OPPOSITE sense (standard positive)
    #   k < 0  (single curvature) → arcs point in SAME sense
    if Mfx != 0:
        R   = W * 1.10    # arc radius
        gx  = W * 0.30    # gap from column face to arc centre
        cx_L = -(W + gx + R)   # arc centre x, left side
        cx_R =  (W + gx + R)   # arc centre x, right side

        # ── BOTTOM end arc (left side) ───────────────────────────────────────
        # Arc from (cx_L, R) down to (cx_L+R, 0) → counter-clockwise = positive Mfx
        # For k>0 (double curv): bottom M is positive (CCW on left face)
        # We draw a 3/4 circle from 90° to 0° (CCW)
        bot_start_x = cx_L
        bot_start_y = R
        bot_end_x   = cx_L + R
        bot_end_y   = 0.0
        shapes.append(dict(
            type="path",
            path=f"M {cx_L:.3f},{R:.3f} A {R:.3f},{R:.3f} 0 0,1 {cx_L+R:.3f},0",
            line=dict(color=MX_C, width=3.0),
            fillcolor="rgba(0,0,0,0)"))
        # arrowhead at end of arc (pointing right → downward tangent)
        annotations.append(dict(
            ax=cx_L+R-0.01, ay=0.12, axref="x", ayref="y",
            x= cx_L+R+0.01, y=-0.02, xref="x",  yref="y",
            arrowhead=2, arrowwidth=2.5, arrowcolor=MX_C,
            showarrow=True, text=""))
        annotations.append(dict(
            x=cx_L - R*0.3, y=-R*0.1,
            text=f"<b>Mfx = {Mfx:.0f} kN·m</b>",
            xanchor="right", yanchor="top",
            showarrow=False, font=dict(size=11, color=MX_C)))

        # ── TOP end arc (right side) ─────────────────────────────────────────
        # For double curvature (k>0): top M is also positive but mirrored
        # Arc from (cx_R, H-R) up to (cx_R-R, H) → CCW
        top_flip = 1 if k >= 0 else -1   # flip for single curvature
        shapes.append(dict(
            type="path",
            path=f"M {cx_R:.3f},{H-R:.3f} A {R:.3f},{R:.3f} 0 0,0 {cx_R-R:.3f},{H:.3f}",
            line=dict(color=MX_C, width=3.0),
            fillcolor="rgba(0,0,0,0)"))
        annotations.append(dict(
            ax=cx_R-R+0.01, ay=H-0.12, axref="x", ayref="y",
            x= cx_R-R-0.01, y=H+0.02,  xref="x",  yref="y",
            arrowhead=2, arrowwidth=2.5, arrowcolor=MX_C,
            showarrow=True, text=""))
        annotations.append(dict(
            x=cx_R + R*0.3, y=H+R*0.1,
            text=f"<b>Mfx = {Mfx:.0f} kN·m</b>",
            xanchor="left", yanchor="bottom",
            showarrow=False, font=dict(size=11, color=MX_C)))

    # ── 4. Mfy moment arcs (weak-axis biaxial) ───────────────────────────────
    if Mfy != 0:
        Ry  = W * 0.70
        # bottom end – above the Cf label zone, left of centre
        shapes.append(dict(
            type="path",
            path=f"M {-Ry:.3f},{-ext_cf*0.05:.3f} A {Ry:.3f},{Ry:.3f} 0 0,0 {Ry:.3f},{-ext_cf*0.05:.3f}",
            line=dict(color=MY_C, width=2.5),
            fillcolor="rgba(0,0,0,0)"))
        annotations.append(dict(
            ax=Ry-0.01, ay=-ext_cf*0.05+0.08, axref="x", ayref="y",
            x= Ry+0.01, y=-ext_cf*0.05-0.05,  xref="x",  yref="y",
            arrowhead=2, arrowwidth=2, arrowcolor=MY_C,
            showarrow=True, text=""))
        annotations.append(dict(
            x=Ry+0.3, y=-ext_cf*0.05,
            text=f"<b>Mfy = {Mfy:.0f} kN·m</b>",
            xanchor="left", yanchor="middle",
            showarrow=False, font=dict(size=10, color=MY_C)))
        # top end
        shapes.append(dict(
            type="path",
            path=f"M {Ry:.3f},{H+ext_cf*0.05:.3f} A {Ry:.3f},{Ry:.3f} 0 0,0 {-Ry:.3f},{H+ext_cf*0.05:.3f}",
            line=dict(color=MY_C, width=2.5),
            fillcolor="rgba(0,0,0,0)"))
        annotations.append(dict(
            ax=-Ry+0.01, ay=H+ext_cf*0.05-0.08, axref="x", ayref="y",
            x= -Ry-0.01, y=H+ext_cf*0.05+0.05,  xref="x",  yref="y",
            arrowhead=2, arrowwidth=2, arrowcolor=MY_C,
            showarrow=True, text=""))
        annotations.append(dict(
            x=Ry+0.3, y=H+ext_cf*0.05,
            text=f"<b>Mfy = {Mfy:.0f} kN·m</b>",
            xanchor="left", yanchor="middle",
            showarrow=False, font=dict(size=10, color=MY_C)))

    # ── 5. L dimension line (right side) ─────────────────────────────────────
    xd = W + 0.55
    annotations += [
        dict(ax=xd, ay=0, axref="x", ayref="y",
             x=xd,  y=H,  xref="x",  yref="y",
             arrowhead=2, arrowside="end+start",
             arrowcolor="#999", arrowwidth=1.2,
             showarrow=True, text=""),
        dict(x=xd+0.25, y=H/2,
             text=f"L = {L_m:.2f} m",
             xanchor="left", yanchor="middle", textangle=90,
             showarrow=False, font=dict(size=9, color="#777")),
    ]

    # ── 6. Section label inside column ───────────────────────────────────────
    annotations.append(dict(
        x=0, y=H/2,
        text=f"<b>{rv['sn']}</b><br>"
             f"d={d_mm} mm  bf={bf_mm} mm<br>"
             f"Kx={rv['Kx']}  Ky={rv['Ky']}",
        xanchor="center", yanchor="middle",
        showarrow=False,
        font=dict(size=10, color="#1A3A5C"),
        bgcolor="rgba(255,255,255,0.75)",
        bordercolor="#1A3A5C", borderwidth=1,
        borderpad=4))

    # ── 7. Sign convention note ──────────────────────────────────────────────
    sign_note = "double curvature (+)" if k >= 0 else "single curvature (−)"
    annotations.append(dict(
        x=0, y=-ext_cf*1.6,
        text=f"k = {k:.2f}  →  {sign_note}",
        xanchor="center", yanchor="top",
        showarrow=False, font=dict(size=9, color="#888")))

    # ── layout ───────────────────────────────────────────────────────────────
    pad_x = W * 7.5
    pad_y_bot = ext_cf * 2.2
    pad_y_top = ext_cf * 2.2

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[-pad_x, pad_x],
        y=[-pad_y_bot, H + pad_y_top],
        mode="markers", marker=dict(opacity=0, size=1)))
    fig.update_layout(
        shapes=shapes, annotations=annotations,
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        height=520,
        margin=dict(l=5, r=5, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        showlegend=False,
    )
    return fig

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
    st.markdown("## 🏗️ Beam-Column  CSA S16-24")
    st.markdown("---")
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

    st.markdown("### Factored loads")
    max_Cf   = max(100, int(0.9*s["A"]*s["Fy"]/1e3/50)*50)
    max_Mrx  = max(50,  int(0.9*s["Zx"]*s["Fy"]/1e6/10)*10)
    max_Mry  = max(10,  int(0.9*s["Zy"]*s["Fy"]/1e6/5)*5)
    Cf_kN   = st.slider("Cf  (kN)", 50.0, float(max_Cf),
                         min(2000.0, max_Cf*.45), 25.0,
                         help="Factored axial compression force")
    Mfx_kNm = st.slider("Mfx (kN·m)", 0.0, float(max_Mrx),
                         min(300.0, max_Mrx*.45), 10.0,
                         help="Factored strong-axis bending moment")
    Mfy_kNm = st.slider("Mfy (kN·m)", 0.0, float(max_Mry),
                         0.0, max(1.0, float(max_Mry)//50),
                         help="Factored weak-axis bending moment (biaxial loading)")
    if Mfy_kNm > 0:
        st.markdown(
            f'<div class="ibox">⚡ <b>Biaxial bending active</b><br>'
            f'Mfx = {Mfx_kNm:.1f} kN·m (strong)  +  '
            f'Mfy = {Mfy_kNm:.1f} kN·m (weak)<br>'
            f'Max Mry = φ·Zy·Fy = {max_Mry:.0f} kN·m</div>',
            unsafe_allow_html=True)

    st.markdown("### Geometry")
    L_mm = st.slider("L  (mm)", 1000.0, 15000.0, 3700.0, 100.0)
    Kx   = st.select_slider("Kx", [0.5,0.65,0.7,1.0,1.2,1.5,2.0], value=1.0)
    Ky   = st.select_slider("Ky", [0.5,0.65,0.7,1.0,1.2,1.5,2.0], value=1.0)

    st.markdown("### Moment parameters")
    k_ratio = st.slider("k = Mf1/Mf2", -1.0, 1.0, 0.67, 0.01,
        help="+1 = double curvature (best);  −1 = single (worst)")
    omega2  = st.slider("ω₂  (LTB gradient)", 0.6, 2.5, 1.0, 0.05,
        help="1.0 = conservative (uniform moment)")
    st.markdown("---")
    st.markdown("""
<div style="font-size:.75rem;color:#666;line-height:1.7">
  <strong style="color:#1565C0">GCI 2011 — Conception de Structures I</strong><br>
  Université Laval<br>
  Prof. Luca Sorelli, ing., Ph.D.<br><br>
  φ = 0.90 &nbsp;|&nbsp; E = 200 000 MPa &nbsp;|&nbsp; G = 77 000 MPa<br>
  Data: CISC HSC 13th ed. T1 · T2 · T3<br>
  Code: CSA S16-24
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  COMPUTE
# ═══════════════════════════════════════════════════════════════════════════════
rv = compute(sn, Cf_kN, Mfx_kNm, Mfy_kNm, L_mm, Kx, Ky, k_ratio, omega2)

# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER  &  KPI STRIP
# ═══════════════════════════════════════════════════════════════════════════════
# ── Course / author header ───────────────────────────────────────────────────
st.markdown("""
<div style="border-bottom:2px solid #1565C0;padding-bottom:10px;margin-bottom:6px">
  <div style="font-size:1.5rem;font-weight:800;color:#1565C0;line-height:1.25;margin-bottom:2px">
    🏗️ Vérification d'une pièce poteau-poutre — CSA S16-24  (Cl. 13)
  </div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:4px">
    <div style="font-size:.85rem;color:#555">
      Propriétés des sections : CISC HSC Table T1 &nbsp;·&nbsp;
      Cr/A : Table T2 &nbsp;·&nbsp; Lu : Table T3
    </div>
    <div style="font-size:.82rem;color:#444;text-align:right;line-height:1.55">
      <strong style="color:#1565C0">GCI 2011 — Conception de Structures I</strong>
      &nbsp;|&nbsp; Université Laval
      &nbsp;|&nbsp; Prof. Luca Sorelli, ing., Ph.D.
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
def kpi(v,lbl,col):
    return (f'<div class="kpi"><div class="kpi-l">{lbl}</div>'
            f'<div class="kpi-v" style="color:{col}">{v}</div></div>')
c1.markdown(kpi(f"Classe {rv['cls']}","Classe de la section",[GR,GR,GO,RD][rv["cls"]-1]),unsafe_allow_html=True)
c2.markdown(kpi(f"{rv['r2']:.4f}","② Vérif. section",rclr(rv["r2"])),unsafe_allow_html=True)
c3.markdown(kpi(f"{rv['r3a']:.4f}","③ Pièce sans dévers.",rclr(rv["r3a"])),unsafe_allow_html=True)
c4.markdown(kpi(f"{rv['r3b']:.4f}","④ Pièce avec dévers.",rclr(rv["r3b"])),unsafe_allow_html=True)
c5.markdown(kpi(f"{rv['gov']:.4f}","GOUVERNANT",rclr(rv["gov"])),unsafe_allow_html=True)
c6.markdown(kpi("✓ OK" if rv["ok"] else "✗ NG","VERDICT",GR if rv["ok"] else RD),unsafe_allow_html=True)
st.markdown("---")

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
    ca, cm, cb = st.columns([1, 0.85, 1.5])
    with ca:
        st.markdown("### Cross-section")
        st.plotly_chart(section_fig(rv), use_container_width=True, key="sec0")
    with cm:
        st.markdown("### Member loading")
        st.plotly_chart(member_fig(rv), use_container_width=True, key="mem0")
    with cb:
        st.markdown("### Dimensions & properties from HSC T1")
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
    st.markdown(f"""<div class="fbox">
φCy = φ·A·Fy = {rv['phi']}×{rv['A']:,}×{rv['Fy']} = <b>{rv['pCy']/1e3:.1f} kN</b> (squash load — no buckling)<br>
Mrx = φ·Zx·Fy = {rv['phi']}×{rv['Zx']/1e3:.0f}×10³×{rv['Fy']} = <b>{rv['Mrx_s']/1e6:.1f} kN·m</b> (Class {rv['cls']}, Fy={rv['Fy']} MPa)<br>
Mry = φ·Zy·Fy = {rv['phi']}×{rv['Zy']/1e3:.0f}×10³×{rv['Fy']} = <b>{rv['Mry_s']/1e6:.1f} kN·m</b><br>
KLx/rx = {rv['Kx']}×{rv['L']:.0f}/{rv['rx']} = <b>{rv['KLx_rx']:.1f}</b>  →  Cr(x)/A = <b>{rv['CrA_x']:.1f} MPa</b>  (Table T2)<br>
KLy/ry = {rv['Ky']}×{rv['L']:.0f}/{rv['ry']} = <b>{rv['KLy_ry']:.1f}</b>  →  Cr(y)/A = <b>{rv['CrA_y']:.1f} MPa</b>  (Table T2 — governs)<br>
Lu = <b>{rv['Lu']:,} mm</b> (Table T3)   Lb = <b>{rv['L']:.0f} mm</b>
→  {'✅  Lb ≤ Lu : no LTB reduction' if rv['L']<=rv['Lu'] else '⚠️  Lb > Lu : LTB check required'}
</div>""", unsafe_allow_html=True)

# ── Tab 1: Classification ───────────────────────────────────────────────────
with t1:
    cls_col=[GR,GR,GO,RD][rv["cls"]-1]
    st.markdown("## ① Classification de la section  [CSA S16-24 Tables 4.1 / 4.2]")
    st.markdown('<div class="ibox">The section class controls whether Mp = φ·Fy·Zx (Class 1&2) or My = φ·Fy·Sx (Class 3) can be reached before local buckling. The web limit is relaxed when Cf is small relative to φCy.</div>',unsafe_allow_html=True)
    ca,cm,cb=st.columns([1,0.85,1.4])
    with ca: st.plotly_chart(section_fig(rv),use_container_width=True,key="sec1")
    with cm: st.plotly_chart(member_fig(rv),use_container_width=True,key="mem1")
    with cb: st.plotly_chart(slender_fig(rv),use_container_width=True,key="slen1")
    st.markdown(f"""<div class="fbox">
<b>FLANGE</b>  b/(2·tf)  ≤  170/√Fy  (Class 2 limit)<br>
  ({rv['bf']/2:.1f}) / {rv['tf']} = <b>{rv['b2tf']:.3f}</b>
  ≤  170/√{rv['Fy']} = <b>{rv['fl'][2]:.3f}</b>  → Flange <b>Class {rv['cf']}</b><br><br>
<b>WEB</b>  h/tw  ≤  (1700/√Fy)·(1 − 0.391·Cf/φCy)  (Class 2 limit)<br>
  φCy = {rv['pCy']/1e3:.1f} kN   {rv['h']}/{rv['tw']} = <b>{rv['htw']:.3f}</b>
  ≤  (1700/√{rv['Fy']})·(1 − 0.391·{rv['Cf']/1e3:.1f}/{rv['pCy']/1e3:.1f}) = <b>{rv['wb'][2]:.3f}</b>  → Web <b>Class {rv['cw']}</b><br><br>
<b>CLASSE GOUVERNANTE = max({rv['cf']}, {rv['cw']}) = Classe {rv['cls']}</b>
  → Mrx = {'φ·Fy·Zx (plastic)' if rv['cls']<=2 else 'φ·Fy·Sx (elastic)'} = <b>{rv['Mrx_s']/1e6:.1f} kN·m</b>
</div>""", unsafe_allow_html=True)

# ── Tab 2: Cross-section ────────────────────────────────────────────────────
with t2:
    st.markdown("## ② Vérification de la section  [CSA S16-24 Cl. 13.8.2]")
    st.markdown('<div class="ibox">Member treated as infinitely short (squash load). Cr = φCy = φ·A·Fy. Checks section can carry combined loads regardless of length. β = 0.6 (fixed). U1x ≥ 1.0.</div>',unsafe_allow_html=True)
    st.plotly_chart(stacked_bar(
        [rv["Ta"],rv["Tb"],rv["Tc"]],
        [f"Cf / φCy = {rv['Cf']/1e3:.1f} / {rv['pCy']/1e3:.1f}",
         f"0.85·U1x·Mfx/Mrx = 0.85×{rv['U1s']:.3f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_s']/1e6:.1f}",
         f"β·Mfy/Mry = 0.6×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}"],
        [TL,OR,PU], rv["r2"],
        "Interaction (Step 2) — each term's share of the 1.0 limit"),
        use_container_width=True, key="s2bar")
    st.markdown(f"""<div class="fbox">
φCy = {rv['phi']}×{rv['A']:,}×{rv['Fy']} = <b>{rv['pCy']/1e3:.1f} kN</b>   Mrx = <b>{rv['Mrx_s']/1e6:.1f} kN·m</b>   β = 0.6<br>
ω1 = 0.6 − 0.4×{rv['k']:.2f} = {rv['om1']:.4f}  (≥ 0.4)<br>
Cex = π²×{rv['E']:.0f}×{rv['A']:,} / {rv['KLx_rx']:.1f}² = <b>{rv['Cex']/1e3:.1f} kN</b><br>
U1x = {rv['om1']:.4f} / (1 − {rv['Cf']/1e3:.1f}/{rv['Cex']/1e3:.1f}) = <b>{rv['U1s']:.4f}</b>  (≥ 1.0)<br><br>
{rv['Cf']/1e3:.1f}/{rv['pCy']/1e3:.1f}  +  0.85×{rv['U1s']:.4f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_s']/1e6:.1f}  +  0.6×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}<br>
= <b>{rv['Ta']:.4f}</b>  +  <b>{rv['Tb']:.4f}</b>  +  <b>{rv['Tc']:.4f}</b>  =  <b>{rv['r2']:.4f}</b>
</div>""", unsafe_allow_html=True)
    st.markdown(rhtml(rv["r2"]),unsafe_allow_html=True)

# ── Tab 3: Step 3a ──────────────────────────────────────────────────────────
with t3:
    st.markdown("## ③ Vérification de la pièce — sans déversement  [CSA S16-24 Cl. 13.8.3]")
    st.markdown('<div class="ibox">Cr uses <b>strong-axis</b> slenderness λ̄x. Checks in-plane member buckling. U1x ≥ 0. β = 0.6 + 0.4·λ̄y.</div>',unsafe_allow_html=True)
    ca,cb=st.columns([1.5,1])
    with ca: st.plotly_chart(col_curve_fig(rv,"x"),use_container_width=True,key="cc3a")
    with cb: st.plotly_chart(stacked_bar(
        [rv["T3a_A"],rv["T3a_B"],rv["T3a_C"]],
        ["Cf/Cr(λ̄x)","0.85·U1x·Mfx/Mrx","β·Mfy/Mry"],
        [TL,OR,PU],rv["r3a"],"Interaction (3a)"),
        use_container_width=True,key="s3abar")
    st.markdown(f"""<div class="fbox">
KLx/rx = {rv['KLx_rx']:.1f}   Fe_x = π²×{rv['E']:.0f}/{rv['KLx_rx']:.1f}² = {rv['Fex']:.1f} MPa   λ̄x = √({rv['Fy']}/{rv['Fex']:.1f}) = <b>{rv['lx']:.4f}</b><br>
Cr(λ̄x) = φ·A·Fy·(1+λ̄x^(2n))^(-1/n)  [n=1.34] = <b>{rv['Crx']/1e3:.1f} kN</b>   Cr/A = <b>{rv['CrA_x']:.1f} MPa</b>  (Table T2)<br>
KLy/ry = {rv['KLy_ry']:.1f}   λ̄y = {rv['ly']:.4f}   β = 0.6+0.4×{rv['ly']:.4f} = <b>{rv['bv']:.4f}</b>  (≤ 0.85)<br>
U1x = <b>{rv['U1a']:.4f}</b>  (≥ 0)<br><br>
{rv['Cf']/1e3:.1f}/{rv['Crx']/1e3:.1f}  +  0.85×{rv['U1a']:.4f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_s']/1e6:.1f}  +  {rv['bv']:.4f}×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}<br>
= <b>{rv['T3a_A']:.4f}</b>  +  <b>{rv['T3a_B']:.4f}</b>  +  <b>{rv['T3a_C']:.4f}</b>  =  <b>{rv['r3a']:.4f}</b>
</div>""", unsafe_allow_html=True)
    st.markdown(rhtml(rv["r3a"]),unsafe_allow_html=True)

# ── Tab 4: Step 3b ──────────────────────────────────────────────────────────
with t4:
    st.markdown("## ④ Vérification de la pièce — avec déversement  [CSA S16-24 Cl. 13.8.4]")
    st.markdown(f'<div class="ibox">Cr uses <b>weak-axis</b> λ̄y. {rv["ltb"]}. U1x ≥ 1.0 (prevents double-counting P-δ already in Mrx).</div>',unsafe_allow_html=True)
    ca,cb=st.columns([1.5,1])
    with ca: st.plotly_chart(col_curve_fig(rv,"y"),use_container_width=True,key="cc3b")
    with cb: st.plotly_chart(stacked_bar(
        [rv["T3b_A"],rv["T3b_B"],rv["T3b_C"]],
        ["Cf/Cr(λ̄y)","0.85·U1x·Mfx/Mrx*","β·Mfy/Mry"],
        [TL,OR,PU],rv["r3b"],"Interaction (3b, LTB)"),
        use_container_width=True,key="s3bbar")
    st.markdown(f"""<div class="fbox">
KLy/ry = {rv['KLy_ry']:.1f}   Fe_y = {rv['Fey']:.1f} MPa   λ̄y = <b>{rv['ly']:.4f}</b><br>
Cr(λ̄y) = <b>{rv['Cry']/1e3:.1f} kN</b>   Cr/A = <b>{rv['CrA_y']:.1f} MPa</b>  (Table T2 — governs)<br>
LTB:  Lb = {rv['L']:.0f} mm   Lu = {rv['Lu']:,} mm  →  {'Mrx* = Mp = ' if rv['ltb_ok'] else 'LTB reduces Mrx* = '}<b>{rv['Mrx_b']/1e6:.1f} kN·m</b>  (Table T3)<br>
U1x = <b>{rv['U1b']:.4f}</b>  (≥ 1.0)<br><br>
{rv['Cf']/1e3:.1f}/{rv['Cry']/1e3:.1f}  +  0.85×{rv['U1b']:.4f}×{rv['Mfx']/1e6:.1f}/{rv['Mrx_b']/1e6:.1f}  +  {rv['bv']:.4f}×{rv['Mfy']/1e6:.1f}/{rv['Mry_s']/1e6:.1f}<br>
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
    st.markdown('<div class="ibox">These curves show how the three interaction ratios respond to load changes. The gold dot marks the current design point. Adjust sliders in the sidebar to watch all results update live.</div>',unsafe_allow_html=True)
    st.plotly_chart(sensitivity_fig(rv),use_container_width=True,key="sens")
    gov_step=("② Vérif. section" if rv["r2"]>=rv["r3a"] and rv["r2"]>=rv["r3b"]
              else ("③ Pièce sans dévers." if rv["r3a"]>=rv["r3b"] else "④ Pièce avec dévers."))
    st.markdown(f"""<div class="fbox">
Vérification gouvernante : <b>{gov_step}</b>  =  <b>{rv['gov']:.4f}</b>  —  {'ADÉQUAT ✓' if rv['ok'] else 'INADÉQUAT ✗'}<br>
Sarcelle = ② Vérif. section  |  Orange = ③ Pièce sans dévers.  |  Violet = ④ Pièce avec dévers.<br>
Green zone = safe (ratio &lt; 1.0)   |   Red zone = inadequate (ratio &gt; 1.0)
</div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='background:#FFF8E1;border:1.5px solid #F57F17;border-radius:6px;
            padding:12px 16px;font-size:.82rem;color:#7B3F00;margin-top:8px'>
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

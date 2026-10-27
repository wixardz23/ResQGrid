"""ResQGrid frontend-only prototype.

This file keeps the visual structure of app.py but removes Gemini, SQLite,
authentication, geocoding, weather, uploads processing, and other backend
actions. The displayed reports are static demo data.
"""

import html

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="ResQGrid —prototype",
    page_icon="🚨",
    layout="wide",
)


CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--bg:#0B1220;--panel:#121B2E;--panel2:#16233B;--line:#22304A;--text:#E6EDF7;--muted:#8FA3BF;--brand:#FF5A4E;--blue:#4DA3FF;}
html,body,.stApp,[class*="css"]{font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;}
.stApp{background:radial-gradient(1100px 480px at 88% -8%,rgba(77,163,255,.12),transparent 60%),radial-gradient(900px 420px at -5% 0%,rgba(255,90,78,.07),transparent 55%),var(--bg);}
header[data-testid="stHeader"]{background:transparent;}
#MainMenu,footer{visibility:hidden;}
[data-testid="stAppDeployButton"],.stDeployButton,.stAppDeployButton{display:none !important;}
.block-container{padding-top:1.2rem;padding-bottom:3rem;max-width:1760px;}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:6px 2px 14px;}
.brand{display:flex;align-items:center;gap:14px;}
.logo{width:46px;height:46px;border-radius:13px;background:linear-gradient(135deg,#FF5A4E,#E8384F);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:24px;color:#fff;box-shadow:0 6px 22px rgba(255,90,78,.35);}
.bt{font-size:26px;font-weight:800;letter-spacing:.04em;line-height:1.1;}
.bs{font-size:13px;color:var(--muted);margin-top:2px;}
.live{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:700;letter-spacing:.12em;color:#7BE5BC;background:#34D39914;border:1px solid #34D39944;padding:6px 14px;border-radius:999px;}
.pulse{width:8px;height:8px;border-radius:50%;background:#34D399;box-shadow:0 0 0 0 rgba(52,211,153,.7);animation:pulse 2s infinite;}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(52,211,153,.6);}70%{box-shadow:0 0 0 9px rgba(52,211,153,0);}100%{box-shadow:0 0 0 0 rgba(52,211,153,0);}}
.stTabs [data-baseweb="tab-list"]{gap:6px;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{height:48px;padding:0 22px;border-radius:12px 12px 0 0;color:var(--muted);font-weight:600;font-size:15px;}
.stTabs [data-baseweb="tab"]:hover{color:var(--text);background:#ffffff08;}
.stTabs [aria-selected="true"]{color:var(--text);background:var(--panel);}
.stTabs [data-baseweb="tab-highlight"]{background:var(--brand);height:3px;}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:16px;}
[data-testid="stVerticalBlockBorderWrapper"]>div[data-testid="stVerticalBlock"]{gap:.6rem;}
.stButton>button,.stDownloadButton>button{border-radius:12px;font-weight:600;border:1px solid #2A3E63;background:var(--panel2);color:var(--text);transition:all .15s ease;}
.stButton>button:hover{border-color:var(--blue);color:#fff;transform:translateY(-1px);}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#FF5A4E,#E8384F);border:none;color:#fff;font-weight:700;font-size:16px;height:52px;box-shadow:0 8px 24px rgba(232,56,79,.30);}
.stButton>button[kind="primary"]:hover{filter:brightness(1.08);color:#fff;}
.stTextInput input,.stTextArea textarea,.stNumberInput input{border-radius:12px;background:#0F1A2E;border:1px solid #2A3E63;}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(77,163,255,.18);}
[data-testid="stFileUploaderDropzone"]{border:1.5px dashed #34476A;border-radius:14px;background:#0F1A2E;}
[data-testid="stFileUploaderDropzone"]:hover{border-color:var(--blue);}
[data-testid="stImage"] img{border-radius:12px;}
[data-testid="stExpander"]{border:1px solid var(--line);border-radius:14px;background:var(--panel);overflow:hidden;}
[data-testid="stExpander"] summary{font-weight:600;padding:14px 16px;}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:14px;overflow:hidden;}
.sec-title{font-size:23px;font-weight:800;margin-top:4px;}
.sec-sub{color:var(--muted);font-size:13.5px;margin-bottom:10px;}
.sec-h{font-size:18px;font-weight:700;margin:26px 0 10px;display:flex;align-items:center;justify-content:space-between;}
.sec-h small{color:var(--muted);font-weight:500;font-size:13px;}
.step{display:flex;align-items:center;gap:12px;}
.step b{width:28px;height:28px;border-radius:50%;background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;flex:none;}
.stp-t{font-weight:700;font-size:16px;line-height:1.2;}
.stp-h{color:var(--muted);font-size:12.5px;}
.or{display:flex;align-items:center;gap:12px;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.12em;font-weight:700;margin:6px 0 2px;}
.or:before,.or:after{content:'';flex:1;height:1px;background:var(--line);}
.pill{display:inline-flex;align-items:center;padding:4px 12px;border-radius:999px;font-size:12.5px;font-weight:700;border:1px solid;white-space:nowrap;margin:0 6px 4px 0;}
.chip{display:inline-block;margin:0 6px 6px 0;padding:5px 11px;border-radius:9px;background:#1B2A45;border:1px solid #2A3E63;font-size:13px;}
.field{margin-bottom:16px;}
.fl{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:5px;}
.fv{font-size:15px;line-height:1.6;}
.fn{font-size:12.5px;color:var(--muted);margin-top:4px;}
.quote{display:block;border-left:3px solid var(--blue);padding:9px 13px;background:#0F1A2E;border-radius:6px;font-style:italic;}
.banner{padding:12px 15px;border-radius:12px;font-size:14px;margin:10px 0;border:1px solid;line-height:1.5;}
.banner.ok{background:#34D39914;border-color:#34D39955;color:#8FEBC6;}
.banner.warn{background:#FFA63D14;border-color:#FFA63D55;color:#FFC983;}
.banner.info{background:#4DA3FF14;border-color:#4DA3FF55;color:#A9D1FF;}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin-bottom:14px;}
.result{background:linear-gradient(180deg,#16233B,#121B2E);border:1px solid var(--line);border-radius:18px;padding:22px;margin-bottom:14px;}
.r-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:700;}
.r-title{font-size:32px;font-weight:800;margin-top:2px;line-height:1.15;}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px;}
.stat{background:#0F1A2E;border:1px solid var(--line);border-radius:13px;padding:13px 15px;}
.sl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.09em;font-weight:700;}
.sv{font-size:32px;font-weight:800;line-height:1.25;}
.sv span{font-size:15px;color:var(--muted);font-weight:600;}
.ss{font-size:12.5px;color:var(--muted);margin-top:6px;line-height:1.45;}
.sev{display:flex;gap:4px;margin-top:6px;}
.sev i{flex:1;height:6px;border-radius:3px;display:block;}
.empty{border:1.5px dashed #2A3E63;border-radius:18px;padding:34px 26px;text-align:center;background:#0F1A2E88;}
.e-ic{font-size:34px;}.e-t{font-size:20px;font-weight:700;margin-top:6px;}.e-s{color:var(--muted);font-size:14px;margin-top:4px;}
.how{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px;text-align:left;}
.how div{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:13.5px;font-weight:600;}
.how b{display:inline-flex;width:22px;height:22px;border-radius:50%;background:var(--brand);color:#fff;align-items:center;justify-content:center;font-size:12px;margin-right:8px;}
.how small{display:block;color:var(--muted);font-weight:500;margin-top:4px;font-size:12px;}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px 18px;}
.kl{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.09em;font-weight:700;}
.kl i{width:9px;height:9px;border-radius:50%;display:inline-block;}.kn{font-size:42px;font-weight:800;line-height:1.15;margin-top:4px;}.ks{font-size:12.5px;color:var(--muted);}
.inc-head{margin-bottom:12px;}.inc-score{color:var(--muted);font-size:13px;margin-left:6px;}.inc-score b{color:var(--text);font-size:15px;}
.nophoto{height:170px;border:1.5px dashed #2A3E63;border-radius:12px;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:13px;background:#0F1A2E;text-align:center;padding:10px;}
.trk{display:flex;align-items:center;margin:18px 0 4px;}.trk-s{display:flex;flex-direction:column;align-items:center;gap:6px;flex:none;width:96px;text-align:center;font-size:12.5px;font-weight:600;color:var(--muted);}
.trk-s b{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#1B2A45;border:2px solid #2A3E63;font-size:14px;}.trk-s.done{color:var(--text);}.trk-s.done b{background:#34D399;border-color:#34D399;color:#05281D;}.trk-s.now{color:var(--text);}.trk-s.now b{background:var(--brand);border-color:var(--brand);color:#fff;box-shadow:0 0 0 5px rgba(255,90,78,.20);}.trk-l{flex:1;height:3px;background:#2A3E63;margin:0 2px 24px;border-radius:2px;}.trk-l.done{background:#34D399;}.trk-code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:30px;font-weight:800;letter-spacing:.08em;margin:6px 0;color:#fff;}
@media (max-width:900px){.stats,.how{grid-template-columns:1fr;}.r-title{font-size:26px;}}
</style>"""


def H(markup: str, target=st):
    target.markdown("".join(line.strip() for line in markup.strip().splitlines()), unsafe_allow_html=True)


def esc(value) -> str:
    return html.escape(str(value))


def pill(text: str, color: str) -> str:
    return f"<span class='pill' style='color:{color};background:{color}22;border-color:{color}66'>{esc(text)}</span>"


def chip(text: str) -> str:
    return f"<span class='chip'>{esc(text)}</span>"


def sev_bar(severity: int, color: str = "#FF5A4E") -> str:
    return "<div class='sev'>" + "".join(
        f"<i style='background:{color if n < severity else '#22304A'}'></i>" for n in range(5)
    ) + "</div>"


def step_head(number, title: str, hint: str) -> str:
    return f"<div class='step'><b>{number}</b><div><div class='stp-t'>{title}</div><div class='stp-h'>{hint}</div></div></div>"


def banner(kind: str, text: str) -> str:
    return f"<div class='banner {kind}'>{esc(text)}</div>"


def kpi(label: str, value, color: str, sub: str) -> str:
    return f"<div class='kpi'><div class='kl'><i style='background:{color}'></i>{label}</div><div class='kn'>{value}</div><div class='ks'>{sub}</div></div>"


H(CSS)
H("""
<div class='topbar'>
  <div class='brand'><div class='logo'>R</div><div><div class='bt'>ResQGrid</div><div class='bs'>Turning disaster reports into coordinated relief</div></div></div>
  <div class='live'><span class='pulse'></span>Live</div>
</div>
""")


tab_submit, tab_track, tab_dashboard = st.tabs(["Submit report", "Track report", "Control room"])


with tab_submit:
    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        H("<div class='sec-title'>New incident report</div><div class='sec-sub'>Frontend preview — backend processing is not connected.</div>")
        with st.container(border=True):
            H(step_head(1, "Photo (optional)", "Helps verify the report"))
            st.file_uploader("Upload incident photo", type=["jpg", "jpeg", "png", "webp"], disabled=True)
        with st.container(border=True):
            H(step_head(2, "Location", "Area, landmark, town and state"))
            st.text_input("Incident location", placeholder="e.g. Sector 17, Chandigarh")
            with st.expander("Exact coordinates (optional)"):
                c1, c2 = st.columns(2)
                c1.number_input("Latitude", value=30.7333, format="%.4f")
                c2.number_input("Longitude", value=76.7794, format="%.4f")
        with st.container(border=True):
            H(step_head(3, "What happened", "Type it, speak it, or both"))
            st.text_area("Incident details", placeholder="Describe what is happening...", height=120)
            H("<div class='or'>or send a voice note</div>")
            st.file_uploader("Upload a voice note", type=["wav", "mp3", "ogg", "flac", "aac"], disabled=True)
        st.button("Analyze & triage report", type="primary", use_container_width=True, disabled=True)

    with col_output:
        H("<div class='sec-title'>Triage assessment</div><div class='sec-sub'>The assessment will appear here after backend integration.</div>")
        H("""
        <div class='empty'>
          <div class='e-ic'>⚡</div><div class='e-t'>Awaiting an incident report</div>
          <div class='e-s'>Submit a photo, location and description to see the triage result.</div>
          <div class='how'><div><b>1</b>Submit<small>Share what happened</small></div><div><b>2</b>Verify<small>Review the assessment</small></div><div><b>3</b>Coordinate<small>Connect responders</small></div></div>
        </div>
        """)


with tab_track:
    col_form, col_status = st.columns([1, 1], gap="large")
    with col_form:
        H("<div class='sec-title'>Track your report</div><div class='sec-sub'>Use the code received after submitting a report.</div>")
        with st.container(border=True):
            H(step_head("🔎", "Your tracking code", "It looks like RAH-7K2M9-QXD4F"))
            st.text_input("Tracking code", placeholder="RAH-XXXXX-XXXXX")
            st.button("Check status", type="primary", use_container_width=True, disabled=True)
        H(banner("info", "If someone is in immediate danger, call 112 right away. Do not wait for an update here."))

    with col_status:
        H("<div class='sec-title'>Report status</div><div class='sec-sub'>Only the status of your own report is shown.</div>")
        H("""
        <div class='empty'>
          <div class='e-ic'>🔎</div><div class='e-t'>Check on your report</div>
          <div class='e-s'>Enter your tracking code to view the response status.</div>
        </div>
        """)


with tab_dashboard:
    H("<div class='sec-title'>Control room</div><div class='sec-sub'>Frontend preview — static incident data for layout testing.</div>")
    st.caption("Authentication and live data are intentionally disabled in this frontend-only version.")

    k1, k2, k3, k4 = st.columns(4)
    H(kpi("Active incidents", 12, "#4DA3FF", "8 awaiting dispatch · 4 dispatched"), k1)
    H(kpi("High priority", 4, "#FF4D5E", "Awaiting dispatch"), k2)
    H(kpi("Medium priority", 5, "#FFA63D", "Awaiting dispatch"), k3)
    H(kpi("Low priority", 3, "#34D399", "Awaiting dispatch"), k4)

    H(banner("ok", "12 reports received → 9 incidents after duplicate review"))
    H("<div class='sec-h'>Live incident map<small>Preview placeholder</small></div>")
    H("<div class='empty'><div class='e-ic'>🗺️</div><div class='e-t'>Live incident map</div><div class='e-s'>The interactive map will be connected when location and incident services are added.</div></div>")

    H("<div class='sec-h'>Ranked incident list<small>Awaiting dispatch first, then by priority</small></div>")
    table = pd.DataFrame([
        [1, "🔴 High", "New", 92.4, "Flash Flood", 5, "30", 3, "Consistent", "Sector 17, Chandigarh"],
        [2, "🟠 Medium", "New", 61.8, "Building Fire", 4, "12", 2, "Partly consistent", "Industrial Area, Mohali"],
        [3, "🟢 Low", "Dispatched", 28.5, "Road Blockage", 2, "Unknown", 1, "Not provided", "Kharar Road"],
    ], columns=["Rank", "Priority", "Status", "Score", "Hazard", "Severity", "People", "Reports", "Photo check", "Location"])
    st.dataframe(table, use_container_width=True, hide_index=True)

    H("<div class='sec-h'>Top incidents<small>Details, dispatch status and responder alerts</small></div>")
    for title, location, level, status, summary, people in [
        ("Flash Flood", "Sector 17, Chandigarh", "High", "New", "Water rising near the market entrance; several people may be stranded.", "30 people"),
        ("Building Fire", "Industrial Area, Mohali", "Medium", "New", "Smoke reported from a warehouse block. Residents are moving away from the area.", "12 people"),
        ("Road Blockage", "Kharar Road", "Low", "Dispatched", "A fallen tree is blocking one lane after heavy rain.", "Unknown"),
    ]:
        with st.expander(f"{title}  ·  {location}  ·  {level} priority  ·  {status}"):
            H(pill(level + " priority", {"High": "#FF4D5E", "Medium": "#FFA63D", "Low": "#34D399"}[level]) + pill(status, "#4DA3FF"))
            c1, c2 = st.columns([1, 2], gap="large")
            with c1:
                H("<div class='nophoto'>No photo preview</div>")
            with c2:
                H(f"<div class='field'><div class='fl'>Summary</div><div class='fv'>{esc(summary)}</div></div>"
                  f"<div class='field'><div class='fl'>People at risk</div><div class='fv'>{esc(people)}</div></div>"
                  f"<div class='field'><div class='fl'>Resources needed</div><div class='fv'>{chip('Emergency team')}{chip('Medical support')}{chip('Traffic control')}</div></div>")
                st.button("Mark dispatched", key=f"dispatch_{title}", disabled=True)
                st.button("Generate responder alert", key=f"alert_{title}", disabled=True)


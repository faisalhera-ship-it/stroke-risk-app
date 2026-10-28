import streamlit as st
import urllib.parse
import pandas as pd
import requests
from datetime import datetime

# --- 1. SETUP UI & GLOBAL STYLES ---
st.set_page_config(page_title="SINTALA v8.0", layout="wide", page_icon="🩺")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root{--navy:#102544;--blue:#1769aa;--gold:#d9ad54;--ink:#18283f;--muted:#64748b;--line:#e4ebf3}
html,body,[class*="css"]{font-family:'Plus Jakarta Sans',sans-serif}
.stApp{background:radial-gradient(circle at 8% 0%,rgba(36,112,184,.08),transparent 27rem),linear-gradient(180deg,#f5f8fc 0%,#f8fafc 55%,#eef4fa 100%);color:var(--ink)}
.block-container{max-width:1440px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3{color:var(--navy);letter-spacing:-.035em;font-weight:800!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#102544 0%,#173b64 100%);border-right:1px solid rgba(255,255,255,.1)}
[data-testid="stSidebar"] *{color:#f7faff}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#e3edf8}
[data-testid="stSidebar"] .stButton>button{background:rgba(255,255,255,.10)!important;color:white!important;border:1px solid rgba(255,255,255,.18)!important}
.stButton>button,.stFormSubmitButton>button{min-height:3rem;border-radius:13px!important;border:1px solid #d6e2ef!important;background:#fff!important;color:var(--navy)!important;font-weight:700!important;box-shadow:0 5px 16px rgba(16,37,68,.06);transition:transform .15s ease,box-shadow .15s ease}
.stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-1px);border-color:#7fa9d5!important;box-shadow:0 9px 22px rgba(16,37,68,.12)}
.stFormSubmitButton>button{background:linear-gradient(135deg,#1769aa,#102f56)!important;color:#fff!important;border:none!important}
.stTextInput input,.stNumberInput input,.stSelectbox [data-baseweb="select"],.stTextArea textarea{border-radius:11px!important;border-color:#d8e3ef!important;background:#fff!important}
div[data-testid="stForm"]{background:rgba(255,255,255,.9);padding:clamp(1rem,2vw,1.7rem);border:1px solid var(--line);border-radius:20px;box-shadow:0 12px 32px rgba(16,37,68,.045)}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);padding:1rem;border-radius:16px;box-shadow:0 5px 18px rgba(16,37,68,.04)}
div[data-testid="stAlert"]{border-radius:13px}hr{border-color:var(--line)!important}
.role-card{min-height:205px;background:linear-gradient(145deg,#fff,#f4f8fd);padding:28px 24px;border-radius:22px;text-align:left;border:1px solid #dce7f2;border-top:5px solid #1769aa;box-shadow:0 14px 34px rgba(16,37,68,.07)}
.role-card h3{margin-top:0;font-size:1.35rem}.role-card p{color:#53657b;line-height:1.65}
.hero-panel{background:linear-gradient(120deg,#102544 0%,#174c7d 68%,#1b6c9e 100%);color:white;padding:clamp(1.5rem,4vw,3rem);border-radius:28px;margin-bottom:1.5rem;box-shadow:0 20px 45px rgba(16,37,68,.18);position:relative;overflow:hidden}
.hero-panel h1,.hero-panel h2,.hero-panel p{color:white!important}
.hero-kicker{color:#f2d28b;text-transform:uppercase;letter-spacing:.16em;font-size:.78rem;font-weight:800;margin-bottom:.5rem}
.hero-sub{color:#dce9f7!important;font-size:1.02rem;line-height:1.7}
.section-eyebrow{text-transform:uppercase;letter-spacing:.12em;color:#647f9d;font-size:.75rem;font-weight:800;margin-bottom:.25rem}
.wa-btn{background:#168c57;color:white!important;padding:14px 18px;border-radius:12px;text-align:center;font-weight:700;text-decoration:none;display:block;margin:12px 0 18px;box-shadow:0 8px 18px rgba(22,140,87,.18)}
.print-report{background:#fff;padding:35px;border:1px solid #cbd5e1;border-radius:12px;color:#111827;line-height:1.6;margin-top:20px;box-shadow:0 10px 28px rgba(16,37,68,.06)}
.kop-surat{text-align:center;border-bottom:4px double #333;margin-bottom:15px}
.scorecard-high,.scorecard-med,.scorecard-low{padding:25px;border-radius:18px;color:#172033;margin-top:1rem;box-shadow:0 10px 26px rgba(16,37,68,.06)}
.scorecard-high{background:#fff1f1;border:1px solid #ffcaca;border-left:7px solid #d93d4b}
.scorecard-med{background:#fff7e8;border:1px solid #ffe0a8;border-left:7px solid #e59a23}
.scorecard-low{background:#ecfbf2;border:1px solid #bce9cc;border-left:7px solid #21945a}
@media(max-width:768px){.block-container{padding-top:1rem}.role-card{min-height:auto;padding:20px}div[data-testid="stForm"]{padding:1rem}}
@media print{.no-print,header,footer,[data-testid="stHeader"],[data-testid="stSidebar"],.stButton,.wa-btn{display:none!important}.print-report{border:none!important;box-shadow:none!important;padding:0!important;width:100%!important}.stApp{background:white!important}}
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'role' not in st.session_state: st.session_state.role = None
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'menu_nakes' not in st.session_state: st.session_state.menu_nakes = "Home"

# --- 3. HOMEPAGE: PILIHAN AKSES (NAKES VS NON-NAKES) ---
if not st.session_state.role:
    st.markdown("""
    <div class="hero-panel">
      <div class="hero-kicker">System Integration Neurology Tanah Laut</div>
      <h1 style="font-size:clamp(2.1rem,5vw,3.5rem);margin:0;">SINTALA <span style="color:#f2d28b;">v8.0</span></h1>
      <p class="hero-sub" style="max-width:760px;margin-top:.7rem;">Stroke Integrated Analysis & Screening System</p>
      <p style="max-width:760px;margin-bottom:0;">Platform pendukung penilaian klinis, skrining risiko stroke, dan dokumentasi untuk membantu alur kerja layanan kesehatan.</p>
    </div>
    <div class="section-eyebrow">Pilih ruang akses</div>
    <h2 style="margin-top:0;">Mulai dari kebutuhan Anda</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='role-card'><h3>👨‍⚕️ Tenaga Medis (Nakes)</h3><p>Akses klinis: FSRP, NIHSS (SOAP), & Siriraj Score</p></div>", unsafe_allow_html=True)
        st.write("")
        dr_input = st.text_input("Nama Dokter / Petugas Medis:")
        if st.button("Masuk Layanan Nakes", use_container_width=True):
            if dr_input:
                st.session_state.role = "Nakes"
                st.session_state.dr = dr_input
                st.rerun()
            else:
                st.warning("Mohon masukkan nama Dokter/Petugas Medis terlebih dahulu.")

    with col2:
        st.markdown("<div class='role-card' style='border-top-color:#28a745;'><h3>👨‍👩‍👧‍👦 Masyarakat (Non-Nakes)</h3><p>Skrining Mandiri Risiko Stroke (Stroke Risk Scorecard)</p></div>", unsafe_allow_html=True)
        st.write("")
        if st.button("Mulai Skrining Mandiri", use_container_width=True):
            st.session_state.role = "Non-Nakes"
            st.rerun()

    st.stop()

# --- 4. SIDEBAR UTAMA ---
with st.sidebar:
    st.markdown("<div style='padding:8px 0 18px;'><div style='font-size:.72rem;letter-spacing:.15em;color:#f2d28b;font-weight:800;'>SINTALA v8.0</div><div style='font-size:1.25rem;font-weight:800;color:#ffffff;'>Clinical Workspace</div></div>", unsafe_allow_html=True)
    st.markdown(f"**Status Akses**  \n{st.session_state.role}")
    if st.session_state.dr:
        st.markdown(f"DPJP/Petugas: **{st.session_state.dr}**")
    
    if st.session_state.role == "Nakes":

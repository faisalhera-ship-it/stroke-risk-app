import streamlit as st
from datetime import datetime

# --- 1. SETUP UI & CSS ---
st.set_page_config(page_title="SINTALA v6.0", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    div.stButton > button {
        height: 60px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }
    
    .print-report {
        background-color: white; padding: 30px; border: 2px solid #333;
        border-radius: 8px; color: black; line-height: 1.5; margin-top: 20px;
    }
    .kop-surat { text-align: center; border-bottom: 3px double #333; margin-bottom: 15px; }
    
    @media print {
        .no-print, header, footer, [data-testid="stHeader"], [data-testid="stSidebar"], .stButton {
            display: none !important;
        }
        .print-report { border: none !important; padding: 0 !important; width: 100% !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'menu' not in st.session_state: st.session_state.menu = "Home"

# --- 3. LOGIN ---
if not st.session_state.dr:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h1 style='text-align:center;'>🩺 SINTALA</h1>", unsafe_allow_html=True)
        dr_input = st.text_input("Nama Dokter Pemeriksa:")
        if st.button("Buka Dashboard", use_container_width=True):
            if dr_input:
                st.session_state.dr = dr_input
                st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.write(f"DPJP: **{st.session_state.dr}**")
    if st.button("🏠 Menu Utama", use_container_width=True): 
        st.session_state.menu = "Home"
        st.rerun()
    st.info("💡 Tekan Ctrl+P untuk print laporan.")

# --- 5. MENU UTAMA ---
if st.session_state.menu == "Home":
    st.subheader("Instrumen Klinis Stroke")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📊 FSRP\n(Skrining)", use_container_width=True): st.session_state.menu = "FSRP"; st.rerun()
    with c2:
        if st.button("🚨 NIHSS\n(Emergency)", use_container_width=True): st.session_state.menu = "NIHSS"; st.rerun()
    with c3:
        if st.button("🧠 SIRIRAJ\n(Diagnostik)", use_container_width=True): st.session_state.menu = "SIRIRAJ"; st.rerun()

# --- 6. MODUL FSRP ---
elif st.session_state.menu == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile")
    with st.form("fsrp_form"):
        p_nama = st.text_input("Nama Pasien")
        p_umur = st.number_input("Umur", 30, 90, 50)
        c1, c2 = st.columns(2)
        with c1:
            tds = st.number_input("TD Sistolik", 90, 220, 120)
            chol = st.number_input("Total Kolesterol", 100, 500, 200)
        with c2:
            cvd = st.selectbox("Penyakit Jantung", [0, 1], format_func=lambda x: "Tidak Ada" if x==0 else "Ada (AF/PJK/CHF)")
            smoke = st.selectbox("Merokok", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        
        submit = st.form_submit_button("Generate Laporan FSRP")
        if submit:
            st.markdown(f"""
                <div class="print-report">
                    <div class="kop-surat"><h2>LAPORAN SKRINING FSRP</h2></div>
                    <p><b>DPJP:</b> {st.session_state.dr} | <b>Waktu:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
                    <p><b>Pasien:</b> {p_nama} ({p_umur} th)</p>
                    <hr>
                    <p>TD Sistolik: {tds} mmHg | Kolesterol: {chol} mg/dL</p>
                    <p>Riwayat Penyakit Jantung: {"Ada" if cvd==1 else "Tidak"}</p>
                    <p>Status Merokok: {"Ya" if smoke==1 else "Tidak"}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 7. MODUL NIHSS (DESKRIPTIF) ---
elif st.session_state.menu == "NIHSS":
    st.header("🚨 NIHSS Assessment (Deskriptif)")
    with st.form("nihss_form"):
        p_nama = st.text_input("Nama Pasien")
        c1, c2 = st.columns(2)
        with c1:
            n1 = st.selectbox("1a. LOC", [0,1,2,3], format_func=lambda x: {0:"0: Sadar", 1:"1: Somnolen", 2:"2: Stupor", 3:"3: Koma"}[x])
            n2 = st.selectbox("2. Gaze", [0,1,2], format_func=lambda x: {0:"0: Normal", 1:"1: Paresis Parsial", 2:"2: Deviasi Paksa"}[x])
            n4 = st.selectbox("4. Facial Palsy", [0,1,2,3], format_func=lambda x: {0:"0: Normal", 1:"1: Minor", 2:"2: Parsial", 3:"3: Komplit"}[x])
        with c2:
            n5 = st.selectbox("5. Motorik Lengan", [0,1,2,3,4], format_func=lambda x: {0:"0: No Drift", 1:"1: Drift", 2:"2: Lawan Gravitasi", 3:"3: Tidak ada upaya", 4:"4: Lumpuh"}[x])
            n9 = st.selectbox("9. Bahasa", [0,1,2,3], format_func=lambda x: {0:"0: Normal", 1:"1: Ringan", 2:"2: Berat", 3:"3: Global"}[x])
            plan = st.text_area("Plan", "O2, Loading Aspilet...")
            
        if st.form_submit_button("Generate Laporan NIHSS"):
            skor = n1+n2+n4+n5+n9
            st.markdown(f"""
                <div class="print-report">
                    <div class="kop-surat"><h2>RESUME MEDIS NIHSS</h2></div>
                    <p><b>DPJP:</b> {st.session_state.dr} | <b>Pasien:</b> {p_nama}</p>
                    <hr>
                    <h3>SKOR NIHSS: {skor}</h3>
                    <p><b>Plan:</b> {plan}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 8. MODUL SIRIRAJ ---
elif st.session_state.menu == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score")
    with st.form("sss_form"):
        p_nama = st.text_input("Nama Pasien")
        c1, c2 = st.columns(2)
        with c1:
            sadar = st.selectbox("Kesadaran", [0,1,2], format_func=lambda x: {0:"Sadar", 1:"Stupor", 2:"Koma"}[x])
            muntah = st.selectbox("Muntah", [0,1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        with c2:
            nyeri = st.selectbox("Nyeri Kepala", [0,1], format_func=lambda x: "Tidak" if x==0 else "Ya")
            dbp = st.number_input("TD Diastolik", 60, 150, 90)
            
        if st.form_submit_button("Hitung Siriraj"):
            sss = (2.5*sadar) + (2*muntah) + (2*nyeri) + (0.1*dbp) - 12
            hasil = "Hemoragik" if sss > 1 else "Iskemik" if sss < -1 else "Perlu CT-Scan"
            st.markdown(f"""
                <div class="print-report">
                    <div class="kop-surat"><h2>HASIL SIRIRAJ STROKE SCORE</h2></div>
                    <p><b>Pasien:</b> {p_nama} | <b>Skor SSS:</b> {sss:.1f}</p>
                    <h3>Interpretasi: Prediksi Stroke {hasil}</h3>
                </div>
            """, unsafe_allow_html=True)

import streamlit as st
from datetime import datetime

# --- 1. SESSION STATE & CONFIG ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""
if 'pilihan_layanan' not in st.session_state:
    st.session_state.pilihan_layanan = None

st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- 2. CSS MODERN & OPTIMASI PRINT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    .hero-card {
        background: white; padding: 40px; border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;
        text-align: center; margin-bottom: 20px;
    }
    .author-badge { color: #004a99; font-weight: 700; font-size: 1.2rem; margin-top: -10px; margin-bottom: 20px; }
    
    @media print {
        header, footer, .no-print, [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, button {
            display: none !important;
        }
        .stApp { background-color: white !important; }
        .print-area {
            position: absolute; left: 0; top: 0; width: 100% !important;
            margin: 0 !important; padding: 30px !important; color: black !important;
        }
        .score-box {
            background-color: #f1f5f9 !important;
            -webkit-print-color-adjust: exact;
            border: 2px solid #004a99 !important;
            padding: 25px !important; border-radius: 12px !important;
            text-align: center !important; margin: 20px 0 !important;
        }
    }

    .score-box {
        background-color: #f1f5f9; padding: 25px; border-radius: 12px;
        border: 2px solid #004a99; text-align: center; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
if not st.session_state.nama_dokter:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_m, _ = st.columns([1, 1.5, 1])
    with col_m:
        st.markdown(f"""
            <div class='hero-card'>
                <h1 style='color: #004a99; margin: 0;'>🩺 SINTALA-STROKE</h1>
                <p class='author-badge'>by. dr. Faisal Bayu</p>
                <p style='color: #64748b;'>Sistem Informasi & Analisa Stroke Terpadu<br>Tanah Laut, Kalimantan Selatan</p>
            </div>
        """, unsafe_allow_html=True)
        dr_name = st.text_input("Nama Lengkap Dokter (DPJP):", placeholder="dr. Faisal Bayu, Sp.N")
        if st.button("Masuk Ke Dashboard", use_container_width=True):
            if dr_name:
                st.session_state.nama_dokter = dr_name
                st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f"### DPJP: \\n**{st.session_state.nama_dokter}**")
    if st.button("🏠 Menu Utama", use_container_width=True):
        st.session_state.pilihan_layanan = None
        st.rerun()
    st.divider()
    st.write("### 🖨️ Cetak Laporan")
    st.markdown('<button onclick="window.print()" style="width:100%; height:3.5em; background:#16a34a; color:white; border:none; border-radius:12px; font-weight:bold; cursor:pointer;">CETAK / SIMPAN PDF</button>', unsafe_allow_html=True)
    st.caption("Developed by dr. Faisal Bayu")

# --- 5. DASHBOARD ---
if st.session_state.pilihan_layanan is None:
    st.markdown("### Dashboard Medis")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📊 FSRP \\n(Risiko 10 Thn)", use_container_width=True, height=100):
            st.session_state.pilihan_layanan = "FSRP"
            st.rerun()
    with c2:
        if st.button("🚨 NIHSS \\n(Defisit Akut)", use_container_width=True, height=100):
            st.session_state.pilihan_layanan = "NIHSS"
            st.rerun()
    with c3:
        if st.button("🧠 SIRIRAJ \\n(Diagnostik)", use_container_width=True, height=100):
            st.session_state.pilihan_layanan = "SIRIRAJ"
            st.rerun()
    st.stop()

# --- 6. MODUL FSRP ---
if st.session_state.pilihan_layanan == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile")
    with st.form("fsrp_form"):
        p_nama = st.text_input("Nama Pasien", "Pasien Anonim")
        col1, col2 = st.columns(2)
        with col1:
            usia = st.checkbox("Usia ≥ 55 Tahun")
            tds = st.number_input("TD Sistolik (mmHg)", 90, 250, 120)
            kol = st.number_input("Kolesterol Total (mg/dL)", 100, 500, 190)
        with col2:
            dm = st.checkbox("Diabetes Melitus")
            smk = st.checkbox("Merokok Aktif")
            jantung = st.multiselect("Riwayat Jantung", ["PJK", "AF", "LVH (EKG)"])
        submit_fsrp = st.form_submit_button("HITUNG ANALISA FSRP", use_container_width=True)

    if submit_fsrp:
        p_kol = 2 if kol >= 200 else 0
        skor_fsrp = sum([usia*2, (tds>=140)*3, smk*3, dm*2, ("PJK" in jantung)*2, ("AF" in jantung)*4, ("LVH (EKG)" in jantung)*5, p_kol])
        kat_fsrp = "TINGGI" if skor_fsrp >= 7 else "RENDAH"
        
        st.markdown(f"""
            <div class="print-area">
                <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px;">
                    <h2 style="margin: 0;">LAPORAN ANALISA RISIKO STROKE (FSRP)</h2>
                    <h4 style="margin: 0; color: #004a99;">SINTALA-STROKE by. dr. Faisal Bayu</h4>
                </div>
                <br>
                <p><b>DPJP:</b> {st.session_state.nama_dokter} | <b>Pasien:</b> {p_nama} | <b>Tgl:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
                <div class="score-box">
                    <h2 style="margin: 0;">TOTAL SKOR: {skor_fsrp}</h2>
                    <h1 style="margin: 5px; color: {'#dc2626' if kat_fsrp == 'TINGGI' else '#16a34a'};">RISIKO: {kat_fsrp}</h1>
                </div>
                <div style="margin-top: 50px; text-align: right;">( {st.session_state.nama_dokter} )</div>
            </div>
        """, unsafe_allow_html=True)

# --- 7. MODUL NIHSS ---
elif st.session_state.pilihan_layanan == "NIHSS":
    st.header("🚨 National Institutes of Health Stroke Scale")
    with st.form("nihss_form"):
        p_nama_nihss = st.text_input("Nama Pasien", "Pasien Anonim")
        c1, c2 = st.columns(2)
        with c1:
            n1a = st.selectbox("1a. LOC", ["0: Sadar", "1: Mengantuk", "2: Stupor", "3: Koma"])
            n1b = st.selectbox("1b. LOC Tanya", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n1c = st.selectbox("1c. LOC Perintah", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n2 = st.selectbox("2. Gaze", ["0: Normal", "1: Paresis", "2: Deviasi"])
            n3 = st.selectbox("3. Visual", ["0: Normal", "1: Parsial", "2: Komplit", "3: Bilateral"])
            n4 = st.selectbox("4. Facial Palsy", ["0: Normal", "1: Minor", "2: Parsial", "3: Komplit"])
        with c2:
            n5 = st.selectbox("5. Motor Lengan", ["0: Normal", "1: Drift", "2: Lawan Gravitasi", "3: Tak Bergerak"])
            n6 = st.selectbox("6. Motor Tungkai", ["0: Normal", "1: Drift", "2: Lawan Gravitasi", "3: Tak Bergerak"])
            n7 = st.selectbox("7. Ataksia", ["0: Tak Ada", "1: 1 Ekstremitas", "2: 2 Ekstremitas"])
            n8 = st.selectbox("8. Sensorik", ["0: Normal", "1: Ringan", "2: Berat"])
            n9 = st.selectbox("9. Afasia", ["0: Normal", "1: Ringan", "2: Berat", "3: Global"])
            n10 = st.selectbox("10. Disartria", ["0: Normal", "1: Ringan", "2: Berat"])
            n11 = st.selectbox("11. Neglect", ["0: Normal", "1: Ringan", "2: Berat"])
        submit_nihss = st.form_submit_button("HITUNG TOTAL NIHSS", use_container_width=True)

    if submit_nihss:
        total_nihss = sum([int(x[0]) for x in [n1a, n1b, n1c, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11]])
        kat_nihss = "Stroke Ringan" if total_nihss <= 4 else "Stroke Sedang" if total_nihss <= 15 else "Stroke Berat"
        st.markdown(f"""
            <div class="print-area">
                <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px;">
                    <h2 style="margin: 0;">LAPORAN EVALUASI NIHSS</h2>
                    <h4 style="margin: 0; color: #004a99;">SINTALA-STROKE by. dr. Faisal Bayu</h4>
                </div>
                <br>
                <p><b>Pasien:</b> {p_nama_nihss} | <b>DPJP:</b> {st.session_state.nama_dokter}</p>
                <div class="score-box">
                    <h1 style="margin: 0; font-size: 45px;">TOTAL SKOR: {total_nihss}</h1>
                    <h3 style="margin: 0;">KATEGORI: {kat_nihss.upper()}</h3>
                </div>
                <div style="margin-top: 50px; text-align: right;">( {st.session_state.nama_dokter} )</div>
            </div>
        """, unsafe_allow_html=True)

# --- 8. MODUL SIRIRAJ ---
elif st.session_state.pilihan_layanan == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score")
    with st.form("sss_form"):
        p_nama_sss = st.text_input("Nama Pasien", "Pasien Anonim")
        c1, c2 = st.columns(2)
        with c1:
            kes = st.selectbox("Kesadaran", ["0: Sadar", "1: Somnolen", "2: Koma"])
            mun = st.radio("Muntah Proyektil", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            nye = st.radio("Nyeri Kepala (2 jam)", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        with c2:
            dia = st.number_input("TD Diastolik", 50, 150, 90)
            ath = st.checkbox("Atheroma (DM/PJK)")
        submit_sss = st.form_submit_button("HITUNG DIAGNOSA SIRIRAJ", use_container_width=True)

    if submit_sss:
        sss = (2.5 * int(kes[0])) + (2 * mun) + (2 * nye) + (0.1 * dia) - (3 * int(ath)) - 12
        diag = "STROKE HEMORAGIK" if sss > 1 else "STROKE INFARK" if sss < -1 else "BORDERLINE (PERLU CT-SCAN)"
        st.markdown(f"""
            <div class="print-area">
                <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px;">
                    <h2 style="margin: 0;">LAPORAN SIRIRAJ STROKE SCORE</h2>
                    <h4 style="margin: 0; color: #004a99;">SINTALA-STROKE by. dr. Faisal Bayu</h4>
                </div>
                <br>
                <div class="score-box">
                    <h2 style="margin: 0; color: #dc2626;">DIAGNOSA KLINIS:</h2>
                    <h1 style="margin: 10px;">{diag}</h1>
                    <p>Skor Siriraj: {sss:.2f}</p>
                </div>
                <div style="margin-top: 50px; text-align: right;">( {st.session_state.nama_dokter} )</div>
            </div>
        """, unsafe_allow_html=True)

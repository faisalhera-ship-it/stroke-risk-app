import streamlit as st
from datetime import datetime

# --- 1. SESSION STATE ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""
if 'pilihan_layanan' not in st.session_state:
    st.session_state.pilihan_layanan = None

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- CUSTOM CSS (PREMIUM MODERN UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f0f2f6; }
    .main-card {
        background: white; padding: 40px; border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04); border: 1px solid #eef0f2;
    }
    .module-card {
        background: white; padding: 30px; border-radius: 20px;
        border-top: 6px solid #004a99; transition: 0.4s ease;
        text-align: center; cursor: pointer; height: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    .module-card:hover { transform: translateY(-10px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); }
    .report-box { 
        background: white; padding: 30px; border-radius: 12px; 
        border: 2px solid #004a99; margin-top: 20px; color: black;
    }
    @media print {
        .no-print, header, footer, [data-testid="stHeader"], section[data-testid="stSidebar"], .stButton { display: none !important; }
        .print-container { 
            display: block !important; border: 2px solid #000 !important; 
            padding: 30px !important; margin: 0 !important; color: black !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIN ---
if not st.session_state.nama_dokter:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1.5, 1])
    with col_m:
        st.markdown("<div class='main-card'><h1 style='text-align: center; color: #004a99;'>🩺 SINTALA-STROKE</h1><p style='text-align: center; color: #6c757d;'>Verifikasi DPJP Tanah Laut</p></div>", unsafe_allow_html=True)
        input_dr = st.text_input("Nama Lengkap Dokter:", placeholder="Contoh: dr. Faisal Bayu")
        if st.button("Masuk Ke Dashboard", use_container_width=True):
            if input_dr:
                st.session_state.nama_dokter = input_dr
                st.rerun()
    st.stop()

# --- 3. DASHBOARD ---
if st.session_state.pilihan_layanan is None:
    st.markdown(f"## Dashboard Medis: {st.session_state.nama_dokter}")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="module-card"><h3>📊 FSRP</h3><p>Profil Risiko Stroke 10 Tahun<br>(+ Faktor Kolesterol)</p></div>', unsafe_allow_html=True)
        if st.button("Buka FSRP", use_container_width=True):
            st.session_state.pilihan_layanan = "FSRP"; st.rerun()
    with c2:
        st.markdown('<div class="module-card" style="border-top-color: #dc3545;"><h3>🚨 NIHSS</h3><p>Evaluasi Defisit Neurologis<br>11 Poin Sesuai Panduan</p></div>', unsafe_allow_html=True)
        if st.button("Buka NIHSS", use_container_width=True):
            st.session_state.pilihan_layanan = "NIHSS"; st.rerun()
    with c3:
        st.markdown('<div class="module-card" style="border-top-color: #ff8c00;"><h3>🧠 SIRIRAJ</h3><p>Siriraj Stroke Score<br>Pembeda Jenis Stroke</p></div>', unsafe_allow_html=True)
        if st.button("Buka Siriraj", use_container_width=True):
            st.session_state.pilihan_layanan = "SIRIRAJ"; st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("SINTALA")
    st.write(f"DPJP: **{st.session_state.nama_dokter}**")
    if st.button("🔄 Menu Utama"):
        st.session_state.pilihan_layanan = None
        st.rerun()
    st.divider()
    st.markdown('<button onclick="window.print()" style="width: 100%; height: 3.5em; background: #28a745; color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer;">🖨️ Cetak Laporan</button>', unsafe_allow_html=True)

# --- 5. MODUL FSRP (DENGAN KOLESTEROL) ---
if st.session_state.pilihan_layanan == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile")
    with st.form("fsrp_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama_p = st.text_input("Nama Pasien", "Pasien Anonim")
            tds = st.number_input("TD Sistolik (mmHg)", 90, 250, 120)
            kolesterol = st.number_input("Kolesterol Total (mg/dL)", 100, 500, 200)
        with col2:
            st.write("**Faktor Risiko & Komorbid**")
            u55 = st.checkbox("Usia ≥ 55 Tahun")
            dm = st.checkbox("Diabetes Melitus")
            smk = st.checkbox("Merokok Aktif")
            jantung = st.multiselect("Riwayat Jantung", ["PJK", "AF", "LVH (EKG)"])
        
        submit = st.form_submit_button("ANALISA RISIKO STROKE", use_container_width=True)

    if submit:
        # Kalkulasi Poin (Penyesuaian Skor FSRP dengan Kolesterol)
        # Poin tambahan: Kolesterol >= 200 mg/dL memberikan +2 poin risiko
        poin_kol = 2 if kolesterol >= 200 else 0
        poin = sum([u55*2, (tds>=140)*3, smk*3, dm*2, ("PJK" in jantung)*2, ("AF" in jantung)*4, ("LVH (EKG)" in jantung)*5, poin_kol])
        
        kategori = "TINGGI" if poin >= 7 else "RENDAH" # Ambang batas naik sedikit karena ada faktor kolesterol
        
        st.markdown(f"""
            <div class="report-box print-container">
                <h2 style="text-align: center; color: #004a99;">LAPORAN ANALISA FSRP</h2>
                <hr>
                <p><b>DPJP:</b> {st.session_state.nama_dokter} | <b>Pasien:</b> {nama_p}</p>
                <p><b>TD Sistolik:</b> {tds} mmHg | <b>Kolesterol Total:</b> {kolesterol} mg/dL</p>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h3 style="margin:0; color: {'#d90429' if kategori == 'TINGGI' else '#2d6a4f'}; text-align: center;">
                        SKOR TOTAL: {poin} Poin (RISIKO {kategori})
                    </h3>
                </div>
                <p style="font-size: 0.9em; color: #666;">*Kriteria Berdasarkan Framingham Stroke Risk Profile yang telah dimodifikasi.</p>
                <br><br>
                <p style="text-align: right;">Tanah Laut, {datetime.now().strftime("%d/%m/%Y")}<br><br><br><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- NIHSS LENGKAP ---
elif st.session_state.pilihan_layanan == "NIHSS":
    st.header("🚨 National Institutes of Health Stroke Scale")
    with st.form("nihss_form"):
        c1, c2 = st.columns(2)
        with c1:
            n1a = st.selectbox("1a. Derajad kesadaran", ["0: Sadar", "1: Mengantuk", "2: Stupor", "3: Koma"])
            n1b = st.selectbox("1b. Derajad kesadaran (Tanya)", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n1c = st.selectbox("1c. Derajad kesadaran (Perintah)", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n2 = st.selectbox("2. GAZE (Mata konjugat)", ["0: Normal", "1: Abnormal 1 mata", "2: Abnormal 2 mata"])
            n3 = st.selectbox("3. Lapang pandang", ["0: Normal", "1: Parsial", "2: Komplit", "3: Bilateral"])
            n4 = st.selectbox("4. Kelumpuhan wajah", ["0: Normal", "1: Minor", "2: Parsial", "3: Komplit"])
            n7 = st.selectbox("7. Ataksia ekstremitas", ["0: Tidak ada", "1: Satu ekstremitas", "2: Dua ekstremitas"])
            n8 = st.selectbox("8. Sensorik", ["0: Normal", "1: Parsial", "2: Berat"])
        with c2:
            n5a = st.selectbox("5a. Motorik Lengan Kanan", ["0: Normal", "1: Jatuh < 10 dtk", "2: Tak lawan gravitasi", "3: Tak ada gerakan"])
            n5b = st.selectbox("5b. Motorik Lengan Kiri", ["0: Normal", "1: Jatuh < 10 dtk", "2: Tak lawan gravitasi", "3: Tak ada gerakan"])
            n6a = st.selectbox("6a. Motorik Tungkai Kanan", ["0: Normal", "1: Jatuh < 5 dtk", "2: Tak lawan gravitasi", "3: Tak ada gerakan"])
            n6b = st.selectbox("6b. Motorik Tungkai Kiri", ["0: Normal", "1: Jatuh < 5 dtk", "2: Tak lawan gravitasi", "3: Tak ada gerakan"])
            n9 = st.selectbox("9. Afasia", ["0: Normal", "1: Ringan", "2: Berat", "3: Bisu"])
            n10 = st.selectbox("10. Disartria", ["0: Normal", "1: Ringan/Pelo", "2: Berat"])
            n11 = st.selectbox("11. Neglect / Inattention", ["0: Normal", "1: Ringan", "2: Hebat"])
        submit_n = st.form_submit_button("HITUNG NIHSS")
    
    if submit_n:
        total = sum([int(x[0]) for x in [n1a, n1b, n1c, n2, n3, n4, n5a, n5b, n6a, n6b, n7, n8, n9, n10, n11]])
        st.markdown(f"<div class='report-box print-container'><h3>SKOR NIHSS: {total}</h3><p>Pemeriksa: {st.session_state.nama_dokter}</p></div>", unsafe_allow_html=True)

# --- SIRIRAJ SCORE ---
elif st.session_state.pilihan_layanan == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score")
    with st.form("sss_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            s_kes = st.selectbox("Kesadaran", ["0: Sadar", "1: Somnolen", "2: Koma"])
            s_mun = st.radio("Muntah Proyektil", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            s_nye = st.radio("Nyeri Kepala (2 jam)", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        with col_b:
            s_dia = st.number_input("TD Diastolik", 50, 150, 90)
            s_ath = st.checkbox("Tanda Atheroma (DM/PJK)")
        submit_s = st.form_submit_button("HITUNG SIRIRAJ")

    if submit_s:
        sss = (2.5 * int(s_kes[0])) + (2 * s_mun) + (2 * s_nye) + (0.1 * s_dia) - (3 * int(s_ath)) - 12
        diag = "HEMORAGIK" if sss > 1 else "INFARK" if sss < -1 else "BORDERLINE"
        st.markdown(f"<div class='report-box print-container'><h3>SIRIRAJ SCORE: {sss:.2f}</h3><h2>DIAGNOSA: {diag}</h2></div>", unsafe_allow_html=True)

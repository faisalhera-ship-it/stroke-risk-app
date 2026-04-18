import streamlit as st
from datetime import datetime

# --- 1. SESSION STATE ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""
if 'pilihan_layanan' not in st.session_state:
    st.session_state.pilihan_layanan = None

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- CUSTOM CSS (PREMIUM DASHBOARD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    /* Login & Header Card */
    .hero-card {
        background: white; padding: 40px; border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;
        text-align: center; margin-bottom: 20px;
    }
    .author-badge {
        color: #004a99; font-weight: 700; font-size: 1.2rem;
        margin-top: -10px; margin-bottom: 20px;
    }
    
    /* Module Navigation */
    .module-box {
        background: white; padding: 30px; border-radius: 20px;
        border-top: 6px solid #004a99; transition: 0.3s;
        text-align: center; height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .module-box:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.08); }
    
    /* Report Styling */
    .report-frame {
        background: white; padding: 40px; border-radius: 15px;
        border: 2px solid #004a99; color: black; margin-top: 25px;
    }

    /* Print Optimization */
    @media print {
        .no-print, [data-testid="stSidebar"], .stButton, header, footer { display: none !important; }
        .report-frame { border: none !important; padding: 0 !important; }
        .stMarkdown { display: block !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if not st.session_state.nama_dokter:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_m, _ = st.columns([1, 1.5, 1])
    with col_m:
        st.markdown("""
            <div class='hero-card'>
                <h1 style='color: #004a99; margin: 0;'>🩺 SINTALA-STROKE</h1>
                <p class='author-badge'>by. dr. Faisal Bayu</p>
                <p style='color: #64748b;'>Sistem Informasi & Analisa Stroke Terpadu<br>Tanah Laut, Kalimantan Selatan</p>
            </div>
        """, unsafe_allow_html=True)
        dr_name = st.text_input("Nama Lengkap DPJP:", placeholder="Contoh: dr. Faisal Bayu, Sp.N")
        if st.button("Masuk Ke Dashboard", use_container_width=True):
            if dr_name:
                st.session_state.nama_dokter = dr_name
                st.rerun()
    st.stop()

# --- 3. DASHBOARD SELECTOR ---
if st.session_state.pilihan_layanan is None:
    st.markdown(f"### Selamat Bertugas, {st.session_state.nama_dokter}")
    st.write("Silakan pilih instrumen pemeriksaan:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="module-box"><h3>📊 FSRP</h3><p>Framingham Stroke Risk Profile<br>(Skrining Risiko 10 Tahun)</p></div>', unsafe_allow_html=True)
        if st.button("Buka Modul FSRP", use_container_width=True):
            st.session_state.pilihan_layanan = "FSRP"; st.rerun()
    with c2:
        st.markdown('<div class="module-box" style="border-top-color: #dc2626;"><h3>🚨 NIHSS</h3><p>National Institutes of Health<br>Stroke Scale (11 Poin Lengkap)</p></div>', unsafe_allow_html=True)
        if st.button("Buka Modul NIHSS", use_container_width=True):
            st.session_state.pilihan_layanan = "NIHSS"; st.rerun()
    with c3:
        st.markdown('<div class="module-box" style="border-top-color: #ea580c;"><h3>🧠 SIRIRAJ</h3><p>Siriraj Stroke Score<br>(Pembeda Infark vs Hemoragik)</p></div>', unsafe_allow_html=True)
        if st.button("Buka Modul SIRIRAJ", use_container_width=True):
            st.session_state.pilihan_layanan = "SIRIRAJ"; st.rerun()
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#004a99;'>SINTALA-STROKE</h2>", unsafe_allow_html=True)
    st.write(f"DPJP: **{st.session_state.nama_dokter}**")
    if st.button("🔄 Kembali ke Menu Utama", use_container_width=True):
        st.session_state.pilihan_layanan = None
        st.rerun()
    st.divider()
    st.write("**Output Laporan:**")
    st.markdown('<button onclick="window.print()" style="width:100%; height:3.5em; background:#16a34a; color:white; border:none; border-radius:12px; font-weight:bold; cursor:pointer;">🖨️ CETAK / SAVE PDF</button>', unsafe_allow_html=True)
    st.caption("Developed by dr. Faisal Bayu")

# --- 5. MODULE LOGIC ---

# --- MODUL FSRP ---
if st.session_state.pilihan_layanan == "FSRP":
    st.header("📊 Modul FSRP (Faktor Risiko 10 Tahun)")
    with st.form("fsrp_form"):
        p_nama = st.text_input("Nama Pasien", "Pasien Anonim")
        col1, col2 = st.columns(2)
        with col1:
            usia = st.checkbox("Usia ≥ 55 Tahun")
            tds = st.number_input("TD Sistolik (mmHg)", 90, 250, 120)
            kolesterol = st.number_input("Kolesterol Total (mg/dL)", 100, 500, 190)
        with col2:
            dm = st.checkbox("Diabetes Melitus")
            smk = st.checkbox("Merokok Aktif")
            jantung = st.multiselect("Riwayat Jantung", ["PJK", "AF", "LVH (EKG)"])
        
        submit_fsrp = st.form_submit_button("ANALISA FSRP", use_container_width=True)
    
    if submit_fsrp:
        p_kol = 2 if kolesterol >= 200 else 0
        skor = sum([usia*2, (tds>=140)*3, smk*3, dm*2, ("PJK" in jantung)*2, ("AF" in jantung)*4, ("LVH (EKG)" in jantung)*5, p_kol])
        kat = "TINGGI" if skor >= 7 else "RENDAH"
        
        st.markdown(f"""
            <div class="report-frame">
                <h2 style="text-align: center;">LAPORAN ANALISA PROFIL RISIKO STROKE</h2>
                <p style="text-align: center; color: #004a99; font-weight: bold;">SINTALA-STROKE by. dr. Faisal Bayu</p>
                <hr>
                <p><b>Nama Pasien:</b> {p_nama}</p>
                <p><b>Dokter Pemeriksa:</b> {st.session_state.nama_dokter}</p>
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0;">
                    <h3 style="margin: 0;">TOTAL SKOR: {skor}</h3>
                    <h2 style="margin: 5px; color: {'#dc2626' if kat == 'TINGGI' else '#16a34a'};">RISIKO: {kat}</h2>
                </div>
                <p style="text-align: right; margin-top: 40px;">Tanah Laut, {datetime.now().strftime('%d %B %Y')}<br><br><br><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- MODUL NIHSS (11 POIN LENGKAP) ---
elif st.session_state.pilihan_layanan == "NIHSS":
    st.header("🚨 Modul NIHSS (Stroke Scale)")
    with st.form("nihss_form"):
        p_nama = st.text_input("Nama Pasien", "Pasien Anonim")
        c1, c2 = st.columns(2)
        with c1:
            n1a = st.selectbox("1a. Kesadaran (LOC)", ["0: Sadar", "1: Somnolen", "2: Stupor", "3: Koma"])
            n1b = st.selectbox("1b. LOC Tanya", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n1c = st.selectbox("1c. LOC Perintah", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n2 = st.selectbox("2. Gaze (Mata)", ["0: Normal", "1: Paresis", "2: Deviasi"])
            n3 = st.selectbox("3. Visual", ["0: Normal", "1: Parsial", "2: Komplit", "3: Bilateral"])
            n4 = st.selectbox("4. Facial Palsy", ["0: Normal", "1: Minor", "2: Parsial", "3: Komplit"])
        with c2:
            n5 = st.selectbox("5. Motor Lengan", ["0: Normal", "1: Drift", "2: Lawan Gravitasi", "3: Flasid"])
            n6 = st.selectbox("6. Motor Tungkai", ["0: Normal", "1: Drift", "2: Lawan Gravitasi", "3: Flasid"])
            n7 = st.selectbox("7. Ataksia", ["0: Tak ada", "1: 1 Ekstremitas", "2: 2 Ekstremitas"])
            n8 = st.selectbox("8. Sensorik", ["0: Normal", "1: Ringan", "2: Berat"])
            n9 = st.selectbox("9. Bahasa/Afasia", ["0: Normal", "1: Ringan", "2: Berat", "3: Global"])
            n10 = st.selectbox("10. Disartria", ["0: Normal", "1: Ringan", "2: Berat"])
            n11 = st.selectbox("11. Neglect", ["0: Normal", "1: Ringan", "2: Berat"])
        
        submit_nihss = st.form_submit_button("HITUNG NIHSS", use_container_width=True)

    if submit_nihss:
        total = sum([int(x[0]) for x in [n1a, n1b, n1c, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11]])
        st.markdown(f'<div class="report-frame"><h2 style="text-align: center;">SKOR NIHSS: {total}</h2><p style="text-align:center;">Pemeriksa: {st.session_state.nama_dokter}</p></div>', unsafe_allow_html=True)

# --- MODUL SIRIRAJ ---
elif st.session_state.pilihan_layanan == "SIRIRAJ":
    st.header("🧠 Modul Siriraj Stroke Score")
    with st.form("sss_form"):
        p_nama = st.text_input("Nama Pasien", "Pasien Anonim")
        c1, c2 = st.columns(2)
        with c1:
            kes = st.selectbox("Kesadaran", ["0: Sadar", "1: Somnolen", "2: Koma"])
            mun = st.radio("Muntah Proyektil", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            nye = st.radio("Nyeri Kepala (2 jam)", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        with c2:
            dia = st.number_input("TD Diastolik", 50, 150, 90)
            ath = st.checkbox("Atheroma (DM/PJK)")
        submit_sss = st.form_submit_button("HITUNG SIRIRAJ", use_container_width=True)

    if submit_sss:
        sss = (2.5 * int(kes[0])) + (2 * mun) + (2 * nye) + (0.1 * dia) - (3 * int(ath)) - 12
        diag = "STROKE HEMORAGIK" if sss > 1 else "STROKE INFARK" if sss < -1 else "BORDERLINE / PERLU CT-SCAN"
        st.markdown(f'<div class="report-frame"><h2 style="text-align:center;">SKOR SSS: {sss:.2f}</h2><h3 style="text-align:center;">HASIL: {diag}</h3></div>', unsafe_allow_html=True)
# --- 5. MODULE LOGIC ---

# --- MODUL FSRP ---
if st.session_state.pilihan_layanan == "FSRP":
    st.header("📊 Modul FSRP (Faktor Risiko 10 Tahun)")
    with st.form("fsrp_form"):
        p_nama = st.text_input("Nama Pasien", "Pasien Anonim")
        col1, col2 = st.columns(2)
        with col1:
            usia = st.checkbox("Usia ≥ 55 Tahun")
            tds = st.number_input("TD Sistolik (mmHg)", 90, 250, 120)
            kolesterol = st.number_input("Kolesterol Total (mg/dL)", 100, 500, 190)
        with col2:
            dm = st.checkbox("Diabetes Melitus")
            smk = st.checkbox("Merokok Aktif")
            jantung = st.multiselect("Riwayat Jantung", ["PJK", "AF", "LVH (EKG)"])
        
        submit_fsrp = st.form_submit_button("ANALISA FSRP", use_container_width=True)
    
    if submit_fsrp:
        p_kol = 2 if kolesterol >= 200 else 0
        skor = sum([usia*2, (tds>=140)*3, smk*3, dm*2, ("PJK" in jantung)*2, ("AF" in jantung)*4, ("LVH (EKG)" in jantung)*5, p_kol])
        kat = "TINGGI" if skor >= 7 else "RENDAH"
        
        st.markdown(f"""
            <div class="report-frame">
                <h2 style="text-align: center;">LAPORAN ANALISA PROFIL RISIKO STROKE</h2>
                <p style="text-align: center; color: #004a99; font-weight: bold;">SINTALA-STROKE by. dr. Faisal Bayu</p>
                <hr>
                <p><b>Nama Pasien:</b> {p_nama}</p>
                <p><b>Dokter Pemeriksa:</b> {st.session_state.nama_dokter}</p>
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0;">
                    <h3 style="margin: 0;">TOTAL SKOR: {skor}</h3>
                    <h2 style="margin: 5px; color: {'#dc2626' if kat == 'TINGGI' else '#16a34a'};">RISIKO: {kat}</h2>
                </div>
                <p style="text-align: right; margin-top: 40px;">Tanah Laut, {datetime.now().strftime('%d %B %Y')}<br><br><br><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- MODUL NIHSS (11 POIN LENGKAP) ---
elif st.session_state.pilihan_layanan == "NIHSS":
    st.header("🚨 Modul NIHSS (Stroke Scale)")
    with st.form("nihss_form"):
        p_nama = st.text_input("Nama Pasien", "Pasien Anonim")
        c1, c2 = st.columns(2)
        with c1:
            n1a = st.selectbox("1a. Kesadaran (LOC)", ["0: Sadar", "1: Somnolen", "2: Stupor", "3: Koma"])
            n1b = st.selectbox("1b. LOC Tanya", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n1c = st.selectbox("1c. LOC Perintah", ["0: Tepat 2", "1: Tepat 1", "2: Salah"])
            n2 = st.selectbox("2. Gaze (Mata)", ["0: Normal", "1: Paresis", "2: Deviasi"])
            n3 = st.selectbox("3. Visual", ["0: Normal", "1: Parsial", "2: Komplit", "3: Bilateral"])
            n4 = st.selectbox("4. Facial Palsy", ["0: Normal", "1: Minor", "2: Parsial", "3: Komplit"])
        with c2:
            n5 = st.selectbox("5. Motor Lengan", ["0: Normal", "1: Drift", "2: Lawan Gravitasi", "3: Flasid"])
            n6 = st.selectbox("6. Motor Tungkai", ["0: Normal", "1: Drift", "2: Lawan Gravitasi", "3: Flasid"])
            n7 = st.selectbox("7. Ataksia", ["0: Tak ada", "1: 1 Ekstremitas", "2: 2 Ekstremitas"])
            n8 = st.selectbox("8. Sensorik", ["0: Normal", "1: Ringan", "2: Berat"])
            n9 = st.selectbox("9. Bahasa/Afasia", ["0: Normal", "1: Ringan", "2: Berat", "3: Global"])
            n10 = st.selectbox("10. Disartria", ["0: Normal", "1: Ringan", "2: Berat"])
            n11 = st.selectbox("11. Neglect", ["0: Normal", "1: Ringan", "2: Berat"])
        
        submit_nihss = st.form_submit_button("HITUNG NIHSS", use_container_width=True)

    if submit_nihss:
        total = sum([int(x[0]) for x in [n1a, n1b, n1c, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11]])
        st.markdown(f'<div class="report-frame"><h2 style="text-align: center;">SKOR NIHSS: {total}</h2><p style="text-align:center;">Pemeriksa: {st.session_state.nama_dokter}</p></div>', unsafe_allow_html=True)

# --- MODUL SIRIRAJ ---
elif st.session_state.pilihan_layanan == "SIRIRAJ":
    st.header("🧠 Modul Siriraj Stroke Score")
    with st.form("sss_form"):
        p_nama = st.text_input("Nama Pasien", "Pasien Anonim")
        c1, c2 = st.columns(2)
        with c1:
            kes = st.selectbox("Kesadaran", ["0: Sadar", "1: Somnolen", "2: Koma"])
            mun = st.radio("Muntah Proyektil", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            nye = st.radio("Nyeri Kepala (2 jam)", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        with c2:
            dia = st.number_input("TD Diastolik", 50, 150, 90)
            ath = st.checkbox("Atheroma (DM/PJK)")
        submit_sss = st.form_submit_button("HITUNG SIRIRAJ", use_container_width=True)

    if submit_sss:
        sss = (2.5 * int(kes[0])) + (2 * mun) + (2 * nye) + (0.1 * dia) - (3 * int(ath)) - 12
        diag = "STROKE HEMORAGIK" if sss > 1 else "STROKE INFARK" if sss < -1 else "BORDERLINE / PERLU CT-SCAN"
        st.markdown(f'<div class="report-frame"><h2 style="text-align:center;">SKOR SSS: {sss:.2f}</h2><h3 style="text-align:center;">HASIL: {diag}</h3></div>', unsafe_allow_html=True)

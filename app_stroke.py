import streamlit as st
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- CSS KHUSUS UNTUK TAMPILAN & AUTO-PRINT ---
st.markdown("""
    <style>
    @media print {
        /* Sembunyikan elemen navigasi saat cetak */
        .stButton, .stSidebar, header, footer, .stSelectbox, .stRadio, .stCheckbox, .stNumberInput, .stTextInput, .stExpander, [data-testid="stHeader"] {
            display: none !important;
        }
        .main { background-color: white !important; }
        .print-container { 
            border: 2px solid black !important; 
            padding: 30px !important; 
            margin: 0 !important;
            display: block !important;
        }
    }
    .report-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #d1d1d1; background-color: white; }
    .high-risk { border-left: 10px solid #dc3545; }
    .low-risk { border-left: 10px solid #28a745; }
    .critical-box { background-color: #fff3f3; border: 1px solid #dc3545; padding: 15px; border-radius: 5px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🩺 SINTALA-STROKE")
    st.write("**Oleh: dr. Faisal Bayu**")
    st.divider()
    layanan = st.radio("Pilih Layanan:", ["Skrining Risiko (FSRP)", "Evaluasi Akut (NIHSS)"])
    st.divider()
    
    # PERBAIKAN TOMBOL CETAK: Menggunakan HTML Button yang memicu fungsi print browser
    st.markdown('<button onclick="window.print()" style="width: 100%; height: 3em; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">🖨️ Cetak Laporan (Print)</button>', unsafe_allow_html=True)

# --- LAYANAN 1: FSRP ---
if layanan == "Skrining Risiko (FSRP)":
    st.header("Kalkulator Risiko Stroke (FSRP)")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            nama_pasien = st.text_input("Nama Pasien", "Pasien Anonim")
            usia = st.number_input("Usia (Tahun)", 20, 100, 50)
            jk = st.selectbox("Jenis Kelamin", ["Pria", "Wanita"])
            tds = st.number_input("Tekanan Darah Sistolik (mmHg)", 90, 250, 130)
        with col2:
            kolesterol = st.number_input("Total Kolesterol (mg/dL)", 50, 1000, 200)
            gds = st.number_input("Gula Darah Sewaktu (mg/dL)", 30, 1000, 100)
            merokok = st.checkbox("Merokok Aktif")
            dm = st.checkbox("Riwayat Diabetes Melitus")

    if st.button("Proses Analisa FSRP"):
        poin = 0
        if usia >= 55: poin += 2
        if tds >= 140: poin += 3
        if kolesterol > 240: poin += 1
        if gds > 200 or dm: poin += 2
        if merokok: poin += 3
        
        kategori = "TINGGI" if poin >= 6 else "RENDAH"
        warna_class = "high-risk" if kategori == "TINGGI" else "low-risk"
        
        st.markdown(f"""
            <div class="report-box {warna_class} print-container">
                <h2 style="text-align: center; margin-bottom: 0;">LAPORAN SKRINING RISIKO STROKE</h2>
                <p style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;">SINTALA-STROKE | dr. Faisal Bayu</p>
                <table style="width: 100%; line-height: 1.6;">
                    <tr><td><b>Nama Pasien</b></td><td>: {nama_pasien}</td><td><b>Kolesterol</b></td><td>: {kolesterol} mg/dL</td></tr>
                    <tr><td><b>Usia / JK</b></td><td>: {usia} Thn / {jk}</td><td><b>Gula Darah</b></td><td>: {gds} mg/dL</td></tr>
                    <tr><td><b>Tekanan Darah</b></td><td>: {tds} mmHg</td><td><b>Status DM</b></td><td>: {"Ya" if dm else "Tidak"}</td></tr>
                </table>
                <hr>
                <h3 style="color: {'red' if kategori == 'TINGGI' else 'green'};">KATEGORI RISIKO: {kategori} ({poin} Poin)</h3>
                <p><b>Rekomendasi Klinis:</b><br>
                - Target TD < 130/80 mmHg.<br>
                - Kelola profil lipid dan kendali glikemik.<br>
                - Diet DASH dan aktivitas fisik rutin 150 menit/minggu.</p>
                <br>
                <p style="text-align: right;">Dicetak pada: {datetime.now().strftime("%d/%m/%Y %H:%M")}<br><br><br><br><b>( dr. Faisal Bayu )</b></p>
            </div>
        """, unsafe_allow_html=True)
        st.success("Analisa selesai. Silakan klik tombol 'Cetak Laporan' di sidebar.")

# --- LAYANAN 2: NIHSS + KONTRAINDIKASI ---
else:
    st.header("Evaluasi Akut & Protokol Trombolisis")
    
    tab1, tab2 = st.tabs(["Skala NIHSS", "Checklist Kontraindikasi"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            loc = st.selectbox("1a. Tingkat Kesadaran", ["0: Sadar penuh", "1: Somnolen", "2: Stupor", "3: Koma"])
            gaze = st.selectbox("2. Gerakan Mata (Gaze)", ["0: Normal", "1: Paresis gaze parsial", "2: Deviasi paksa"])
            motor_ki = st.selectbox("5. Motorik Lengan Kiri", ["0: Tanpa jatuh", "1: Jatuh < 10 dtk", "2: Lawan gravitasi", "3: Flasid"])
        with col_b:
            motor_ka = st.selectbox("5. Motorik Lengan Kanan", ["0: Tanpa jatuh", "1: Jatuh < 10 dtk", "2: Lawan gravitasi", "3: Flasid"])
            bahasa = st.selectbox("9. Bahasa (Afasia)", ["0: Normal", "1: Afasia ringan", "2: Afasia berat", "3: Global"])
            bicara = st.selectbox("10. Artikulasi (Disartria)", ["0: Normal", "1: Ringan/Pelo", "2: Berat"])
        
        total_nihss = int(loc[0]) + int(gaze[0]) + int(motor_ki[0]) + int(motor_ka[0]) + int(bahasa[0]) + int(bicara[0])
        st.metric("Total Skor NIHSS", total_nihss)

    with tab2:
        st.subheader("⚠️ Skrining Kontraindikasi rTPA")
        abs1 = st.checkbox("Riwayat perdarahan intrakranial (ICH)")
        abs2 = st.checkbox("Trauma kepala berat / Stroke dalam 3 bulan terakhir")
        abs3 = st.checkbox("Tekanan Darah >185/110 mmHg (Refrakter)")
        abs4 = st.checkbox("Perdarahan internal aktif")

    if st.button("Selesaikan Laporan IGD"):
        status_trombolisis = "TIDAK LAYAK" if (abs1 or abs2 or abs3 or abs4) else "PERTIMBANGKAN"
        
        st.markdown(f"""
            <div class="report-box print-container">
                <h2 style="text-align: center;">RESUME EVALUASI STROKE AKUT</h2>
                <p style="text-align: center; border-bottom: 2px solid black;">SINTALA-STROKE | Unit Gawat Darurat</p>
                <table style="width: 100%; line-height: 1.8;">
                    <tr><td><b>SKOR NIHSS</b></td><td>: {total_nihss}</td></tr>
                    <tr><td><b>STATUS TROMBOLISIS</b></td><td>: <span style="color: {'red' if status_trombolisis == 'TIDAK LAYAK' else 'orange'}; font-weight: bold;">{status_trombolisis}</span></td></tr>
                </table>
                <div class="critical-box">
                    <b>Catatan Klinis:</b><br>
                    {"- Terdeteksi Kontraindikasi Absolut! Jangan lakukan trombolisis." if status_trombolisis == "TIDAK LAYAK" else "- Tidak ada kontraindikasi absolut. Segera aktivasi tim Stroke / Spesialis Saraf."}
                </div>
                <br>
                <p style="text-align: right;">Pemeriksa,<br><br><br><br><b>( dr. Faisal Bayu )</b></p>
            </div>
        """, unsafe_allow_html=True)
        st.success("Laporan IGD siap cetak.")

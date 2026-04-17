import streamlit as st
from datetime import datetime

# --- 1. SESSION STATE UNTUK LOGIN ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- CSS PRINT & UI ---
st.markdown("""
    <style>
    @media print {
        .stButton, .stSidebar, header, footer, [data-testid="stHeader"], .no-print, .stTabs {
            display: none !important;
        }
        .main { background-color: white !important; }
        .print-container { 
            border: 2px solid black !important; 
            padding: 30px !important; 
            display: block !important;
            color: black !important;
        }
    }
    .report-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #d1d1d1; background-color: white; }
    .high-risk { border-left: 10px solid #dc3545; }
    .low-risk { border-left: 10px solid #28a745; }
    .critical-box { background-color: #fff3f3; border: 1px solid #dc3545; padding: 15px; border-radius: 5px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. POP-UP LOGIN ---
if not st.session_state.nama_dokter:
    st.markdown("## 🩺 Selamat Datang di SINTALA-STROKE")
    with st.container():
        st.write("Silakan masukkan identitas Dokter untuk memulai layanan:")
        input_dr = st.text_input("Nama Lengkap Dokter (beserta gelar):")
        if st.button("Masuk Aplikasi"):
            if input_dr:
                st.session_state.nama_dokter = input_dr
                st.rerun()
            else:
                st.warning("Nama Dokter wajib diisi.")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🩺 SINTALA-STROKE")
    st.write(f"Login sebagai: \n**{st.session_state.nama_dokter}**")
    if st.button("Log Out / Ganti Dokter"):
        st.session_state.nama_dokter = ""
        st.rerun()
    st.divider()
    layanan = st.radio("Pilih Layanan:", ["Skrining Risiko (FSRP)", "Evaluasi Akut (NIHSS)"])
    st.divider()
    st.markdown('<button onclick="window.print()" style="width: 100%; height: 3em; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">🖨️ Cetak Laporan (Print)</button>', unsafe_allow_html=True)

# --- 4. LAYANAN 1: FSRP (VERSI CHECKLIST) ---
if layanan == "Skrining Risiko (FSRP)":
    st.header("Kalkulator Risiko Stroke (FSRP)")
    
    col1, col2 = st.columns(2)
    with col1:
        nama_pasien = st.text_input("Nama Pasien", "Pasien Anonim")
        jk = st.selectbox("Jenis Kelamin", ["Pria", "Wanita"])
        tds = st.number_input("Tekanan Darah Sistolik (mmHg)", 90, 250, 120)
    
    with col2:
        st.write("**Checklist Faktor Risiko:**")
        u55 = st.checkbox("Usia ≥ 55 Tahun")
        smk = st.checkbox("Merokok Aktif")
        dm = st.checkbox("Riwayat Diabetes (DM)")
        st.write("**Checklist Penyakit Jantung:**")
        pjk = st.checkbox("Penyakit Jantung Koroner (PJK)")
        af = st.checkbox("Fibrilasi Atrium (AF)")
        lvh = st.checkbox("LV Hipertrofi (EKG)")

    if st.button("Proses Analisa FSRP"):
        # Logika Poin
        poin = sum([u55*2, (tds>=140)*3, smk*3, dm*2, pjk*2, af*4, lvh*5])
        kategori = "TINGGI" if poin >= 6 else "RENDAH"
        warna_class = "high-risk" if kategori == "TINGGI" else "low-risk"
        
        st.markdown(f"""
            <div class="report-box {warna_class} print-container">
                <h2 style="text-align: center; margin-bottom: 0;">LAPORAN SKRINING RISIKO STROKE</h2>
                <p style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;">RSUD/PUSKESMAS TANAH LAUT</p>
                <table style="width: 100%; line-height: 1.6;">
                    <tr><td><b>Nama Pasien</b></td><td>: {nama_pasien}</td><td><b>DPJP</b></td><td>: {st.session_state.nama_dokter}</td></tr>
                    <tr><td><b>Usia</b></td><td>: {">= 55 Thn" if u55 else "< 55 Thn"}</td><td><b>TD Sistolik</b></td><td>: {tds} mmHg</td></tr>
                </table>
                <hr>
                <h3 style="color: {'red' if kategori == 'TINGGI' else 'green'};">KATEGORI RISIKO: {kategori} ({poin} Poin)</h3>
                <p><b>Faktor Terdeteksi:</b> {"Merokok, " if smk else ""}{"DM, " if dm else ""}{"PJK, " if pjk else ""}{"AF, " if af else ""}{"LVH" if lvh else "-"}</p>
                <br>
                <p style="text-align: right;">Tanah Laut, {datetime.now().strftime("%d/%m/%Y")}<br>Dokter Pemeriksa,<br><br><br><br><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 5. LAYANAN 2: NIHSS & KONTRAINDIKASI ---
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
        status = "TIDAK LAYAK" if (abs1 or abs2 or abs3 or abs4) else "LAYAK (PERTIMBANGKAN)"
        
        st.markdown(f"""
            <div class="report-box print-container">
                <h2 style="text-align: center;">RESUME EVALUASI STROKE AKUT</h2>
                <hr>
                <table style="width: 100%; line-height: 1.8;">
                    <tr><td><b>SKOR NIHSS</b></td><td>: {total_nihss}</td></tr>
                    <tr><td><b>STATUS TROMBOLISIS</b></td><td>: <b>{status}</b></td></tr>
                </table>
                <div class="critical-box">
                    <b>Catatan DPJP:</b><br>
                    {st.session_state.nama_dokter} - Segera aktivasi protokol stroke.
                </div>
                <br><br>
                <p style="text-align: right;"><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

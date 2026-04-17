import streamlit as st
from datetime import datetime

# --- 1. SESSION STATE ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""
if 'pilihan_layanan' not in st.session_state:
    st.session_state.pilihan_layanan = None

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- CSS PRINT & UI ---
st.markdown("""
    <style>
    @media print {
        .stButton, .stSidebar, header, footer, [data-testid="stHeader"], .no-print, .stTabs, .stSelectbox {
            display: none !important;
        }
        .main { background-color: white !important; }
        .print-container { 
            border: 2px solid black !important; 
            padding: 20px !important; 
            display: block !important;
            color: black !important;
            font-size: 12pt;
        }
    }
    .report-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #d1d1d1; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKA LOGIN & PEMILIHAN LAYANAN ---
if not st.session_state.nama_dokter:
    st.markdown("## 🩺 Selamat Datang di SINTALA-STROKE")
    input_dr = st.text_input("Masukkan Nama Lengkap Dokter (beserta gelar):")
    if st.button("Masuk Aplikasi"):
        if input_dr:
            st.session_state.nama_dokter = input_dr
            st.rerun()
    st.stop()

if st.session_state.pilihan_layanan is None:
    st.markdown(f"### Halo, {st.session_state.nama_dokter}")
    st.write("Silakan pilih modul layanan yang ingin digunakan:")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📊 Skrining Risiko (FSRP)", use_container_width=True):
            st.session_state.pilihan_layanan = "FSRP"
            st.rerun()
    with col_b:
        if st.button("🚨 Evaluasi Akut (NIHSS)", use_container_width=True):
            st.session_state.pilihan_layanan = "NIHSS"
            st.rerun()
    st.stop()

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🩺 SINTALA-STROKE")
    st.write(f"DPJP: **{st.session_state.nama_dokter}**")
    st.write(f"Layanan: **{st.session_state.pilihan_layanan}**")
    if st.button("⬅️ Ganti Modul / Reset"):
        st.session_state.pilihan_layanan = None
        st.rerun()
    st.divider()
    st.markdown('<button onclick="window.print()" style="width: 100%; height: 3em; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">🖨️ Cetak Laporan</button>', unsafe_allow_html=True)

# --- 4. MODUL FSRP ---
if st.session_state.pilihan_layanan == "FSRP":
    st.header("Kalkulator Risiko Stroke (FSRP)")
    col1, col2 = st.columns(2)
    with col1:
        nama_p = st.text_input("Nama Pasien", "Pasien Anonim")
        tds = st.number_input("TD Sistolik (mmHg)", 90, 250, 120)
    with col2:
        u55 = st.checkbox("Usia ≥ 55 Tahun")
        smk = st.checkbox("Merokok Aktif")
        dm = st.checkbox("Diabetes Melitus")
        jantung = st.multiselect("Riwayat Penyakit Jantung", ["PJK", "AF", "LVH (EKG)"])

    if st.button("Proses Analisa FSRP"):
        poin = sum([u55*2, (tds>=140)*3, smk*3, dm*2, ("PJK" in jantung)*2, ("AF" in jantung)*4, ("LVH (EKG)" in jantung)*5])
        kategori = "TINGGI" if poin >= 6 else "RENDAH"
        
        st.markdown(f"""
            <div class="report-box print-container">
                <h2 style="text-align: center;">LAPORAN SKRINING RISIKO STROKE (FSRP)</h2>
                <hr>
                <p><b>Nama Pasien:</b> {nama_p} | <b>Pemeriksa:</b> {st.session_state.nama_dokter}</p>
                <p><b>TD Sistolik:</b> {tds} mmHg | <b>Kategori Risiko:</b> {kategori} ({poin} Poin)</p>
                <br><p style="text-align: right;"><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 5. MODUL NIHSS (SESUAI PANDUAN GAMBAR) ---
else:
    st.header("Skala Stroke NIHSS (Evaluasi Lengkap)")
    st.info("Pilih skor sesuai hasil pemeriksaan fisik pasien.")
    
    with st.expander("1. Kesadaran (LOC)", expanded=True):
        c1a = st.selectbox("1a. Derajat Kesadaran", ["0: Sadar", "1: Mengantuk", "2: Stupor", "3: Koma"])
        c1b = st.selectbox("1b. LOC (Menjawab Pertanyaan: Bulan & Usia)", ["0: Keduanya tepat", "1: Satu tepat", "2: Salah semua"])
        c1c = st.selectbox("1c. LOC (Melaksanakan Perintah: Buka Mata & Genggam Tangan)", ["0: Keduanya tepat", "1: Satu tepat", "2: Salah semua"])
    
    with st.expander("2 - 4. Penglihatan & Wajah"):
        c2 = st.selectbox("2. Gerakan mata konjugat horisontal (GAZE)", ["0: Normal", "1: Abnormal pada satu mata", "2: Abnormal pada kedua mata"])
        c3 = st.selectbox("3. Lapang pandang pada tes konfrontasi", ["0: Tidak ada gangguan", "1: Hemianopia parsial", "2: Hemianopia komplit", "3: Hemianopia bilateral"])
        c4 = st.selectbox("4. Kelumpuhan wajah", ["0: Normal", "1: Minor", "2: Parsial", "3: Komplit"])

    with st.expander("5 - 6. Motorik (Lengan & Tungkai)"):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            c5a = st.selectbox("5a. Motorik Lengan Kanan", ["0: Tidak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tidak dapat diluruskan penuh", "3: Tidak dapat menahan gravitasi", "4: Tidak ada gerakan"])
            c6a = st.selectbox("6a. Motorik Tungkai Kanan", ["0: Tidak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tidak dapat diluruskan penuh", "3: Tidak dapat menahan gravitasi", "4: Tidak ada gerakan"])
        with col_m2:
            c5b = st.selectbox("5b. Motorik Lengan Kiri", ["0: Tidak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tidak dapat diluruskan penuh", "3: Tidak dapat menahan gravitasi", "4: Tidak ada gerakan"])
            c6b = st.selectbox("6b. Motorik Tungkai Kiri", ["0: Tidak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tidak dapat diluruskan penuh", "3: Tidak dapat menahan gravitasi", "4: Tidak ada gerakan"])

    with st.expander("7 - 11. Ataksia, Sensorik & Bahasa"):
        c7 = st.selectbox("7. Ataksia ekstremitas", ["0: Tidak ada", "1: Pada satu ekstremitas", "2: Pada dua atau lebih"])
        c8 = st.selectbox("8. Sensorik", ["0: Normal", "1: Parsial", "2: Terganggu berat"])
        c9 = st.selectbox("9. Afasia", ["0: Tidak ada afasia", "1: Afasia ringan-sedang", "2: Afasia berat", "3: Bisu"])
        c10 = st.selectbox("10. Disartria", ["0: Normal", "1: Disartria ringan-sedang", "2: Distartria berat"])
        c11 = st.selectbox("11. Neglect / Inattention", ["0: Normal", "1: Ringan", "2: Hebat"])

    if st.button("Selesaikan Laporan NIHSS"):
        scores = [c1a, c1b, c1c, c2, c3, c4, c5a, c5b, c6a, c6b, c7, c8, c9, c10, c11]
        total_nihss = sum([int(s.split(":")[0]) for s in scores])
        
        st.markdown(f"""
            <div class="report-box print-container">
                <h2 style="text-align: center;">RESUME PEMERIKSAAN NIHSS</h2>
                <hr>
                <p><b>Dokter Pemeriksa:</b> {st.session_state.nama_dokter}</p>
                <p><b>Tanggal Pemeriksaan:</b> {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
                <h3 style="background-color: #f0f0f0; padding: 10px;">TOTAL SKOR NIHSS: {total_nihss}</h3>
                <p><b>Interpretasi:</b> 
                {"Stroke Ringan" if total_nihss <= 4 else "Stroke Sedang" if total_nihss <= 15 else "Stroke Berat"}</p>
                <br><br><br>
                <p style="text-align: right;"><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

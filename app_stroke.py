import streamlit as st
from datetime import datetime

# --- SESSION STATE ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""
if 'pilihan_layanan' not in st.session_state:
    st.session_state.pilihan_layanan = None

# --- CONFIG & CSS ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide")
st.markdown("""
    <style>
    .report-box { padding: 30px; border-radius: 10px; border: 2px solid #004a99; background: white; color: black; }
    .stForm { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    @media print { .no-print, .stButton, section[data-testid="stSidebar"] { display: none !important; } }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN & NAV ---
if not st.session_state.nama_dokter:
    st.title("🩺 SINTALA-STROKE")
    input_dr = st.text_input("Identitas Dokter (DPJP):")
    if st.button("Masuk"):
        if input_dr:
            st.session_state.nama_dokter = input_dr
            st.rerun()
    st.stop()

if st.session_state.pilihan_layanan != "NIHSS":
    st.subheader(f"Halo, {st.session_state.nama_dokter}")
    if st.button("🚨 Buka Evaluasi Lengkap NIHSS"):
        st.session_state.pilihan_layanan = "NIHSS"
        st.rerun()
    st.stop()

# --- MODUL NIHSS LENGKAP (SESUAI GAMBAR PANDUAN) ---
st.header("Evaluasi Defisit Neurologis (Skala NIHSS)")
st.info("Pilih skor berdasarkan hasil pemeriksaan fisik sesuai panduan.")

with st.form("form_nihss_lengkap"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Tingkat Kesadaran (LOC)")
        c1a = st.selectbox("1.a Derajat kesadaran", ["0: Sadar", "1: Mengantuk", "2: Stupor", "3: Koma"])
        c1b = st.selectbox("1.b LOC (Menjawab pertanyaan)", ["0: Menjawab 2 pertanyaan tepat", "1: Menjawab 1 pertanyaan tepat", "2: Salah semua"])
        c1c = st.selectbox("1.c LOC (Melaksanakan perintah)", ["0: Mengikuti 2 perintah tepat", "1: Mengikuti 1 perintah tepat", "2: Salah semua"])
        
        st.subheader("2 - 4. Saraf Kranial")
        c2 = st.selectbox("2. Gerakan mata konjugat horisontal (GAZE)", ["0: Normal", "1: Abnormal pd satu mata", "2: Abnormal pd kedua mata"])
        c3 = st.selectbox("3. Lapang pandang pada tes konfrontasi", ["0: Tak ada gangguan", "1: Hemianopia parsial", "2: Hemianopia komplit", "3: Hemianopia bilateral"])
        c4 = st.selectbox("4. Kelumpuhan wajah", ["0: Normal", "1: Minor", "2: Parsial", "3: Komplit"])

        st.subheader("7 - 8. Koordinasi & Sensorik")
        c7 = st.selectbox("7. Ataksia ekstremitas", ["0: Tak ada", "1: Pd satu ekstremitas", "2: Pd dua atau lebih"])
        c8 = st.selectbox("8. Sensorik", ["0: Normal", "1: Parsial", "2: Terganggu berat"])

    with col2:
        st.subheader("5 - 6. Fungsi Motorik")
        c5a = st.selectbox("5.a Motorik lengan kanan", ["0: Tak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tdk dpt diluruskan penuh", "3: Tdk dpt menahan gravitasi", "4: Tdk ada gerakan"])
        c5b = st.selectbox("5.b Motorik lengan kiri", ["0: Tak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tdk dpt diluruskan penuh", "3: Tdk dpt menahan gravitasi", "4: Tdk ada gerakan"])
        c6a = st.selectbox("6.a Motorik tungkai kanan", ["0: Tak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tdk dpt diluruskan penuh", "3: Tdk dpt menahan gravitasi", "4: Tdk ada gerakan"])
        c6b = st.selectbox("6.b Motorik tungkai kiri", ["0: Tak ada kelumpuhan", "1: Jatuh sebelum 10 detik", "2: Tdk dpt diluruskan penuh", "3: Tdk dpt menahan gravitasi", "4: Tdk ada gerakan"])

        st.subheader("9 - 11. Bahasa & Atensi")
        c9 = st.selectbox("9. Afasia", ["0: Tak ada afasia", "1: Afasia ringan-sedang", "2: Afasia berat", "3: Bisu"])
        c10 = st.selectbox("10. Disartria", ["0: Normal", "1: Disartria ringan-sedang", "2: Distartria berat"])
        c11 = st.selectbox("11. Neglect / Inattention", ["0: Normal", "1: Ringan", "2: Hebat"])

    submit_nihss = st.form_submit_button("HITUNG TOTAL & BUAT LAPORAN", use_container_width=True)

if submit_nihss:
    # Ekstraksi angka dari pilihan teks
    items = [c1a, c1b, c1c, c2, c3, c4, c5a, c5b, c6a, c6b, c7, c8, c9, c10, c11]
    total_score = sum([int(s.split(":")[0]) for s in items])
    
    # Interpretasi
    if total_score == 0: interpretasi = "Normal"
    elif total_score <= 4: interpretasi = "Stroke Ringan"
    elif total_score <= 15: interpretasi = "Stroke Sedang"
    elif total_score <= 20: interpretasi = "Stroke Sedang-Berat"
    else: interpretasi = "Stroke Berat"

    st.markdown(f"""
        <div class="report-box print-container">
            <h2 style="text-align: center;">HASIL EVALUASI NIHSS</h2>
            <hr>
            <p><b>Dokter Pemeriksa:</b> {st.session_state.nama_dokter}</p>
            <p><b>Waktu Periksa:</b> {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
            <div style="background: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
                <h1 style="margin:0;">SKOR: {total_score}</h1>
                <h3>INTERPRETASI: {interpretasi}</h3>
            </div>
            <br>
            <p style="text-align: right;">Tanah Laut, {datetime.now().strftime("%d/%m/%Y")}<br><br><br><b>( {st.session_state.nama_dokter} )</b></p>
        </div>
    """, unsafe_allow_html=True)

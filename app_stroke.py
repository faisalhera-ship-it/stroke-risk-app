import streamlit as st
from datetime import datetime

# --- 1. SESSION STATE ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""
if 'pilihan_layanan' not in st.session_state:
    st.session_state.pilihan_layanan = None

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- CUSTOM CSS (MODERN UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f4f7f9; }
    
    .module-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center;
        transition: 0.3s; border-top: 5px solid #004a99; margin-bottom: 10px;
    }
    .module-card:hover { transform: translateY(-5px); }
    
    .report-box { 
        background: white; padding: 30px; border-radius: 10px; 
        border: 2px solid #004a99; margin-top: 20px; color: black;
    }

    @media print {
        .no-print, header, footer, [data-testid="stHeader"], section[data-testid="stSidebar"], .stButton, .stTabs {
            display: none !important;
        }
        .print-container { display: block !important; border: 1px solid black !important; padding: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKA LOGIN ---
if not st.session_state.nama_dokter:
    st.markdown("<h1 style='text-align: center; color: #004a99; margin-top: 50px;'>🩺 SINTALA-STROKE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sistem Informasi & Analisa Stroke Terpadu - Tanah Laut</p>", unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        input_dr = st.text_input("Identitas Dokter (DPJP):", placeholder="Contoh: dr. Faisal Bayu")
        if st.button("Masuk Sistem", use_container_width=True):
            if input_dr:
                st.session_state.nama_dokter = input_dr
                st.rerun()
    st.stop()

# --- 3. DASHBOARD UTAMA ---
if st.session_state.pilihan_layanan is None:
    st.markdown(f"### Selamat Datang, {st.session_state.nama_dokter}")
    st.write("Silakan pilih alat diagnostik yang diperlukan:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-card"><h4>📊 FSRP</h4><p>Skrining Risiko Stroke 10 Tahun</p></div>', unsafe_allow_html=True)
        if st.button("Buka Modul FSRP", use_container_width=True):
            st.session_state.pilihan_layanan = "FSRP"
            st.rerun()
    with col2:
        st.markdown('<div class="module-card"><h4>🚨 NIHSS</h4><p>Evaluasi Defisit Neurologis Akut</p></div>', unsafe_allow_html=True)
        if st.button("Buka Modul NIHSS", use_container_width=True):
            st.session_state.pilihan_layanan = "NIHSS"
            st.rerun()
    with col3:
        st.markdown('<div class="module-card" style="border-top-color: #ff8c00;"><h4>🧠 SIRIRAJ</h4><p>Pembeda Infark vs Hemoragik</p></div>', unsafe_allow_html=True)
        if st.button("Buka Modul SIRIRAJ", use_container_width=True):
            st.session_state.pilihan_layanan = "SIRIRAJ"
            st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("SINTALA-STROKE")
    st.write(f"DPJP: **{st.session_state.nama_dokter}**")
    st.write(f"Aktif: **{st.session_state.pilihan_layanan}**")
    if st.button("🔄 Menu Utama / Ganti Modul"):
        st.session_state.pilihan_layanan = None
        st.rerun()
    st.divider()
    st.markdown('<button onclick="window.print()" style="width: 100%; height: 3.5em; background-color: #28a745; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">🖨️ Cetak Laporan</button>', unsafe_allow_html=True)

# --- 5. KONTEN MODUL FSRP ---
if st.session_state.pilihan_layanan == "FSRP":
    st.header("Modul Skrining FSRP")
    with st.form("form_fsrp"):
        c1, c2 = st.columns(2)
        with c1:
            nama_p = st.text_input("Nama Pasien", "Pasien Anonim")
            tds = st.number_input("TD Sistolik (mmHg)", 90, 250, 120)
        with c2:
            u55 = st.checkbox("Usia ≥ 55 Tahun")
            dm = st.checkbox("Riwayat Diabetes")
            smk = st.checkbox("Merokok Aktif")
            jantung = st.multiselect("Riwayat Jantung", ["PJK", "AF", "LVH (EKG)"])
        
        submit_fsrp = st.form_submit_button("PROSES ANALISA", use_container_width=True)
        
    if submit_fsrp:
        poin = sum([u55*2, (tds>=140)*3, smk*3, dm*2, ("PJK" in jantung)*2, ("AF" in jantung)*4, ("LVH (EKG)" in jantung)*5])
        kategori = "TINGGI" if poin >= 6 else "RENDAH"
        st.markdown(f"""
            <div class="report-box print-container">
                <h3 style="text-align: center;">HASIL SKRINING FSRP</h3>
                <hr><p><b>Pasien:</b> {nama_p} | <b>Poin:</b> {poin} | <b>Risiko:</b> {kategori}</p>
                <br><p style="text-align: right;"><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 6. KONTEN MODUL NIHSS ---
elif st.session_state.pilihan_layanan == "NIHSS":
    st.header("Modul Evaluasi NIHSS")
    with st.form("form_nihss"):
        col_a, col_b = st.columns(2)
        with col_a:
            c1a = st.selectbox("1a. LOC", ["0: Sadar", "1: Mengantuk", "2: Stupor", "3: Koma"])
            c1b = st.selectbox("1b. LOC Tanya", ["0: Tepat", "1: Satu tepat", "2: Salah"])
            c2 = st.selectbox("2. GAZE", ["0: Normal", "1: Paresis", "2: Deviasi"])
            c5a = st.selectbox("5a. Lengan (Kanan)", ["0: Normal", "1: Drift", "2: Gravitasi", "3: Flasid"])
        with col_b:
            c5b = st.selectbox("5b. Lengan (Kiri)", ["0: Normal", "1: Drift", "2: Gravitasi", "3: Flasid"])
            c9 = st.selectbox("9. Afasia", ["0: Normal", "1: Ringan", "2: Berat", "3: Global"])
            c10 = st.selectbox("10. Disartria", ["0: Normal", "1: Pelo", "2: Berat"])
        
        submit_nihss = st.form_submit_button("HITUNG TOTAL NIHSS", use_container_width=True)

    if submit_nihss:
        total = int(c1a[0]) + int(c1b[0]) + int(c2[0]) + int(c5a[0]) + int(c5b[0]) + int(c9[0]) + int(c10[0])
        st.markdown(f'<div class="report-box print-container"><h2 style="text-align: center;">Skor NIHSS: {total}</h2><p style="text-align: center;">Tanda Tangan DPJP: {st.session_state.nama_dokter}</p></div>', unsafe_allow_html=True)

# --- 7. KONTEN MODUL SIRIRAJ ---
elif st.session_state.pilihan_layanan == "SIRIRAJ":
    st.header("Modul Siriraj Stroke Score")
    with st.form("form_siriraj"):
        c1, c2 = st.columns(2)
        with c1:
            kesadaran = st.selectbox("Kesadaran", ["0: Sadar penuh", "1: Somnolen", "2: Koma"])
            muntah = st.radio("Muntah Proyektil", ["0: Tidak", "1: Ya"])
        with c2:
            nyeri = st.radio("Nyeri Kepala Hebat", ["0: Tidak", "1: Ya"])
            td_d = st.number_input("TD Diastolik (mmHg)", 50, 200, 90)
            atheroma = st.checkbox("Riwayat DM/PJK")
            
        submit_sss = st.form_submit_button("HITUNG SIRIRAJ", use_container_width=True)

    if submit_sss:
        sss = (2.5 * int(kesadaran[0])) + (2 * int(muntah[0])) + (2 * int(nyeri[0])) + (0.1 * td_d) - (3 * int(atheroma)) - 12
        st.markdown(f'<div class="report-box print-container"><h2 style="text-align: center;">Skor SSS: {sss:.2f}</h2><p style="text-align: center;">DPJP: {st.session_state.nama_dokter}</p></div>', unsafe_allow_html=True)

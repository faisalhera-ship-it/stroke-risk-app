import streamlit as st
from datetime import datetime

# --- 1. SESSION STATE ---
if 'nama_dokter' not in st.session_state:
    st.session_state.nama_dokter = ""
if 'pilihan_layanan' not in st.session_state:
    st.session_state.pilihan_layanan = None

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE", layout="wide", page_icon="🩺")

# --- CUSTOM CSS (MODERN & CLEAN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f4f7f9; }
    
    /* Card Design */
    .module-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        transition: 0.3s;
        border-top: 5px solid #004a99;
    }
    .module-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    
    /* Result Box */
    .report-box { 
        background: white; 
        padding: 30px; 
        border-radius: 10px; 
        border: 2px solid #004a99; 
        margin-top: 20px;
    }

    /* Print Setup */
    @media print {
        .no-print, header, footer, [data-testid="stHeader"], section[data-testid="stSidebar"], .stButton {
            display: none !important;
        }
        .print-container { display: block !important; border: 1px solid black !important; padding: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKA LOGIN ---
if not st.session_state.nama_dokter:
    st.markdown("<h1 style='text-align: center; color: #004a99;'>🩺 SINTALA-STROKE</h1>", unsafe_allow_html=True)
    with st.columns([1,2,1])[1]:
        input_dr = st.text_input("Identitas Dokter (DPJP):", placeholder="dr. Faisal Bayu")
        if st.button("Masuk Sistem", use_container_width=True):
            if input_dr:
                st.session_state.nama_dokter = input_dr
                st.rerun()
    st.stop()

# --- 3. DASHBOARD UTAMA (PILIHAN LAYANAN) ---
if st.session_state.pilihan_layanan is None:
    st.markdown(f"### Selamat Datang, {st.session_state.nama_dokter}")
    st.write("Silakan pilih alat diagnostik:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-card"><h4>📊 FSRP</h4><p>Skrining Risiko 10 Tahun</p></div>', unsafe_allow_html=True)
        if st.button("Buka FSRP", use_container_width=True):
            st.session_state.pilihan_layanan = "FSRP"
            st.rerun()
    with col2:
        st.markdown('<div class="module-card"><h4>🚨 NIHSS</h4><p>Evaluasi Defisit Akut</p></div>', unsafe_allow_html=True)
        if st.button("Buka NIHSS", use_container_width=True):
            st.session_state.pilihan_layanan = "NIHSS"
            st.rerun()
    with col3:
        st.markdown('<div class="module-card" style="border-top-color: #ff8c00;"><h4>🧠 SIRIRAJ</h4><p>Pembeda Infark vs Hemoragik</p></div>', unsafe_allow_html=True)
        if st.button("Buka Siriraj", use_container_width=True):
            st.session_state.pilihan_layanan = "SIRIRAJ"
            st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("SINTALA")
    st.write(f"DPJP: **{st.session_state.nama_dokter}**")
    if st.button("🔄 Kembali ke Menu Utama"):
        st.session_state.pilihan_layanan = None
        st.rerun()
    st.divider()
    st.markdown('<button onclick="window.print()" style="width: 100%; height: 3em; background-color: #28a745; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">🖨️ Cetak Laporan</button>', unsafe_allow_html=True)

# --- 5. MODUL SIRIRAJ STROKE SCORE (SSS) ---
if st.session_state.pilihan_layanan == "SIRIRAJ":
    st.header("Siriraj Stroke Score (SSS)")
    st.info("Digunakan untuk membedakan jenis stroke secara klinis jika CT-Scan tidak tersedia.")
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            kesadaran = st.selectbox("Kesadaran", ["0: Sadar penuh", "1: Somnolen/Stupor", "2: Koma"])
            muntah = st.radio("Muntah Proyektil (dalam 2 jam)", ["0: Tidak", "1: Ya"])
            nyeri_kepala = st.radio("Nyeri Kepala Hebat (dalam 2 jam)", ["0: Tidak", "1: Ya"])
        with c2:
            td_diastolik = st.number_input("Tekanan Darah Diastolik (mmHg)", 50, 200, 90)
            atheroma = st.multiselect("Tanda Atheroma", ["DM", "PJK", "Klaudikasio Intermiten"])
            atheroma_val = 1 if len(atheroma) > 0 else 0

    if st.button("HITUNG SIRIRAJ SCORE", use_container_width=True):
        # Rumus SSS = (2.5 x kesadaran) + (2 x muntah) + (2 x nyeri) + (0.1 x diastolik) - (3 x atheroma) - 12
        sss = (2.5 * int(kesadaran[0])) + (2 * int(muntah[0])) + (2 * int(nyeri_kepala[0])) + (0.1 * td_diastolik) - (3 * atheroma_val) - 12
        
        hasil = ""
        warna = ""
        if sss > 1:
            hasil = "STROKE HEMORAGIK"
            warna = "#dc3545"
        elif sss < -1:
            hasil = "STROKE INFARK / NON-HEMORAGIK"
            warna = "#28a745"
        else:
            hasil = "HASIL MERAGUKAN (Membutuhkan CT-Scan)"
            warna = "#ff8c00"

        st.markdown(f"""
            <div class="report-box print-container">
                <h3 style="text-align: center;">HASIL DIAGNOSA KLINIS (SIRIRAJ)</h3>
                <hr>
                <p><b>Pemeriksa:</b> {st.session_state.nama_dokter}</p>
                <p><b>Skor Siriraj:</b> {sss:.2f}</p>
                <h2 style="color: {warna}; text-align: center;">{hasil}</h2>
                <hr>
                <p style="font-size: 0.8em;">*Catatan: Skor >1 (Hemoragik), <-1 (Infark), -1 s/d 1 (Zona Abu-abu/Borderline).</p>
                <br>
                <p style="text-align: right;">Tanah Laut, {datetime.now().strftime("%d/%m/%Y")}<br><br><br><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 6. MODUL LAIN (FSRP & NIHSS TETAP SAMA DENGAN UI BARU) ---
elif st.session_state.pilihan_layanan == "FSRP":
    st.header("Modul FSRP")
    # ... kodingan FSRP sebelumnya ...
    st.write("Silakan isi data untuk Skrining FSRP.")

elif st.session_state.pilihan_layanan == "NIHSS":
    st.header("Modul NIHSS")
    # ... kodingan NIHSS sebelumnya ...
    st.write("Silakan isi data untuk Evaluasi NIHSS.")

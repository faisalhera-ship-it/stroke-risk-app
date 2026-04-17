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
        .stButton, .stSidebar, header, footer, [data-testid="stHeader"], .no-print {
            display: none !important;
        }
        .main { background-color: white !important; }
        .print-container { 
            border: 2px solid black !important; 
            padding: 30px !important; 
            display: block !important;
        }
    }
    .report-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #d1d1d1; background-color: white; }
    .high-risk { border-left: 10px solid #dc3545; }
    .low-risk { border-left: 10px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. POP-UP LOGIN (DI AWAL) ---
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
    st.stop() # Menghentikan kode di bawahnya sampai dokter login

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🩺 SINTALA-STROKE")
    st.write(f"Login sebagai: \n**{st.session_state.nama_dokter}**")
    if st.button("Log Out / Ganti Dokter", size="small"):
        st.session_state.nama_dokter = ""
        st.rerun()
    st.divider()
    layanan = st.radio("Pilih Layanan:", ["Skrining Risiko (FSRP)", "Evaluasi Akut (NIHSS)"])
    st.divider()
    st.markdown('<button onclick="window.print()" style="width: 100%; height: 3em; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">🖨️ Cetak Laporan (Print)</button>', unsafe_allow_html=True)

# --- 4. LAYANAN 1: FSRP (VERSI CHECKLIST) ---
if layanan == "Skrining Risiko (FSRP)":
    st.header("Kalkulator Risiko Stroke (FSRP) - Versi Checklist")
    
    col1, col2 = st.columns(2)
    with col1:
        nama_pasien = st.text_input("Nama Pasien", "Pasien Anonim")
        jk = st.selectbox("Jenis Kelamin", ["Pria", "Wanita"])
        tds = st.number_input("Tekanan Darah Sistolik (mmHg)", 90, 250, 120)
    
    with col2:
        st.write("**Checklist Faktor Risiko:**")
        u55 = st.checkbox("Usia ≥ 55 Tahun")
        smk = st.checkbox("Merokok Aktif")
        dm = st.checkbox("Riwayat Diabetes Melitus (DM)")
        st.divider()
        st.write("**Checklist Penyakit Jantung:**")
        pjk = st.checkbox("Penyakit Jantung Koroner (PJK)")
        af = st.checkbox("Fibrilasi Atrium (AF)")
        lvh = st.checkbox("LV Hipertrofi (via EKG/Echo)")

    if st.button("Proses Analisa FSRP"):
        # Logika Poin
        poin = 0
        if u55: poin += 2
        if tds >= 140: poin += 3
        if smk: poin += 3
        if dm: poin += 2
        if pjk: poin += 2
        if af: poin += 4
        if lvh: poin += 5
        
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
                <p><b>Faktor Risiko Terdeteksi:</b><br>
                {"- Merokok " if smk else ""}{"- DM " if dm else ""}{"- PJK " if pjk else ""}{"- AF " if af else ""}{"- LVH" if lvh else ""}</p>
                <br>
                <p style="text-align: right;">Tanah Laut, {datetime.now().strftime("%d/%m/%Y")}<br>Dokter Pemeriksa/DPJP,<br><br><br><br><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 5. LAYANAN 2: NIHSS ---
else:
    st.header("Evaluasi Akut & Protokol Trombolisis")
    # (Kode NIHSS sama seperti sebelumnya, tapi tanda tangan otomatis memakai st.session_state.nama_dokter)
    st.write(f"Evaluator: **{st.session_state.nama_dokter}**")
    
    # ... (Bagian kodingan NIHSS sebelumnya disisipkan di sini)
    if st.button("Selesaikan Laporan IGD"):
         st.markdown(f"""
            <div class="report-box print-container">
                <h2 style="text-align: center;">RESUME EVALUASI STROKE AKUT</h2>
                <hr>
                <p style="text-align: right;">DPJP: <b>{st.session_state.nama_dokter}</b></p>
                <br><br><br>
                <p style="text-align: right;"><b>( {st.session_state.nama_dokter} )</b></p>
            </div>
        """, unsafe_allow_html=True)

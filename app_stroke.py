import streamlit as st
from datetime import datetime
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SINTALA-STROKE by dr. Faisal", layout="wide")

# Hapus baris lama yang berisi API Key langsung
# Ganti dengan blok ini:
import streamlit as st
import google.generativeai as genai

# Mengambil kunci secara aman dari Secrets, bukan ditulis manual
if "GOOGLE_API_KEY" in st.secrets:
    api_key_faisal = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key_faisal)
else:
    st.error("API Key belum terpasang di Secrets Dashboard.")

model = genai.GenerativeModel('gemini-1.5-flash')
# --- CUSTOM CSS UNTUK PRINT ---
st.markdown("""
    <style>
    @media print {
        .stButton, .stSidebar, header, footer, .stSelectbox, .stCheckbox, .stRadio, .stSlider, .stNumberInput, .stTextInput { 
            display: none !important; 
        }
        .main { background-color: white !important; }
        .print-box { 
            border: 2px solid black !important; 
            padding: 25px !important; 
            margin-bottom: 20px !important;
            display: block !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: NAVIGASI ---
st.sidebar.title("🩺 SINTALA-STROKE")
st.sidebar.subheader("by dr. Faisal")
st.sidebar.write("Sistem Informasi & Analisa Stroke Tanah Laut")
st.sidebar.divider()
mode = st.sidebar.selectbox("Pilih Layanan", ["Skrining Risiko (FSRP)", "Evaluasi Akut (NIHSS)"])

# --- MODE 1: SKRINING RISIKO (FSRP) ---
if mode == "Skrining Risiko (FSRP)":
    st.title("🧠 Skrining Risiko Stroke (FSRP)")
    st.caption("Edukasi preventif berdasarkan Framingham Stroke Risk Profile")
    
    with st.sidebar:
        st.header("📋 Data Pasien")
        nama = st.text_input("Nama Pasien", "Pasien Anonim")
        usia = st.slider("Usia", 20, 100, 50)
        gender = st.radio("Jenis Kelamin", ["Pria", "Wanita"])
        st.divider()
        sbp = st.number_input("Tekanan Darah Sistolik (mmHg)", 90, 250, 130)
        kol = st.number_input("Total Kolesterol (mg/dL)", 100, 500, 200)
        obat_ht = st.checkbox("Konsumsi Obat Hipertensi")
        merokok = st.checkbox("Perokok Aktif")
        dm = st.checkbox("Riwayat Diabetes")
        jantung = st.checkbox("Riwayat Jantung/LVH")
        af = st.checkbox("Atrial Fibrilasi (EKG)")

    # Logika Kalkulasi Poin
    poin = (1 if usia < 45 else 3 if usia < 60 else 5 if usia < 70 else 7)
    if sbp >= 140: poin += (4 if obat_ht else 2)
    if kol >= 200: poin += 1
    if merokok: poin += 3
    if dm: poin += 3
    if jantung: poin += 3
    if af: poin += 4

    if st.button("Hitung & Analisa AI Sekarang"):
        res = "Tinggi" if poin > 15 else "Sedang" if poin > 8 else "Rendah"
        warna = "red" if res == "Tinggi" else "orange" if res == "Sedang" else "green"
        
        # Perbaikan st.markdown baris 71 (Syntax Error Fixed)
        report_html = f"""
        <div class="print-box" style="border: 2px solid #333; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
            <h2 style="text-align: center; margin-bottom: 0;">SINTALA-STROKE REPORT</h2>
            <p style="text-align: center; font-style: italic;">By dr. Faisal Bayu - Tanah Laut</p>
            <hr>
            <table style="width:100%; border-collapse: collapse;">
                <tr><td style="padding: 5px;"><b>Nama Pasien</b></td><td>: {nama}</td></tr>
                <tr><td style="padding: 5px;"><b>Usia / Gender</b></td><td>: {usia} Thn / {gender}</td></tr>
                <tr><td style="padding: 5px;"><b>Tekanan Darah</b></td><td>: {sbp} mmHg</td></tr>
                <tr><td style="padding: 5px;"><b>Status Merokok</b></td><td>: {'Ya' if merokok else 'Tidak'}</td></tr>
                <tr style="background-color: #f0f0f0;">
                    <td style="padding: 10px;"><b>KATEGORI RISIKO</b></td>
                    <td>: <b style="color:{warna};">{res.upper()}</b> ({poin} Poin)</td>
                </tr>
            </table>
            <p style="font-size: 0.8em; margin-top: 15px;">Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>
        """
        st.markdown(report_html, unsafe_allow_html=True)
        
        # Analisa AI
        prompt_fsrp = f"Pasien {gender}, {usia}th. TD:{sbp}, Merokok:{merokok}, DM:{dm}. Risiko:{res}. Berikan analisa pencegahan spesifik singkat."
        
        with st.spinner("AI sedang menganalisa..."):
            analisa = model.generate_content(prompt_fsrp)
            st.markdown("### 📋 Analisa Deep Prevention (AI)")
            st.write(analisa.text)
        
        st.info("💡 Tekan **Ctrl + P** untuk print laporan.")

# --- MODE 2: EVALUASI AKUT (NIHSS) ---
elif mode == "Evaluasi Akut (NIHSS)":
    st.title("🚑 Evaluasi Stroke Akut (NIHSS)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Kalkulator NIHSS")
        nama_akut = st.text_input("Nama Pasien IGD", "Pasien Emergency")
        n1 = st.selectbox("1a. LOC", [0, 1, 2, 3])
        n2 = st.selectbox("1b. LOC Questions", [0, 1, 2])
        n3 = st.selectbox("1c. LOC Commands", [0, 1, 2])
        n4 = st.selectbox("2. Best Gaze", [0, 1, 2])
        n5 = st.selectbox("3. Visual Fields", [0, 1, 2, 3])
        n6 = st.selectbox("4. Facial Palsy", [0, 1, 2, 3])
        n7 = st.selectbox("5. Motor Arm (L/R)", [0, 1, 2, 3, 4])
        n8 = st.selectbox("6. Motor Leg (L/R)", [0, 1, 2, 3, 4])
        n9 = st.selectbox("7. Limb Ataxia", [0, 1, 2])
        n10 = st.selectbox("8. Sensory", [0, 1, 2])
        n11 = st.selectbox("9. Best Language", [0, 1, 2, 3])
        n12 = st.selectbox("10. Dysarthria", [0, 1, 2])
        n13 = st.selectbox("11. Extinction/Inattention", [0, 1, 2])
        total_nihss = sum([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13])

    with col2:
        st.subheader("2. Kontraindikasi rtPA")
        abs1 = st.checkbox("Riwayat Perdarahan Intrakranial (ICH)")
        abs2 = st.checkbox("Tekanan Darah > 185/110 mmHg")
        abs3 = st.checkbox("Trauma/Stroke < 3 bulan")
        st.divider()
        rel1 = st.checkbox("Onset > 4.5 Jam")
        rel2 = st.checkbox("Gula Darah Abnormal (<50 atau >400)")

    if st.button("Analisa Kelayakan"):
        kontra = any([abs1, abs2, abs3])
        
        st.markdown(f"""
        <div class="print-box" style="border: 2px solid red; padding: 20px; background-color: #fff0f0;">
            <h2 style="color:red; text-align:center;">LEMBAR EVALUASI IGD (SINTALA-STROKE)</h2>
            <p style="text-align: center;">By dr. Faisal Bayu</p>
            <hr>
            <p><b>Nama Pasien:</b> {nama_akut}</p>
            <p><b>Total Skor NIHSS: {total_nihss}</b></p>
            <p><b>Kontraindikasi Absolut:</b> {'❌ ADA' if kontra else '✅ TIDAK ADA'}</p>
        </div>
        """, unsafe_allow_html=True)

        prompt_nihss = f"Pasien stroke akut NIHSS {total_nihss}. Kontraindikasi: {kontra}. Berikan instruksi klinis segera."
        with st.spinner("AI menganalisa..."):
            instruksi = model.generate_content(prompt_nihss)
            st.write(instruksi.text)
        st.info("💡 Tekan **Ctrl + P** untuk print.")

import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Stroke Risk AI - dr. Faisal", layout="centered")

# --- HEADER ---
st.title("🧠 Stroke Risk Predictor AI")
st.write("Aplikasi skrining preventif berdasarkan *Framingham Stroke Risk Profile*.")
st.divider()

# --- SIDEBAR INPUT ---
st.sidebar.header("📋 Data Klinis Pasien")
nama = st.sidebar.text_input("Nama Pasien", value="Pasien Anonim")

# Perubahan: Umur 20-100 tahun
usia = st.sidebar.slider("Usia (Tahun)", 20, 100, 50)
gender = st.sidebar.radio("Jenis Kelamin", ["Pria", "Wanita"])

st.sidebar.divider()
st.sidebar.write("### Tanda Vital & Lab")
sbp = st.sidebar.number_input("Tekanan Darah Sistolik (mmHg)", 90, 250, 130)
kolesterol = st.sidebar.number_input("Total Kolesterol (mg/dL)", 100, 500, 200)
obat_hipertensi = st.sidebar.checkbox("Sedang Konsumsi Obat Hipertensi")

st.sidebar.divider()
st.sidebar.write("### Faktor Risiko & Komorbid")
merokok = st.sidebar.checkbox("Perokok Aktif")
diabetes = st.sidebar.checkbox("Riwayat Diabetes")
riwayat_jantung = st.sidebar.checkbox("Riwayat Jantung (CVD/LVH)")
af_ekg = st.sidebar.checkbox("Atrial Fibrilasi (Hasil EKG)")

# --- LOGIKA PERHITUNGAN (FSRP MODIFIED) ---
def kalkulasi_skor_stroke(usia, sbp, kol, obat, dm, rokok, cvd, af):
    poin = 0
    
    # 1. Skor Usia
    if usia >= 80: poin += 10
    elif usia >= 70: poin += 7
    elif usia >= 60: poin += 5
    elif usia >= 45: poin += 3
    else: poin += 1
    
    # 2. Skor Tekanan Darah (Sistolik)
    if obat:
        if sbp >= 160: poin += 6
        elif sbp >= 140: poin += 4
        else: poin += 2
    else:
        if sbp >= 160: poin += 3
        elif sbp >= 140: poin += 2

    # 3. Skor Kolesterol (Total)
    if kol >= 240: poin += 3
    elif kol >= 200: poin += 1
    
    # 4. Faktor Risiko Lainnya
    if dm: poin += 3
    if rokok: poin += 3
    if cvd: poin += 3
    if af: poin += 4
    
    # Mapping Poin ke Persentase Risiko 10 Tahun (Estimasi)
    if poin <= 5: risiko = "Rendah (<5%)"
    elif poin <= 12: risiko = "Sedang (5-15%)"
    elif poin <= 20: risiko = "Tinggi (15-30%)"
    else: risiko = "Sangat Tinggi (>30%)"
    
    return poin, risiko

# --- TAMPILAN UTAMA & HASIL ---
if st.button("Analisa Risiko Sekarang"):
    total_poin, kategori = kalkulasi_skor_stroke(usia, sbp, kolesterol, obat_hipertensi, diabetes, merokok, riwayat_jantung, af_ekg)
    
    st.subheader(f"Hasil Analisa: {nama}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Poin", total_poin)
    with col2:
        st.metric("Kategori Risiko", kategori)
    
    st.divider()
    
    # Edukasi Berdasarkan Input
    st.write("### 🩺 Rekomendasi Medis (AI Preview):")
    
    saran = []
    if sbp >= 140: saran.append("- Optimalkan kontrol tekanan darah (Target <130/80 mmHg).")
    if kolesterol >= 200: saran.append("- Evaluasi profil lipid dan pertimbangkan diet rendah lemak/statin.")
    if merokok: saran.append("- **Sangat Disarankan:** Program berhenti merokok untuk menurunkan risiko secara drastis.")
    if af_ekg: saran.append("- AF terdeteksi: Perlu evaluasi antikoagulan untuk cegah emboli.")
    
    if saran:
        for s in saran:
            st.write(s)
    else:
        st.success("Parameter klinis pasien saat ini dalam batas optimal. Pertahankan gaya hidup sehat!")

    # Pesan untuk Dokter (Internal)
    st.info("Catatan Dokter: Alat ini adalah instrumen skrining. Keputusan klinis tetap berdasarkan pemeriksaan fisik dan penunjang lengkap.")

else:
    st.info("Masukkan data pasien di bilah samping (sidebar) dan klik tombol Analisa.")
import streamlit as st
from datetime import datetime
import urllib.parse

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="SINTALA-STROKE v3.2", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; }
    .report-card { 
        background: white; padding: 30px; border-radius: 15px; 
        border: 2px solid #004a99; margin-top: 20px; 
    }
    .stButton>button { border-radius: 10px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def get_wa_link(phone, message):
    phone = "".join(filter(str.isdigit, phone))
    if phone.startswith("0"): phone = "62" + phone[1:]
    return f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

# --- 3. SESSION STATE ---
if 'pilihan' not in st.session_state: st.session_state.pilihan = None
if 'nama_dr' not in st.session_state: st.session_state.nama_dr = ""

# --- 4. LOGIN ---
if not st.session_state.nama_dr:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h2 style='text-align:center;'>🩺 SINTALA-STROKE</h2>", unsafe_allow_html=True)
        name = st.text_input("Identitas Dokter (DPJP):", placeholder="dr. Faisal Bayu")
        if st.button("Masuk Sistem", use_container_width=True):
            if name: st.session_state.nama_dr = name; st.rerun()
    st.stop()

# --- 5. SIDEBAR & MENU ---
with st.sidebar:
    st.title("SINTALA v3.2")
    st.write(f"DPJP: **{st.session_state.nama_dr}**")
    if st.button("🏠 Menu Utama", use_container_width=True):
        st.session_state.pilihan = None; st.rerun()
    st.divider()
    st.caption("Developed for Tanah Laut Healthcare")

if st.session_state.pilihan is None:
    st.subheader("Pilih Instrumen Analisa:")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📊 FSRP\n(Skrining)", use_container_width=True, height=100): st.session_state.pilihan = "FSRP"; st.rerun()
    with c2: 
        if st.button("🚨 NIHSS\n(Emergency)", use_container_width=True, height=100): st.session_state.pilihan = "NIHSS"; st.rerun()
    with c3: 
        if st.button("🧠 SIRIRAJ\n(Diagnostik)", use_container_width=True, height=100): st.session_state.pilihan = "SIRIRAJ"; st.rerun()
    st.stop()

# --- 6. MODUL FSRP (DENGAN KALKULATOR) ---
if st.session_state.pilihan == "FSRP":
    st.header("📊 Kalkulator FSRP & Edukasi")
    with st.form("fsrp_calc"):
        col1, col2 = st.columns(2)
        with col1:
            p_nama = st.text_input("Nama Pasien")
            p_wa = st.text_input("Nomor WA Pasien (08...)")
            usia = st.checkbox("Usia ≥ 55 Tahun")
            tds = st.number_input("TD Sistolik", 90, 220, 120)
        with col2:
            smk = st.checkbox("Merokok")
            dm = st.checkbox("Diabetes")
            jantung = st.checkbox("Riwayat Penyakit Jantung (AF/PJK)")
            kol = st.checkbox("Kolesterol > 200")
        
        btn = st.form_submit_button("Hitung Skor & Siapkan WA")

    if btn:
        skor = sum([usia*2, (tds>=140)*3, smk*3, dm*2, jantung*4, kol*2])
        risiko = "TINGGI" if skor >= 7 else "RENDAH"
        
        msg = (f"*HASIL SKRINING SINTALA*\n\nHalo {p_nama}, risiko stroke Anda saat ini: *{risiko}* (Skor:{skor}).\n\n"
               f"*Edukasi Dokter:*\n1. Kontrol tensi rutin\n2. Kurangi garam & lemak\n3. Olahraga 30 menit/hari\n\n"
               f"Jika ada keluhan bicara pelo atau lemah separuh badan, segera ke RS!")
        
        st.markdown(f"<div class='report-card'><h3>Hasil: Risiko {risiko}</h3><p>Total Skor: {skor}</p></div>", unsafe_allow_html=True)
        st.markdown(f'<a href="{get_wa_link(p_wa, msg)}" target="_blank"><button style="width:100%; padding:12px; background:#25D366; color:white; border:none; border-radius:10px; cursor:pointer;">📲 KIRIM HASIL KE WA PASIEN</button></a>', unsafe_allow_html=True)

# --- 7. MODUL NIHSS & SIRIRAJ (DENGAN FORMAT SOAP) ---
elif st.session_state.pilihan in ["NIHSS", "SIRIRAJ"]:
    st.header(f"🚨 Form Emergency {st.session_state.pilihan}")
    with st.form("emergency_soap"):
        c1, c2 = st.columns(2)
        with c1:
            p_nama = st.text_input("Nama Pasien")
            p_umur = st.text_input("Umur")
            onset = st.text_input("Onset (Jam)")
            rs_tujuan = st.selectbox("RS Tujuan", ["RSUD H. Boejasin", "RS Borneo Citra", "RS Ciputra"])
        with c2:
            td = st.text_input("TD (mmHg)", "140/90")
            nadi = st.text_input("Nadi", "88")
            gcs = st.text_input("GCS", "E4V5M6")
            lat = st.selectbox("Lateralisasi", ["Kiri", "Kanan", "Tidak Ada"])
        
        keluhan = st.text_area("Subjek: Keluhan & Riwayat")
        
        # Logika Skor (Dokter bisa isi manual dari hasil pemeriksaan)
        skor_val = st.number_input(f"Input Skor {st.session_state.pilihan} Terhitung", 0, 42, 0)
        plan = st.text_area("Plan: Tindakan/Terapi", "O2 3LPM, IVFD RL 20tpm, Loading Aspilet...")
        
        btn_soap = st.form_submit_button("Generate WA SOAP")

    if btn_soap:
        # Daftar Nomor IGD (Silakan update nomor aslinya, Dok)
        igd_numbers = {"RSUD H. Boejasin": "0811000", "RS Borneo Citra": "0811111", "RS Ciputra": "0811222"}
        
        soap_msg = (
            f"*RUJUKAN EMERGENCY STROKE*\n"
            f"Tujuan: *IGD {rs_tujuan}*\n\n"
            f"*S:* {p_nama} ({p_umur}th). {keluhan}. Onset {onset}.\n"
            f"*O:* TD:{td}, HR:{nadi}, GCS:{gcs}, Lat:{lat}. Skor {st.session_state.pilihan}:{skor_val}\n"
            f"*A:* Suspek Stroke (Rujukan Puskesmas)\n"
            f"*P:* {plan}\n\n"
            f"Mohon atensi dok. Terimakasih."
        )
        st.markdown(f'<a href="{get_wa_link(igd_numbers[rs_tujuan], soap_msg)}" target="_blank"><button style="width:100%; padding:15px; background:#dc2626; color:white; border:none; border-radius:12px; cursor:pointer;">🚨 KIRIM WA SOAP KE IGD RS</button></a>', unsafe_allow_html=True)

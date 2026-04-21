import streamlit as st
from datetime import datetime
import urllib.parse

# --- 1. CONFIG & CSS ---
st.set_page_config(page_title="SINTALA-STROKE v3.0", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .emergency-card { background: #fee2e2; padding: 20px; border-radius: 12px; border-left: 5px solid #dc2626; margin-bottom: 20px; }
    .edu-card { background: #f0fdf4; padding: 20px; border-radius: 12px; border-left: 5px solid #16a34a; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNGSI KIRIM WA ---
def send_wa(phone, message):
    # Bersihkan nomor telepon (hilangkan spasi/tanda baca)
    phone = "".join(filter(str.isdigit, phone))
    if phone.startswith("0"):
        phone = "62" + phone[1:]
    
    encoded_msg = urllib.parse.quote(message)
    wa_url = f"https://wa.me/{phone}?text={encoded_msg}"
    return wa_url

# --- 3. SESSION STATE ---
if 'pilihan' not in st.session_state: st.session_state.pilihan = None

# --- 4. MODUL FSRP (EDUKASI PASIEN) ---
if st.session_state.pilihan == "FSRP":
    st.header("📊 Screening FSRP & Edukasi Pasien")
    with st.form("fsrp_wa"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Pasien")
            wa_pasien = st.text_input("Nomor WA Pasien (Contoh: 0812...)")
            skor = st.slider("Skor FSRP Terhitung", 0, 20, 5)
        with col2:
            edukasi = st.multiselect("Pesan Edukasi Tambahan", 
                                    ["Kurangi Garam", "Olahraga 30 Menit", "Kontrol Rutin Puskesmas", "Stop Rokok"])
        
        if st.form_submit_button("Generate WA Edukasi"):
            res = "TINGGI" if skor >= 7 else "RENDAH"
            pesan_wa = (
                f"*HASIL SKRINING STROKE - SINTALA*\n\n"
                f"Halo Bapak/Ibu *{nama}*,\n"
                f"Berdasarkan pemeriksaan hari ini, tingkat risiko stroke Anda adalah: *{res}* (Skor: {skor}).\n\n"
                f"*Saran Dokter:*\n"
                f"- {', '.join(edukasi) if edukasi else 'Tetap jaga pola hidup sehat'}\n\n"
                f"Segera ke fasilitas kesehatan jika muncul gejala *SeGeRa Ke RS* (Senyum miring, Gerak lemah, Bicara pelo). Tetap semangat!"
            )
            st.markdown(f'<a href="{send_wa(wa_pasien, pesan_wa)}" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">📲 KIRIM EDUKASI KE WA PASIEN</button></a>', unsafe_allow_html=True)

# --- 5. MODUL EMERGENCY (NIHSS & SIRIRAJ - WA SOAP) ---
elif st.session_state.pilihan in ["NIHSS", "SIRIRAJ"]:
    st.header(f"🚨 Rujukan Emergency via {st.session_state.pilihan}")
    
    with st.form("soap_form"):
        st.subheader("Informasi Pasien & SOAP")
        c1, c2, c3 = st.columns(3)
        with c1:
            nama_p = st.text_input("Nama Pasien")
            umur = st.text_input("Umur")
            rs_tujuan = st.selectbox("RS Tujuan (IGD)", ["RSUD H. Boejasin", "RS Borneo Citra Medika", "RS Ciputra"])
        with c2:
            td = st.text_input("TD (mmHg)", "120/80")
            nadi = st.text_input("Nadi", "88")
            gcs = st.text_input("GCS", "E4V5M6")
        with c3:
            rr = st.text_input("RR", "20")
            skor_val = st.number_input(f"Skor {st.session_state.pilihan}", 0, 42, 10)
            lat = st.selectbox("Lateralisasi", ["Kiri", "Kanan", "Tidak Ada"])

        subjek = st.text_area("Subjective (Keluhan Utama & Onset)")
        plan = st.text_area("Plan (Tindakan yang sudah dilakukan)", "Oksigen 3LPM, IVFD RL 20 tpm, Loading...")
        
        # Database Nomor IGD (Contoh)
        igd_numbers = {
            "RSUD H. Boejasin": "08115000000", # Ganti nomor aslinya Dok
            "RS Borneo Citra Medika": "08115111111",
            "RS Ciputra": "08115222222"
        }

        if st.form_submit_button("Kirim SOAP ke IGD"):
            soap_msg = (
                f"*RUJUKAN EMERGENCY STROKE*\n"
                f"Kepada: *IGD {rs_tujuan}*\n\n"
                f"*S (Subjective):*\n- Pasien: {nama_p} ({umur}th)\n- Keluhan: {subjek}\n\n"
                f"*O (Objective):*\n- TD: {td} | HR: {nadi} | GCS: {gcs} | RR: {rr}\n"
                f"- Status Neuro: Lateralisasi {lat}\n"
                f"- Skor {st.session_state.pilihan}: {skor_val}\n\n"
                f"*A (Assessment):*\n- Suspek Stroke (Rujukan dari Puskesmas)\n\n"
                f"*P (Plan):*\n- {plan}\n\n"
                f"Mohon persiapan ruang resusitasi/CT-Scan. Terima kasih."
            )
            st.markdown(f'<a href="{send_wa(igd_numbers[rs_tujuan], soap_msg)}" target="_blank"><button style="width:100%; padding:15px; background:#dc2626; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold;">🚨 KIRIM SOAP KE WA IGD RS</button></a>', unsafe_allow_html=True)

# --- MENU UTAMA ---
else:
    st.title("🩺 SINTALA v3.0")
    st.write("Selamat Datang, dr. Faisal Bayu. Pilih menu:")
    if st.button("📊 FSRP (Skrining & Edukasi WA)"): st.session_state.pilihan = "FSRP"; st.rerun()
    if st.button("🚨 NIHSS / SIRIRAJ (Emergency SOAP WA)"): st.session_state.pilihan = "NIHSS"; st.rerun()

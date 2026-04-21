import streamlit as st
from datetime import datetime
import urllib.parse

# --- 1. CONFIG & CSS (Optimasi Tampilan & Print) ---
st.set_page_config(page_title="SINTALA-STROKE v3.1", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; }
    .report-box {
        background-color: #ffffff; padding: 25px; border-radius: 15px;
        border: 2px solid #004a99; margin-top: 20px;
    }
    @media print {
        .no-print, [data-testid="stSidebar"], .stButton, button { display: none !important; }
        .print-area { display: block !important; width: 100% !important; padding: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNGSI WA ENGINE ---
def generate_wa_link(phone, message):
    phone = "".join(filter(str.isdigit, phone))
    if phone.startswith("0"): phone = "62" + phone[1:]
    encoded_msg = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded_msg}"

# --- 3. SESSION STATE ---
if 'nama_dokter' not in st.session_state: st.session_state.nama_dokter = ""
if 'pilihan' not in st.session_state: st.session_state.pilihan = None

# --- 4. LOGIN ---
if not st.session_state.nama_dokter:
    _, col_m, _ = st.columns([1, 1.5, 1])
    with col_m:
        st.markdown("<h1 style='text-align:center; color:#004a99;'>🩺 SINTALA-STROKE</h1>", unsafe_allow_html=True)
        dr_name = st.text_input("Nama Dokter (DPJP):")
        if st.button("Masuk Dashboard", use_container_width=True):
            if dr_name: st.session_state.nama_dokter = dr_name; st.rerun()
    st.stop()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("SINTALA v3.1")
    st.write(f"DPJP: **{st.session_state.nama_dokter}**")
    if st.button("🏠 Menu Utama", use_container_width=True):
        st.session_state.pilihan = None; st.rerun()
    st.divider()
    st.markdown('<button onclick="window.print()" style="width:100%; height:3em; background:#16a34a; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">🖨️ PRINT LAPORAN (PDF)</button>', unsafe_allow_html=True)

# --- 6. MENU UTAMA ---
if st.session_state.pilihan is None:
    st.subheader("Pilih Instrumen Medis:")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📊 FSRP\n(Skrining & Edukasi)", use_container_width=True, height=100): st.session_state.pilihan = "FSRP"; st.rerun()
    with c2: 
        if st.button("🚨 NIHSS\n(Defisit Akut)", use_container_width=True, height=100): st.session_state.pilihan = "NIHSS"; st.rerun()
    with c3: 
        if st.button("🧠 SIRIRAJ\n(Diagnostik)", use_container_width=True, height=100): st.session_state.pilihan = "SIRIRAJ"; st.rerun()
    st.stop()

# --- 7. MODUL FSRP (DENGAN WA EDUKASI) ---
if st.session_state.pilihan == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile")
    with st.form("fsrp_form"):
        col1, col2 = st.columns(2)
        with col1:
            p_nama = st.text_input("Nama Pasien")
            p_wa = st.text_input("WA Pasien (08...)")
            usia = st.checkbox("Usia ≥ 55 Tahun")
            tds = st.number_input("TD Sistolik", 90, 250, 120)
        with col2:
            smk = st.checkbox("Merokok Aktif")
            dm = st.checkbox("Diabetes Melitus")
            jantung = st.multiselect("Riwayat Jantung", ["PJK", "AF", "LVH"])
            kol = st.number_input("Kolesterol Total", 100, 400, 190)
        submit = st.form_submit_button("HITUNG & GENERATE EDUKASI")

    if submit:
        skor = sum([usia*2, (tds>=140)*3, smk*3, dm*2, (len(jantung)>0)*3, (kol>=200)*2])
        res = "TINGGI" if skor >= 7 else "RENDAH"
        
        # Pesan WA Edukasi
        msg = (f"*HASIL SKRINING SINTALA*\nHalo {p_nama}, risiko stroke Anda: *{res}* (Skor:{skor}).\n"
               f"Saran: Kurangi garam, olahraga rutin, dan kontrol ke Puskesmas/RS.")
        
        st.markdown(f"""<div class='report-box print-area'>
            <h3>HASIL ANALISA FSRP</h3>
            <p>Pasien: {p_nama} | Skor: <b>{skor}</b></p>
            <h2 style='color:{'red' if res=='TINGGI' else 'green'};'>RISIKO {res}</h2>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f'<a href="{generate_wa_link(p_wa, msg)}" target="_blank"><button style="width:100%; padding:12px; background:#25D366; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer; margin-top:10px;">📲 KIRIM EDUKASI KE WA PASIEN</button></a>', unsafe_allow_html=True)

# --- 8. MODUL NIHSS & SIRIRAJ (DENGAN WA SOAP) ---
elif st.session_state.pilihan in ["NIHSS", "SIRIRAJ"]:
    st.header(f"🚨 Rujukan Emergency via {st.session_state.pilihan}")
    with st.form("emergency_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            p_nama = st.text_input("Nama Pasien")
            p_umur = st.text_input("Umur")
            rs_tujuan = st.selectbox("Tujuan IGD", ["RSUD H. Boejasin", "RS Borneo Citra", "RS Ciputra"])
        with c2:
            td = st.text_input("TD", "140/90")
            gcs = st.text_input("GCS", "E4V5M6")
            lat = st.selectbox("Lateralisasi", ["Kiri", "Kanan", "Tidak Ada"])
        with c3:
            s_val = st.number_input(f"Skor {st.session_state.pilihan}", 0, 42, 5)
            onset = st.text_input("Onset (Jam Lalu)", "2 Jam")
        
        subjek = st.text_area("Keluhan Utama (S)")
        plan = st.text_area("Tindakan Awal (P)", "O2 3LPM, IVFD RL...")
        
        submit_em = st.form_submit_button("GENERATE WA SOAP")

    if submit_em:
        # Database Nomor IGD
        igd_db = {"RSUD H. Boejasin": "0811000000", "RS Borneo Citra": "0811111111", "RS Ciputra": "0811222222"}
        
        soap_msg = (
            f"*RUJUKAN STROKE (SINTALA)*\n"
            f"Ke: *IGD {rs_tujuan}*\n\n"
            f"*S:* {p_nama} ({p_umur}th), Keluhan: {subjek}, Onset: {onset}\n"
            f"*O:* TD:{td}, GCS:{gcs}, Lat:{lat}, Skor {st.session_state.pilihan}:{s_val}\n"
            f"*A:* Suspek Stroke\n"
            f"*P:* {plan}"
        )
        
        st.info("Pratinjau Laporan SOAP Berhasil Dibuat!")
        st.markdown(f'<a href="{generate_wa_link(igd_db[rs_tujuan], soap_msg)}" target="_blank"><button style="width:100%; padding:15px; background:#dc2626; color:white; border:none; border-radius:12px; font-weight:bold; cursor:pointer;">🚨 KIRIM SOAP KE WA IGD RS</button></a>', unsafe_allow_html=True)

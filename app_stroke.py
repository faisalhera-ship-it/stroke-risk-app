import streamlit as st
import urllib.parse
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="SINTALA v3.5", layout="wide", page_icon="🩺")

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; }
    .wa-btn {
        display: block; width: 100%; padding: 15px; background-color: #25D366;
        color: white; text-align: center; font-weight: bold; border-radius: 12px;
        text-decoration: none; margin-top: 15px;
    }
    .soap-box { background: white; padding: 20px; border-radius: 15px; border: 2px solid #004a99; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI HELPER ---
def wa_link(nomor, pesan):
    no = "".join(filter(str.isdigit, nomor))
    if no.startswith("0"): no = "62" + no[1:]
    return f"https://wa.me/{no}?text={urllib.parse.quote(pesan)}"

# --- SESSION STATE ---
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'menu' not in st.session_state: st.session_state.menu = None

# --- LOGIN ---
if not st.session_state.dr:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h2 style='text-align:center;'>🩺 SINTALA-STROKE</h2>", unsafe_allow_html=True)
        nama = st.text_input("Nama Dokter (DPJP):", placeholder="dr. Faisal Bayu")
        if st.button("Masuk"):
            if nama: st.session_state.dr = nama; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.write(f"DPJP: **{st.session_state.dr}**")
    if st.button("🏠 Menu Utama", use_container_width=True):
        st.session_state.menu = None; st.rerun()

# --- MENU UTAMA ---
if st.session_state.menu is None:
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📊 FSRP", use_container_width=True, height=100): st.session_state.menu = "FSRP"; st.rerun()
    with c2: 
        if st.button("🚨 NIHSS", use_container_width=True, height=100): st.session_state.menu = "NIHSS"; st.rerun()
    with c3: 
        if st.button("🧠 SIRIRAJ", use_container_width=True, height=100): st.session_state.menu = "SIRIRAJ"; st.rerun()
    st.stop()

# --- MODUL NIHSS (11 PARAMETER) ---
if st.session_state.menu == "NIHSS":
    st.header("🚨 NIHSS Scoring (National Institutes of Health Stroke Scale)")
    with st.form("nihss_form"):
        p_nama = st.text_input("Nama Pasien")
        p_wa = st.selectbox("RS Tujuan", ["RSUD H. Boejasin", "RS Borneo Citra", "RS Ciputra"])
        
        c1, c2 = st.columns(2)
        with c1:
            n1 = st.selectbox("1a. Kesadaran (LOC)", [0,1,2,3], format_func=lambda x: f"{x} - {'Sadar' if x==0 else 'Somnolen' if x==1 else 'Stupor' if x==2 else 'Koma'}")
            n2 = st.selectbox("1b. Tanya LOC (Bulan/Usia)", [0,1,2], format_func=lambda x: f"{x} - {'Benar Semua' if x==0 else '1 Benar' if x==1 else 'Salah Semua'}")
            n3 = st.selectbox("2. Gerakan Mata (Gaze)", [0,1,2])
            n4 = st.selectbox("3. Lapang Pandang (Visual)", [0,1,2,3])
            n5 = st.selectbox("4. Kelumpuhan Wajah", [0,1,2,3])
            n6 = st.selectbox("5a/b. Motorik Lengan (Ka/Ki)", [0,1,2,3,4])
        with c2:
            n7 = st.selectbox("6a/b. Motorik Tungkai (Ka/Ki)", [0,1,2,3,4])
            n8 = st.selectbox("7. Ataksia Anggota Gerak", [0,1,2])
            n9 = st.selectbox("8. Sensorik", [0,1,2])
            n10 = st.selectbox("9. Bahasa (Afasia)", [0,1,2,3])
            n11 = st.selectbox("10. Disartria", [0,1,2])
            n12 = st.selectbox("11. Pengabaian (Neglect)", [0,1,2])

        sub = st.text_area("Subjek: Keluhan & Onset")
        submit = st.form_submit_button("HITUNG SKOR & GENERATE SOAP")

    if submit:
        total = sum([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12])
        kat = "Ringan" if total <= 4 else "Sedang" if total <= 15 else "Sedang-Berat" if total <= 24 else "Berat"
        
        soap = (f"*RUJUKAN STROKE (NIHSS)*\nKe: IGD {p_wa}\n\n"
                f"*S:* {p_nama}. {sub}\n"
                f"*O:* Skor NIHSS: {total} ({kat})\n"
                f"*A:* Suspek Stroke Akut\n"
                f"*P:* Mohon persiapan CT-Scan & Tirah Baring.")
        
        st.success(f"Skor NIHSS: {total} - {kat}")
        st.markdown(f'<a href="{wa_link("0811000", soap)}" target="_blank" class="wa-btn" style="background:#dc2626;">🚨 KIRIM WA SOAP KE IGD</a>', unsafe_allow_html=True)

# --- MODUL SIRIRAJ ---
elif st.session_state.menu == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score (SSS)")
    st.info("SSS = (2.5 x Derajat Kesadaran) + (2 x Muntah) + (2 x Nyeri Kepala) + (0.1 x TD Diastolik) - (3 x Atheroma) - 12")
    with st.form("sss_form"):
        p_nama = st.text_input("Nama Pasien")
        c1, c2 = st.columns(2)
        with c1:
            sadar = st.selectbox("Derajat Kesadaran", [0, 1, 2], format_func=lambda x: f"{x} - {'Sadar' if x==0 else 'Mengantuk' if x==1 else 'Koma'}")
            muntah = st.radio("Muntah (dalam 2 jam)", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
            nyeri = st.radio("Nyeri Kepala (dalam 2 jam)", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        with col2:
            diastolik = st.number_input("Tekanan Darah Diastolik", 60, 150, 90)
            atheroma = st.radio("Atheroma (DM/PJK/Klaudikasio)", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        
        sub_sss = st.text_area("Keluhan Tambahan")
        btn_sss = st.form_submit_button("HITUNG SIRIRAJ")

    if btn_sss:
        # Rumus Siriraj
        skor_sss = (2.5 * sadar) + (2 * muntah) + (2 * nyeri) + (0.1 * diastolik) - (3 * atheroma) - 12
        hasil = "Stroke Hemoragik (SH)" if skor_sss > 1 else "Stroke Iskemik (SS)" if skor_sss < -1 else "Meragukan (Perlu CT-Scan)"
        
        soap_sss = (f"*RUJUKAN STROKE (SIRIRAJ)*\n\n"
                    f"*S:* {p_nama}. {sub_sss}\n"
                    f"*O:* Skor Siriraj: {skor_sss:.1f} ({hasil})\n"
                    f"*A:* {hasil}\n"
                    f"*P:* Rujuk untuk CT-Scan segera.")
        
        st.markdown(f"<div class='soap-box'><h3>Skor: {skor_sss:.1f}</h3><h4>Prediksi: {hasil}</h4></div>", unsafe_allow_html=True)
        st.markdown(f'<a href="{wa_link("0811000", soap_sss)}" target="_blank" class="wa-btn">🚨 KIRIM WA KE IGD</a>', unsafe_allow_html=True)

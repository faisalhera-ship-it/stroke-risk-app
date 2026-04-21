import streamlit as st
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="SINTALA v3.6", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .wa-btn {
        display: block; width: 100%; padding: 12px; background-color: #25D366;
        color: white; text-align: center; font-weight: bold; border-radius: 10px;
        text-decoration: none; margin-top: 10px;
    }
    .skor-box { background: white; padding: 20px; border-radius: 15px; border: 2px solid #004a99; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER ---
def buat_wa(no, text):
    no = "".join(filter(str.isdigit, no))
    if no.startswith("0"): no = "62" + no[1:]
    return f"https://wa.me/{no}?text={urllib.parse.quote(text)}"

# --- LOGIN & MENU ---
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'pilihan' not in st.session_state: st.session_state.pilihan = None

if not st.session_state.dr:
    st.title("🩺 SINTALA-STROKE")
    nama = st.text_input("Nama Dokter (DPJP):")
    if st.button("Masuk"): 
        st.session_state.dr = nama
        st.rerun()
    st.stop()

with st.sidebar:
    st.write(f"DPJP: **{st.session_state.dr}**")
    if st.button("🏠 Menu Utama"): 
        st.session_state.pilihan = None
        st.rerun()

if st.session_state.pilihan is None:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚨 NIHSS (Stroke Scale)", use_container_width=True, height=150): st.session_state.pilihan = "NIHSS"; st.rerun()
    with c2:
        if st.button("🧠 SIRIRAJ (Diagnostik)", use_container_width=True, height=150): st.session_state.pilihan = "SIRIRAJ"; st.rerun()
    st.stop()

# --- MODUL NIHSS ---
if st.session_state.pilihan == "NIHSS":
    st.header("🚨 NIHSS Calculator")
    with st.form("nihss_form"):
        p_nama = st.text_input("Nama Pasien")
        p_no = st.text_input("No WA IGD / Pasien")
        col1, col2 = st.columns(2)
        with col1:
            loc = st.selectbox("1a. LOC (Kesadaran)", [0,1,2,3], help="0:Sadar, 1:Somnolen, 2:Stupor, 3:Koma")
            loc_q = st.selectbox("1b. LOC Tanya (Bulan/Usia)", [0,1,2])
            gaze = st.selectbox("2. Gaze (Mata)", [0,1,2])
            vis = st.selectbox("3. Visual", [0,1,2,3])
            face = st.selectbox("4. Facial Palsy", [0,1,2,3])
            arm_r = st.selectbox("5a. Motorik Lengan (Kanan)", [0,1,2,3,4])
        with col2:
            arm_l = st.selectbox("5b. Motorik Lengan (Kiri)", [0,1,2,3,4])
            leg_r = st.selectbox("6a. Motorik Tungkai (Kanan)", [0,1,2,3,4])
            leg_l = st.selectbox("6b. Motorik Tungkai (Kiri)", [0,1,2,3,4])
            ataxia = st.selectbox("7. Ataksia", [0,1,2])
            sensory = st.selectbox("8. Sensorik", [0,1,2])
            aphasia = st.selectbox("9. Bahasa (Afasia)", [0,1,2,3])
        
        subj = st.text_area("S: Keluhan & Onset")
        plan = st.text_area("P: Tindakan", "O2, IVFD RL...")
        hitung = st.form_submit_button("Hitung & Generate SOAP")

    if hitung:
        skor = sum([loc, loc_q, gaze, vis, face, arm_r, arm_l, leg_r, leg_l, ataxia, sensory, aphasia])
        kat = "Ringan" if skor <= 4 else "Sedang" if skor <= 15 else "Sedang-Berat" if skor <= 24 else "Berat"
        
        pesan = f"*RUJUKAN NIHSS*\nS: {subj}\nO: Skor NIHSS {skor} ({kat})\nA: Suspek Stroke\nP: {plan}"
        st.markdown(f"<div class='skor-box'><h2>Skor: {skor}</h2><h4>Kategori: {kat}</h4></div>", unsafe_allow_html=True)
        st.markdown(f'<a href="{buat_wa(p_no, pesan)}" target="_blank" class="wa-btn">🚨 KIRIM SOAP KE WA</a>', unsafe_allow_html=True)

# --- MODUL SIRIRAJ ---
elif st.session_state.pilihan == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score")
    with st.form("sss_form"):
        p_nama = st.text_input("Nama Pasien")
        p_no = st.text_input("No WA IGD")
        c1, c2 = st.columns(2)
        with c1:
            sadar = st.selectbox("Kesadaran", [0, 1, 2], format_func=lambda x: ["Sadar", "Mengantuk/Stupor", "Semi-koma/Koma"][x])
            muntah = st.selectbox("Muntah (2 Jam)", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
            nyeri = st.selectbox("Nyeri Kepala (2 Jam)", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        with c2:
            diastolik = st.number_input("TD Diastolik (mmHg)", 60, 150, 90)
            atheroma = st.selectbox("Atheroma (DM/PJK)", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        
        btn_sss = st.form_submit_button("Hitung Siriraj")

    if btn_sss:
        sss = (2.5 * sadar) + (2 * muntah) + (2 * nyeri) + (0.1 * diastolik) - (3 * atheroma) - 12
        interpretasi = "Stroke Hemoragik" if sss > 1 else "Stroke Iskemik" if sss < -1 else "Perlu CT-Scan"
        
        pesan_sss = f"*RUJUKAN SIRIRAJ*\nPasien: {p_nama}\nSkor: {sss:.1f}\nAss: {interpretasi}"
        st.markdown(f"<div class='skor-box'><h2>Skor: {sss:.1f}</h2><h4>Prediksi: {interpretasi}</h4></div>", unsafe_allow_html=True)
        st.markdown(f'<a href="{buat_wa(p_no, pesan_sss)}" target="_blank" class="wa-btn">🚨 KIRIM WA KE IGD</a>', unsafe_allow_html=True)

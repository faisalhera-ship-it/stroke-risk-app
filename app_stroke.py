import streamlit as st
import urllib.parse

# --- CONFIG & STYLES ---
st.set_page_config(page_title="SINTALA v5.3", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .wa-card { background: white; padding: 20px; border-radius: 15px; border-left: 10px solid #25D366; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; }
    .stSelectbox label { font-weight: bold; color: #004a99; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def kirim_wa(nomor, pesan):
    no = "".join(filter(str.isdigit, nomor))
    if no.startswith("0"): no = "62" + no[1:]
    return f"https://wa.me/{no}?text={urllib.parse.quote(pesan)}"

RS_LIST = {
    "RSUD H. Boejasin Pelaihari": "08123456789",
    "RS Ciputra Banjarmasin": "08110000000",
    "RSUD Ulin Banjarmasin": "08115555555"
}

# --- SESSION STATE ---
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'menu' not in st.session_state: st.session_state.menu = "Home"

# --- LOGIN ---
if not st.session_state.dr:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#004a99;'>🩺 SINTALA</h1>", unsafe_allow_html=True)
        dr_name = st.text_input("Nama Dokter Pemeriksa:")
        if st.button("Buka Dashboard", use_container_width=True):
            if dr_name: st.session_state.dr = dr_name; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.write(f"DPJP: **{st.session_state.dr}**")
    if st.button("🏠 Menu Utama"): st.session_state.menu = "Home"; st.rerun()

# --- MENU UTAMA ---
if st.session_state.menu == "Home":
    st.subheader("Instrumen Klinis Terintegrasi")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📊 FSRP\n(Skrining & Kolesterol)", use_container_width=True): st.session_state.menu = "FSRP"; st.rerun()
    with c2:
        if st.button("🚨 NIHSS\n(11 Parameter Deskriptif)", use_container_width=True): st.session_state.menu = "NIHSS"; st.rerun()
    with c3:
        if st.button("🧠 SIRIRAJ\n(Diagnostik Deskriptif)", use_container_width=True): st.session_state.menu = "SIRIRAJ"; st.rerun()

# --- MODUL NIHSS (11 PARAMETER DESKRIPTIF) ---
elif st.session_state.menu == "NIHSS":
    st.header("🚨 NIHSS Full Assessment")
    with st.form("nihss_detailed"):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            nama = st.text_input("Nama Pasien")
            umur = st.number_input("Umur", 0, 100, 50)
            rs_tuju = st.selectbox("Pilih RS Tujuan", list(RS_LIST.keys()))
        with c_p2:
            s_subj = st.text_area("S: Keluhan & Onset")
            s_obj_v = st.text_input("O: Vital Sign", "TD: / , N: , GCS: , RR: ")

        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            n1a = st.selectbox("1a. Tingkat Kesadaran (LOC)", [0,1,2,3], format_func=lambda x: {0:"0: Sadar Penuh", 1:"1: Mengantuk/Somnolen", 2:"2: Stupor (Butuh rangsang kuat)", 3:"3: Koma/Refleks Motorik Saja"}[x])
            n1b = st.selectbox("1b. LOC Tanya (Bulan & Umur)", [0,1,2], format_func=lambda x: {0:"0: Benar Keduanya", 1:"1: Benar Satu", 2:"2: Salah Keduanya"}[x])
            n1c = st.selectbox("1c. LOC Perintah (Genggam tangan)", [0,1,2], format_func=lambda x: {0:"0: Mampu Keduanya", 1:"1: Mampu Satu", 2:"2: Tidak Mampu"}[x])
            n2 = st.selectbox("2. Gerakan Mata (Gaze)", [0,1,2], format_func=lambda x: {0:"0: Normal", 1:"1: Paresis Gaze Parsial", 2:"2: Deviasi Konjugat Paksa"}[x])
            n3 = st.selectbox("3. Lapang Pandang (Visual)", [0,1,2,3], format_func=lambda x: {0:"0: Tidak Ada Gangguan", 1:"1: Hemianopsia Parsial", 2:"2: Hemianopsia Komplit", 3:"3: Hemianopsia Bilateral"}[x])
            n4 = st.selectbox("4. Kelumpuhan Wajah", [0,1,2,3], format_func=lambda x: {0:"0: Normal", 1:"1: Minor (Asimetris senyum)", 2:"2: Parsial (Total bawah)", 3:"3: Komplit (Atas & Bawah)"}[x])
            n5 = st.selectbox("5. Motorik Lengan (Kiri & Kanan)", [0,1,2,3,4], format_func=lambda x: {0:"0: No Drift (10 dtk)", 1:"1: Drift sebelum 10 dtk", 2:"2: Ada upaya melawan gravitasi", 3:"3: Tidak ada upaya gravitasi", 4:"4: Tidak ada gerakan"}[x])
        with col_b:
            n6 = st.selectbox("6. Motorik Tungkai (Kiri & Kanan)", [0,1,2,3,4], format_func=lambda x: {0:"0: No Drift (5 dtk)", 1:"1: Drift sebelum 5 dtk", 2:"2: Ada upaya melawan gravitasi", 3:"3: Tidak ada upaya gravitasi", 4:"4: Tidak ada gerakan"}[x])
            n7 = st.selectbox("7. Ataksia Anggota Gerak", [0,1,2], format_func=lambda x: {0:"0: Tidak Ada", 1:"1: Satu Anggota Gerak", 2:"2: Dua Anggota Gerak"}[x])
            n8 = st.selectbox("8. Sensorik", [0,1,2], format_func=lambda x: {0:"0: Normal", 1:"1: Defisit Ringan-Sedang", 2:"2: Defisit Berat/Anestesi"}[x])
            n9 = st.selectbox("9. Bahasa Terbaik", [0,1,2,3], format_func=lambda x: {0:"0: Normal", 1:"1: Afasia Ringan-Sedang", 2:"2: Afasia Berat", 3:"3: Mutisme/Global Afasia"}[x])
            n10 = st.selectbox("10. Disartria", [0,1,2,3], format_func=lambda x: {0:"0: Normal", 1:"1: Ringan-Sedang", 2:"2: Berat (Pelo berat)", 3:"3: Intubasi/Lainnya"}[x])
            n11 = st.selectbox("11. Pengabaian (Neglect)", [0,1,2], format_func=lambda x: {0:"0: Tidak Ada", 1:"1: Inatensi Parsial", 2:"2: Inatensi Komplit"}[x])
            s_plan = st.text_area("P: Plan & Terapi", "O2, IVFD, Aspilet 160mg, Clopidogrel 300mg...")

        if st.form_submit_button("Generate & Kirim Rujukan SOAP"):
            skor = sum([n1a,n1b,n1c,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11])
            kat = "Ringan" if skor <= 4 else "Sedang" if skor <= 15 else "Berat"
            msg = f"*RUJUKAN STROKE (SINTALA)*\nYth. IGD {rs_tuju}\n\n*DATA PASIEN:* {nama} ({umur} th)\n*S:* {s_subj}\n*O:* {s_obj_v}, NIHSS: {skor} ({kat})\n*A:* Suspek Stroke Akut\n*P:* {s_plan}\n\nDPJP: {st.session_state.dr}"
            st.markdown(f'<a href="{kirim_wa(RS_LIST[rs_tuju], msg)}" target="_blank" class="wa-card">🚑 KIRIM DATA SOAP KE IGD</a>', unsafe_allow_html=True)

# --- MODUL SIRIRAJ (DESKRIPTIF) ---
elif st.session_state.menu == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score")
    with st.form("sss_detailed"):
        p_nama = st.text_input("Nama Pasien")
        rs_tuju = st.selectbox("RS Tujuan", list(RS_LIST.keys()))
        c1, c2 = st.columns(2)
        with c1:
            sadar = st.selectbox("Kesadaran", [0,1,2], format_func=lambda x: {0:"0: Sadar Penuh", 1:"1: Mengantuk/Stupor", 2:"2: Koma"}[x])
            muntah = st.selectbox("Muntah (2 jam terakhir)", [0,1], format_func=lambda x: {0:"0: Tidak Ada", 1:"1: Ada"}[x])
            nyeri = st.selectbox("Nyeri Kepala (2 jam terakhir)", [0,1], format_func=lambda x: {0:"0: Tidak Ada", 1:"1: Ada"}[x])
        with c2:
            diastolik = st.number_input("TD Diastolik (mmHg)", 60, 150, 90)
            atheroma = st.selectbox("Tanda Atheroma (DM/PJK)", [0,1], format_func=lambda x: {0:"0: Tidak Ada", 1:"1: Ada (DM/PJK/Klaudikasio)"}[x])
            s_plan_s = st.text_area("Plan", "Stabilisasi TD, Evaluasi CT-Scan")

        if st.form_submit_button("Hitung & Kirim SOAP"):
            sss = (2.5*sadar) + (2*muntah) + (2*nyeri) + (0.1*diastolik) - (3*atheroma) - 12
            diag = "Hemoragik" if sss > 1 else "Iskemik" if sss < -1 else "Perlu CT-Scan"
            msg = f"*RUJUKAN SIRIRAJ (SINTALA)*\nIGD {rs_tuju}\n\nPasien: {p_nama}\nO: TD Diastolik {diastolik}, SSS: {sss:.1f}\nA: Prediksi {diag}\nP: {s_plan_s}\n\nDPJP: {st.session_state.dr}"
            st.success(f"Skor SSS: {sss:.1f} ({diag})")
            st.markdown(f'<a href="{kirim_wa(RS_LIST[rs_tuju], msg)}" target="_blank" class="wa-card">🚑 KIRIM DATA KE IGD</a>', unsafe_allow_html=True)

# --- MODUL FSRP (EDUKASI) ---
elif st.session_state.menu == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile")
    with st.form("fsrp_final"):
        p_nama = st.text_input("Nama Pasien")
        p_wa = st.text_input("No WA Pasien")
        c1, c2 = st.columns(2)
        with c1:
            u = st.number_input("Umur", 30, 90, 50)
            tds = st.number_input("TD Sistolik", 90, 220, 120)
            chol = st.number_input("Total Kolesterol", 100, 500, 200)
        with c2:
            dm = st.selectbox("Diabetes", [0,1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            smoke = st.selectbox("Merokok", [0,1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        
        if st.form_submit_button("Kirim Edukasi"):
            res = "Perlu Perhatian Khusus" if tds > 140 or chol > 200 else "Risiko Terkontrol"
            edukasi = f"Halo Bapak/Ibu {p_nama}, Hasil skrining FSRP Anda: {res}. Mohon jaga pola makan dan kontrol TD rutin."
            st.markdown(f'<a href="{kirim_wa(p_wa, edukasi)}" target="_blank" class="wa-card">📲 KIRIM EDUKASI</a>', unsafe_allow_html=True)

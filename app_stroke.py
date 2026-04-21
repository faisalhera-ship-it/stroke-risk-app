import streamlit as st
import urllib.parse

# --- CONFIG & STYLES ---
st.set_page_config(page_title="SINTALA v5.2", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .wa-card { background: white; padding: 20px; border-radius: 15px; border-left: 10px solid #25D366; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def kirim_wa(nomor, pesan):
    no = "".join(filter(str.isdigit, nomor))
    if no.startswith("0"): no = "62" + no[1:]
    return f"https://wa.me/{no}?text={urllib.parse.quote(pesan)}"

# Database RS Rujukan (Bisa Dokter sesuaikan nomornya)
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
    st.subheader("Instrumen Klinis Digital")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📊 FSRP\n(Skrining + Kolesterol)", use_container_width=True): st.session_state.menu = "FSRP"; st.rerun()
    with c2:
        if st.button("🚨 NIHSS\n(SOAP Rujukan IGD)", use_container_width=True): st.session_state.menu = "NIHSS"; st.rerun()
    with c3:
        if st.button("🧠 SIRIRAJ\n(SOAP Rujukan IGD)", use_container_width=True): st.session_state.menu = "SIRIRAJ"; st.rerun()

# --- MODUL FSRP (DENGAN KOLESTEROL) ---
elif st.session_state.menu == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile (Full)")
    with st.form("fsrp_full"):
        p_nama = st.text_input("Nama Pasien")
        p_wa = st.text_input("No WA Pasien (Untuk Edukasi)")
        
        col1, col2 = st.columns(2)
        with col1:
            u = st.number_input("Umur (30-90 th)", 30, 90, 50)
            tds = st.number_input("TD Sistolik (mmHg)", 90, 220, 120)
            chol = st.number_input("Total Kolesterol (mg/dL)", 100, 500, 200)
            h_td = st.selectbox("Terapi Hipertensi?", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        with col2:
            dm = st.selectbox("Diabetes?", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            smoke = st.selectbox("Merokok?", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            af = st.selectbox("Atrial Fibrilasi?", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
            lvh = st.selectbox("LV Hypertrophy (EKG)?", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")

        if st.form_submit_button("Analisis Risiko & Kirim Edukasi"):
            # Logika evaluasi risiko sederhana untuk pesan WA
            risiko_level = "Tinggi" if tds > 160 or chol > 240 or dm == 1 else "Sedang" if tds > 140 or chol > 200 else "Rendah"
            
            edukasi = f"""*HASIL SKRINING RISIKO STROKE (FSRP)*

Halo Bapak/Ibu *{p_nama}*, berikut hasil pemeriksaan Anda:
- TD Sistolik: {tds} mmHg
- Total Kolesterol: {chol} mg/dL
- Status Risiko: *{risiko_level}*

*EDUKASI SEDERHANA:*
1. Kontrol rutin TD & Kolesterol Anda.
2. Kurangi makanan berlemak dan bersantan.
3. Aktivitas fisik minimal 30 menit sehari.
4. Segera ke RS jika ada kelemahan sisi tubuh secara mendadak.

Salam sehat,
*{st.session_state.dr}*"""
            
            st.success(f"Analisis Selesai: Risiko {risiko_level}")
            st.markdown(f'<a href="{kirim_wa(p_wa, edukasi)}" target="_blank" class="wa-card">📲 Kirim Edukasi & Hasil ke Pasien</a>', unsafe_allow_html=True)

# --- MODUL NIHSS (11 PARAMETER LENGKAP) ---
elif st.session_state.menu == "NIHSS":
    st.header("🚨 NIHSS Full Assessment (Rujukan SOAP)")
    with st.form("nihss_full"):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            nama = st.text_input("Nama Pasien")
            umur = st.number_input("Umur", 0, 100, 50)
            rs_tuju = st.selectbox("Pilih RS Tujuan IGD", list(RS_LIST.keys()))
        with c_p2:
            s_subj = st.text_area("S: Keluhan & Onset", placeholder="Onset, Riwayat Penyakit...")
            s_obj_v = st.text_input("O: TD, Nadi, GCS, RR", "TD: / , N: , GCS: , RR: ")
            s_obj_n = st.text_input("O: Status Neurologis", "Lateralisasi (+/-), Hemiparese...")

        st.divider()
        st.subheader("11 Parameter NIHSS")
        col_a, col_b = st.columns(2)
        with col_a:
            n1a = st.selectbox("1a. LOC", [0,1,2,3])
            n1b = st.selectbox("1b. LOC Tanya", [0,1,2])
            n1c = st.selectbox("1c. LOC Perintah", [0,1,2])
            n2 = st.selectbox("2. Gaze", [0,1,2])
            n3 = st.selectbox("3. Visual", [0,1,2,3])
            n4 = st.selectbox("4. Facial Palsy", [0,1,2,3])
            n5a = st.selectbox("5a. Motorik Lengan (Kiri)", [0,1,2,3,4])
            n5b = st.selectbox("5b. Motorik Lengan (Kanan)", [0,1,2,3,4])
        with col_b:
            n6a = st.selectbox("6a. Motorik Tungkai (Kiri)", [0,1,2,3,4])
            n6b = st.selectbox("6b. Motorik Tungkai (Kanan)", [0,1,2,3,4])
            n7 = st.selectbox("7. Ataksia", [0,1,2])
            n8 = st.selectbox("8. Sensorik", [0,1,2])
            n9 = st.selectbox("9. Bahasa", [0,1,2,3])
            n10 = st.selectbox("10. Disartria", [0,1,2])
            n11 = st.selectbox("11. Neglect", [0,1,2])
            s_plan = st.text_area("P: Tindakan/Plan", "Infus, O2, Loading obat...")

        if st.form_submit_button("Generate & Kirim Rujukan SOAP"):
            skor_n = sum([n1a,n1b,n1c,n2,n3,n4,n5a,n5b,n6a,n6b,n7,n8,n9,n10,n11])
            msg = f"""*RUJUKAN NIHSS (SINTALA)*
Yth. Sejawat IGD {rs_tuju}

*DATA PASIEN:* {nama} ({umur} th)
*S:* {s_subj}
*O:* {s_obj_v}
Neuro: {s_obj_n}, NIHSS Skor: {skor_n}
*A:* Suspek Stroke Akut
*P:* {s_plan}

DPJP: {st.session_state.dr}"""
            st.markdown(f'<a href="{kirim_wa(RS_LIST[rs_tuju], msg)}" target="_blank" class="wa-card">🚑 KIRIM DATA SOAP KE IGD</a>', unsafe_allow_html=True)

# --- MODUL SIRIRAJ ---
elif st.session_state.menu == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score (Full)")
    with st.form("sss_form"):
        p_nama = st.text_input("Nama Pasien")
        rs_tuju = st.selectbox("Pilih RS Tujuan", list(RS_LIST.keys()))
        c1, c2 = st.columns(2)
        with c1:
            sadar = st.selectbox("Kesadaran", [0, 1, 2])
            muntah = st.selectbox("Muntah", [0, 1])
            nyeri = st.selectbox("Nyeri Kepala", [0, 1])
        with c2:
            diastolik = st.number_input("TD Diastolik", 60, 150, 90)
            atheroma = st.selectbox("Atheroma (DM/PJK)", [0, 1])
            s_plan_s = st.text_area("Plan", "Stabilisasi...")

        if st.form_submit_button("Kirim SOAP Siriraj"):
            sss = (2.5 * sadar) + (2 * muntah) + (2 * nyeri) + (0.1 * diastolik) - (3 * atheroma) - 12
            diag = "Hemoragik" if sss > 1 else "Iskemik" if sss < -1 else "Perlu CT-Scan"
            
            msg = f"""*RUJUKAN SIRIRAJ (SINTALA)*
Pasien: {p_nama}
Skor SSS: {sss:.1f}
Prediksi: {diag}
Plan: {s_plan_s}
DPJP: {st.session_state.dr}"""
            st.markdown(f'<a href="{kirim_wa(RS_LIST[rs_tuju], msg)}" target="_blank" class="wa-card">🚑 KIRIM DATA KE IGD</a>', unsafe_allow_html=True)

import streamlit as st
import urllib.parse
from datetime import datetime

# --- CONFIG & STYLES ---
st.set_page_config(page_title="SINTALA v5.4", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .wa-card { background: white; padding: 20px; border-radius: 15px; border-left: 10px solid #25D366; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;}
    .print-container { 
        background: white; padding: 40px; border: 2px solid #333; border-radius: 5px; 
        color: black; font-family: 'Courier New', Courier, monospace; line-height: 1.2;
    }
    .stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; }
    
    @media print {
        .no-print, .stSidebar, header, footer, .stButton, .wa-card { display: none !important; }
        .print-container { border: none !important; padding: 0 !important; width: 100% !important; }
    }
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
        if st.button("Masuk Dashboard", use_container_width=True):
            if dr_name: st.session_state.dr = dr_name; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.write(f"DPJP: **{st.session_state.dr}**")
    if st.button("🏠 Menu Utama"): st.session_state.menu = "Home"; st.rerun()
    st.divider()
    st.info("Tips: Setelah laporan muncul, tekan Ctrl+P untuk cetak.")

# --- MENU UTAMA ---
if st.session_state.menu == "Home":
    st.subheader("Instrumen Klinis Digital")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📊 FSRP\n(Skrining & Edukasi)", use_container_width=True): st.session_state.menu = "FSRP"; st.rerun()
    with c2:
        if st.button("🚨 NIHSS\n(Full SOAP & Print)", use_container_width=True): st.session_state.menu = "NIHSS"; st.rerun()
    with c3:
        if st.button("🧠 SIRIRAJ\n(Full SOAP & Print)", use_container_width=True): st.session_state.menu = "SIRIRAJ"; st.rerun()

# --- MODUL NIHSS (DESKRIPTIF + PRINT) ---
elif st.session_state.menu == "NIHSS":
    st.header("🚨 NIHSS Assessment & Referral")
    with st.form("nihss_detailed"):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            nama = st.text_input("Nama Pasien")
            umur = st.number_input("Umur", 0, 100, 50)
            rs_tuju = st.selectbox("RS Tujuan", list(RS_LIST.keys()))
        with c_p2:
            s_subj = st.text_area("S: Subjective (Keluhan/Onset)")
            s_obj_v = st.text_input("O: Vital Sign", "TD: 150/90, N: 88, GCS: 15, RR: 20")

        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            n1a = st.selectbox("1a. LOC", [0,1,2,3], format_func=lambda x: {0:"0: Sadar", 1:"1: Somnolen", 2:"2: Stupor", 3:"3: Koma"}[x])
            n1b = st.selectbox("1b. LOC Tanya", [0,1,2], format_func=lambda x: {0:"0: Benar 2", 1:"1: Benar 1", 2:"2: Salah semua"}[x])
            n1c = st.selectbox("1c. LOC Perintah", [0,1,2])
            n2 = st.selectbox("2. Gaze", [0,1,2])
            n3 = st.selectbox("3. Visual", [0,1,2,3])
            n4 = st.selectbox("4. Facial Palsy", [0,1,2,3])
            n5 = st.selectbox("5. Motor Lengan", [0,1,2,3,4])
        with col_b:
            n6 = st.selectbox("6. Motor Tungkai", [0,1,2,3,4])
            n7 = st.selectbox("7. Ataksia", [0,1,2])
            n8 = st.selectbox("8. Sensorik", [0,1,2])
            n9 = st.selectbox("9. Bahasa", [0,1,2,3])
            n10 = st.selectbox("10. Disartria", [0,1,2])
            n11 = st.selectbox("11. Neglect", [0,1,2])
            s_plan = st.text_area("P: Plan", "Loading Aspilet, Stabilisasi")

        submit = st.form_submit_button("Generate Laporan & Kirim WA")

    if submit:
        total = sum([n1a,n1b,n1c,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11])
        kat = "Ringan" if total <= 4 else "Sedang" if total <= 15 else "Berat"
        
        # Pesan WA
        msg = f"*RUJUKAN NIHSS*\nPasien: {nama} ({umur} th)\nS: {s_subj}\nO: {s_obj_v}, Skor NIHSS: {total}\nA: Suspek Stroke\nP: {s_plan}"
        st.markdown(f'<a href="{kirim_wa(RS_LIST[rs_tuju], msg)}" target="_blank" class="wa-card">📲 KIRIM DATA SOAP KE IGD</a>', unsafe_allow_html=True)
        
        # Preview Cetak
        st.subheader("📄 Preview Laporan (Siap Print)")
        st.markdown(f"""
        <div class="print-container">
            <h2 style="text-align:center;">LAPORAN PEMERIKSAAN STROKE (SINTALA)</h2>
            <hr>
            <p><b>Tanggal:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')} | <b>Pemeriksa:</b> {st.session_state.dr}</p>
            <p><b>Nama Pasien:</b> {nama} ({umur} th)</p>
            <hr>
            <p><b>[S] SUBJECTIVE:</b><br>{s_subj}</p>
            <p><b>[O] OBJECTIVE:</b><br>{s_obj_v}</p>
            <p><b>SKOR NIHSS: {total} (Kategori: {kat})</b></p>
            <p><b>[A] ASSESSMENT:</b> Suspek Stroke Akut</p>
            <p><b>[P] PLAN:</b><br>{s_plan}</p>
            <br><br><br>
            <p style="text-align:right;">( {st.session_state.dr} )</p>
        </div>
        """, unsafe_allow_html=True)

# --- MODUL SIRIRAJ (DESKRIPTIF + PRINT) ---
elif st.session_state.menu == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score Analysis")
    with st.form("sss_form"):
        p_nama = st.text_input("Nama Pasien")
        p_umur = st.number_input("Umur", 0, 100, 50)
        rs_tuju = st.selectbox("RS Tujuan", list(RS_LIST.keys()))
        c1, c2 = st.columns(2)
        with c1:
            sadar = st.selectbox("Kesadaran", [0,1,2], format_func=lambda x: {0:"0: Sadar", 1:"1: Stupor", 2:"2: Koma"}[x])
            muntah = st.selectbox("Muntah", [0,1], format_func=lambda x: {0:"0: Tidak", 1:"1: Ya"}[x])
            nyeri = st.selectbox("Nyeri Kepala", [0,1], format_func=lambda x: {0:"0: Tidak", 1:"1: Ya"}[x])
        with c2:
            diastolik = st.number_input("TD Diastolik", 60, 150, 90)
            atheroma = st.selectbox("Atheroma", [0,1], format_func=lambda x: {0:"0: Tidak", 1:"1: Ada (DM/PJK)"}[x])
            s_plan_s = st.text_area("Plan", "Evaluasi CT Scan")

        if st.form_submit_button("Generate & Kirim"):
            sss = (2.5*sadar) + (2*muntah) + (2*nyeri) + (0.1*diastolik) - (3*atheroma) - 12
            diag = "Hemoragik" if sss > 1 else "Iskemik" if sss < -1 else "Perlu CT-Scan"
            
            msg = f"*RUJUKAN SIRIRAJ*\nPasien: {p_nama}\nSSS: {sss:.1f}\nPrediksi: {diag}"
            st.markdown(f'<a href="{kirim_wa(RS_LIST[rs_tuju], msg)}" target="_blank" class="wa-card">📲 KIRIM DATA KE IGD</a>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="print-container">
                <h2 style="text-align:center;">HASIL SKORING SIRIRAJ</h2>
                <hr>
                <p><b>Pasien:</b> {p_nama} ({p_umur} th) | <b>Tgl:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
                <p><b>Hasil Skor:</b> {sss:.1f}</p>
                <p><b>Interpretasi:</b> Prediksi Stroke {diag}</p>
                <p><b>Plan:</b> {s_plan_s}</p>
                <br><br>
                <p style="text-align:right;">Pemeriksa: {st.session_state.dr}</p>
            </div>
            """, unsafe_allow_html=True)

# --- MODUL FSRP ---
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

import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. SETUP UI & CSS ---
st.set_page_config(page_title="SINTALA v5.7", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    div.stButton > button {
        height: 70px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        margin-bottom: 10px;
    }
    
    .print-report {
        background-color: white; padding: 40px; border: 2px solid #333;
        border-radius: 8px; color: black; line-height: 1.5; margin-top: 20px;
    }
    .kop-surat { text-align: center; border-bottom: 4px double #333; margin-bottom: 20px; }
    
    @media print {
        .no-print, header, footer, [data-testid="stSidebar"], .stButton, [data-testid="stHeader"] {
            display: none !important;
        }
        .print-report { border: none !important; padding: 0 !important; width: 100% !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'menu' not in st.session_state: st.session_state.menu = "Home"

# --- 3. LOGIN ---
if not st.session_state.dr:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#004a99;'>🩺 SINTALA</h1>", unsafe_allow_html=True)
        dr_input = st.text_input("Nama Dokter Pemeriksa:")
        if st.button("Masuk Dashboard", use_container_width=True):
            if dr_input:
                st.session_state.dr = dr_input
                st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.write(f"DPJP: **{st.session_state.dr}**")
    if st.button("🏠 Menu Utama", use_container_width=True): 
        st.session_state.menu = "Home"
        st.rerun()
    st.info("Gunakan Ctrl+P untuk print laporan ke PDF/Kertas.")

# --- 5. MENU UTAMA ---
if st.session_state.menu == "Home":
    st.subheader("Instrumen Klinis Stroke")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📊 FSRP\n(Skrining & CVD)", use_container_width=True): st.session_state.menu = "FSRP"; st.rerun()
    with c2:
        if st.button("🚨 NIHSS\n(Emergency)", use_container_width=True): st.session_state.menu = "NIHSS"; st.rerun()
    with c3:
        if st.button("🧠 SIRIRAJ\n(Diagnostik)", use_container_width=True): st.session_state.menu = "SIRIRAJ"; st.rerun()

# --- 6. MODUL FSRP (UPDATED: JANTUNG & PRINT) ---
elif st.session_state.menu == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile (FSRP)")
    with st.form("form_fsrp"):
        p_nama = st.text_input("Nama Pasien")
        p_umur = st.number_input("Umur (30-90 th)", 30, 90, 50)
        c1, c2 = st.columns(2)
        with c1:
            tds = st.number_input("TD Sistolik (mmHg)", 90, 220, 120)
            chol = st.number_input("Total Kolesterol (mg/dL)", 100, 500, 200)
            dm = st.selectbox("Diabetes Mellitus", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        with c2:
            smoke = st.selectbox("Merokok", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
            cvd = st.selectbox("Penyakit Jantung (CVD/PJK/AF)", [0, 1], 
                                format_func=lambda x: "Tidak Ada" if x==0 else "Ada (Riwayat PJK/Gagal Jantung/AF)")
            lvh = st.selectbox("LVH (Hasil EKG)", [0, 1], format_func=lambda x: "Tidak Ada" if x==0 else "Ada")
        
        submit_fsrp = st.form_submit_button("Analisis Risiko & Generate Laporan")

    if submit_fsrp:
        # Logika Prediksi Sederhana untuk Resume
        risiko = "Tinggi" if tds > 160 or dm == 1 or cvd == 1 else "Sedang" if tds > 140 or chol > 240 else "Rendah"
        tgl_skrg = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Preview Laporan Siap Cetak
        st.markdown(f"""
            <div class="print-report">
                <div class="kop-surat">
                    <h2 style="margin:0;">HASIL SKRINING RISIKO STROKE (FSRP)</h2>
                    <p style="margin:0;">Pemeriksa: {st.session_state.dr} | Waktu: {tgl_skrg}</p>
                </div>
                <p><b>DATA PASIEN:</b> {p_nama} ({p_umur} th)</p>
                <hr>
                <table style="width:100%; border-collapse: collapse;">
                    <tr><td style="padding:5px;">TD Sistolik</td><td>: {tds} mmHg</td></tr>
                    <tr><td style="padding:5px;">Total Kolesterol</td><td>: {chol} mg/dL</td></tr>
                    <tr><td style="padding:5px;">Diabetes Mellitus</td><td>: {"Ya" if dm==1 else "Tidak"}</td></tr>
                    <tr><td style="padding:5px;">Riwayat Penyakit Jantung</td><td>: {"Ada" if cvd==1 else "Tidak Ada"}</td></tr>
                    <tr><td style="padding:5px;">Status Merokok</td><td>: {"Ya" if smoke==1 else "Tidak"}</td></tr>
                    <tr><td style="padding:5px;">LVH (EKG)</td><td>: {"Positif" if lvh==1 else "Negatif"}</td></tr>
                </table>
                <hr>
                <h3 style="color: #d9534f;">KESIMPULAN: RISIKO {risiko.upper()}</h3>
                <p><i>Catatan: Hasil ini merupakan instrumen skrining awal. Segera konsultasikan lebih lanjut untuk manajemen faktor risiko.</i></p>
                <br><br>
                <p style="text-align:right;">Pemeriksa,<br><br><br><b>( {st.session_state.dr} )</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        # Tombol WA Edukasi (Hanya muncul di web, tidak di print)
        msg_wa = f"Hasil Skrining FSRP - Pasien: {p_nama}. Risiko Stroke: {risiko}. Mohon jaga pola makan dan kontrol rutin."
        url_wa = "https://wa.me/?text=" + urllib.parse.quote(msg_wa)
        st.markdown(f'<div class="no-print"><a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 KIRIM EDUKASI KE PASIEN (WA)</div></a></div>', unsafe_allow_html=True)

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

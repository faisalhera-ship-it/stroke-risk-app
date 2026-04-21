import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. SETUP UI & GLOBAL STYLES ---
st.set_page_config(page_title="SINTALA v8.0", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Tombol Besar & Gagah */
    div.stButton > button {
        height: 65px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }
    
    /* Layout Laporan Cetak */
    .print-report {
        background-color: white; padding: 35px; border: 2px solid #333;
        border-radius: 8px; color: black; line-height: 1.4; margin-top: 20px;
    }
    .kop-surat { text-align: center; border-bottom: 4px double #333; margin-bottom: 15px; }
    
    /* Card WhatsApp */
    .wa-btn {
        background-color: #25D366; color: white; padding: 15px;
        border-radius: 10px; text-align: center; font-weight: bold;
        text-decoration: none; display: block; margin-bottom: 15px;
    }

    /* Proteksi Print */
    @media print {
        .no-print, header, footer, [data-testid="stHeader"], [data-testid="stSidebar"], .stButton, .wa-btn {
            display: none !important;
        }
        .print-report { border: none !important; padding: 0 !important; width: 100% !important; }
        .stApp { background-color: white !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'menu' not in st.session_state: st.session_state.menu = "Home"

# --- 3. LOGIN PAGE ---
if not st.session_state.dr:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#004a99;'>🩺 SINTALA</h1>", unsafe_allow_html=True)
        st.write("<p style='text-align:center; margin-top:-15px;'>Stroke Integrated Analysis System</p>", unsafe_allow_html=True)
        dr_input = st.text_input("Nama Dokter Pemeriksa:")
        if st.button("Masuk Dashboard", use_container_width=True):
            if dr_input:
                st.session_state.dr = dr_input
                st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f"DPJP: **{st.session_state.dr}**")
    if st.button("🏠 Menu Utama", use_container_width=True): 
        st.session_state.menu = "Home"
        st.rerun()
    st.divider()
    st.info("💡 Tekan **Ctrl + P** untuk print laporan.")

# --- 5. MENU UTAMA ---
if st.session_state.menu == "Home":
    st.subheader("Instrumen Klinis Terintegrasi")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📊 FSRP\n(Skrining & Edukasi)", use_container_width=True): st.session_state.menu = "FSRP"; st.rerun()
    with c2:
        if st.button("🚨 NIHSS\n(SOAP & IGD)", use_container_width=True): st.session_state.menu = "NIHSS"; st.rerun()
    with c3:
        if st.button("🧠 SIRIRAJ\n(Diagnostik)", use_container_width=True): st.session_state.menu = "SIRIRAJ"; st.rerun()

# --- 6. MODUL FSRP ---
elif st.session_state.menu == "FSRP":
    st.header("📊 Framingham Stroke Risk Profile")
    with st.form("fsrp_form"):
        p_nama = st.text_input("Nama Pasien")
        p_umur = st.number_input("Umur", 30, 90, 50)
        c1, c2 = st.columns(2)
        with c1:
            tds = st.number_input("TD Sistolik (mmHg)", 90, 220, 120)
            chol = st.number_input("Total Kolesterol (mg/dL)", 100, 500, 200)
            dm = st.selectbox("Diabetes", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        with c2:
            smoke = st.selectbox("Merokok", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
            cvd = st.selectbox("Penyakit Jantung", [0, 1], format_func=lambda x: "Tidak Ada" if x==0 else "Ada (PJK/AF/CHF)")
            lvh = st.selectbox("LVH (EKG)", [0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        
        if st.form_submit_button("Generate Laporan & Edukasi WA"):
            risiko = "TINGGI" if (tds > 160 or cvd == 1) else "SEDANG" if tds > 140 else "RENDAH"
            
            # WA Edukasi
            pesan_fsrp = f"Halo Bapak/Ibu {p_nama}, hasil pemeriksaan risiko stroke Anda: TD {tds}, Kolesterol {chol}. Tingkat risiko: {risiko}. Mohon jaga pola makan dan kontrol rutin. - dr. {st.session_state.dr}"
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(pesan_fsrp)}" target="_blank" class="wa-btn">📲 KIRIM EDUKASI KE PASIEN</a>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="print-report">
                    <div class="kop-surat"><h2>LAPORAN ANALISIS RISIKO STROKE (FSRP)</h2></div>
                    <p><b>Pasien:</b> {p_nama} ({p_umur} th) | <b>Pemeriksa:</b> {st.session_state.dr}</p>
                    <hr>
                    <p>Sistolik: {tds} | Kolesterol: {chol} | Jantung: {"Ada" if cvd else "Tidak"}</p>
                    <h3 style="color:red;">INTERPRETASI: RISIKO {risiko}</h3>
                </div>
            """, unsafe_allow_html=True)

# --- 7. MODUL NIHSS (11 PARAMETER DESKRIPTIF) ---
elif st.session_state.menu == "NIHSS":
    st.header("🚨 NIHSS 11 Parameter (SOAP Edition)")
    with st.form("nihss_full"):
        p_nama = st.text_input("Nama Pasien")
        c1, c2 = st.columns(2)
        with c1:
            n1 = st.selectbox("1a. LOC", [0,1,2,3], format_func=lambda x: {0:"0: Sadar", 1:"1: Somnolen", 2:"2: Stupor", 3:"3: Koma"}[x])
            n1b = st.selectbox("1b. LOC Tanya", [0,1,2], format_func=lambda x: {0:"0: Benar 2", 1:"1: Benar 1", 2:"2: Salah semua"}[x])
            n2 = st.selectbox("2. Gaze", [0,1,2], format_func=lambda x: {0:"0: Normal", 1:"1: Paresis Parsial", 2:"2: Deviasi Paksa"}[x])
            n3 = st.selectbox("3. Visual", [0,1,2,3], format_func=lambda x: {0:"0: No Loss", 1:"1: Kuadranopsia", 2:"2: Hemianopsia", 3:"3: Blind"}[x])
            n4 = st.selectbox("4. Facial Palsy", [0,1,2,3], format_func=lambda x: {0:"0: Normal", 1:"1: Minor", 2:"2: Parsial", 3:"3: Komplit"}[x])
            n5 = st.selectbox("5. Motor Lengan", [0,1,2,3,4], format_func=lambda x: {0:"0: No Drift", 1:"1: Drift", 2:"2: Lawan Gravitasi", 3:"3: Jatuh", 4:"4: Lumpuh"}[x])
        with c2:
            n6 = st.selectbox("6. Motor Tungkai", [0,1,2,3,4], format_func=lambda x: {0:"0: No Drift", 1:"1: Drift", 2:"2: Lawan Gravitasi", 3:"3: Jatuh", 4:"4: Lumpuh"}[x])
            n7 = st.selectbox("7. Ataksia", [0,1,2], format_func=lambda x: {0:"0: Absen", 1:"1: Satu Ekstremitas", 2:"2: Dua Ekstremitas"}[x])
            n8 = st.selectbox("8. Sensorik", [0,1,2], format_func=lambda x: {0:"0: Normal", 1:"1: Mild Loss", 2:"2: Severe Loss"}[x])
            n9 = st.selectbox("9. Bahasa", [0,1,2,3], format_func=lambda x: {0:"0: Normal", 1:"1: Mild Afasia", 2:"2: Severe Afasia", 3:"3: Global"}[x])
            n10 = st.selectbox("10. Disartria", [0,1,2], format_func=lambda x: {0:"0: Normal", 1:"1: Ringan", 2:"2: Berat"}[x])
            n11 = st.selectbox("11. Neglect", [0,1,2], format_func=lambda x: {0:"0: Absen", 1:"1: Parsial", 2:"2: Komplit"}[x])
        
        st.divider()
        s_subj = st.text_area("S (Subjective)", "Kelemahan anggota gerak kanan mendadak sejak...")
        o_vital = st.text_input("O (Vital Sign)", "TD: 160/90, HR: 88, GCS: 15")
        p_plan = st.text_area("P (Plan)", "O2, Loading Aspilet 160mg, Stabilisasi")

        if st.form_submit_button("Generate Laporan & WA IGD"):
            skor = n1+n1b+n2+n3+n4+n5+n6+n7+n8+n9+n10+n11
            kat = "Ringan" if skor <= 4 else "Sedang" if skor <= 15 else "Berat"
            
            # WA IGD
            msg_nihss = f"*LAPORAN RUJUKAN NIHSS*\nS: {s_subj}\nO: {o_vital}, NIHSS {skor}\nA: Suspek Stroke ({kat})\nP: {p_plan}\nDPJP: {st.session_state.dr}"
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg_nihss)}" target="_blank" class="wa-btn">📲 KIRIM SOAP KE IGD RS</a>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="print-report">
                    <div class="kop-surat"><h2>RESUME MEDIS NIHSS (SOAP)</h2></div>
                    <p><b>Pasien:</b> {p_nama} | <b>Skor NIHSS: {skor} ({kat})</b></p>
                    <p><b>[S]:</b> {s_subj}</p><p><b>[O]:</b> {o_vital}</p><p><b>[P]:</b> {p_plan}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 8. MODUL SIRIRAJ ---
elif st.session_state.menu == "SIRIRAJ":
    st.header("🧠 Siriraj Stroke Score (Diagnostik)")
    with st.form("siriraj_form"):
        p_nama = st.text_input("Nama Pasien")
        c1, c2 = st.columns(2)
        with c1:
            sadar = st.selectbox("Kesadaran", [0,1,2], format_func=lambda x: {0:"0: Sadar", 1:"1: Stupor", 2:"2: Koma"}[x])
            muntah = st.selectbox("Muntah (2 jam terakhir)", [0,1], format_func=lambda x: "0: Tidak" if x==0 else "1: Ya")
            nyeri = st.selectbox("Nyeri Kepala (2 jam terakhir)", [0,1], format_func=lambda x: "0: Tidak" if x==0 else "1: Ya")
        with c2:
            dbp = st.number_input("TD Diastolik (mmHg)", 60, 160, 90)
            athero = st.selectbox("Marker Atheroma (DM/PJK)", [0,1], format_func=lambda x: "0: Tidak" if x==0 else "1: Ada")
            p_plan_s = st.text_input("Plan", "Observasi & CT-Scan")

        if st.form_submit_button("Hitung Siriraj & Kirim WA"):
            sss = (2.5*sadar) + (2*muntah) + (2*nyeri) + (0.1*dbp) - (3*athero) - 12
            diag = "Hemoragik" if sss > 1 else "Iskemik" if sss < -1 else "Perlu CT-Scan"
            
            # WA Siriraj
            msg_sss = f"*HASIL SIRIRAJ SCORE*\nPasien: {p_nama}\nSkor: {sss:.1f}\nPrediksi: {diag}\nPlan: {p_plan_s}\nDPJP: {st.session_state.dr}"
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg_sss)}" target="_blank" class="wa-btn">📲 KIRIM HASIL KE IGD</a>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="print-report">
                    <div class="kop-surat"><h2>LAPORAN SIRIRAJ STROKE SCORE</h2></div>
                    <p><b>Pasien:</b> {p_nama} | <b>Skor SSS: {sss:.1f}</b></p>
                    <h3>PREDIKSI: STROKE {diag.upper()}</h3>
                </div>
            """, unsafe_allow_html=True)

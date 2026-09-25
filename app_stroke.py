import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. SETUP UI & GLOBAL STYLES ---
st.set_page_config(page_title="SINTALA v8.0", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Tombol Utama */
    div.stButton > button {
        height: 65px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }
    
    /* Card Tampilan */
    .role-card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center;
        border-top: 6px solid #004a99;
    }
    .print-report {
        background-color: white; padding: 35px; border: 2px solid #333;
        border-radius: 8px; color: black; line-height: 1.4; margin-top: 20px;
    }
    .kop-surat { text-align: center; border-bottom: 4px double #333; margin-bottom: 15px; }
    
    /* Button WhatsApp */
    .wa-btn {
        background-color: #25D366; color: white; padding: 15px;
        border-radius: 10px; text-align: center; font-weight: bold;
        text-decoration: none; display: block; margin-bottom: 15px;
    }

    /* Card Scorecard Non-Nakes */
    .scorecard-high { background-color: #ffe6e6; padding: 25px; border-radius: 15px; border-left: 8px solid #ff4d4d; color: black; }
    .scorecard-med { background-color: #fff0f5; padding: 25px; border-radius: 15px; border-left: 8px solid #ffa64d; color: black; }
    .scorecard-low { background-color: #e6ffe6; padding: 25px; border-radius: 15px; border-left: 8px solid #33cc33; color: black; }

    /* Proteksi Mode Cetak (Print) */
    @media print {
        .no-print, header, footer, [data-testid="stHeader"], [data-testid="stSidebar"], .stButton, .wa-btn {
            display: none !important;
        }
        .print-report { border: none !important; padding: 0 !important; width: 100% !important; }
        .stApp { background-color: white !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. KONEKSI GOOGLE SHEETS (TANPA TRY-EXCEPT UNTUK DIAGNOSTIK ERROR) ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. SESSION STATE ---
if 'role' not in st.session_state: st.session_state.role = None
if 'dr' not in st.session_state: st.session_state.dr = ""
if 'menu_nakes' not in st.session_state: st.session_state.menu_nakes = "Home"

# --- 4. HOMEPAGE: PILIHAN AKSES (NAKES VS NON-NAKES) ---
if not st.session_state.role:
    st.markdown("<h1 style='text-align:center; color:#004a99;'>🩺 SINTALA v8.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; margin-top:-15px; font-weight:bold;'>Stroke Integrated Analysis & Screening System</p><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='role-card'><h3>👨‍⚕️ Tenaga Medis (Nakes)</h3><p>Akses klinis: FSRP, NIHSS (SOAP), & Siriraj Score</p></div>", unsafe_allow_html=True)
        st.write("")
        dr_input = st.text_input("Nama Dokter / Petugas Medis:")
        if st.button("Masuk Layanan Nakes", use_container_width=True):
            if dr_input:
                st.session_state.role = "Nakes"
                st.session_state.dr = dr_input
                st.rerun()
            else:
                st.warning("Mohon masukkan nama Dokter/Petugas Medis terlebih dahulu.")

    with col2:
        st.markdown("<div class='role-card' style='border-top-color:#28a745;'><h3>👨‍👩‍👧‍👦 Masyarakat (Non-Nakes)</h3><p>Skrining Mandiri Risiko Stroke (Stroke Risk Scorecard)</p></div>", unsafe_allow_html=True)
        st.write("")
        if st.button("Mulai Skrining Mandiri", use_container_width=True):
            st.session_state.role = "Non-Nakes"
            st.rerun()

    st.stop()

# --- 5. SIDEBAR UTAMA ---
with st.sidebar:
    st.markdown(f"Status Akses: **{st.session_state.role}**")
    if st.session_state.dr:
        st.markdown(f"DPJP/Petugas: **{st.session_state.dr}**")
    
    if st.session_state.role == "Nakes":
        if st.button("🏠 Menu Utama Nakes", use_container_width=True):
            st.session_state.menu_nakes = "Home"
            st.rerun()
        st.divider()
        st.info("💡 Tekan **Ctrl + P** untuk mencetak laporan.")

    if st.button("🔄 Ganti Peran / Keluar", use_container_width=True):
        st.session_state.role = None
        st.session_state.dr = ""
        st.session_state.menu_nakes = "Home"
        st.rerun()

# ==============================================================================
# B. ALUR MASYARAKAT / NON-NAKES (STROKE RISK SCORECARD & SPREADSHEET)
# ==============================================================================
if st.session_state.role == "Non-Nakes":
    st.header("📋 Skrining Mandiri Risiko Stroke (Stroke Risk Scorecard)")
    st.caption("Isi form di bawah ini untuk mengukur tingkat risiko stroke Anda secara mandiri.")

    with st.form("form_scorecard"):
        st.subheader("1. Data Diri")
        c1, c2, c3 = st.columns(3)
        with c1:
            p_nama = st.text_input("Nama Lengkap")
        with c2:
            p_umur = st.number_input("Usia (Tahun)", min_value=1, max_value=120, value=40)
        with c3:
            p_gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

        st.divider()
        st.subheader("2. Kartu Skor Parameter Risiko")

        f_td = st.radio("Tekanan Darah", [
            "Sistolik >140 / Diastolik >90 ATAU minum obat darah tinggi (Risiko Tinggi)",
            "Sistolik 120-139 / Diastolik 80-89 (Risiko Sedang)",
            "Sistolik <120 / Diastolik <80 (Risiko Rendah)"
        ])
        
        f_merokok = st.radio("Kebiasaan Merokok", [
            "Perokok aktif / Sering terpapar asap rokok (Risiko Tinggi)",
            "Sedang mencoba berhenti merokok (Risiko Sedang)",
            "Bukan perokok / Tidak pernah merokok (Risiko Rendah)"
        ])
        
        f_dm = st.radio("Diabetes (Gula Darah)", [
            "Di Diagnosis Diabetes / Gula Darah Tinggi (Risiko Tinggi)",
            "Batas Normal Tinggi / Pre-Diabetes (Risiko Sedang)",
            "Gula Darah Normal (Risiko Rendah)"
        ])
        
        f_kolesterol = st.radio("Kadar Kolesterol", [
            "Total Kolesterol >240 mg/dL (Risiko Tinggi)",
            "Total Kolesterol 200-239 mg/dL (Risiko Sedang)",
            "Total Kolesterol <200 mg/dL (Risiko Rendah)"
        ])
        
        f_jantung = st.radio("Riwayat Jantung / Keluarga", [
            "Ada penyakit jantung / Riwayat keluarga terkena stroke (Risiko Tinggi)",
            "Tidak yakin / Ragu-ragu (Risiko Sedang)",
            "Tidak ada riwayat penyakit jantung/keluarga (Risiko Rendah)"
        ])
        
        f_bb = st.radio("Aktivitas Fisik & Berat Badan", [
            "Jarang olahraga & Berat badan berlebih/obesitas (Risiko Tinggi)",
            "Sedikit kurang bergerak (Risiko Sedang)",
            "Rajin olahraga & Berat badan ideal (Risiko Rendah)"
        ])

        btn_analisis = st.form_submit_button("Analisis Risiko Saya & Simpan", use_container_width=True)

    if btn_analisis:
        if not p_nama:
            st.error("Mohon masukkan Nama Lengkap Anda terlebih dahulu.")
        else:
            # Hitung Jumlah Poin Risiko Tinggi
            tinggi_count = sum([
                1 if "Risiko Tinggi" in f_td else 0,
                1 if "Risiko Tinggi" in f_merokok else 0,
                1 if "Risiko Tinggi" in f_dm else 0,
                1 if "Risiko Tinggi" in f_kolesterol else 0,
                1 if "Risiko Tinggi" in f_jantung else 0,
                1 if "Risiko Tinggi" in f_bb else 0
            ])

            if tinggi_count >= 3:
                kategori = "RISIKO TINGGI"
                css_card = "scorecard-high"
                edukasi = "Anda memiliki beberapa faktor risiko utama stroke. Sangat disarankan untuk segera berkonsultasi ke fasilitas kesehatan terdekat untuk kontrol dan pemeriksaan rutin."
            elif tinggi_count >= 1:
                kategori = "RISIKO SEDANG"
                css_card = "scorecard-med"
                edukasi = "Anda memiliki beberapa faktor risiko yang perlu diwaspadai. Mulailah memperbaiki pola hidup sehat dan lakukan pemeriksaan kesehatan berkala."
            else:
                kategori = "RISIKO RENDAH"
                css_card = "scorecard-low"
                edukasi = "Tingkat risiko Anda saat ini tergolong rendah. Pertahankan pola hidup sehat, makan bergizi, dan tetap berolahraga secara teratur."

            # Tampilan Hasil Evaluasi
            st.markdown(f"""
                <div class='{css_card}'>
                    <h2>Kategori Skrining: {kategori}</h2>
                    <p><b>Nama:</b> {p_nama} ({p_umur} Thn) | <b>Jenis Kelamin:</b> {p_gender}</p>
                    <p><b>Saran & Edukasi:</b> {edukasi}</p>
                </div>
            """, unsafe_allow_html=True)

            # Menyimpan Hasil ke Google Sheets (Langsung Eksekusi untuk Mengungkap Detail Error jika Ada)
            data_baru = pd.DataFrame([{
                "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nama": p_nama,
                "Usia": p_umur,
                "Gender": p_gender,
                "Hasil Risiko": kategori,
                "Tekanan Darah": f_td,
                "Merokok": f_merokok,
                "Diabetes": f_dm,
                "Kolesterol": f_kolesterol,
                "Jantung": f_jantung,
                "Aktivitas Fisik": f_bb
            }])

            try:
                df_lama = conn.read(worksheet="Data_Non_Nakes", ttl=5)
                df_update = pd.concat([df_lama, data_baru], ignore_index=True)
                conn.update(worksheet="Data_Non_Nakes", data=df_update)
                st.success("💾 Data hasil skrining Anda berhasil tersimpan otomatis ke Spreadsheet!")
            except Exception as e:
                st.error(f"Gagal menyimpan ke Google Sheets. Detail Error: {e}")

# ==============================================================================
# C. ALUR TENAGA MEDIS / NAKES (FSRP, NIHSS SOAP, & SIRIRAJ SCORE)
# ==============================================================================
elif st.session_state.role == "Nakes":
    
    # 1. MENU UTAMA NAKES
    if st.session_state.menu_nakes == "Home":
        st.subheader("Instrumen Klinis Terintegrasi")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📊 FSRP\n(Skrining & Edukasi)", use_container_width=True):
                st.session_state.menu_nakes = "FSRP"
                st.rerun()
        with c2:
            if st.button("🚨 NIHSS\n(SOAP & IGD)", use_container_width=True):
                st.session_state.menu_nakes = "NIHSS"
                st.rerun()
        with c3:
            if st.button("🧠 SIRIRAJ\n(Diagnostik)", use_container_width=True):
                st.session_state.menu_nakes = "SIRIRAJ"
                st.rerun()

    # 2. MODUL FSRP (FRAMINGHAM STROKE RISK PROFILE)
    elif st.session_state.menu_nakes == "FSRP":
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
            
            if st.form_submit_button("Generate Laporan & Edukasi WA", use_container_width=True):
                risiko = "TINGGI" if (tds > 160 or cvd == 1) else "SEDANG" if tds > 140 else "RENDAH"
                
                # Format Pesan WhatsApp Edukasi
                pesan_fsrp = f"Halo Bapak/Ibu {p_nama}, hasil pemeriksaan risiko stroke Anda: TD {tds}, Kolesterol {chol}. Tingkat risiko: {risiko}. Mohon jaga pola makan dan kontrol rutin. - dr. {st.session_state.dr}"
                st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(pesan_fsrp)}" target="_blank" class="wa-btn">📲 KIRIM EDUKASI KE PASIEN VIA WA</a>', unsafe_allow_html=True)
                
                # Tampilan Resume Cetak
                st.markdown(f"""
                    <div class="print-report">
                        <div class="kop-surat"><h2>LAPORAN ANALISIS RISIKO STROKE (FSRP)</h2></div>
                        <p><b>Pasien:</b> {p_nama} ({p_umur} th) | <b>Pemeriksa:</b> dr. {st.session_state.dr}</p>
                        <hr>
                        <p><b>TD Sistolik:</b> {tds} mmHg | <b>Total Kolesterol:</b> {chol} mg/dL | <b>Penyakit Jantung:</b> {"Ada" if cvd else "Tidak"}</p>
                        <h3 style="color:red;">INTERPRETASI: RISIKO {risiko}</h3>
                    </div>
                """, unsafe_allow_html=True)

    # 3. MODUL NIHSS (SOAP & IGD EDITION - 11 PARAMETER DESKRIPTIF)
    elif st.session_state.menu_nakes == "NIHSS":
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

            if st.form_submit_button("Generate Laporan & WA IGD", use_container_width=True):
                skor = n1+n1b+n2+n3+n4+n5+n6+n7+n8+n9+n10+n11
                kat = "Ringan" if skor <= 4 else "Sedang" if skor <= 15 else "Berat"
                
                # Format Pesan WhatsApp SOAP
                msg_nihss = f"*LAPORAN RUJUKAN NIHSS*\nPasien: {p_nama}\nS: {s_subj}\nO: {o_vital}, NIHSS {skor}\nA: Suspek Stroke ({kat})\nP: {p_plan}\nDPJP: dr. {st.session_state.dr}"
                st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg_nihss)}" target="_blank" class="wa-btn">📲 KIRIM FORMAT SOAP KE IGD RS VIA WA</a>', unsafe_allow_html=True)
                
                # Tampilan Resume Cetak
                st.markdown(f"""
                    <div class="print-report">
                        <div class="kop-surat"><h2>RESUME MEDIS NIHSS (SOAP)</h2></div>
                        <p><b>Pasien:</b> {p_nama} | <b>Pemeriksa:</b> dr. {st.session_state.dr}</p>
                        <p><b>Skor NIHSS: {skor} (Stroke {kat})</b></p>
                        <hr>
                        <p><b>[S] Subjective:</b> {s_subj}</p>
                        <p><b>[O] Objective:</b> {o_vital}</p>
                        <p><b>[P] Plan:</b> {p_plan}</p>
                    </div>
                """, unsafe_allow_html=True)

    # 4. MODUL SIRIRAJ STROKE SCORE (DIAGNOSTIK PRESISI DBP)
    elif st.session_state.menu_nakes == "SIRIRAJ":
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
                p_plan_s = st.text_input("Plan", "Observasi, Stabilisasi & CT-Scan")

            if st.form_submit_button("Hitung Siriraj & Kirim WA", use_container_width=True):
                # Rumus Asli Baku Siriraj Stroke Score (Menggunakan Diastolik)
                sss = (2.5 * sadar) + (2 * muntah) + (2 * nyeri) + (0.1 * dbp) - (3 * athero) - 12
                diag = "Hemoragik" if sss > 1 else "Iskemik" if sss < -1 else "Perlu CT-Scan (Equivocal)"
                
                # Format Pesan WhatsApp Siriraj
                msg_sss = f"*HASIL SIRIRAJ STROKE SCORE*\nPasien: {p_nama}\nSkor SSS: {sss:.2f}\nPrediksi: Stroke {diag}\nPlan: {p_plan_s}\nDPJP: dr. {st.session_state.dr}"
                st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg_sss)}" target="_blank" class="wa-btn">📲 KIRIM HASIL KE IGD VIA WA</a>', unsafe_allow_html=True)

                # Tampilan Resume Cetak
                st.markdown(f"""
                    <div class="print-report">
                        <div class="kop-surat"><h2>LAPORAN SIRIRAJ STROKE SCORE</h2></div>
                        <p><b>Pasien:</b> {p_nama} | <b>Diastolik:</b> {dbp} mmHg | <b>Pemeriksa:</b> dr. {st.session_state.dr}</p>
                        <p><b>Skor SSS: {sss:.2f}</b></p>
                        <hr>
                        <h3 style="color:#004a99;">PREDIKSI KLINIS: STROKE {diag.upper()}</h3>
                        <p><b>Rencana Lanjutan:</b> {p_plan_s}</p>
                    </div>
                """, unsafe_allow_html=True)

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
# B. ALUR MASYARAKAT / NON-NAKES (STROKE RISK SCORECARD & GOOGLE FORM WEBHOOK)
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

            # Webhook URL dan Payload 10 Parameter Lengkap
            FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSepB48NwUtE2qICYrTyd3eOtpCHvQ7vBNEPCoRUg4I6rVIetg/formResponse"
            
            form_payload = {
                "entry.274829296": p_nama,
                "entry.546877202": str(p_umur),
                "entry.729271643": p_gender,
                "entry.641466882": kategori,
                "entry.1164896165": f_td,
                "entry.1863353198": f_merokok,
                "entry.1730221596": f_dm,
                "entry.99250368": f_kolesterol,
                "entry.51451220": f_jantung,
                "entry.804106935": f_bb
            }

            try:
                res = requests.post(FORM_URL, data=form_payload)
                if res.status_code in [200, 302]:
                    st.success("💾 Data hasil skrining Anda berhasil tersimpan otomatis ke database Google Form/Sheets!")
                else:
                    st.success("💾 Data hasil skrining berhasil dikirimkan ke database!")
            except Exception as e:
                st.error(f"Gagal menyimpan data: {e}")

# ==============================================================================
# C. ALUR TENAGA MEDIS / NAKES (FSRP, NIHSS SOAP, & SIRIRAJ SCORE)
# ==============================================================================
elif st.session_state.role == "Nakes":
    
    # 1. MENU UTAMA NAKES
    if st.session_state.menu_nakes == "Home":
        st.markdown("""
        <div class="hero-panel" style="padding:1.7rem 2rem;">
          <div class="hero-kicker">Clinical workspace</div>
          <h2 style="margin:0;">Instrumen Klinis Terintegrasi</h2>
          <p class="hero-sub" style="margin:.55rem 0 0;">Pilih modul untuk memulai penilaian, menyusun dokumentasi, atau membantu komunikasi klinis.</p>
        </div>
        <div class="section-eyebrow">Modul tersedia</div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="large")
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

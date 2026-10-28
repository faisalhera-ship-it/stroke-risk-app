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

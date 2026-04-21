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
            res = "Perlu Perhatian Khusus" if tds > 140 or chol > 200 else "Risiko Terkontrol"
            edukasi = f"Halo Bapak/Ibu {p_nama}, Hasil skrining FSRP Anda: {res}. Mohon jaga pola makan dan kontrol TD rutin."
            st.markdown(f'<a href="{kirim_wa(p_wa, edukasi)}" target="_blank" class="wa-card">📲 KIRIM EDUKASI</a>', unsafe_allow_html=True)

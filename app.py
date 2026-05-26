import streamlit as st
import google.generativeai as genai
from PIL import Image

# =====================================================================
# 1. KONFIGURASI API KEY (Tanam Kunci Kamu di Sini)
# Ganti tulisan di dalam tanda petik dengan API Key asli dari Google AI Studio
# Contoh: GEMINI_API_KEY = "AIzaSy..."
# =====================================================================
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Menghubungkan aplikasi langsung ke server AI Gemini
genai.configure(api_key=GEMINI_API_KEY)


# 2. Konfigurasi Halaman & Tema
st.set_page_config(page_title="NutriView - Hitung Gizi Foto Makanan", page_icon="🥗", layout="centered")

st.title("🥗 NutriView AI")
st.subheader("Hitung Gizi Makananmu Lewat Foto")
st.write("Unggah foto makananmu, dan AI akan menganalisis perkiraan kandungan gizinya.")


# 3. Fitur Utama: Analisis Makanan (Langsung terbuka untuk semua orang)
uploaded_file = st.file_uploader("Pilih atau Ambil Foto Makanan...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Makanan yang Diunggah', use_column_width=True)
    
    # Tombol Analisis
    if st.button("Hitung Kandungan Gizi 🚀"):
        with st.spinner("AI sedang menganalisis makananmu... Mohon tunggu..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = """
                Bertindaklah sebagai ahli gizi profesional. Analisis foto makanan berikut dan berikan output dalam Bahasa Indonesia dengan format yang rapi:
                1. **Nama Makanan**: Identifikasi nama makanan/hidangan di foto.
                2. **Estimasi Berat**: Perkiraan porsi dalam gram.
                3. **Tabel Nilai Nutrisi**: Berikan perkiraan jumlah:
                   - Kalori (kcal)
                   - Karbohidrat (gram)
                   - Protein (gram)
                   - Lemak (gram)
                4. **Kesimpulan Singkat**: Apakah makanan ini sehat/seimbang? Berikan rekomendasi singkat.
                """
                
                response = model.generate_content([prompt, image])
                st.success("Analisis Selesai!")
                st.markdown("### 📊 Hasil Perhitungan Gizi:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- PEMBATAS SEKSI ---
st.markdown("---")

# 4. Fitur Saran dan Kritik
st.subheader("💬 Hubungi Kami (Saran & Kritik)")
with st.form(key="form_saran_kritik", clear_on_submit=True):
    nama = st.text_input("Nama (Opsional):")
    email = st.text_input("Email (Opsional):")
    tipe_pesan = st.selectbox("Jenis Pesan:", ["Saran Pengembangan", "Kritik / Bug", "Lainnya"])
    pesan = st.text_area("Tulis saran atau kritik Anda di sini:")
    submit_button = st.form_submit_button(label="Kirim Masukan")
    
    if submit_button:
        if pesan.strip() == "":
            st.error("Pesan tidak boleh kosong!")
        else:
            with open("saran_kritik.txt", "a", encoding="utf-8") as f:
                f.write(f"Tipe: {tipe_pesan} | Oleh: {nama}\nPesan: {pesan}\n{'-'*30}\n")
            st.success("Terima kasih! Masukan Anda telah berhasil direkam oleh NutriView.")
            # =====================================================================
# 5. MENU ADMIN RAHASIA (Hanya untuk pemilik aplikasi)
# =====================================================================
st.markdown("---")
with st.expander("🔐 Menu Admin (Khusus Pengembang)"):
    input_password = st.text_input("Masukkan Password Admin:", type="password")
    
    # Kamu bisa mengganti "survei123" dengan password buatanmu sendiri
    if input_password == "survei123": 
        st.success("Akses Diterima!")
        
        try:
            # Membaca file saran yang tersimpan di server
            with open("saran_kritik.txt", "r", encoding="utf-8") as f:
                data_saran = f.read()
            
            # Tombol sakti untuk download file ke laptop/HP kamu
            st.download_button(
                label="📥 Unduh File Saran & Kritik (.txt)",
                data=data_saran,
                file_name="hasil_survei_nutriview.txt",
                mime="text/plain"
                )
            
            # Menampilkan isi pesannya langsung di layar admin
            st.markdown("### 📝 Isi Pesan Saat Ini:")
            st.text_area("", value=data_saran, height=250)
            
        except FileNotFoundError:
            st.info("Belum ada saran atau kritik yang masuk dari responden.")

import streamlit as st
import google.generativeai as genai
from PIL import Image

# =====================================================================
# 1. KONFIGURASI API KEY (Menggunakan Brankas Aman Streamlit Secrets)
# =====================================================================
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.warning("⚠️ API Key belum dikonfigurasi di Streamlit Secrets.")


# =====================================================================
# 2. KONFIGURASI HALAMAN & CUSTOM TEMA (Menyesuaikan Otomatis)
# =====================================================================
st.set_page_config(page_title="NutriView - Hitung Gizi Foto Makanan", page_icon="🥗", layout="centered")

# Skrip CSS: Hanya mengubah Light Mode ke Cornflower Blue. Dark Mode dibiarkan otomatis putih bawaan sistem.
custom_css = """
<style>
    /* Hanya mengatur Mode Terang (Light Mode) */
    @media (prefers-color-scheme: light) {
        h1, h2, h3, .stSubheader {
            color: #6495ED !important;
        }
        div.stButton > button:first-child {
            background-color: #6495ED !important;
            color: white !important;
            border: none;
        }
    }
    
    /* Mode Gelap (Dark Mode) dibiarkan MENYESUAIKAN otomatis agar teks berwarna putih/terang */
    @media (prefers-color-scheme: dark) {
        div.stButton > button:first-child {
            background-color: #6495ED !important; /* Tombol tetap biru cerah agar kontras */
            color: white !important;
            border: none;
        }
    }
    
    /* Efek hover tombol universal */
    div.stButton > button:first-child:hover {
        opacity: 0.85;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# =====================================================================
# 3. FITUR UTAMA: ANALISIS MAKANAN
# =====================================================================
st.title("🥗 NutriView AI")
st.subheader("Hitung Gizi Makananmu Lewat Foto")
st.write("Unggah foto makananmu, dan AI akan menganalisis perkiraan kandungan gizinya.")

uploaded_file = st.file_uploader("Pilih atau Ambil Foto Makanan...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Makanan yang Diunggah', use_column_width=True)
    
    # FITUR REVISI / KOREKSI MENU: Kotak Catatan Tambahan untuk AI
    catatan_user = st.text_input(
        label="✍️ Catatan Tambahan / Koreksi Menu (Opsional):",
        placeholder="Contoh: Yang bulat kuning itu jeruk ya, bukan mangga. Atau: Ini nasi merah dan ayam bakar."
    )
    
    # Tombol Analisis
    if st.button("Hitung Kandungan Gizi 🚀"):
        with st.spinner("AI sedang menganalisis makananmu... Mohon tunggu..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Prompt instruksi khusus ahli gizi
                prompt = f"""
                Bertindaklah sebagai ahli gizi profesional. Analisis foto makanan berikut dan berikan output dalam Bahasa Indonesia dengan format yang rapi:
                1. **Nama Makanan**: Identifikasi nama makanan/hidangan di foto.
                2. **Estimasi Berat**: Perkiraan porsi dalam gram.
                3. **Tabel Nilai Nutrisi**: Berikan perkiraan jumlah Kalori (kcal), Karbohidrat (g), Protein (g), dan Lemak (g).
                4. **Kesimpulan Singkat**: Apakah makanan ini sehat/seimbang? Berikan rekomendasi singkat.
                
                PENTING: Jika pengguna memberikan catatan atau koreksi di bawah ini, prioritaskan catatan tersebut dalam analisis dan perhitungan gizimu!
                Catatan dari pengguna: "{catatan_user}"
                """
                
                response = model.generate_content([prompt, image])
                st.success("Analisis Selesai!")
                st.markdown("### 📊 Hasil Perhitungan Gizi:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- PEMBATAS SEKSI ---
st.markdown("---")


# =====================================================================
# 4. FITUR SARAN DAN KRITIK
# =====================================================================
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

# --- PEMBATAS SEKSI ---
st.markdown("---")


# =====================================================================
# 5. MENU ADMIN RAHASIA (Pintu Belakang untuk Ambil Hasil Survei)
# =====================================================================
with st.expander("🔐 Menu Admin (Khusus Pengembang)"):
    input_password = st.text_input("Masukkan Password Admin:", type="password")
    
    if input_password == "survei123": 
        st.success("Akses Diterima!")
        try:
            with open("saran_kritik.txt", "r", encoding="utf-8") as f:
                data_saran = f.read()
            
            st.download_button(
                label="📥 Unduh File Saran & Kritik (.txt)",
                data=data_saran,
                file_name="hasil_survei_nutriview.txt",
                mime="text/plain"
            )
            st.markdown("### 📝 Isi Pesan Saat Ini:")
            st.text_area("", value=data_saran, height=250)
        except FileNotFoundError:
            st.info("Belum ada saran atau kritik yang masuk dari responden.")

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

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

# Skrip CSS untuk mengatur tampilan warna
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
    
    /* Mode Gelap (Dark Mode) otomatis putih bawaan sistem */
    @media (prefers-color-scheme: dark) {
        div.stButton > button:first-child {
            background-color: #6495ED !important;
            color: white !important;
            border: none;
        }
    }
    
    /* Efek hover tombol */
    div.stButton > button:first-child:hover {
        opacity: 0.85;
    }
    
    /* Efek Animasi Berkedip/Denyut untuk Logo Saat Loading */
    @keyframes pulse {
        0% { opacity: 0.4; transform: scale(0.98); }
        50% { opacity: 1; transform: scale(1.02); }
        100% { opacity: 0.4; transform: scale(0.98); }
    }
    .loading-logo {
        animation: pulse 1.5s infinite ease-in-out;
        display: block;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
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
        
        # 🌟 INDIKATOR LOADING KUSTOM MENGGUNAKAN LOGO 🌟
        # Membuat area kosong sementara untuk memunculkan logo saat loading berjalan
        l<img src="https://cdn.flipsnack.com/users/C6C8FBF6AED/images/profile?v=0" width="120">
        
        with loading_area.container():
            st.markdown("<br>", unsafe_allow_html=True)
            # Trik memunculkan Logo dengan animasi berkedip (pulse) lewat HTML kustom
            # Catatan: Ganti URL gambar di bawah ini dengan link logo aslimu jika ada, saat ini menggunakan logo bawaan salad
            st.markdown(
                '''
                <div class="loading-logo">
                    <span style="font-size: 70px;">🥗</span>
                    <h3 style="margin-top: 10px;">NutriView AI sedang menghitung gizi...</h3>
                    <p style="font-style: italic;">Mohon tunggu sebentar ya...</p>
                </div>
                ''', 
                unsafe_allow_html=True
            )
        
        # Jalankan proses analisis AI di latar belakang
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
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
            
            # Setelah AI selesai berpikir, hapus tampilan loading logo agar bersih kembali
            loading_area.empty()
            
            st.success("Analisis Selesai!")
            st.markdown("### 📊 Hasil Perhitungan Gizi:")
            st.write(response.text)
            
        except Exception as e:
            loading_area.empty() # Hapus loading jika terjadi error
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

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# =====================================================================
# 1. KONFIGURASI API KEY (Menggunakan Brankas Aman Streamlit Secrets)
# =====================================================================
try:
    if "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        st.error("⚠️ API Key tidak ditemukan. Pastikan sudah dimasukkan di Streamlit Secrets.")
except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan saat memuat API Key: {e}")

# =====================================================================
# 2. KONFIGURASI HALAMAN & CUSTOM TEMA (Menyesuaikan Otomatis)
# =====================================================================
st.set_page_config(page_title="NutriView - Hitung Gizi Foto Makanan Sekolah", page_icon="🏫", layout="centered")

# Skrip CSS Pintar: Mengubah Aksen (Cornflower Blue) & ANIMASI LOADING LOGO SEKOLAH (Berwarna <-> Hitam Putih)
custom_css = """
<style>
    /* 1. Setting Teks/Aksen Tergantung Light/Dark Mode Sistem */
    
    /* Mode Terang (Light Mode) JUDUL BIRU CERAH */
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
    
    /* Mode Gelap (Dark Mode) - Dibiarkan otomatis putih bawaan sistem agar teks terbaca */
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

    /* ========================================= */
    /* 2. DEFINISI ANIMASI COLOR-FADE LOGO (Loading) */
    /* ========================================= */
    
    /* @keyframes 'colorFade': Mengubah grayscale(100%/Hitam Putih) ke grayscale(0%/Berwarna) bolak balik */
    @keyframes colorFade {
        0%   { filter: grayscale(100%); opacity: 0.6; } /* Awal: Hitam Putih, Agak Pudar */
        50%  { filter: grayscale(0%); opacity: 1.0; }   /* Tengah: Berwarna Penuh, Terang */
        100% { filter: grayscale(100%); opacity: 0.6; } /* Akhir: Kembali Hitam Putih, Pudar */
    }

    .color-fade-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
        /* Terapkan animasi 'colorFade' selama 2 detik, repeat tak terbatas, transisi halus */
        animation: colorFade 2s infinite ease-in-out; 
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# =====================================================================
# 3. FITUR UTAMA: ANALISIS MAKANAN SEKOLAH
# =====================================================================
st.title("🏫 NutriView Sekolah")
st.subheader("Hitung Gizi Makananmu Lewat Foto")
st.write("Belajar makan sehat! Unggah foto makananmu, dan AI akan menganalisis perkiraan kandungan gizinya.")

uploaded_file = st.file_uploader("Pilih atau Ambil Foto Jajanan/Makanan Sekolah...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Makanan Sekolah yang Diunggah', use_column_width=True)
    
    # FITUR REVISI / KOREKSI MENU: Kotak Catatan Tambahan untuk AI
    catatan_user = st.text_input(
        label="✍️ Catatan Tambahan / Koreksi Menu Sekolah (Opsional):",
        placeholder="Contoh: Yang putih lonjong itu telur rebus ya, bukan bakso gajah. Atau: Ini nasi uduk sekolah."
    )
    
    # Tombol Analisis
    if st.button("Hitung Kandungan Gizi Jajanan Sekolah 🚀"):
        
        # =============================================================
        # 🌟 INDIKATOR LOADING KUSTOM: COLOR-FADE LOGO SEKOLAH 🌟
        # =============================================================
        # Membuat placeholder kosong untuk animasi loading kustom
        loading_area = st.empty()
        
        # Ganti Teks dengan animasi yang sesuai di CSS
        with loading_area.container():
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # --- PENTING ---
            # TEMP ELKAN LINK ALAMAT GAMBAR LOGO SEKOLAHMU dari Google ke dalam tanda petik `src` di bawah ini.
            # (Saat ini saya pasang logo sekolah generatif sebagai contoh, silakan ganti).
            st.markdown(
                f'''
                <div class="color-fade-logo">
                    <img src="https://www.sman7bks.sch.id/media_library/images/5690a29e44fc8a2b235821eb4cbf765a.png" width="130">
                    <h3 style="margin-top: 15px;">NutriView Sekolah sedang menghitung gizi...</h3>
                    <p style="font-style: italic;">Sabar ya, logo sekolahmu sedang 'berubah warna' selagi AI berpikir...</p>
                </div>
                ''', 
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Jalankan proses analisis AI di latar belakang
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Bertindaklah sebagai ahli gizi profesional sekolah yang ramah. Analisis foto makanan/jajanan sekolah berikut dan berikan output dalam Bahasa Indonesia dengan format yang rapi dan mudah dimengerti siswa:
            1. **Identifikasi Makanan Sekolah**: Tuliskan nama makanan/hidangan di foto.
            2. **Estimasi Porsi Jajanan**: Perkiraan berat dalam gram.
            3. **Tabel Nilai Nutrisi Utama**: Kalori (kcal), Karbohidrat (g), Protein (g), dan Lemak (g).
            4. **Kesimpulan Ramah Siswa**: Apakah jajanan ini sehat/seimbang? Berikan rekomendasi singkat dan positif agar siswa makan lebih sehat di sekolah.
            
            PENTING: Jika pengguna memberikan catatan sekolah/koreksi di bawah ini, prioritaskan catatan tersebut dalam analisis dan perhitungan gizimu!
            Catatan dari pengguna/siswa: "{catatan_user}"
            """
            
            response = model.generate_content([prompt, image])
            
            # Setelah AI selesai berpikir, hapus indikator loading kustom logo sekolah
            loading_area.empty()
            
            st.success("Analisis Selesai! Selamat belajar tentang makananmu! 📚")
            st.markdown("### 📊 Hasil Perhitungan Gizi Jajanan Sekolahmu:")
            st.write(response.text)
            
        except Exception as e:
            loading_area.empty() # Hapus loading logo sekolah jika terjadi error
            st.error(f"Terjadi kesalahan saat AI memproses foto. Mungkin kunci rahasia salah di Secrets atau link foto error. Error: {e}")

# --- PEMBATAS SEKSI ---
st.markdown("---")


# =====================================================================
# 4. FITUR SARAN DAN KRITIK SEKOLAH
# =====================================================================
st.subheader("💬 Hubungi Kami (Saran & Kritik Sekolah)")
st.write("Aplikasi ini untuk belajar makan sehat. Kasih masukan ya biar makin bagus!")

with st.form(key="form_saran_kritik", clear_on_submit=True):
    nama = st.text_input("Nama/Kelas (Opsional):")
    tipe_pesan = st.selectbox("Jenis Masukan Sekolah:", ["Saran Fitur Baru", "Lapor Bug (Mogok)", "Ide Jajanan Sehat", "Lainnya"])
    pesan = st.text_area("Tulis saran atau kritik Anda di sini:")
    submit_button = st.form_submit_button(label="Kirim Masukan 📩")
    
    if submit_button:
        if pesan.strip() == "":
            st.error("Pesan tidak boleh kosong!")
        else:
            with open("saran_kritik.txt", "a", encoding="utf-8") as f:
                f.write(f"Tipe: {tipe_pesan} | Oleh: {nama}\nPesan: {pesan}\n{'-'*30}\n")
            st.success("Terima kasih! Masukan Anda telah berhasil direkam oleh NutriView Sekolah.")

# --- PEMBATAS SEKSI ---
st.markdown("---")


# =====================================================================
# 5. MENU ADMIN RAHASIA SEKOLAH (Pintu Belakang untuk Ambil Hasil Survei)
# =====================================================================
with st.expander("🔐 Menu Admin (Khusus Guru/Pengembang Sekolah)"):
    input_password = st.text_input("Masukkan Password Admin Sekolah:", type="password")
    
    if input_password == "survei123": 
        st.success("Akses Diterima!")
        try:
            with open("saran_kritik.txt", "r", encoding="utf-8") as f:
                data_saran = f.read()
            
            st.download_button(
                label="📥 Unduh File Saran & Kritik Sekolah (.txt)",
                data=data_saran,
                file_name="hasil_survei_nutriview_sekolah.txt",
                mime="text/plain"
            )
            st.markdown("### 📝 Isi Pesan Survei Sekolah Saat Ini:")
            st.text_area("", value=data_saran, height=250)
        except FileNotFoundError:
            st.info("Belum ada saran atau kritik yang masuk dari survei sekolah.")

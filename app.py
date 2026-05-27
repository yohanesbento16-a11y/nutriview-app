import streamlit as st
import json
import os
import base64

# =====================================================================
# 1. KONFIGURASI HALAMAN & CSS AJAIB
# =====================================================================
st.set_page_config(page_title="NutriView - Kantin Sehat Sekolah", page_icon="🏫", layout="centered")

custom_css = """
<style>
    /* Sembunyikan ikon GitHub di header agar aman */
    [data-testid="stHeader"] a[href*="github.com"] {
        display: none !important;
    }

    /* Tema Warna Judul & Tombol */
    @media (prefers-color-scheme: light) {
        h1, h2, h3, .stSubheader { color: #6495ED !important; }
        div.stButton > button:first-child { background-color: #6495ED !important; color: white !important; border: none; }
    }
    @media (prefers-color-scheme: dark) {
        div.stButton > button:first-child { background-color: #6495ED !important; color: white !important; border: none; }
    }
    div.stButton > button:first-child:hover { opacity: 0.85; }
    
    /* Percantik tampilan kartu menu */
    .menu-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# =====================================================================
# 2. SISTEM DATABASE LOKAL (Penyimpanan JSON)
# =====================================================================
DB_FILE = "menu_sekolah.json"

# Fungsi membaca data dari file
def muat_data_menu():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] # Kembalikan list kosong jika file belum ada

# Fungsi menyimpan data ke file
def simpan_data_menu(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Load data saat aplikasi berjalan
data_menu = muat_data_menu()


# =====================================================================
# 3. TAMPILAN ANTARMUKA (MENGGUNAKAN TAB)
# =====================================================================
st.title("🏫 NutriView Sekolah")
st.write("Informasi gizi jajanan sehat kantin sekolah kita hari ini!")

# Membuat 2 Halaman (Tab)
tab_siswa, tab_admin = st.tabs(["🍽️ Menu Hari Ini", "🔐 Panel Admin Kantin"])

# ---------------------------------------------------------------------
# TAB 1: HALAMAN SISWA (Melihat Menu)
# ---------------------------------------------------------------------
with tab_siswa:
    st.subheader("Menu Tersedia Hari Ini")
    
    if len(data_menu) == 0:
        st.info("Belum ada menu yang ditambahkan untuk hari ini. Silakan tunggu Admin mengunggah menu.")
    else:
        # Tampilkan setiap menu yang ada di database
        for idx, menu in enumerate(data_menu):
            with st.container():
                st.markdown('<div class="menu-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Menampilkan foto (dari format Base64)
                    if menu["foto_base64"]:
                        gambar_bytes = base64.b64decode(menu["foto_base64"])
                        st.image(gambar_bytes, use_column_width=True)
                    else:
                        st.info("Tidak ada foto")
                        
                with col2:
                    st.markdown(f"### {menu['nama']}")
                    st.write(f"⚖️ **Porsi/Berat:** {menu['porsi']}")
                    
                    # Tabel Nutrisi Rapi
                    st.markdown("**Kandungan Gizi:**")
                    kolom_gizi1, kolom_gizi2, kolom_gizi3, kolom_gizi4 = st.columns(4)
                    kolom_gizi1.metric("Kalori", f"{menu['kalori']} kcal")
                    kolom_gizi2.metric("Karbo", f"{menu['karbo']} g")
                    kolom_gizi3.metric("Protein", f"{menu['protein']} g")
                    kolom_gizi4.metric("Lemak", f"{menu['lemak']} g")
                    
                st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------
# TAB 2: HALAMAN ADMIN (Tambah Data & Feedback)
# ---------------------------------------------------------------------
with tab_admin:
    input_password = st.text_input("Masukkan Password Admin Sekolah:", type="password")
    
    if input_password == "survei123":
        st.success("Akses Diterima! Selamat datang, Admin.")
        
        # Fitur 1: Tambah Menu Baru
        with st.expander("➕ Tambah Menu Baru", expanded=True):
            with st.form("form_tambah_menu", clear_on_submit=True):
                nama_makanan = st.text_input("Nama Jajanan / Makanan:")
                porsi = st.text_input("Estimasi Porsi (Contoh: 1 Porsi / 200 gram):")
                
                # Input Gizi
                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    kalori = st.number_input("Kalori (kcal)", min_value=0.0, step=1.0)
                    karbo = st.number_input("Karbohidrat (g)", min_value=0.0, step=1.0)
                with col_k2:
                    protein = st.number_input("Protein (g)", min_value=0.0, step=1.0)
                    lemak = st.number_input("Lemak (g)", min_value=0.0, step=1.0)
                
                # Unggah Foto Makanan
                foto_upload = st.file_uploader("Unggah Foto Makanan", type=["jpg", "jpeg", "png"])
                
                submit_menu = st.form_submit_button("Simpan Menu ke Database 💾")
                
                if submit_menu:
                    if nama_makanan.strip() == "":
                        st.error("Nama makanan tidak boleh kosong!")
                    else:
                        # Ubah foto menjadi teks base64 agar bisa disimpan di dalam file json
                        foto_b64 = ""
                        if foto_upload is not None:
                            foto_bytes = foto_upload.read()
                            foto_b64 = base64.b64encode(foto_bytes).decode('utf-8')
                            
                        # Buat data menu baru
                        menu_baru = {
                            "nama": nama_makanan,
                            "porsi": porsi,
                            "kalori": kalori,
                            "karbo": karbo,
                            "protein": protein,
                            "lemak": lemak,
                            "foto_base64": foto_b64
                        }
                        
                        data_menu.append(menu_baru)
                        simpan_data_menu(data_menu)
                        st.success(f"Berhasil menambahkan {nama_makanan} ke Menu Hari Ini!")
                        st.rerun() # Refresh aplikasi agar menu langsung muncul
        
        # Fitur 2: Hapus Menu
        with st.expander("🗑️ Hapus Menu"):
            if len(data_menu) > 0:
                pilihan_hapus = st.selectbox("Pilih menu yang ingin dihapus:", [m["nama"] for m in data_menu])
                if st.button("Hapus Menu Terpilih"):
                    data_menu = [m for m in data_menu if m["nama"] != pilihan_hapus]
                    simpan_data_menu(data_menu)
                    st.success(f"Menu '{pilihan_hapus}' berhasil dihapus.")
                    st.rerun()
            else:
                st.info("Belum ada data menu.")
                
        # Fitur 3: Lihat Saran & Kritik Siswa
        with st.expander("📬 Kotak Masukan Siswa"):
            try:
                with open("saran_kritik.txt", "r", encoding="utf-8") as f:
                    data_saran = f.read()
                st.text_area("Isi Kotak Saran Saat Ini:", value=data_saran, height=200)
                st.download_button("📥 Unduh File Saran (.txt)", data=data_saran, file_name="saran_sekolah.txt")
            except FileNotFoundError:
                st.info("Belum ada saran atau kritik yang masuk.")

# =====================================================================
# 4. KOTAK SARAN (UNTUK SISWA) - Tampil di bagian paling bawah
# =====================================================================
st.markdown("---")
st.subheader("💬 Hubungi Admin Kantin")
with st.form("form_saran", clear_on_submit=True):
    nama_siswa = st.text_input("Nama/Kelas (Opsional):")
    pesan_siswa = st.text_area("Tulis saran, request jajanan sehat, atau kritik di sini:")
    if st.form_submit_button("Kirim Masukan 📩"):
        if pesan_siswa.strip():
            with open("saran_kritik.txt", "a", encoding="utf-8") as f:
                f.write(f"Dari: {nama_siswa}\nPesan: {pesan_siswa}\n{'-'*30}\n")
            st.success("Terima kasih! Masukanmu sudah terkirim.")
        else:
            st.error("Pesan tidak boleh kosong.")

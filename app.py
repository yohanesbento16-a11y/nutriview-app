import streamlit as st
import time
import streamlit.components.v1 as components

# =====================================================================
# KONFIGURASI HALAMAN & CSS BUCIN
# =====================================================================
st.set_page_config(page_title="Untuk Abey 💌", page_icon="💖", layout="centered")

custom_css = """
<style>
    /* Sembunyikan elemen bawaan Streamlit agar terlihat seperti web asli */
    header, [data-testid="stHeader"] { display: none !important; }
    .stAppDeployButton { display: none !important; }
    footer { display: none !important; }

    /* Desain font dan warna pastel untuk tema romantis */
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Pacifico&display=swap');
    
    h1, h2, h3 { 
        font-family: 'Comic Neue', cursive !important; 
        color: #ff4b4b !important; 
        text-align: center;
    }
    p, label, .stRadio, .stCheckbox { 
        font-family: 'Comic Neue', cursive !important; 
        font-size: 18px !important;
    }
    
    /* Desain Tombol Standar */
    div.stButton > button { 
        background-color: #ff4b4b !important; 
        color: white !important; 
        border-radius: 20px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        background-color: #ff7aa2 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# =====================================================================
# PENGATURAN STATE HALAMAN (Untuk pindah-pindah menu & simpan pilihan)
# =====================================================================
if 'halaman' not in st.session_state:
    st.session_state.halaman = 1

# Database sementara untuk menyimpan status tombol kegiatan
if 'kegiatan_dipilih' not in st.session_state:
    st.session_state.kegiatan_dipilih = {
        "makan bareng 🍽️": False,
        "nonton 🎬": False,
        "jalan aja 🚶‍♂️": False,
        "main ajaa 🎡": False,
        "photoboot 📸": False
    }

# =====================================================================
# HALAMAN 1: LOADING & AMPLOP CINTA
# =====================================================================
if st.session_state.halaman == 1:
    if 'loading_selesai' not in st.session_state:
        teks_loading = st.empty()
        bar_loading = st.progress(0)
        
        for persen in range(100):
            time.sleep(0.03)
            bar_loading.progress(persen + 1)
            teks_loading.markdown(f"<h3 style='color:#ffb6c1;'>Menyiapkan kejutan untuk Abey... {persen+1}%</h3>", unsafe_allow_html=True)
            
        st.session_state.loading_selesai = True
        st.rerun()
    else:
        st.markdown("<h2>Undangan Pribadi buat abey 💌</h2>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 80px;'>📩</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Buka Suratnya ✨"):
                st.session_state.halaman = 2
                st.rerun()

# =====================================================================
# HALAMAN 2: PERTANYAAN UTAMA (Tombol Kabur)
# =====================================================================
elif st.session_state.halaman == 2:
    st.markdown("<h2>maukah kamu jayan jayan cama anesyi? 🥺👉👈</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 60px;'>🧸✨</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("mauuu!! 💖"):
            st.session_state.halaman = 3
            st.rerun()
            
    with col2:
        components.html("""
            <div style="width: 100%; height: 200px; position: relative;">
                <button id="btnKabur" 
                    style="
                        position: absolute; left: 20%; top: 20%; 
                        padding: 10px 20px; font-size: 16px; font-weight: bold;
                        border: none; background-color: #e0e0e0; color: #555; 
                        border-radius: 20px; cursor: pointer;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                        transition: top 0.1s, left 0.1s;
                    " 
                    onmouseover="kabur()">ga ah 🙈</button>
            </div>
            <script>
                function kabur() {
                    var btn = document.getElementById('btnKabur');
                    var container = btn.parentElement;
                    var maxX = container.clientWidth - btn.clientWidth;
                    var maxY = container.clientHeight - btn.clientHeight;
                    
                    var x = Math.floor(Math.random() * maxX);
                    var y = Math.floor(Math.random() * maxY);
                    
                    btn.style.left = x + 'px';
                    btn.style.top = y + 'px';
                }
            </script>
        """, height=250)

# =====================================================================
# HALAMAN 3: LOADING TRANSISI "YEYY MAUUU"
# =====================================================================
elif st.session_state.halaman == 3:
    st.markdown("<h2 style='margin-top: 100px;'>yeyy abey mauuu 🥰🎉</h2>", unsafe_allow_html=True)
    with st.spinner(""):
        time.sleep(2.5) 
    st.balloons()
    st.session_state.halaman = 4
    st.rerun()

# =====================================================================
# HALAMAN 4: ATUR TANGGAL & WAKTU
# =====================================================================
elif st.session_state.halaman == 4:
    st.markdown("<h2>kapan cayang na atu free? ⏰</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.session_state.tanggal = st.date_input("Pilih Tanggal Kencan:")
    st.session_state.waktu = st.time_input("Pilih Jam Kencan:")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Lanjut 🚀"):
        st.session_state.halaman = 5
        st.rerun()

# =====================================================================
# HALAMAN 5: NANTI KITA NGAPAIN AJA? (Sekarang Pakai Tombol Ikon)
# =====================================================================
elif st.session_state.halaman == 5:
    st.markdown("<h2>nanti kita ngapain aja? 🤔</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Klik ikon di bawah untuk memilih (Boleh pilih lebih dari satu ya!):")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Membuat grid baris dan kolom untuk tombol ikon
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    kolom_list = [col1, col2, col3, col4, col5]
    kegiatan_keys = list(st.session_state.kegiatan_dipilih.keys())
    
    # Menampilkan tombol layaknya saklar (Toggle)
    for i, kegiatan in enumerate(kegiatan_keys):
        is_selected = st.session_state.kegiatan_dipilih[kegiatan]
        # Jika dipilih, tambahkan centang dan ubah labelnya
        label = f"✅ {kegiatan}" if is_selected else kegiatan
        
        with kolom_list[i]:
            if st.button(label, key=f"btn_{i}"):
                # Balikkan status (Jika False jadi True, jika True jadi False)
                st.session_state.kegiatan_dipilih[kegiatan] = not is_selected
                st.rerun()
    
    st.markdown("<hr style='border-top: 1px dashed #ddd;'>", unsafe_allow_html=True)
    st.session_state.ide_sendiri = st.text_input("Ada ide tambahan lain? (Ketik di sini) 💡")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Lanjut 🚀"):
        # Menyaring hanya kegiatan yang dipilih (berstatus True)
        st.session_state.kegiatan = [k for k, v in st.session_state.kegiatan_dipilih.items() if v]
        st.session_state.halaman = 6
        st.rerun()

# =====================================================================
# HALAMAN 6: DRESS CODE
# =====================================================================
elif st.session_state.halaman == 6:
    st.markdown("<h2>dress codenya? 👗👔</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    pilihan_baju = ["santai 👕", "cute/imut 🎀", "satu warna 🎨", "rapih/formal 👔", "couple 👫"]
    st.session_state.dresscode = st.radio("Pilih gaya baju kita nanti:", pilihan_baju)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Lanjut 🚀"):
        st.session_state.halaman = 7
        st.rerun()

# =====================================================================
# HALAMAN 7: PESAN UNTUK ANESYI
# =====================================================================
elif st.session_state.halaman == 7:
    st.markdown("<h2>pesan untuk anesyi 💌</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.session_state.pesan_abey = st.text_area("Tulis kata-kata manis atau request khusus buat anesyi:")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Bikin Tiketnya 🎟️"):
        st.session_state.halaman = 8
        st.rerun()

# =====================================================================
# HALAMAN 8: HASIL CETAK TIKET
# =====================================================================
elif st.session_state.halaman == 8:
    st.balloons()
    st.markdown("<h2>🎉 TIKET KENCAN KITA 🎉</h2>", unsafe_allow_html=True)
    
    # Menggabungkan data kegiatan yang dipilih
    list_kegiatan = ", ".join(st.session_state.kegiatan)
    if st.session_state.ide_sendiri:
        if list_kegiatan:
            list_kegiatan += f", {st.session_state.ide_sendiri}"
        else:
            list_kegiatan = st.session_state.ide_sendiri
            
    # Format tanggal & waktu
    tgl_format = st.session_state.tanggal.strftime("%d %B %Y")
    waktu_format = st.session_state.waktu.strftime("%H:%M")
    
    # Desain Tiket dengan HTML
    desain_tiket = f"""
    <div style="border: 4px dashed #ff4b4b; border-radius: 20px; padding: 25px; background-color: #fff0f5; color: #333; margin-top: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #ff4b4b; margin-top: 0; font-size: 28px;">💕 OFFICIAL DATE PASS 💕</h2>
        <div style="font-size: 18px; font-family: 'Comic Neue', cursive;">
            <p><strong>Kepada:</strong> Abey tersayang 🧸</p>
            <p><strong>Dari:</strong> Anesyi 🎀</p>
            <hr style="border-top: 2px dashed #ffb6c1; margin: 15px 0;">
            <p><strong>📅 Hari/Tanggal:</strong> {tgl_format}</p>
            <p><strong>⏰ Waktu:</strong> {waktu_format} WIB</p>
            <p><strong>🎡 Agenda Kita:</strong> {list_kegiatan if list_kegiatan else 'Jalan-jalan random aja!'}</p>
            <p><strong>👗 Dress Code:</strong> {st.session_state.dresscode}</p>
            <hr style="border-top: 2px dashed #ffb6c1; margin: 15px 0;">
            <p><strong>💌 Pesan dari Abey:</strong> <br> <i>"{st.session_state.pesan_abey if st.session_state.pesan_abey else 'Gak sabar ketemu!'}"</i></p>
        </div>
        <h3 style="text-align: center; color: #ff4b4b; margin-top: 30px;">Sampai ketemu, cayangg! ❤️</h3>
    </div>
    """
    st.markdown(desain_tiket, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("Yeay! Tiketnya sudah jadi. Jangan lupa di-screenshot dan kirim ke Anesyi ya! 📸")

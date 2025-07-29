import streamlit as st
from fpdf import FPDF
import os
import base64

# --- Background Gambar ---
with open("images/bg.jpg", "rb") as img_file:
    encoded = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.3);
        z-index: -1;
    }}
    </style>
""", unsafe_allow_html=True)


# Fungsi untuk membuat PDF
class PDF(FPDF):
    def header(self):
        self.image("logo.png", x=10, y=8, w=30)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 30, 'PT. ZTT CABLE INDONESIA', align='C', ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

def generate_pdf(nama, bagian, tanggal_mulai, tanggal_selesai):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Konten Surat
    pdf.multi_cell(0, 10, f"""
                                                                                                         Karawang, {tanggal_selesai}

    Kepada Yth,
    Sdr.{nama}

    Dengan ini PT ZTT Cable Indonesia menyatakan bahwa:
    Nama          : {nama},
    Bagian        : {bagian}.
    Masa Kerja : {tanggal_mulai} sampai dengan {tanggal_selesai}.

    Telah bekerja di perusahaan kami dengan dedikasi dan tanggung jawab yang baik selama masa kerjanya. Dalam periode tersebut, menunjukkan kinerja yang memuaskan, memiliki etos kerja yang tinggi, serta mampu bekerja sama dalam tim maupun individu dengan sangat baik.




                                                                                                               Hormat kami,

                                                                                                          PT ZTT Cable Indonesia
                                                                                                 """)
    return pdf

# Sidebar untuk navigasi
st.sidebar.title("Menu")
menu_option = st.sidebar.radio(
    "Pilih Menu:",
    ("Form Paklaring", "Profil Perusahaan", "Sejarah Perusahaan")
)

# Header
st.markdown(
    """
    <div style="background-color: #D3D3D3; padding: 0px; text-align: center;">
        <h1 style="font-family: 'Times New Roman', serif; font-size: 20px; color: ##ADD8E6; margin: 0;">ASPEKER</h1>
        <p style="font-family: 'Times New Roman', serif; font-size: 18px; color: ##ADD8E6; margin: 2;">
            <strong>Aplikasi Surat Pengalaman Kerja</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


if menu_option == "Form Paklaring":
    # UI Aplikasi
    col1, col2 = st.columns([1, 6])  # Kolom pertama untuk logo, kolom kedua untuk teks

    with col1:
        # Menampilkan logo perusahaan
        st.image("static/logo1.png", width=90)  # Ganti "static/logo1.png" dengan path logo Anda

    with col2:
        # Menampilkan teks "PT. ZTT Cable Indonesia"
        st.markdown(
            """
            <h1 style="font-family: Monospace, sans-serif; font-size: 35px; font-weight: bold; color:blue; margin-bottom: 10px;">
            PT. ZTT Cable Indonesia
            </h1>
            """, unsafe_allow_html=True
        )

    # Menampilkan alamat perusahaan
    st.markdown(
    """
    <div style="text-align: center; font-family: Times New Roman, serif; font-size: 20px; color: #000000; margin-top: 10px;">
        Kawasan Industri Suryacipta VII, Jalan Surya Madya Kav 1-66G1&G2,<br>
        Mulyasari, Kec. Ciampel, Karawang, Jawa Barat 41363<br>
        Telepon: (021) 29337670
    </div>
    <hr style="border: 1px solid #FFFFFF; margin: 20px 0;">
    """,
    unsafe_allow_html=True
)

    st.write("")  # Baris kosong

    st.markdown(
    """
    <div style="text-align: center; font-family: 'Times New Roman', serif; font-size: 20px; color: #000000;">
        Silahkan Input Data Disini
    </div>
    """, unsafe_allow_html=True
)

    st.write("")  # Baris kosong

    # Form Input Data
    with st.form("paklaring_form"):
        nama = st.text_input("Nama Karyawan", placeholder="Masukkan nama karyawan")
        bagian = st.text_input("Bagian Kerja", placeholder="Masukkan bagian kerja")
        tanggal_mulai = st.date_input("Tanggal Mulai Bekerja")
        tanggal_selesai = st.date_input("Tanggal Selesai Bekerja")
        submit = st.form_submit_button("Buat Surat")

    if submit:
        if not nama or not bagian:
            st.error("Nama dan Bagian Kerja harus diisi!")
        else:
            # Generate PDF
            pdf = generate_pdf(
                nama,
                bagian,
                tanggal_mulai.strftime("%d-%m-%Y"),
                tanggal_selesai.strftime("%d-%m-%Y"),
            )
            output_path = f"{nama}_paklaring.pdf"
            pdf.output(output_path)

            # Tampilkan Link Unduhan
            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="Unduh Surat Paklaring",
                    data=file,
                    file_name=output_path,
                    mime="application/pdf",
                )
            st.balloons()
            st.success("Surat berhasil dibuat dan dapat diunduh!", icon="✅")

            # Hapus file setelah diunduh
            os.remove(output_path)

            st.write("")  # Baris kosong
            st.write("")  # Baris kosong
            st.write("")  # Baris kosong
            st.write("")  # Baris kosong

            # Footer
    st.markdown(
        """
        <div style="background-color:#B0B0B0; color: ##ADD8E6; padding:10px; text-align:center; font-family:Times New Roman, serif;">
            <p style="font-size:18px;">Copyright 2024</p>
        </div>
        <hr style="border: 1px solid #FFFFFF; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )

elif menu_option == "Profil Perusahaan":
      # Menampilkan logo perusahaan
    col1, col2 = st.columns([1, 6])  # Kolom pertama untuk logo, kolom kedua untuk teks

    with col1:
        # Menampilkan logo perusahaan
        st.image("static/logo2.png", width=90)  # Ganti dengan path logo perusahaan yang benar

    with col2:
     # Menampilkan teks "PT. ZTT Cable Indonesia"
        st.markdown(
            """
            <h1 style="font-family: Monospace, sans-serif; font-size: 35px; font-weight: bold; color:blue; margin-bottom: 10px;">
            PT. ZTT Cable Indonesia
            </h1>
            """, unsafe_allow_html=True
        )

        # Menampilkan alamat perusahaan
    st.markdown(
    """
    <div style="text-align: center; font-family: Times New Roman, serif; font-size: 20px; color: #000000; margin-top: 10px;">
        Kawasan Industri Suryacipta VII, Jalan Surya Madya Kav 1-66G1&G2,<br>
        Mulyasari, Kec. Ciampel, Karawang, Jawa Barat 41363<br>
        Telepon: (021) 29337670
    </div>
    <hr style="border: 1px solid #FFFFFF; margin: 20px 0;">
    """,
    unsafe_allow_html=True
)

    st.write("")  # Baris kosong

    # Teks
    st.markdown(
    """
    <div style="text-align: center; font-family: 'Times New Roman', serif; font-size: 20px; color: #000000;">
        Profil Perusahaan
    </div>
    """, unsafe_allow_html=True
)

    st.markdown(
    """
    <div style="text-align: justify; font-family: 'Times New Roman', serif; font-size: 18px; color: #000000; margin-top: 20px;">
        <b>PT. ZTT Cable Indonesia</b> adalah perusahaan yang bergerak di bidang manufaktur kabel serat optik, kabel aluminium, serta konduktor. Kami menyediakan solusi kabel untuk berbagai industri, termasuk telekomunikasi, energi, dan infrastruktur lainnya. Sebagai bagian dari ZTT Group, yang berpusat di Tiongkok, perusahaan ini memiliki pengalaman lebih dari 30 tahun dalam menghasilkan produk berkualitas tinggi untuk kebutuhan global.
    </div>
    """, unsafe_allow_html=True
)

    st.write("")  # Baris kosong

    # Teks
    st.markdown(
    """
    <div style="text-align: center; font-family: 'Times New Roman', serif; font-size: 20px; color: #000000;">
        Standar Kualitas Produk
    </div>
    """, unsafe_allow_html=True
)

    st.write("")  # Baris kosong

   # Menampilkan deskripsi Kualitas Produk
    st.markdown(
    """
    <p style="font-family: 'Times New Roman', serif; font-size: 18px; color: #000000; text-align: justify;">
        PT. ZTT Cable Indonesia berkomitmen untuk menyediakan produk kabel berkualitas tinggi yang memenuhi standar internasional. Setiap produk yang kami hasilkan, mulai dari kabel serat optik, kabel aluminium, hingga konduktor, telah melalui serangkaian uji kualitas yang ketat untuk memastikan kinerja dan keandalannya.
    </p>
    """, unsafe_allow_html=True
    )

    st.write("")  # Baris kosong

    # Teks
    st.markdown(
    """
    <div style="text-align: center; font-family: 'Times New Roman', serif; font-size: 20px; color: #000000;">
        Jenis Produk
    </div>
    """, unsafe_allow_html=True
)

    st.write("")  # Baris kosong
    st.write("")  # Baris kosong

    # Menambahkan kolom untuk menampilkan produk
    col1, col2, col3, col4 = st.columns(4)  # Membagi layar menjadi 4 kolom untuk produk

    with col1:
        # Gambar dan penjelasan untuk produk pertama
        st.image("static2/produk1.png", caption="Kabel Serat Optik;")  # Ganti dengan jalur gambar produk 1
        st.markdown(
        """
        <div style="text-align: center; color: #000000;">
            Kabel serat optik berkualitas tinggi untuk transmisi data yang cepat dan handal.
        </div>
        """, unsafe_allow_html=True
    )


    with col2:
        # Gambar dan penjelasan untuk produk kedua
        st.image("static2/produk2.png", caption="Aluminium Rod")  # Ganti dengan jalur gambar produk 2
        st.markdown(
    """
    <div style="text-align: center; color: #000000;">
        Aluminium Rod untuk berbagai aplikasi industri dan konstruksi.
    </div>
    """, unsafe_allow_html=True
)


    with col3:
        # Gambar dan penjelasan untuk produk ketiga
        st.image("static2/produk3.png", caption="Konduktor")  # Ganti dengan jalur gambar produk 3
        st.markdown(
    """
    <div style="text-align: center; color: #000000;">
        Konduktor berkualitas tinggi untuk kebutuhan jaringan listrik dan komunikasi.
    </div>
    """, unsafe_allow_html=True
)


    with col4:
        # Gambar dan penjelasan untuk produk keempat
        st.image("static2/produk4.png", caption="Fiber Optik")  # Ganti dengan jalur gambar produk 4
        st.markdown(
    """
    <div style="text-align: center; color: #000000;">
        Fiber optik digunakan dalam jaringan telekomunikasi untuk mengirimkan sinyal suara, data, dan lain-lain
    </div>
    """, unsafe_allow_html=True
)
        st.write("")  # Baris kosong

        # Teks
    st.markdown(
    """
    <div style="text-align: center; font-family: 'Times New Roman', serif; font-size: 20px; color: #000000;">
        Hubungi Kami
    </div>
    """, unsafe_allow_html=True
)
    st.write("")  # Baris kosong

    # Informasi kontak
    st.markdown(
        """
        <div style="text-align: center; font-family: 'Times New Roman', serif; font-size: 18px; color: #000000;">
            <span style="margin-right: 20px;">Email: indonesia@zttgroup.com</span>
            <span style="margin-right: 20px;">Website: www.zttcable.com</span>
            <span>Telepon: (021) 29337670</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")  # Baris kosong
    st.write("")  # Baris kosong

    # Footer
    st.markdown(
        """
        <div style="background-color:#B0B0B0; color: ##ADD8E6; padding:10px; text-align:center; font-family:Times New Roman, serif;">
            <p style="font-size:18px;">Copyright 2025</p>
        </div>
        <hr style="border: 1px solid #FFFFFF; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )

    # Menambahkan konten Sejarah Berdirinya Perusahaan
elif menu_option == "Sejarah Perusahaan":
      # Menampilkan logo perusahaan
    col1, col2 = st.columns([1, 6])  # Kolom pertama untuk logo, kolom kedua untuk teks

    with col1:
        # Menampilkan logo perusahaan
        st.image("static/logo3.png", width=90)  # Ganti dengan path logo perusahaan yang benar

    with col2:
     # Menampilkan teks "PT. ZTT Cable Indonesia"
        st.markdown(
            """
            <h1 style="font-family: Monospace, sans-serif; font-size: 35px; font-weight: bold; color:blue; margin-bottom: 10px;">
            PT. ZTT Cable Indonesia
            </h1>
            """, unsafe_allow_html=True
        )

        # Menampilkan alamat perusahaan
    st.markdown(
    """
    <div style="text-align: center; font-family: Times New Roman, serif; font-size: 20px; color: #000000; margin-top: 10px;">
        Kawasan Industri Suryacipta VII, Jalan Surya Madya Kav 1-66G1&G2,<br>
        Mulyasari, Kec. Ciampel, Karawang, Jawa Barat 41363<br>
        Telepon: (021) 29337670
    </div>
    <hr style="border: 1px solid #FFFFFF; margin: 20px 0;">
    """,
    unsafe_allow_html=True
)

    st.write("")  # Baris kosong

    # Teks
    st.markdown(
    """
    <div style="text-align: center; font-family: 'Times New Roman', serif; font-size: 20px; color: #000000; width: 250;">
        Sejarah Perusahaan
    </div>
    """, unsafe_allow_html=True
)

    # Menambahkan kolom untuk menampilkan produk
    col1, col2 = st.columns(2)  # Membagi layar menjadi 4 kolom untuk produk

    with col1:
       # Gambar dan penjelasan untuk produk pertama
        st.image("static3/asset.png", caption="")  # Ganti dengan jalur gambar produk 1
        st.markdown(
        """
        <div style="text-align: center;">

        </div>
        """, unsafe_allow_html=True
    )

    with col2:
       # Gambar dan penjelasan untuk produk pertama
        st.image("static3/asset1.png", caption="")  # Ganti dengan jalur gambar produk 1
        st.markdown(
        """
        <div style="text-align: center;">

        </div>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: justify; font-family: 'Times New Roman', serif; font-size: 18px; color: #000000;">
            PT. ZTT Cable Indonesia didirikan pada tahun 2017 sebagai bagian dari ZTT Group yang berpusat di China.
            Perusahaan ini didirikan untuk memenuhi permintaan industri kabel serat optik dan produk kabel lainnya di pasar Indonesia.
            Dengan komitmen untuk memberikan produk berkualitas tinggi dan solusi inovatif, PT. ZTT Cable Indonesia berhasil
            menjadi pemimpin dalam produksi kabel serat optik dan kabel untuk berbagai sektor industri, termasuk telekomunikasi dan energi.
            Seiring dengan pertumbuhan pesat, perusahaan terus memperluas kapasitas produksi dan jangkauan distribusi,
            serta memastikan keberlanjutan dengan penerapan teknologi terbaru dalam setiap proses produksi.
        </div>
        """, unsafe_allow_html=True
    )

    st.write("")  # Baris kosong
    st.write("")  # Baris kosong
    st.write("")  # Baris kosong
    st.write("")  # Baris kosong

     # Footer
    st.markdown(
        """
        <div style="background-color:#B0B0B0; color: ##ADD8E6; padding:10px; text-align:center; font-family:Times New Roman, serif;">
            <p style="font-size:18px;">Copyright 2025</p>
        </div>
        <hr style="border: 1px solid #FFFFFF; margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )

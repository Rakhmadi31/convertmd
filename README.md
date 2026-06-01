# Aplikasi Konversi Dokumen Markdown >< DOCX/DOC/PDF

## Deskripsi
Aplikasi ini adalah antarmuka Streamlit untuk mengonversi file Markdown (`.md`) ke file `.docx`, `.doc`, atau `.pdf`, serta mengonversi file `.docx`, `.doc`, dan `.pdf` kembali ke Markdown (`.md`). Konversi dilakukan menggunakan Pandoc sebagai mesin standar untuk memastikan kompatibilitas dokumen yang baik.

## Fitur Utama
- Unggah file `.md`, `.docx`, `.doc`, atau `.pdf`
- Pilih format konversi yang diinginkan
- Unduh hasil konversi langsung melalui browser

## Persyaratan
- Python 3.x
- Streamlit terinstal
- Pandoc terinstal di sistem

## Cara Menjalankan
1. Aktifkan environment Python Anda.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run konvertmd.py
   ```
4. Buka URL yang ditampilkan di browser.
5. Unggah file dan pilih format konversi.

## Catatan
- Pastikan Pandoc terpasang secara native di sistem Anda. Paket Python `pandoc` tidak cukup karena aplikasi memanggil binary `pandoc`.
- Untuk konversi PDF, aplikasi menggunakan `xelatex` bila tersedia. Pastikan TeX engine seperti `texlive-xetex`/`texlive-latex-recommended` terpasang.
- Tabel PDF sekarang diproses dengan filter Pandoc khusus agar isi sel panjang dibungkus (wrap text) sehingga tabel tidak saling tumpang tindih.

## About
Aplikasi ini cocok untuk penggunaan akademik dan profesional, membantu mengonversi dokumen dengan cepat dan memudahkan proses kolaborasi lintas format.

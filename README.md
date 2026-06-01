# Aplikasi Konversi Dokumen Markdown ↔️ DOCX

## Deskripsi
Aplikasi ini adalah antarmuka Streamlit untuk mengonversi file Markdown (`.md`) ke file `.docx`, serta mengonversi file `.docx` dan `.doc` kembali ke Markdown (`.md`). Konversi dilakukan menggunakan Pandoc sebagai mesin standar untuk memastikan kompatibilitas dokumen.

## Fitur Utama
- Unggah file `.md`, `.docx`, atau `.doc`
- Pilih format konversi yang diinginkan
- Unduh hasil konversi langsung melalui browser
- Pilihan bahasa UI: Bahasa Indonesia dan English

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
- Aplikasi saat ini hanya mendukung `.docx` sebagai output Word. Format `.doc` lama tidak disediakan sebagai output.
- Di Streamlit Community Cloud, dukungan TeX/PDF sering terbatas, jadi fokus aplikasi adalah konversi Markdown ↔ DOCX.

## About
Aplikasi ini cocok untuk penggunaan akademik dan profesional, membantu mengonversi dokumen dengan cepat dan memudahkan proses kolaborasi lintas format.

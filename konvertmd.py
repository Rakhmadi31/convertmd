import streamlit as st
from pathlib import Path
import tempfile
import shutil

pandoc_path = shutil.which("pandoc")
pandoc_available = pandoc_path is not None

# Detect availability of TeX engines for PDF generation
tex_engine = shutil.which("xelatex") or shutil.which("pdflatex")
pdf_engine_available = tex_engine is not None

def convert_file(
    uploaded_file, 
    to_format: str, 
    save_dir: Path
):
    import subprocess
    output_path = save_dir / f"{uploaded_file.name.split('.')[0]}.{to_format}"
    # Write uploaded file to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
        tmp.write(uploaded_file.read())
        tmp.flush()
        input_path = tmp.name

        pandoc_path = shutil.which("pandoc")
        if pandoc_path is None:
            st.error(
                "Pandoc tidak ditemukan. "
                "Pasang Pandoc secara native di sistem Anda terlebih dahulu. "
                "Contoh: `sudo apt install pandoc` atau lihat https://pandoc.org/installing.html"
            )
            return None

        try:
            cmd = [pandoc_path, input_path, "-o", str(output_path)]
            if to_format == "pdf":
                xelatex_path = shutil.which("xelatex")
                if xelatex_path:
                    cmd.extend(["--pdf-engine=xelatex"])
                else:
                    cmd.extend(["--pdf-engine=pdflatex"])

                lua_filter = Path(__file__).parent / "pandoc_wrap_tables.lua"
                if lua_filter.exists():
                    cmd.extend(["--lua-filter", str(lua_filter)])

            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
            return output_path
        except subprocess.CalledProcessError as e:
            message = e.stderr.strip() if e.stderr else str(e)
            st.error(f"Gagal mengonversi file: {message}")
            return None
        except FileNotFoundError:
            st.error(
                "Pandoc tidak ditemukan. "
                "Pastikan executable `pandoc` tersedia di PATH sistem Anda."
            )
            return None

st.set_page_config(page_title="Konversi File MD <-> DOCX / PDF", page_icon="📝")
st.title("Aplikasi Konversi File: Markdown ↔️ DOCX/DOC/PDF")

st.markdown("""
**Fitur:**  
- Konversi file _Markdown_ (`.md`) ke `.docx`, `.doc`, atau `.pdf`
- Konversi file `.docx`, `.doc`, dan `.pdf` ke _Markdown_ (`.md`)
- Antarmuka sederhana, cocok untuk akademisi & profesional

**Metodologi:**  
Konversi memanfaatkan _Pandoc_ untuk memastikan kompatibilitas format dokumen (justifikasi: pandoc adalah perangkat lunak standar konversi dokumen bereputasi dan mendukung metodologi replikasi penelitian, _validitas_ dan _reliabilitas_ konversi tinggi).
""")

tab_upload, tab_about = st.tabs(["Konversi File", "Tentang"])

with tab_upload:
    uploaded_file = st.file_uploader("Unggah file (.md, .docx, .doc, .pdf):", type=['md', 'docx', 'doc', 'pdf'])
    col1, col2 = st.columns(2)

    if uploaded_file:
        st.write("**Nama File:**", uploaded_file.name)
        file_ext = uploaded_file.name.split(".")[-1].lower()
        formats_to = []
        if file_ext == "md":
            formats_to = ["docx"]
            if pdf_engine_available:
                formats_to.append("pdf")
        elif file_ext in ["docx", "doc", "pdf"]:
            formats_to = ["md"]
        else:
            st.error("Tipe file tidak didukung.")
        
        with col1:
            if formats_to:
                to_format = st.selectbox("Konversi ke format:", formats_to)
                if pandoc_available:
                    convert_btn = st.button("Konversi")
                else:
                    st.button("Konversi", disabled=True)
        with col2:
            if pandoc_available:
                if not pdf_engine_available:
                    st.info("Konversi ke PDF dinonaktifkan: TeX engine (xelatex/pdflatex) tidak tersedia di server.")
                else:
                    st.write("")
            else:
                st.warning(
                    "Pandoc tidak ditemukan di sistem Anda. "
                    "Silakan instal Pandoc secara native dengan mengikuti panduan resmi di https://pandoc.org/installing.html. "
                    "Catatan: `pip install pandoc` tidak menginstal executable Pandoc."
                )
        
        if 'convert_btn' in locals() and convert_btn:
            with st.spinner("Mengonversi..."):
                save_dir = Path(tempfile.gettempdir())
                converted = convert_file(uploaded_file, to_format, save_dir)
                if converted and converted.exists():
                    st.success(f"Konversi berhasil ke {converted.suffix.upper()[1:]}")
                    with open(converted, "rb") as f:
                        st.download_button(
                            label=f"Unduh {converted.name}",
                            data=f.read(),
                            file_name=converted.name
                        )
                elif not pandoc_available:
                    st.error(
                        "Konversi gagal karena Pandoc tidak tersedia. "
                        "Silakan instal Pandoc terlebih dahulu dan muat ulang aplikasi."
                    )
    else:
        st.info("Silakan unggah file terlebih dahulu.")

with tab_about:
    st.header("Penjelasan Akademik")
    st.markdown("""
- **Metode:**  
  Proses konversi dokumen berbasis framework _Pandoc_, yang mendukung interoperabilitas multi-format dokumen ilmiah dan sesuai standar akademik internasional (Chicago Notes-Bibliography, PUEBI).
- **Justifikasi Metodologis:**  
  Pandoc dipilih karena _reliable_, _open-source_, memungkinkan pelacakan perubahan (_traceability_) dan _repeatability_ riset.
- **Keterbatasan:**  
  Format sangat kompleks (mis: tabel besar, gambar tersemat, formula matematika tingkat lanjut) bisa memerlukan validasi hasil konversi manual.
- **Referensi:**  
  - Pandoc User's Guide: https://pandoc.org/MANUAL.html

**Saran Pengembangan:**
- Integrasi dengan pengenalan metadata otomatis untuk bibliometrik.
- Penambahan fitur pratinjau hasil.
- Pengembangan pipeline batch processing untuk riset skala besar.

_Dikembangkan sesuai etika akademik oleh Rakhmadi Irfansyah Putra_.
""")
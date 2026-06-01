import streamlit as st
from pathlib import Path
import tempfile
import shutil
import subprocess

pandoc_path = shutil.which("pandoc")
pandoc_available = pandoc_path is not None


# --- Bilingual strings (id/en) ---
TEXT = {
    "id": {
        "page_title": "Konversi File MD <-> DOCX",
        "title": "Aplikasi Konversi File: Markdown ↔️ DOCX/DOC",
        "features": """
**Fitur:**  
- Konversi file _Markdown_ (`.md`) ke `.docx`
- Konversi file `.docx` dan `.doc` ke _Markdown_ (`.md`)
- Antarmuka sederhana, cocok untuk akademisi & profesional

**Metodologi:**  
Konversi memanfaatkan _Pandoc_ untuk memastikan kompatibilitas format dokumen.
""",
        "upload_label": "Unggah file (.md, .docx, .doc):",
        "file_name": "Nama File:",
        "type_not_supported": "Tipe file tidak didukung.",
        "convert_to": "Konversi ke format:",
        "convert_btn": "Konversi",
        "pandoc_missing": (
            "Pandoc tidak ditemukan di sistem Anda. "
            "Silakan instal Pandoc secara native: https://pandoc.org/installing.html"
        ),
        "converting": "Mengonversi...",
        "convert_success": "Konversi berhasil ke",
        "convert_failed": "Konversi gagal karena Pandoc tidak tersedia. Silakan instal Pandoc terlebih dahulu dan muat ulang aplikasi.",
        "download": "Unduh",
        "about_header": "Penjelasan Akademik",
        "upload_first": "Silakan unggah file terlebih dahulu.",
        "about_md": """
- **Metode:**  
-  Proses konversi dokumen berbasis framework _Pandoc_, yang mendukung interoperabilitas multi-format dokumen ilmiah dan sesuai standar akademik internasional (Chicago Notes-Bibliography, PUEBI).
- **Justifikasi Metodologis:**  
-  Pandoc dipilih karena _reliable_, _open-source_, memungkinkan pelacakan perubahan (_traceability_) dan _repeatability_ riset.
- **Keterbatasan:**  
-  Format sangat kompleks (mis: tabel besar, gambar tersemat, formula matematika tingkat lanjut) bisa memerlukan validasi hasil konversi manual.
- **Referensi:**  
-  - Pandoc User's Guide: https://pandoc.org/MANUAL.html
-
-**Saran Pengembangan:**
-- Integrasi dengan pengenalan metadata otomatis untuk bibliometrik.
-- Penambahan fitur pratinjau hasil.
-- Pengembangan pipeline batch processing untuk riset skala besar.
-
-_Dikembangkan sesuai etika akademik oleh Rakhmadi Irfansyah Putra_.
""",
    },
    "en": {
        "page_title": "Convert MD <-> DOCX",
        "title": "File Conversion App: Markdown ↔️ DOCX/DOC",
        "features": """
**Features:**
- Convert _Markdown_ (`.md`) to `.docx`
- Convert `.docx` and `.doc` to _Markdown_ (`.md`)
- Simple interface, suitable for academics & professionals

**Methodology:**
Conversion uses Pandoc to ensure document format compatibility.
""",
        "upload_label": "Upload file (.md, .docx, .doc):",
        "file_name": "File Name:",
        "type_not_supported": "File type not supported.",
        "convert_to": "Convert to format:",
        "convert_btn": "Convert",
        "pandoc_missing": (
            "Pandoc not found on the system. "
            "Please install Pandoc natively: https://pandoc.org/installing.html"
        ),
        "converting": "Converting...",
        "convert_success": "Conversion succeeded to",
        "convert_failed": "Conversion failed because Pandoc is not available. Please install Pandoc and reload the app.",
        "download": "Download",
        "about_header": "Academic Notes",
        "upload_first": "Please upload a file first.",
        "about_md": """
- **Methodology:**  
-  The conversion pipeline uses Pandoc to support multi-format document interoperability.
- **References:**  
-  - Pandoc User's Guide: https://pandoc.org/MANUAL.html
-
-_Developed with academic ethics by Rakhmadi Irfansyah Putra_.
""",
    },
}

# language selection key: 'id' or 'en'
lang = st.sidebar.selectbox("Language / Bahasa", options=["id", "en"], index=0)
T = TEXT[lang]


def convert_file(
    uploaded_file,
    to_format: str,
    save_dir: Path,
):
    output_path = save_dir / f"{Path(uploaded_file.name).stem}.{to_format}"
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
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
            return output_path
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.strip() if e.stderr else ""
            stdout = e.stdout.strip() if e.stdout else ""
            message = stderr or stdout or str(e)
            if stderr and stdout:
                message = f"{stderr}\n{stdout}"
            st.error(f"Gagal mengonversi file: exit code {e.returncode}. {message}")
            return None
        except FileNotFoundError:
            st.error(
                "Pandoc tidak ditemukan. "
                "Pastikan executable `pandoc` tersedia di PATH sistem Anda."
            )
            return None


st.set_page_config(page_title=T["page_title"], page_icon="📝")
st.title(T["title"])

st.markdown(T["features"])

tab_upload, tab_about = st.tabs(["Konversi File", "Tentang"])

with tab_upload:
    uploaded_file = st.file_uploader(T["upload_label"], type=["md", "docx", "doc"])
    col1, col2 = st.columns(2)

    if uploaded_file:
        st.write("**" + T["file_name"] + "**", uploaded_file.name)
        file_ext = uploaded_file.name.split(".")[-1].lower()
        formats_to = []
        if file_ext == "md":
            formats_to = ["docx"]
        elif file_ext in ["docx", "doc"]:
            formats_to = ["md"]
        else:
            st.error(T["type_not_supported"])

        with col1:
            if formats_to:
                to_format = st.selectbox(T["convert_to"], formats_to)
                if pandoc_available:
                    convert_btn = st.button(T["convert_btn"])
                else:
                    st.button(T["convert_btn"], disabled=True)
        with col2:
            if pandoc_available:
                st.write("")
            else:
                st.warning(T["pandoc_missing"]) 

        if 'convert_btn' in locals() and convert_btn:
            with st.spinner(T["converting"]):
                save_dir = Path(tempfile.gettempdir())
                converted = convert_file(uploaded_file, to_format, save_dir)
                if converted and converted.exists():
                    st.success(f"{T['convert_success']} {converted.suffix.upper()[1:]}")
                    with open(converted, "rb") as f:
                        st.download_button(
                            label=f"{T['download']} {converted.name}",
                            data=f.read(),
                            file_name=converted.name,
                        )
                elif not pandoc_available:
                    st.error(T["convert_failed"]) 
    else:
        st.info(T["upload_first"])

with tab_about:
    st.header(T["about_header"])
    st.markdown(T["about_md"]) 

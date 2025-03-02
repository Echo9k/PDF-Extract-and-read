# pdf_processor.py
import os
import time
from pathlib import Path
import uuid
import logging
import pymupdf

from magic_pdf.data.data_reader_writer import FileBasedDataReader
from magic_pdf.libs.hash_utils import compute_sha256
from magic_pdf.tools.common import do_parse, prepare_env
from utils import compress_directory_to_zip, replace_image_with_base64


def read_fn(path):
    disk_rw = FileBasedDataReader(os.path.dirname(path))
    return disk_rw.read(os.path.basename(path))

def parse_pdf(doc_path, output_dir, end_page_id, is_ocr, layout_mode, formula_enable, table_enable, language):
    """
    Parse the PDF using the specified parameters.
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        file_name = f"{Path(doc_path).stem}_{int(time.time())}"
        pdf_data = read_fn(doc_path)
        parse_method = "ocr" if is_ocr else "auto"
        local_image_dir, local_md_dir = prepare_env(output_dir, file_name, parse_method)
        do_parse(
            output_dir,
            file_name,
            pdf_data,
            [],
            parse_method,
            False,
            end_page_id=end_page_id,
            layout_model=layout_mode,
            formula_enable=formula_enable,
            table_enable=table_enable,
            lang=language,
            f_dump_orig_pdf=False,
        )
        return local_md_dir, file_name
    except Exception as e:
        logging.exception("Error in parse_pdf: %s", e)
        raise

def to_pdf(file_path):
    """
    Ensures the file is in PDF format. Converts if necessary.
    """
    with pymupdf.open(file_path) as f:
        if f.is_pdf:
            return file_path
        else:
            pdf_bytes = f.convert_to_pdf()
            unique_filename = f"{uuid.uuid4()}.pdf"
            tmp_file_path = os.path.join(os.path.dirname(file_path), unique_filename)
            with open(tmp_file_path, 'wb') as tmp_pdf_file:
                tmp_pdf_file.write(pdf_bytes)
            return tmp_file_path

def to_markdown(file_path, end_pages, is_ocr, layout_mode, formula_enable, table_enable, language, output_dir="./output"):
    """
    Converts the PDF to markdown and compresses the result.
    """
    file_path = to_pdf(file_path)
    end_pages = min(end_pages, 20)
    local_md_dir, file_name = parse_pdf(file_path, output_dir, end_pages - 1, is_ocr, layout_mode, formula_enable, table_enable, language)
    archive_zip_path = os.path.join(output_dir, compute_sha256(local_md_dir) + ".zip")
    if compress_directory_to_zip(local_md_dir, archive_zip_path):
        logging.info("Compression successful")
    else:
        logging.error("Compression failed")
    md_path = os.path.join(local_md_dir, f"{file_name}.md")
    with open(md_path, 'r', encoding='utf-8') as f:
        txt_content = f.read()
    md_content = replace_image_with_base64(txt_content, local_md_dir)
    new_pdf_path = os.path.join(local_md_dir, f"{file_name}_layout.pdf")
    return md_content, txt_content, archive_zip_path, new_pdf_path

def file_to_pdf(file_obj):
    if file_obj is not None:
        try:
            pdf_path = to_pdf(file_obj.name)
            log_info("File converted to PDF successfully.")
            return pdf_path
        except Exception as e:
            log_error(f"Error converting file to PDF: {e}")
    return None
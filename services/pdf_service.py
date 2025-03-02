# services/pdf_service.py
import os
import fitz  # pymupdf for PDF metadata extraction
from pdf_processor import to_markdown
from utils import compress_directory_to_zip

def process_pdf(file, max_pages, is_ocr, layout_mode, formula_enable, table_enable, language, output_dir="./output"):
    """
    Process the uploaded file:
      - Save the file to a temporary directory.
      - Convert it to PDF and then to Markdown.
      - Extract metadata from the processed PDF.
    Returns markdown content, raw markdown text, archive zip path, new PDF path, and metadata.
    """
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    
    # Save the uploaded file locally.
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    
    try:
        # Use your existing to_markdown function.
        md_content, md_text, archive_zip_path, new_pdf_path = to_markdown(
            temp_path, max_pages, is_ocr, layout_mode, formula_enable, table_enable, language, output_dir
        )
        
        # Extract metadata from the new PDF.
        metadata = extract_metadata(new_pdf_path)
    finally:
        # Clean up temporary file.
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return md_content, md_text, archive_zip_path, new_pdf_path, metadata

def extract_metadata(pdf_path):
    """
    Extract metadata from a PDF using pymupdf (fitz).
    Returns a dictionary with metadata and page count.
    """
    try:
        doc = fitz.open(pdf_path)
        meta = doc.metadata  # standard metadata from the PDF
        meta["page_count"] = doc.page_count
        doc.close()
        return meta
    except Exception as e:
        return {"error": str(e)}

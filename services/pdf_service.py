import os
import re
import fitz  # PyMuPDF
import logging
from collections import Counter
from pdf_processor import to_markdown

def convert_pdf_to_markdown(file_path: str, end_pages: int, is_ocr: bool,
                            layout_mode: str, formula_enable: bool, table_enable: bool,
                            language: str, output_dir: str = "./output"):
    """
    Converts the PDF to markdown using the existing pdf_processor.to_markdown function.
    """
    return to_markdown(file_path, end_pages, is_ocr, layout_mode, formula_enable, table_enable, language, output_dir)

def extract_pdf_metadata(file_path: str, top_k: int = 5) -> dict:
    """
    Opens a PDF file, extracts metadata (including page count) and computes top k keywords.
    """
    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata or {}
        metadata["page_count"] = doc.page_count

        # Extract text from all pages
        all_text = ""
        for page in doc:
            all_text += page.get_text()

        # Tokenize and filter out basic stopwords
        tokens = re.findall(r'\w+', all_text.lower())
        stopwords = {
            "the", "and", "to", "of", "a", "in", "for", "is",
            "on", "that", "with", "as", "at", "by", "an"
        }
        filtered_tokens = [word for word in tokens if word not in stopwords and len(word) > 2]
        counter = Counter(filtered_tokens)
        top_keywords = counter.most_common(top_k)

        return {"metadata": metadata, "top_keywords": top_keywords}
    except Exception as e:
        logging.exception("Error extracting PDF metadata: %s", e)
        raise


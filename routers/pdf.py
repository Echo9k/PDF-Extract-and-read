from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import tempfile
import os
import logging

from services.pdf_service import convert_pdf_to_markdown, extract_pdf_metadata

router = APIRouter(prefix="/pdf", tags=["PDF Processing"])

@router.post("/convert")
async def convert_pdf(
    file: UploadFile = File(...),
    end_pages: int = Form(10),
    is_ocr: bool = Form(False),
    layout_mode: str = Form("auto"),
    formula_enable: bool = Form(False),
    table_enable: bool = Form(False),
    language: str = Form("auto")
):
    """
    Convert an uploaded PDF file to Markdown.
    """
    try:
        # Save the uploaded file to a temporary file.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Convert PDF to markdown using the service.
        md_content, txt_content, archive_zip_path, new_pdf_path = convert_pdf_to_markdown(
            tmp_path, end_pages, is_ocr, layout_mode, formula_enable, table_enable, language
        )
        os.remove(tmp_path)
        return {
            "markdown_content": md_content,
            "text_content": txt_content,
            "archive_zip_path": archive_zip_path,
            "new_pdf_path": new_pdf_path
        }
    except Exception as e:
        logging.exception("Error processing PDF: %s", e)
        raise HTTPException(status_code=500, detail="PDF processing failed.")

@router.post("/metadata")
async def get_metadata(
    file: UploadFile = File(...),
    top_k: int = Form(5)
):
    """
    Extract metadata and top k keywords from an uploaded PDF file.
    """
    try:
        # Save the uploaded file to a temporary file.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Extract metadata and keywords using the service.
        result = extract_pdf_metadata(tmp_path, top_k)
        os.remove(tmp_path)
        return result
    except Exception as e:
        logging.exception("Error extracting metadata: %s", e)
        raise HTTPException(status_code=500, detail="Metadata extraction failed.")

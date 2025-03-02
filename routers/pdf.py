from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from services.pdf_service import process_pdf, extract_pdf_metadata

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    max_pages: int = Form(10),
    is_ocr: bool = Form(False),
    layout_mode: str = Form("layoutlmv3"),
    formula_enable: bool = Form(True),
    table_enable: bool = Form(True),
    language: str = Form("auto")
):
    try:
        markdown_text, metadata = process_pdf(
            file=file,
            max_pages=max_pages,
            is_ocr=is_ocr,
            layout_mode=layout_mode,
            formula_enable=formula_enable,
            table_enable=table_enable,
            language=language
        )
        return JSONResponse(content={"markdown": markdown_text, "metadata": metadata})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing error: {e}")

@router.get("/metadata")
async def get_pdf_metadata(file_path: str):
    try:
        metadata = extract_pdf_metadata(file_path)
        return JSONResponse(content={"metadata": metadata})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metadata extraction error: {e}")

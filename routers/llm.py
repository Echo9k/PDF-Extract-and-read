# routers/llm.py
from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import JSONResponse
from services.llm_service import correct_text_with_llm

router = APIRouter(prefix="/llm", tags=["LLM"])

@router.post("/correct")
async def correct_text(text: str = Form(...)):
    try:
        corrected_text = correct_text_with_llm(text)
        return JSONResponse(content={"corrected_text": corrected_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text correction: {e}")

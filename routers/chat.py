# routers/chat.py
from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import JSONResponse
from services.chat_service import query_chatbot

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/query")
async def chat_query(user_query: str = Form(...)):
    try:
        result = query_chatbot(user_query)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat query: {e}")

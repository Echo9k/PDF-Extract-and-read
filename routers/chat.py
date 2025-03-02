from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatQuery(BaseModel):
    query: str

@router.post("/query")
async def chat_query(request: ChatQuery):
    """
    Query the chatbot with a text query.
    """
    try:
        # Here you would integrate with your chat_service (ElasticSearch and LangChain)
        # For now, return a placeholder response.
        response = {
            "query": request.query,
            "response": f"Response to '{request.query}' from chatbot."
        }
        return response
    except Exception as e:
        logging.exception("Error processing chat query: %s", e)
        raise HTTPException(status_code=500, detail="Chat processing failed.")

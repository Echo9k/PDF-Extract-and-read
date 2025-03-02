from fastapi import FastAPI
from routers import pdf, llm, chat

app = FastAPI(title="PDF Chatbot API")

app.include_router(pdf.router)
app.include_router(llm.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

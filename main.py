import uvicorn
from fastapi import FastAPI
from app.routers import upload, chat, risks, analysis

app = FastAPI(title="Projeto RAG")

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(risks.router)
app.include_router(analysis.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)

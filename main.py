import uvicorn
from fastapi import FastAPI
from app.routers import upload

app = FastAPI(title="Projeto RAG")

app.include_router(upload.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)

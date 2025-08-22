import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_core.documents import Document
# Imports de funções dos seus outros arquivos
from app.ia.agents.agent_embedding import create_embeddings
from pydantic import BaseModel
from app.ia.utils import query_embedding, query_chat_history
from datetime import datetime
import time

router = APIRouter(prefix="/chat", tags=["Chat"])



class QueryRequest(BaseModel):
    query: str
    chat_id: str


@router.post("/question")
def query_document(request: QueryRequest):
    start_time = time.time()


    # Explicitly embed the query using embed_query

    chat_history_db = query_chat_history()

    response = query_embedding(pergunta=request.query, chat_id=request.chat_id, chat_history_db=chat_history_db)

    print(f"Resposta: {response['answer']}")

    chat_history_doc = Document(
            page_content=f"Usuário: {request.query}\nIA: {response['answer']}",
            metadata={"chat_id": request.chat_id, "user": request.query, "ai": response['answer'],
                      "timestamp": datetime.now().isoformat()}
    )
    chat_history_db.add_documents([chat_history_doc])

    print(f"Tempo: {time.time() - start_time} segundos")
    return {"answer": response['answer']}

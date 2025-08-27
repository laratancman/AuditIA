import time
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.documents import Document

# <<< CORREÇÃO: Importa a função corrigida de agent_conversation
from app.ia.agents.agent_conversation import generate_embedding_response
# <<< CORREÇÃO: Importa os bancos de dados de vetores
from app.ia.utils import pg_vector, query_chat_history

router = APIRouter(prefix="/chat", tags=["Chat"])

class QueryRequest(BaseModel):
    query: str
    chat_id: str

@router.post("/question")
def query_document(request: QueryRequest):
    start_time = time.time()
    
    chat_history_db = query_chat_history()
    # TODO: Implementar a lógica para buscar e formatar o histórico da conversa
    # Por enquanto, usaremos uma string vazia como placeholder
    formatted_history = ""

    # <<< CORREÇÃO: Chama a função corrigida, passando o banco de vetores principal (pg_vector)
    response = generate_embedding_response(
        db_retriever=pg_vector, 
        query=request.query, 
        history=formatted_history
    )

    # <<< CORREÇÃO CRÍTICA: Verifica se a resposta é válida antes de usá-la
    if not response or 'answer' not in response:
        raise HTTPException(status_code=500, detail="Erro ao obter resposta da IA.")

    # Se a verificação passar, podemos usar a resposta com segurança
    answer = response['answer']
    print(f"Resposta: {answer}")

    # Salva a interação no histórico
    chat_history_doc = Document(
        page_content=f"Usuário: {request.query}\nIA: {answer}",
        metadata={
            "chat_id": request.chat_id, 
            "user": request.query, 
            "ai": answer,
            "timestamp": datetime.now().isoformat()
        }
    )
    chat_history_db.add_documents([chat_history_doc])

    print(f"Tempo: {time.time() - start_time} segundos")
    
    return {"answer": answer}
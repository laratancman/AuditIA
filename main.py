import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- 1. Importar o CORSMiddleware

from app.routers import upload, analysis
from app.schemas import Base
from database import engine

# Esta linha é a responsável por criar a tabela "documents"
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Projeto AuditIA - Arquitetura Final")

# --- NOVO CÓDIGO PARA CORRIGIR O ERRO DE CORS ---

# 2. Definir as origens permitidas.
#    Esta é a lista de URLs do frontend que podem acessar sua API.
origins = [
    "http://localhost:3001",  # A origem do seu frontend
    "http://localhost",
    "http://localhost:3000", # Adicione outras portas se necessário (ex: React usa 3000)
]

# 3. Adicionar o middleware de CORS à aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite as origens especificadas
    allow_credentials=True, # Permite cookies (importante para autenticação)
    allow_methods=["*"],    # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],    # Permite todos os cabeçalhos
)
# --- FIM DO CÓDIGO DE CORS ---


# Rota para adicionar documentos à base
app.include_router(upload.router)

# Rota para analisar um documento existente na base
app.include_router(analysis.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
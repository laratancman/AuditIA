# Em app/ia/vectorstore.py

import asyncio
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from config import GEMINI_API_KEY
from database import DATABASE_URL

COLLECTION_NAME = "auditia_docs"

def get_google_embeddings():
    """
    Inicializa e retorna o modelo de embeddings do Google Gemini.
    """
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", 
        google_api_key=GEMINI_API_KEY
    )

async def _aingest_documents_async(documents: list[Document]):
    """
    Função auxiliar assíncrona que realiza a ingestão de forma nativa.
    """
    embeddings_model = get_google_embeddings()

    # Usamos o método assíncrono 'afrom_documents' do PGVector
    await PGVector.afrom_documents(
        documents=documents,
        embedding=embeddings_model,
        collection_name=COLLECTION_NAME,
        connection_string=DATABASE_URL,
    )

def ingest_documents(documents: list[Document]):
    """
    Função síncrona que o endpoint chama.
    Ela cria um event loop temporário para rodar a lógica assíncrona.
    """
    if not documents:
        print("Nenhum documento para ingerir.")
        return

    try:
        # asyncio.run() cria um novo event loop, executa nossa função async, e o fecha.
        asyncio.run(_aingest_documents_async(documents))
        print(f"{len(documents)} chunks foram processados e salvos no Vector Store.")
    except Exception as e:
        print(f"Erro durante a ingestão assíncrona de documentos: {e}")
        raise e

def init_vectorstore():
    """
    Inicializa uma conexão com um Vector Store existente para fazer buscas.
    """
    embeddings_model = get_google_embeddings()
    return PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=DATABASE_URL,
        embedding_function=embeddings_model
    )
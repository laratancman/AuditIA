# Em app/ia/vectorstore.py

import asyncio
from ..models import google_embedding
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from config import GEMINI_API_KEY
from database import DATABASE_URL
from app.ia.utils import chunk_split

COLLECTION_NAME = "auditia_docs"


async def _aingest_documents_async(documents: list[Document]):
    """
    Função auxiliar assíncrona que realiza a ingestão de forma nativa.
    """

    # Usamos o método assíncrono 'afrom_documents' do PGVector
    await PGVector.afrom_documents(
        documents=documents,
        embedding=google_embedding,
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

def create_embeddings(pdf_text, s3_url):

    text_chunks = chunk_split(pdf_text)

    documents_to_ingest = [
        Document(page_content=chunk, metadata={"source": s3_url})
        for chunk in text_chunks
    ]

    ingest_documents(documents_to_ingest)

    return len(documents_to_ingest)
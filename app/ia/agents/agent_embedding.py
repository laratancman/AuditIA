# Em app/ia/vectorstore.py

import asyncio
from ..models import google_embedding
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
from config import GEMINI_API_KEY
from database import DATABASE_URL
from app.ia.utils import chunk_split, clean_text_data, pg_vector

COLLECTION_NAME = "auditia_docs"

def create_embeddings(pdf_pages, file_name):

    documents = [
        Document(
            page_content=clean_text_data(page.page_content),
            metadata={
                "page_number": idx + 1,
                "file_name": file_name
            }
        )
        for idx, page in enumerate(pdf_pages)
    ]

    pg_vector.add_documents(documents)

from langchain_community.vectorstores import PGVector
from langchain.schema import Document
from database import engine, sessionmaker, DATABASE_URL
from models import google_embedding
# Iniciar o vectorstore
def init_vectorstore(collection_name="embeddings"):
    return PGVector(
        connection_string=DATABASE_URL,
        collection_name=collection_name,
        embedding_function=google_embedding
    )

def ingest_documents(chunks, metadatas, vectorstore):
    docs = [Document(page_content=chunk, metadata=md) for chunk, md in zip(chunks, metadatas)]
    vectorstore.add_documents(docs)


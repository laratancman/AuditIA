import os

import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION, AWS_S3_BUCKET, DATABASE_URL
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .models import google_embedding
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import PyPDFLoader


s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION
)

pg_vector = PGVector(
    embeddings=google_embedding,
    collection_name="auditia_docs",
    connection=DATABASE_URL,
    use_jsonb=True
)

pg_vector.create_tables_if_not_exists()


def check_s3(s3):
    try:
        s3.head_bucket(Bucket=AWS_S3_BUCKET)
        print("S3 está online e funcional")
    except ClientError as e:
        print("Erro ao conectar ao S3:", e)

def upload_file(file_path, key):
    s3.upload_file(file_path, AWS_S3_BUCKET, key)
    return f"https://{AWS_S3_BUCKET}.s3.{AWS_S3_REGION}.amazonaws.com/{key}"

def read_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    os.remove(file_path)
    return pages

def chunk_split(text, chunk_size=500, chunk_overlap=50):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    return splitter.split_text(text)

def query_embedding(pergunta, chat_id, chat_history_db):
    query_embedding = google_embedding.embed_query(pergunta)

    # Perform similarity search using the embedded query
    results = pg_vector.similarity_search_with_score_by_vector(embedding=query_embedding, k=10)

    files = [result[0].metadata["file_name"] for result in results]
    pages = [result[0].metadata["page_number"] for result in results]
    vectors = [result[1] for result in results]

    print(f"Documentos: {files} - Páginas: {pages}")
    print(f"Vetores das respostas mais próximas: {vectors}")
    if results:
        print(f"Documentos próximos: {results[0][0].page_content}")

    context = ""
    for doc, score in results:
        context += f"Arquivo: {doc.metadata['file_name']}\nPágina: {doc.metadata['page_number']}\nTexto: {doc.page_content}\n\n"

    history = ""
    conversation_history = chat_history_db.similarity_search_with_score(
        query=pergunta, k=3, filter={"chat_id": chat_id}
    )
    for history_doc, score in conversation_history:
        history += f"Usuário: {history_doc.metadata['user']}\nIA: {history_doc.metadata['ai']}\n\n"

def query_chat_history():
    return PGVector(
        embeddings=google_embedding,
        collection_name="chat_history",
        connection=DATABASE_URL,
        use_jsonb=True
    )

def clean_text_data(text):
    if text is not None:
        return text.replace('\x00', '').encode('utf-8').decode('utf-8')
    return text
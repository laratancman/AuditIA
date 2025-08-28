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
    # A remoção do arquivo foi movida para o bloco 'finally' nos routers para mais segurança
    return pages

def chunk_split(text, chunk_size=500, chunk_overlap=50):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return splitter.split_text(text)

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

# --- NOVA FUNÇÃO ADICIONADA ---
def get_full_text_by_filename(file_name: str) -> str:
    """
    Busca todos os chunks de um documento no banco de vetores pelo nome do arquivo,
    ordena-os e remonta o texto completo.
    """
    if not pg_vector:
        raise ConnectionError("A conexão com o banco de vetores não está disponível.")

    retriever = pg_vector.as_retriever(
        search_kwargs={
            'filter': {'file_name': file_name},
            'k': 1000  # Pega um número grande de chunks para garantir que todos venham
        }
    )

    docs_encontrados = retriever.invoke(" ")

    documentos_do_arquivo = [doc for doc in docs_encontrados if doc.metadata.get("file_name") == file_name]

    if not documentos_do_arquivo:
        return ""

    documentos_ordenados = sorted(documentos_do_arquivo, key=lambda doc: doc.metadata.get('page_number', 0))

    texto_completo = "\n".join([doc.page_content for doc in documentos_ordenados])

    print(f"Texto completo para '{file_name}' reconstruído com sucesso a partir de {len(documentos_ordenados)} chunks.")
    return texto_completo
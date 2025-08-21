# import os.path

# from fastapi import UploadFile, File, HTTPException
# from app.ia.vectorstore import init_vectorstore, ingest_documents
# from app.ia.utils import upload_file, chunk_split, read_pdf
# from fastapi import APIRouter
# import uuid

# router = APIRouter(prefix="/documents", tags=["Chat"])

# @router.post("/upload")
# async def upload_document(file: UploadFile = File(...)):
#     if file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Arquivo deve ser PDF")

#     tmp_dir = "/tmp"
#     os.makedirs(tmp_dir, exist_ok=True)

#     temp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}.pdf")

#     with open(temp_path, "wb") as f:
#         f.write(await file.read())

#     s3_key = f"documents/{os.path.basename(temp_path)}"
#     s3_url = upload_file(temp_path, s3_key)
#     pdf_text = read_pdf(file_path=temp_path)
#     chunks = chunk_split(pdf_text)

#     metadatas = [{"source": s3_url, "chunk": i} for i in range(len(chunks))]
#     ingest_documents(chunks, metadatas, init_vectorstore())    

# Em app/routers/upload.py

# ... outros imports

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/routers/upload.py

# Em app/ia/vectorstore.py

# Em app/routers/upload.py

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_core.documents import Document

# Imports de funções dos seus outros arquivos
from app.ia.vectorstore import ingest_documents
from app.ia.utils import upload_file, chunk_split, read_pdf

router = APIRouter(prefix="/documents", tags=["chat"])

@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    """
    Endpoint síncrono para upload, processamento e vetorização de documentos.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Arquivo deve ser PDF")

    temp_path = None
    try:
        # --- ETAPA 1: SALVAR E PROCESSAR O ARQUIVO ---
        tmp_dir = "/tmp/audit_ia"
        os.makedirs(tmp_dir, exist_ok=True)
        temp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}_{file.filename}")
        
        # --- A CORREÇÃO ESTÁ AQUI ---
        # Lemos o arquivo de forma 100% síncrona acessando file.file
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
        
        # Opcional: Upload para S3 para ter um backup
        s3_key = f"documents/{os.path.basename(temp_path)}"
        s3_url = upload_file(temp_path, s3_key)
        
        # Extrair texto e dividir em pedaços
        pdf_text = read_pdf(file_path=temp_path)
        if not pdf_text or not pdf_text.strip():
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")

        text_chunks = chunk_split(pdf_text)

        # --- ETAPA 2: PREPARAR E INGERIR OS DOCUMENTOS ---

        documents_to_ingest = [
            Document(page_content=chunk, metadata={"source": s3_url}) 
            for chunk in text_chunks
        ]
        
        ingest_documents(documents_to_ingest)

        return {
            "filename": file.filename,
            "s3_url": s3_url,
            "chunks_created": len(documents_to_ingest),
            "message": "Documento processado e vetorizado com sucesso!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro no processamento: {str(e)}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
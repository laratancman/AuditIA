import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_core.documents import Document
# Imports de funções dos seus outros arquivos
from app.ia.agents.agent_embedding import create_embeddings
from app.ia.utils import upload_file, read_pdf

router = APIRouter(prefix="/documents", tags=["Documentos"])

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
        pdf_pages = read_pdf(file_path=temp_path)
        if not pdf_pages:
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")

        create_embeddings(pdf_pages=pdf_pages, file_name=file.filename)

        return {
            "filename": file.filename,
            "s3_url": s3_url,
            "chunks_created": None,
            "message": "Documento processado e vetorizado com sucesso!"
        }





    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro no processamento: {str(e)}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
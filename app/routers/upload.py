import os
import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, select

# Importações do projeto
from app.ia.agents.agent_embedding import create_embeddings
from app.ia.utils import upload_file, read_pdf
from database import SessionLocal
from app.schemas import Document, DocumentStatus # <--- NOVA IMPORTAÇÃO

router = APIRouter(prefix="/documents", tags=["1. Gestão de Documentos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Verificar se o documento já existe para evitar duplicatas
    existing_document = db.execute(select(Document).where(Document.file_name == file.filename)).scalar_one_or_none()
    if existing_document:
        raise HTTPException(status_code=409, detail=f"Documento '{file.filename}' já existe.")

    # 2. Salvar o arquivo temporariamente
    temp_path = None
    try:
        tmp_dir = "/tmp/audit_ia"
        os.makedirs(tmp_dir, exist_ok=True)
        temp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(temp_path, "wb") as f:
            f.write(file.file.read())

        # 3. Fazer o upload para o S3
        s3_key = f"documents/{os.path.basename(temp_path)}"
        s3_url = upload_file(temp_path, s3_key)

        # 4. Criar o registro no banco de dados com status PENDING
        db_document = Document(
            file_name=file.filename,
            s3_url=s3_url,
            status=DocumentStatus.PROCESSING
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        # 5. Processar o PDF e criar os embeddings
        pdf_pages = read_pdf(file_path=temp_path)
        if not pdf_pages:
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")

        create_embeddings(pdf_pages=pdf_pages, file_name=file.filename)

        # 6. Atualizar o status para COMPLETED
        db_document.status = DocumentStatus.COMPLETED
        db.commit()

        return {
            "message": "Documento processado e salvo com sucesso!",
            "document_id": db_document.id,
            "filename": db_document.file_name,
        }

    except Exception as e:
        # Se ocorrer um erro, atualiza o status para FAILED
        if 'db_document' in locals() and db_document:
            db_document.status = DocumentStatus.FAILED
            db.commit()
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro no processamento: {str(e)}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/", response_model=List[str])
def get_all_documents(db: Session = Depends(get_db)):
    """
    Retorna uma lista com os nomes de todos os documentos que foram
    processados com sucesso (status COMPLETED).
    """
    # Agora a consulta é muito mais simples, rápida e na tabela correta
    documents = db.execute(
        select(Document.file_name)
        .where(Document.status == DocumentStatus.COMPLETED)
        .order_by(Document.file_name)
    ).scalars().all()
    
    return documents
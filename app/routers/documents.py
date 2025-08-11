from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from app.models import get_db, Document, DocumentCreate, DocumentUpdate, DocumentResponse, User

router = APIRouter(prefix="/documents", tags=["documents"])

# Configuração para upload de arquivos
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    file: UploadFile = File(...),
    titulo: str = None,
    descricao: str = None,
    tipo_documento: str = None,
    numero_contrato: str = None,
    valor_contrato: str = None,
    data_vencimento: Optional[datetime] = None,
    observacoes: str = None,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Criar um novo documento com upload de arquivo
    """
    # Validar tipo de arquivo
    allowed_types = ["pdf", "docx", "doc", "txt"]
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não suportado. Tipos permitidos: {', '.join(allowed_types)}"
        )
    
    # Salvar arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Criar documento
    document_data = DocumentCreate(
        titulo=titulo or file.filename,
        descricao=descricao,
        tipo_documento=tipo_documento,
        numero_contrato=numero_contrato,
        valor_contrato=valor_contrato,
        data_vencimento=data_vencimento,
        observacoes=observacoes,
        nome_arquivo=filename,
        tipo_arquivo=file_extension,
        tamanho_arquivo=file.size
    )
    
    db_document = Document(
        **document_data.dict(),
        user_id=user_id,
        caminho_arquivo=file_path,
        status="pendente"
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    tipo_documento: str = None,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Listar documentos com filtros opcionais
    """
    query = db.query(Document)
    
    if status:
        query = query.filter(Document.status == status)
    
    if tipo_documento:
        query = query.filter(Document.tipo_documento == tipo_documento)
    
    if user_id:
        query = query.filter(Document.user_id == user_id)
    
    documents = query.offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    """
    Obter um documento específico por ID
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    return document

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int, document_update: DocumentUpdate, db: Session = Depends(get_db)):
    """
    Atualizar um documento
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = document_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_document, field, value)
    
    db.commit()
    db.refresh(db_document)
    return db_document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """
    Deletar um documento
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Remover arquivo físico
    if os.path.exists(db_document.caminho_arquivo):
        os.remove(db_document.caminho_arquivo)
    
    db.delete(db_document)
    db.commit()
    
    return None

@router.patch("/{document_id}/status", response_model=DocumentResponse)
def update_document_status(document_id: int, status: str, db: Session = Depends(get_db)):
    """
    Atualizar status de um documento
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    valid_statuses = ["pendente", "processando", "analisado", "erro"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
        )
    
    db_document.status = status
    if status == "analisado":
        db_document.data_processamento = datetime.now()
    
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/{document_id}/clauses")
def get_document_clauses(document_id: int, db: Session = Depends(get_db)):
    """
    Obter cláusulas de um documento
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    return document.clauses

@router.get("/{document_id}/entities")
def get_document_entities(document_id: int, db: Session = Depends(get_db)):
    """
    Obter entidades de um documento
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    return document.entities

@router.get("/{document_id}/compliance-flags")
def get_document_compliance_flags(document_id: int, db: Session = Depends(get_db)):
    """
    Obter flags de compliance de um documento
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    return document.compliance_flags

@router.get("/{document_id}/deadline-alerts")
def get_document_deadline_alerts(document_id: int, db: Session = Depends(get_db)):
    """
    Obter alertas de prazo de um documento
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    return document.deadline_alerts 
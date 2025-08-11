from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import get_db, Clause, ClauseCreate, ClauseUpdate, ClauseResponse, Document

router = APIRouter(prefix="/clauses", tags=["clauses"])

@router.post("/", response_model=ClauseResponse, status_code=status.HTTP_201_CREATED)
def create_clause(clause: ClauseCreate, db: Session = Depends(get_db)):
    """
    Criar uma nova cláusula
    """
    # Verificar se o documento existe
    document = db.query(Document).filter(Document.id == clause.document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    db_clause = Clause(**clause.dict())
    db.add(db_clause)
    db.commit()
    db.refresh(db_clause)
    return db_clause

@router.get("/", response_model=List[ClauseResponse])
def get_clauses(
    skip: int = 0,
    limit: int = 100,
    document_id: int = None,
    tipo_clausula: str = None,
    categoria: str = None,
    status: str = None,
    relevancia: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar cláusulas com filtros opcionais
    """
    query = db.query(Clause)
    
    if document_id:
        query = query.filter(Clause.document_id == document_id)
    
    if tipo_clausula:
        query = query.filter(Clause.tipo_clausula == tipo_clausula)
    
    if categoria:
        query = query.filter(Clause.categoria == categoria)
    
    if status:
        query = query.filter(Clause.status == status)
    
    if relevancia:
        query = query.filter(Clause.relevancia == relevancia)
    
    clauses = query.offset(skip).limit(limit).all()
    return clauses

@router.get("/{clause_id}", response_model=ClauseResponse)
def get_clause(clause_id: int, db: Session = Depends(get_db)):
    """
    Obter uma cláusula específica por ID
    """
    clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if clause is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cláusula não encontrada"
        )
    return clause

@router.put("/{clause_id}", response_model=ClauseResponse)
def update_clause(clause_id: int, clause_update: ClauseUpdate, db: Session = Depends(get_db)):
    """
    Atualizar uma cláusula
    """
    db_clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if db_clause is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cláusula não encontrada"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = clause_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_clause, field, value)
    
    db.commit()
    db.refresh(db_clause)
    return db_clause

@router.delete("/{clause_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clause(clause_id: int, db: Session = Depends(get_db)):
    """
    Deletar uma cláusula
    """
    db_clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if db_clause is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cláusula não encontrada"
        )
    
    db.delete(db_clause)
    db.commit()
    
    return None

@router.patch("/{clause_id}/status", response_model=ClauseResponse)
def update_clause_status(clause_id: int, status: str, db: Session = Depends(get_db)):
    """
    Atualizar status de uma cláusula
    """
    db_clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if db_clause is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cláusula não encontrada"
        )
    
    valid_statuses = ["detectada", "validada", "rejeitada"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
        )
    
    db_clause.status = status
    if status == "validada":
        from datetime import datetime
        db_clause.data_validacao = datetime.now()
    
    db.commit()
    db.refresh(db_clause)
    return db_clause

@router.get("/{clause_id}/entities")
def get_clause_entities(clause_id: int, db: Session = Depends(get_db)):
    """
    Obter entidades de uma cláusula
    """
    clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if clause is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cláusula não encontrada"
        )
    
    return clause.entities

@router.get("/{clause_id}/compliance-flags")
def get_clause_compliance_flags(clause_id: int, db: Session = Depends(get_db)):
    """
    Obter flags de compliance de uma cláusula
    """
    clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if clause is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cláusula não encontrada"
        )
    
    return clause.compliance_flags

@router.get("/types/")
def get_clause_types(db: Session = Depends(get_db)):
    """
    Obter tipos de cláusulas disponíveis
    """
    types = db.query(Clause.tipo_clausula).distinct().all()
    return [t[0] for t in types if t[0]]

@router.get("/categories/")
def get_clause_categories(db: Session = Depends(get_db)):
    """
    Obter categorias de cláusulas disponíveis
    """
    categories = db.query(Clause.categoria).distinct().all()
    return [c[0] for c in categories if c[0]]

@router.get("/statistics/")
def get_clauses_statistics(db: Session = Depends(get_db)):
    """
    Obter estatísticas das cláusulas
    """
    total_clauses = db.query(Clause).count()
    clauses_by_status = db.query(Clause.status, db.func.count(Clause.id)).group_by(Clause.status).all()
    clauses_by_type = db.query(Clause.tipo_clausula, db.func.count(Clause.id)).group_by(Clause.tipo_clausula).all()
    clauses_by_relevance = db.query(Clause.relevancia, db.func.count(Clause.id)).group_by(Clause.relevancia).all()
    
    return {
        "total": total_clauses,
        "by_status": dict(clauses_by_status),
        "by_type": dict(clauses_by_type),
        "by_relevance": dict(clauses_by_relevance)
    } 
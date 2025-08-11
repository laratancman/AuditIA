from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models import get_db, ComplianceFlag, ComplianceFlagCreate, ComplianceFlagUpdate, ComplianceFlagResponse, Document, Clause, User

router = APIRouter(prefix="/compliance-flags", tags=["compliance-flags"])

@router.post("/", response_model=ComplianceFlagResponse, status_code=status.HTTP_201_CREATED)
def create_compliance_flag(flag: ComplianceFlagCreate, db: Session = Depends(get_db)):
    """
    Criar uma nova flag de compliance
    """
    # Verificar se o documento existe
    document = db.query(Document).filter(Document.id == flag.document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Verificar se a cláusula existe (se fornecida)
    if flag.clause_id:
        clause = db.query(Clause).filter(Clause.id == flag.clause_id).first()
        if not clause:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cláusula não encontrada"
            )
    
    # Verificar se o usuário existe (se fornecido)
    if flag.user_id:
        user = db.query(User).filter(User.id == flag.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
    
    db_flag = ComplianceFlag(**flag.dict())
    db.add(db_flag)
    db.commit()
    db.refresh(db_flag)
    return db_flag

@router.get("/", response_model=List[ComplianceFlagResponse])
def get_compliance_flags(
    skip: int = 0,
    limit: int = 100,
    document_id: int = None,
    clause_id: int = None,
    user_id: int = None,
    tipo_problema: str = None,
    categoria: str = None,
    status: str = None,
    severidade: str = None,
    prioridade: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar flags de compliance com filtros opcionais
    """
    query = db.query(ComplianceFlag)
    
    if document_id:
        query = query.filter(ComplianceFlag.document_id == document_id)
    
    if clause_id:
        query = query.filter(ComplianceFlag.clause_id == clause_id)
    
    if user_id:
        query = query.filter(ComplianceFlag.user_id == user_id)
    
    if tipo_problema:
        query = query.filter(ComplianceFlag.tipo_problema == tipo_problema)
    
    if categoria:
        query = query.filter(ComplianceFlag.categoria == categoria)
    
    if status:
        query = query.filter(ComplianceFlag.status == status)
    
    if severidade:
        query = query.filter(ComplianceFlag.severidade == severidade)
    
    if prioridade:
        query = query.filter(ComplianceFlag.prioridade == prioridade)
    
    flags = query.offset(skip).limit(limit).all()
    return flags

@router.get("/{flag_id}", response_model=ComplianceFlagResponse)
def get_compliance_flag(flag_id: int, db: Session = Depends(get_db)):
    """
    Obter uma flag de compliance específica por ID
    """
    flag = db.query(ComplianceFlag).filter(ComplianceFlag.id == flag_id).first()
    if flag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flag de compliance não encontrada"
        )
    return flag

@router.put("/{flag_id}", response_model=ComplianceFlagResponse)
def update_compliance_flag(flag_id: int, flag_update: ComplianceFlagUpdate, db: Session = Depends(get_db)):
    """
    Atualizar uma flag de compliance
    """
    db_flag = db.query(ComplianceFlag).filter(ComplianceFlag.id == flag_id).first()
    if db_flag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flag de compliance não encontrada"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = flag_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_flag, field, value)
    
    db.commit()
    db.refresh(db_flag)
    return db_flag

@router.delete("/{flag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_compliance_flag(flag_id: int, db: Session = Depends(get_db)):
    """
    Deletar uma flag de compliance
    """
    db_flag = db.query(ComplianceFlag).filter(ComplianceFlag.id == flag_id).first()
    if db_flag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flag de compliance não encontrada"
        )
    
    db.delete(db_flag)
    db.commit()
    
    return None

@router.patch("/{flag_id}/status", response_model=ComplianceFlagResponse)
def update_compliance_flag_status(flag_id: int, status: str, db: Session = Depends(get_db)):
    """
    Atualizar status de uma flag de compliance
    """
    db_flag = db.query(ComplianceFlag).filter(ComplianceFlag.id == flag_id).first()
    if db_flag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flag de compliance não encontrada"
        )
    
    valid_statuses = ["aberto", "em_analise", "resolvido", "ignorado"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
        )
    
    db_flag.status = status
    if status == "resolvido":
        db_flag.data_resolucao = datetime.now()
    
    db.commit()
    db.refresh(db_flag)
    return db_flag

@router.get("/types/")
def get_compliance_flag_types(db: Session = Depends(get_db)):
    """
    Obter tipos de problemas disponíveis
    """
    types = db.query(ComplianceFlag.tipo_problema).distinct().all()
    return [t[0] for t in types if t[0]]

@router.get("/categories/")
def get_compliance_flag_categories(db: Session = Depends(get_db)):
    """
    Obter categorias de flags de compliance disponíveis
    """
    categories = db.query(ComplianceFlag.categoria).distinct().all()
    return [c[0] for c in categories if c[0]]

@router.get("/statistics/")
def get_compliance_flags_statistics(db: Session = Depends(get_db)):
    """
    Obter estatísticas das flags de compliance
    """
    total_flags = db.query(ComplianceFlag).count()
    flags_by_status = db.query(ComplianceFlag.status, db.func.count(ComplianceFlag.id)).group_by(ComplianceFlag.status).all()
    flags_by_type = db.query(ComplianceFlag.tipo_problema, db.func.count(ComplianceFlag.id)).group_by(ComplianceFlag.tipo_problema).all()
    flags_by_severity = db.query(ComplianceFlag.severidade, db.func.count(ComplianceFlag.id)).group_by(ComplianceFlag.severidade).all()
    flags_by_priority = db.query(ComplianceFlag.prioridade, db.func.count(ComplianceFlag.id)).group_by(ComplianceFlag.prioridade).all()
    
    return {
        "total": total_flags,
        "by_status": dict(flags_by_status),
        "by_type": dict(flags_by_type),
        "by_severity": dict(flags_by_severity),
        "by_priority": dict(flags_by_priority)
    }

@router.get("/urgent/")
def get_urgent_compliance_flags(db: Session = Depends(get_db)):
    """
    Obter flags de compliance urgentes
    """
    urgent_flags = db.query(ComplianceFlag).filter(
        ComplianceFlag.status == "aberto",
        ComplianceFlag.prioridade.in_(["alta", "urgente"]),
        ComplianceFlag.severidade.in_(["alta", "critica"])
    ).all()
    
    return urgent_flags

@router.get("/expiring/")
def get_expiring_compliance_flags(days: int = 7, db: Session = Depends(get_db)):
    """
    Obter flags de compliance com prazo expirando
    """
    from datetime import timedelta
    expiry_date = datetime.now() + timedelta(days=days)
    
    expiring_flags = db.query(ComplianceFlag).filter(
        ComplianceFlag.status == "aberto",
        ComplianceFlag.data_limite <= expiry_date
    ).all()
    
    return expiring_flags 
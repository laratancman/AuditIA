from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import os

from app.models import get_db, Report, ReportCreate, ReportUpdate, ReportResponse, Document, User

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    """
    Criar um novo relatório
    """
    # Verificar se o usuário existe
    user = db.query(User).filter(User.id == report.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Verificar se o documento existe (se fornecido)
    if report.document_id:
        document = db.query(Document).filter(Document.id == report.document_id).first()
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documento não encontrado"
            )
    
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/", response_model=List[ReportResponse])
def get_reports(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    document_id: int = None,
    tipo_relatorio: str = None,
    categoria: str = None,
    status: str = None,
    formato: str = None,
    prioridade: str = None,
    publico: bool = None,
    db: Session = Depends(get_db)
):
    """
    Listar relatórios com filtros opcionais
    """
    query = db.query(Report)
    
    if user_id:
        query = query.filter(Report.user_id == user_id)
    
    if document_id:
        query = query.filter(Report.document_id == document_id)
    
    if tipo_relatorio:
        query = query.filter(Report.tipo_relatorio == tipo_relatorio)
    
    if categoria:
        query = query.filter(Report.categoria == categoria)
    
    if status:
        query = query.filter(Report.status == status)
    
    if formato:
        query = query.filter(Report.formato == formato)
    
    if prioridade:
        query = query.filter(Report.prioridade == prioridade)
    
    if publico is not None:
        query = query.filter(Report.publico == publico)
    
    reports = query.offset(skip).limit(limit).all()
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """
    Obter um relatório específico por ID
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado"
        )
    return report

@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: int, report_update: ReportUpdate, db: Session = Depends(get_db)):
    """
    Atualizar um relatório
    """
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = report_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_report, field, value)
    
    db.commit()
    db.refresh(db_report)
    return db_report

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    """
    Deletar um relatório
    """
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado"
        )
    
    # Remover arquivo físico se existir
    if db_report.caminho_arquivo and os.path.exists(db_report.caminho_arquivo):
        os.remove(db_report.caminho_arquivo)
    
    db.delete(db_report)
    db.commit()
    
    return None

@router.patch("/{report_id}/status", response_model=ReportResponse)
def update_report_status(report_id: int, status: str, db: Session = Depends(get_db)):
    """
    Atualizar status de um relatório
    """
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado"
        )
    
    valid_statuses = ["gerado", "processando", "erro", "arquivado"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
        )
    
    db_report.status = status
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/types/")
def get_report_types(db: Session = Depends(get_db)):
    """
    Obter tipos de relatórios disponíveis
    """
    types = db.query(Report.tipo_relatorio).distinct().all()
    return [t[0] for t in types if t[0]]

@router.get("/categories/")
def get_report_categories(db: Session = Depends(get_db)):
    """
    Obter categorias de relatórios disponíveis
    """
    categories = db.query(Report.categoria).distinct().all()
    return [c[0] for c in categories if c[0]]

@router.get("/formats/")
def get_report_formats(db: Session = Depends(get_db)):
    """
    Obter formatos de relatórios disponíveis
    """
    formats = db.query(Report.formato).distinct().all()
    return [f[0] for f in formats if f[0]]

@router.get("/statistics/")
def get_reports_statistics(db: Session = Depends(get_db)):
    """
    Obter estatísticas dos relatórios
    """
    total_reports = db.query(Report).count()
    reports_by_status = db.query(Report.status, db.func.count(Report.id)).group_by(Report.status).all()
    reports_by_type = db.query(Report.tipo_relatorio, db.func.count(Report.id)).group_by(Report.tipo_relatorio).all()
    reports_by_format = db.query(Report.formato, db.func.count(Report.id)).group_by(Report.formato).all()
    reports_by_priority = db.query(Report.prioridade, db.func.count(Report.id)).group_by(Report.prioridade).all()
    
    return {
        "total": total_reports,
        "by_status": dict(reports_by_status),
        "by_type": dict(reports_by_type),
        "by_format": dict(reports_by_format),
        "by_priority": dict(reports_by_priority)
    }

@router.get("/public/")
def get_public_reports(db: Session = Depends(get_db)):
    """
    Obter relatórios públicos
    """
    public_reports = db.query(Report).filter(Report.publico == True).all()
    return public_reports

@router.get("/recent/")
def get_recent_reports(limit: int = 10, db: Session = Depends(get_db)):
    """
    Obter relatórios recentes
    """
    recent_reports = db.query(Report).order_by(Report.data_geracao.desc()).limit(limit).all()
    return recent_reports

@router.get("/by-user/{user_id}")
def get_reports_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obter relatórios de um usuário específico
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user.reports 
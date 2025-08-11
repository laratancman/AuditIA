from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.models import get_db, DeadlineAlert, DeadlineAlertCreate, DeadlineAlertUpdate, DeadlineAlertResponse, Document, User

router = APIRouter(prefix="/deadline-alerts", tags=["deadline-alerts"])

@router.post("/", response_model=DeadlineAlertResponse, status_code=status.HTTP_201_CREATED)
def create_deadline_alert(alert: DeadlineAlertCreate, db: Session = Depends(get_db)):
    """
    Criar um novo alerta de prazo
    """
    # Verificar se o documento existe
    document = db.query(Document).filter(Document.id == alert.document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Verificar se o usuário existe (se fornecido)
    if alert.user_id:
        user = db.query(User).filter(User.id == alert.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
    
    db_alert = DeadlineAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/", response_model=List[DeadlineAlertResponse])
def get_deadline_alerts(
    skip: int = 0,
    limit: int = 100,
    document_id: int = None,
    user_id: int = None,
    tipo_prazo: str = None,
    categoria: str = None,
    status: str = None,
    prioridade: str = None,
    severidade: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar alertas de prazo com filtros opcionais
    """
    query = db.query(DeadlineAlert)
    
    if document_id:
        query = query.filter(DeadlineAlert.document_id == document_id)
    
    if user_id:
        query = query.filter(DeadlineAlert.user_id == user_id)
    
    if tipo_prazo:
        query = query.filter(DeadlineAlert.tipo_prazo == tipo_prazo)
    
    if categoria:
        query = query.filter(DeadlineAlert.categoria == categoria)
    
    if status:
        query = query.filter(DeadlineAlert.status == status)
    
    if prioridade:
        query = query.filter(DeadlineAlert.prioridade == prioridade)
    
    if severidade:
        query = query.filter(DeadlineAlert.severidade == severidade)
    
    alerts = query.offset(skip).limit(limit).all()
    return alerts

@router.get("/{alert_id}", response_model=DeadlineAlertResponse)
def get_deadline_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Obter um alerta de prazo específico por ID
    """
    alert = db.query(DeadlineAlert).filter(DeadlineAlert.id == alert_id).first()
    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta de prazo não encontrado"
        )
    return alert

@router.put("/{alert_id}", response_model=DeadlineAlertResponse)
def update_deadline_alert(alert_id: int, alert_update: DeadlineAlertUpdate, db: Session = Depends(get_db)):
    """
    Atualizar um alerta de prazo
    """
    db_alert = db.query(DeadlineAlert).filter(DeadlineAlert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta de prazo não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = alert_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deadline_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Deletar um alerta de prazo
    """
    db_alert = db.query(DeadlineAlert).filter(DeadlineAlert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta de prazo não encontrado"
        )
    
    db.delete(db_alert)
    db.commit()
    
    return None

@router.patch("/{alert_id}/status", response_model=DeadlineAlertResponse)
def update_deadline_alert_status(alert_id: int, status: str, db: Session = Depends(get_db)):
    """
    Atualizar status de um alerta de prazo
    """
    db_alert = db.query(DeadlineAlert).filter(DeadlineAlert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta de prazo não encontrado"
        )
    
    valid_statuses = ["ativo", "vencido", "renovado", "cancelado"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
        )
    
    db_alert.status = status
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.patch("/{alert_id}/notify", response_model=DeadlineAlertResponse)
def mark_deadline_alert_notified(alert_id: int, db: Session = Depends(get_db)):
    """
    Marcar alerta de prazo como notificado
    """
    db_alert = db.query(DeadlineAlert).filter(DeadlineAlert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta de prazo não encontrado"
        )
    
    db_alert.notificado = True
    db_alert.data_notificacao = datetime.now()
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/types/")
def get_deadline_alert_types(db: Session = Depends(get_db)):
    """
    Obter tipos de prazos disponíveis
    """
    types = db.query(DeadlineAlert.tipo_prazo).distinct().all()
    return [t[0] for t in types if t[0]]

@router.get("/categories/")
def get_deadline_alert_categories(db: Session = Depends(get_db)):
    """
    Obter categorias de alertas de prazo disponíveis
    """
    categories = db.query(DeadlineAlert.categoria).distinct().all()
    return [c[0] for c in categories if c[0]]

@router.get("/statistics/")
def get_deadline_alerts_statistics(db: Session = Depends(get_db)):
    """
    Obter estatísticas dos alertas de prazo
    """
    total_alerts = db.query(DeadlineAlert).count()
    alerts_by_status = db.query(DeadlineAlert.status, db.func.count(DeadlineAlert.id)).group_by(DeadlineAlert.status).all()
    alerts_by_type = db.query(DeadlineAlert.tipo_prazo, db.func.count(DeadlineAlert.id)).group_by(DeadlineAlert.tipo_prazo).all()
    alerts_by_priority = db.query(DeadlineAlert.prioridade, db.func.count(DeadlineAlert.id)).group_by(DeadlineAlert.prioridade).all()
    alerts_by_severity = db.query(DeadlineAlert.severidade, db.func.count(DeadlineAlert.id)).group_by(DeadlineAlert.severidade).all()
    
    return {
        "total": total_alerts,
        "by_status": dict(alerts_by_status),
        "by_type": dict(alerts_by_type),
        "by_priority": dict(alerts_by_priority),
        "by_severity": dict(alerts_by_severity)
    }

@router.get("/expiring/")
def get_expiring_deadline_alerts(days: int = 30, db: Session = Depends(get_db)):
    """
    Obter alertas de prazo vencendo em X dias
    """
    expiry_date = datetime.now() + timedelta(days=days)
    
    expiring_alerts = db.query(DeadlineAlert).filter(
        DeadlineAlert.data_limite <= expiry_date,
        DeadlineAlert.status == "ativo"
    ).all()
    
    return expiring_alerts

@router.get("/overdue/")
def get_overdue_deadline_alerts(db: Session = Depends(get_db)):
    """
    Obter alertas de prazo vencidos
    """
    overdue_alerts = db.query(DeadlineAlert).filter(
        DeadlineAlert.data_limite < datetime.now(),
        DeadlineAlert.status == "ativo"
    ).all()
    
    return overdue_alerts

@router.get("/urgent/")
def get_urgent_deadline_alerts(db: Session = Depends(get_db)):
    """
    Obter alertas de prazo urgentes
    """
    urgent_alerts = db.query(DeadlineAlert).filter(
        DeadlineAlert.status == "ativo",
        DeadlineAlert.prioridade.in_(["alta", "urgente"]),
        DeadlineAlert.severidade.in_(["alta", "critica"])
    ).all()
    
    return urgent_alerts

@router.get("/unnotified/")
def get_unnotified_deadline_alerts(db: Session = Depends(get_db)):
    """
    Obter alertas de prazo não notificados
    """
    unnotified_alerts = db.query(DeadlineAlert).filter(
        DeadlineAlert.status == "ativo",
        DeadlineAlert.notificado == False
    ).all()
    
    return unnotified_alerts 
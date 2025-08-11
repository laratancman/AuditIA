from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models import get_db, Feedback, FeedbackCreate, FeedbackUpdate, FeedbackResponse, User, Document, Clause, Entity

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])

@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Criar um novo feedback
    """
    # Verificar se o usuário existe
    user = db.query(User).filter(User.id == feedback.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Verificar se o documento existe (se fornecido)
    if feedback.document_id:
        document = db.query(Document).filter(Document.id == feedback.document_id).first()
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documento não encontrado"
            )
    
    # Verificar se a cláusula existe (se fornecida)
    if feedback.clause_id:
        clause = db.query(Clause).filter(Clause.id == feedback.clause_id).first()
        if not clause:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cláusula não encontrada"
            )
    
    # Verificar se a entidade existe (se fornecida)
    if feedback.entity_id:
        entity = db.query(Entity).filter(Entity.id == feedback.entity_id).first()
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entidade não encontrada"
            )
    
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/", response_model=List[FeedbackResponse])
def get_feedbacks(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    document_id: int = None,
    clause_id: int = None,
    entity_id: int = None,
    tipo_feedback: str = None,
    categoria: str = None,
    status: str = None,
    prioridade: str = None,
    impacto: str = None,
    anonimo: bool = None,
    db: Session = Depends(get_db)
):
    """
    Listar feedbacks com filtros opcionais
    """
    query = db.query(Feedback)
    
    if user_id:
        query = query.filter(Feedback.user_id == user_id)
    
    if document_id:
        query = query.filter(Feedback.document_id == document_id)
    
    if clause_id:
        query = query.filter(Feedback.clause_id == clause_id)
    
    if entity_id:
        query = query.filter(Feedback.entity_id == entity_id)
    
    if tipo_feedback:
        query = query.filter(Feedback.tipo_feedback == tipo_feedback)
    
    if categoria:
        query = query.filter(Feedback.categoria == categoria)
    
    if status:
        query = query.filter(Feedback.status == status)
    
    if prioridade:
        query = query.filter(Feedback.prioridade == prioridade)
    
    if impacto:
        query = query.filter(Feedback.impacto == impacto)
    
    if anonimo is not None:
        query = query.filter(Feedback.anonimo == anonimo)
    
    feedbacks = query.offset(skip).limit(limit).all()
    return feedbacks

@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """
    Obter um feedback específico por ID
    """
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback não encontrado"
        )
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(feedback_id: int, feedback_update: FeedbackUpdate, db: Session = Depends(get_db)):
    """
    Atualizar um feedback
    """
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = feedback_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_feedback, field, value)
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """
    Deletar um feedback
    """
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback não encontrado"
        )
    
    db.delete(db_feedback)
    db.commit()
    
    return None

@router.patch("/{feedback_id}/status", response_model=FeedbackResponse)
def update_feedback_status(feedback_id: int, status: str, db: Session = Depends(get_db)):
    """
    Atualizar status de um feedback
    """
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback não encontrado"
        )
    
    valid_statuses = ["aberto", "em_analise", "resolvido", "rejeitado"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
        )
    
    db_feedback.status = status
    if status == "resolvido":
        db_feedback.data_resolucao = datetime.now()
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.patch("/{feedback_id}/respond", response_model=FeedbackResponse)
def respond_to_feedback(feedback_id: int, resposta: str, db: Session = Depends(get_db)):
    """
    Responder a um feedback
    """
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback não encontrado"
        )
    
    db_feedback.resposta = resposta
    db_feedback.status = "resolvido"
    db_feedback.data_resolucao = datetime.now()
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/types/")
def get_feedback_types(db: Session = Depends(get_db)):
    """
    Obter tipos de feedback disponíveis
    """
    types = db.query(Feedback.tipo_feedback).distinct().all()
    return [t[0] for t in types if t[0]]

@router.get("/categories/")
def get_feedback_categories(db: Session = Depends(get_db)):
    """
    Obter categorias de feedback disponíveis
    """
    categories = db.query(Feedback.categoria).distinct().all()
    return [c[0] for c in categories if c[0]]

@router.get("/statistics/")
def get_feedbacks_statistics(db: Session = Depends(get_db)):
    """
    Obter estatísticas dos feedbacks
    """
    total_feedbacks = db.query(Feedback).count()
    feedbacks_by_status = db.query(Feedback.status, db.func.count(Feedback.id)).group_by(Feedback.status).all()
    feedbacks_by_type = db.query(Feedback.tipo_feedback, db.func.count(Feedback.id)).group_by(Feedback.tipo_feedback).all()
    feedbacks_by_priority = db.query(Feedback.prioridade, db.func.count(Feedback.id)).group_by(Feedback.prioridade).all()
    feedbacks_by_impact = db.query(Feedback.impacto, db.func.count(Feedback.id)).group_by(Feedback.impacto).all()
    
    # Calcular média de avaliação
    avg_rating = db.query(db.func.avg(Feedback.avaliacao)).scalar()
    avg_satisfaction = db.query(db.func.avg(Feedback.satisfacao)).scalar()
    
    return {
        "total": total_feedbacks,
        "by_status": dict(feedbacks_by_status),
        "by_type": dict(feedbacks_by_type),
        "by_priority": dict(feedbacks_by_priority),
        "by_impact": dict(feedbacks_by_impact),
        "average_rating": float(avg_rating) if avg_rating else 0,
        "average_satisfaction": float(avg_satisfaction) if avg_satisfaction else 0
    }

@router.get("/open/")
def get_open_feedbacks(db: Session = Depends(get_db)):
    """
    Obter feedbacks abertos
    """
    open_feedbacks = db.query(Feedback).filter(Feedback.status == "aberto").all()
    return open_feedbacks

@router.get("/high-priority/")
def get_high_priority_feedbacks(db: Session = Depends(get_db)):
    """
    Obter feedbacks de alta prioridade
    """
    high_priority_feedbacks = db.query(Feedback).filter(
        Feedback.prioridade.in_(["alta", "urgente"]),
        Feedback.status == "aberto"
    ).all()
    
    return high_priority_feedbacks

@router.get("/anonymous/")
def get_anonymous_feedbacks(db: Session = Depends(get_db)):
    """
    Obter feedbacks anônimos
    """
    anonymous_feedbacks = db.query(Feedback).filter(Feedback.anonimo == True).all()
    return anonymous_feedbacks

@router.get("/by-user/{user_id}")
def get_feedbacks_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obter feedbacks de um usuário específico
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user.feedbacks 
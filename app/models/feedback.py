from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .database import Base

class Feedback(Base):
    """Modelo para feedbacks de usuários"""
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_feedback = Column(String(100), nullable=False)  # analise, sugestao, erro, melhoria
    categoria = Column(String(100), nullable=True)  # compliance, interface, funcionalidade, etc.
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    avaliacao = Column(Integer, nullable=True)  # 1-5 estrelas
    satisfacao = Column(Float, nullable=True)  # 0-1 score de satisfação
    status = Column(String(50), default="aberto")  # aberto, em_analise, resolvido, rejeitado
    prioridade = Column(String(50), default="media")  # baixa, media, alta, urgente
    impacto = Column(String(50), default="medio")  # baixo, medio, alto
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_resolucao = Column(DateTime(timezone=True), nullable=True)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    resposta = Column(Text, nullable=True)  # resposta da equipe
    observacoes = Column(Text, nullable=True)
    anonimo = Column(Boolean, default=False)
    tags = Column(Text, nullable=True)  # JSON com tags para categorização
    
    # Relacionamentos
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="feedbacks")
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    document = relationship("Document", back_populates="feedbacks")
    clause_id = Column(Integer, ForeignKey("clauses.id"), nullable=True)
    clause = relationship("Clause", back_populates="feedbacks")
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=True)
    entity = relationship("Entity", back_populates="feedbacks")

# Schemas Pydantic para API
class FeedbackBase(BaseModel):
    tipo_feedback: str
    categoria: Optional[str] = None
    titulo: str
    descricao: str
    avaliacao: Optional[int] = None
    satisfacao: Optional[float] = None
    prioridade: str = "media"
    impacto: str = "medio"
    observacoes: Optional[str] = None
    anonimo: bool = False

class FeedbackCreate(FeedbackBase):
    document_id: Optional[int] = None
    clause_id: Optional[int] = None
    entity_id: Optional[int] = None

class FeedbackUpdate(BaseModel):
    tipo_feedback: Optional[str] = None
    categoria: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    avaliacao: Optional[int] = None
    satisfacao: Optional[float] = None
    status: Optional[str] = None
    prioridade: Optional[str] = None
    impacto: Optional[str] = None
    resposta: Optional[str] = None
    observacoes: Optional[str] = None
    anonimo: Optional[bool] = None

class FeedbackResponse(FeedbackBase):
    id: int
    status: str
    data_criacao: datetime
    data_resolucao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    resposta: Optional[str] = None
    user_id: int
    document_id: Optional[int] = None
    clause_id: Optional[int] = None
    entity_id: Optional[int] = None
    
    class Config:
        from_attributes = True 
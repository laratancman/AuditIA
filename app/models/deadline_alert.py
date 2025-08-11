from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .database import Base

class DeadlineAlert(Base):
    """Modelo para alertas de prazos"""
    __tablename__ = "deadline_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo_prazo = Column(String(100), nullable=False)  # vencimento, renovacao, pagamento, etc.
    categoria = Column(String(100), nullable=True)  # financeira, temporal, legal, etc.
    data_limite = Column(DateTime(timezone=True), nullable=False)
    data_lembrete = Column(DateTime(timezone=True), nullable=True)  # quando deve ser lembrado
    status = Column(String(50), default="ativo")  # ativo, vencido, renovado, cancelado
    prioridade = Column(String(50), default="media")  # baixa, media, alta, urgente
    severidade = Column(String(50), default="media")  # baixa, media, alta, critica
    dias_antecedencia = Column(Integer, default=30)  # dias antes do prazo para alertar
    acao_requerida = Column(Text, nullable=True)
    responsavel = Column(String(255), nullable=True)
    observacoes = Column(Text, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    notificado = Column(Boolean, default=False)
    data_notificacao = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="deadline_alerts")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="deadline_alerts")

# Schemas Pydantic para API
class DeadlineAlertBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    tipo_prazo: str
    categoria: Optional[str] = None
    data_limite: datetime
    data_lembrete: Optional[datetime] = None
    prioridade: str = "media"
    severidade: str = "media"
    dias_antecedencia: int = 30
    acao_requerida: Optional[str] = None
    responsavel: Optional[str] = None
    observacoes: Optional[str] = None

class DeadlineAlertCreate(DeadlineAlertBase):
    user_id: Optional[int] = None

class DeadlineAlertUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    tipo_prazo: Optional[str] = None
    categoria: Optional[str] = None
    data_limite: Optional[datetime] = None
    data_lembrete: Optional[datetime] = None
    status: Optional[str] = None
    prioridade: Optional[str] = None
    severidade: Optional[str] = None
    dias_antecedencia: Optional[int] = None
    acao_requerida: Optional[str] = None
    responsavel: Optional[str] = None
    observacoes: Optional[str] = None
    notificado: Optional[bool] = None

class DeadlineAlertResponse(DeadlineAlertBase):
    id: int
    status: str
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    notificado: bool
    data_notificacao: Optional[datetime] = None
    document_id: int
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True 
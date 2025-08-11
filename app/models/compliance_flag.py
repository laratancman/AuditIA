from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .database import Base

class ComplianceFlag(Base):
    """Modelo para sinalizações de compliance"""
    __tablename__ = "compliance_flags"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_problema = Column(String(100), nullable=False)  # prazo_vencido, valor_inadequado, etc.
    categoria = Column(String(100), nullable=False)  # financeira, temporal, legal, etc.
    severidade = Column(String(50), default="media")  # baixa, media, alta, critica
    descricao = Column(Text, nullable=False)
    recomendacao = Column(Text, nullable=True)
    status = Column(String(50), default="aberto")  # aberto, em_analise, resolvido, ignorado
    prioridade = Column(String(50), default="media")  # baixa, media, alta, urgente
    data_deteccao = Column(DateTime(timezone=True), server_default=func.now())
    data_resolucao = Column(DateTime(timezone=True), nullable=True)
    data_limite = Column(DateTime(timezone=True), nullable=True)
    responsavel = Column(String(255), nullable=True)
    observacoes = Column(Text, nullable=True)
    acao_requerida = Column(Text, nullable=True)
    impacto = Column(String(100), nullable=True)  # baixo, medio, alto
    risco = Column(String(100), nullable=True)  # baixo, medio, alto
    
    # Relacionamentos
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="compliance_flags")
    clause_id = Column(Integer, ForeignKey("clauses.id"), nullable=True)
    clause = relationship("Clause", back_populates="compliance_flags")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="compliance_flags")

# Schemas Pydantic para API
class ComplianceFlagBase(BaseModel):
    tipo_problema: str
    categoria: str
    severidade: str = "media"
    descricao: str
    recomendacao: Optional[str] = None
    prioridade: str = "media"
    data_limite: Optional[datetime] = None
    responsavel: Optional[str] = None
    observacoes: Optional[str] = None
    acao_requerida: Optional[str] = None
    impacto: Optional[str] = None
    risco: Optional[str] = None

class ComplianceFlagCreate(ComplianceFlagBase):
    clause_id: Optional[int] = None
    user_id: Optional[int] = None

class ComplianceFlagUpdate(BaseModel):
    tipo_problema: Optional[str] = None
    categoria: Optional[str] = None
    severidade: Optional[str] = None
    descricao: Optional[str] = None
    recomendacao: Optional[str] = None
    status: Optional[str] = None
    prioridade: Optional[str] = None
    data_limite: Optional[datetime] = None
    responsavel: Optional[str] = None
    observacoes: Optional[str] = None
    acao_requerida: Optional[str] = None
    impacto: Optional[str] = None
    risco: Optional[str] = None

class ComplianceFlagResponse(ComplianceFlagBase):
    id: int
    status: str
    data_deteccao: datetime
    data_resolucao: Optional[datetime] = None
    document_id: int
    clause_id: Optional[int] = None
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True 
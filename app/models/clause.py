from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .database import Base

class Clause(Base):
    """Modelo para cláusulas detectadas em documentos"""
    __tablename__ = "clauses"
    
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text, nullable=False)
    tipo_clausula = Column(String(100), nullable=False)  # penalidade, prazo, valor, etc.
    categoria = Column(String(100), nullable=True)  # financeira, temporal, responsabilidade, etc.
    posicao_inicio = Column(Integer, nullable=True)  # posição no documento
    posicao_fim = Column(Integer, nullable=True)
    pagina = Column(Integer, nullable=True)
    confianca = Column(Float, nullable=True)  # score de confiança da detecção (0-1)
    relevancia = Column(String(50), default="media")  # baixa, media, alta, critica
    status = Column(String(50), default="detectada")  # detectada, validada, rejeitada
    data_deteccao = Column(DateTime(timezone=True), server_default=func.now())
    data_validacao = Column(DateTime(timezone=True), nullable=True)
    observacoes = Column(Text, nullable=True)
    contexto = Column(Text, nullable=True)  # texto ao redor da cláusula
    
    # Relacionamentos
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="clauses")
    entities = relationship("Entity", back_populates="clause")
    compliance_flags = relationship("ComplianceFlag", back_populates="clause")
    feedbacks = relationship("Feedback", back_populates="clause")

# Schemas Pydantic para API
class ClauseBase(BaseModel):
    texto: str
    tipo_clausula: str
    categoria: Optional[str] = None
    relevancia: str = "media"
    observacoes: Optional[str] = None
    contexto: Optional[str] = None

class ClauseCreate(ClauseBase):
    posicao_inicio: Optional[int] = None
    posicao_fim: Optional[int] = None
    pagina: Optional[int] = None
    confianca: Optional[float] = None

class ClauseUpdate(BaseModel):
    texto: Optional[str] = None
    tipo_clausula: Optional[str] = None
    categoria: Optional[str] = None
    relevancia: Optional[str] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None
    contexto: Optional[str] = None

class ClauseResponse(ClauseBase):
    id: int
    posicao_inicio: Optional[int] = None
    posicao_fim: Optional[int] = None
    pagina: Optional[int] = None
    confianca: Optional[float] = None
    status: str
    data_deteccao: datetime
    data_validacao: Optional[datetime] = None
    document_id: int
    
    class Config:
        from_attributes = True 
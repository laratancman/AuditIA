from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .database import Base

class Entity(Base):
    """Modelo para entidades extraídas por PLN"""
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(500), nullable=False)
    tipo_entidade = Column(String(100), nullable=False)  # data, valor, pessoa, empresa, etc.
    categoria = Column(String(100), nullable=True)  # financeira, temporal, organizacional, etc.
    valor_normalizado = Column(String(255), nullable=True)  # valor padronizado
    posicao_inicio = Column(Integer, nullable=True)
    posicao_fim = Column(Integer, nullable=True)
    pagina = Column(Integer, nullable=True)
    confianca = Column(Float, nullable=True)  # score de confiança (0-1)
    relevancia = Column(String(50), default="media")  # baixa, media, alta
    status = Column(String(50), default="detectada")  # detectada, validada, rejeitada
    data_deteccao = Column(DateTime(timezone=True), server_default=func.now())
    data_validacao = Column(DateTime(timezone=True), nullable=True)
    observacoes = Column(Text, nullable=True)
    contexto = Column(Text, nullable=True)  # texto ao redor da entidade
    
    # Relacionamentos
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="entities")
    clause_id = Column(Integer, ForeignKey("clauses.id"), nullable=True)
    clause = relationship("Clause", back_populates="entities")
    feedbacks = relationship("Feedback", back_populates="entity")

# Schemas Pydantic para API
class EntityBase(BaseModel):
    texto: str
    tipo_entidade: str
    categoria: Optional[str] = None
    valor_normalizado: Optional[str] = None
    relevancia: str = "media"
    observacoes: Optional[str] = None
    contexto: Optional[str] = None

class EntityCreate(EntityBase):
    posicao_inicio: Optional[int] = None
    posicao_fim: Optional[int] = None
    pagina: Optional[int] = None
    confianca: Optional[float] = None
    clause_id: Optional[int] = None

class EntityUpdate(BaseModel):
    texto: Optional[str] = None
    tipo_entidade: Optional[str] = None
    categoria: Optional[str] = None
    valor_normalizado: Optional[str] = None
    relevancia: Optional[str] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None
    contexto: Optional[str] = None

class EntityResponse(EntityBase):
    id: int
    posicao_inicio: Optional[int] = None
    posicao_fim: Optional[int] = None
    pagina: Optional[int] = None
    confianca: Optional[float] = None
    status: str
    data_deteccao: datetime
    data_validacao: Optional[datetime] = None
    document_id: int
    clause_id: Optional[int] = None
    
    class Config:
        from_attributes = True 
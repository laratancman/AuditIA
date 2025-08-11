from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .database import Base

class Document(Base):
    """Modelo para documentos e contratos"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_arquivo = Column(String(1000), nullable=False)
    tipo_arquivo = Column(String(50), nullable=False)  # pdf, docx, txt, etc.
    tamanho_arquivo = Column(Integer, nullable=True)  # em bytes
    status = Column(String(50), default="pendente")  # pendente, processando, analisado, erro
    data_upload = Column(DateTime(timezone=True), server_default=func.now())
    data_processamento = Column(DateTime(timezone=True), nullable=True)
    data_vencimento = Column(DateTime(timezone=True), nullable=True)
    tipo_documento = Column(String(100), nullable=True)  # contrato, aditivo, anexo, etc.
    numero_contrato = Column(String(100), nullable=True)
    valor_contrato = Column(String(100), nullable=True)
    partes_envolvidas = Column(Text, nullable=True)  # JSON com informações das partes
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="documents")
    clauses = relationship("Clause", back_populates="document")
    entities = relationship("Entity", back_populates="document")
    compliance_flags = relationship("ComplianceFlag", back_populates="document")
    deadline_alerts = relationship("DeadlineAlert", back_populates="document")
    reports = relationship("Report", back_populates="document")
    feedbacks = relationship("Feedback", back_populates="document")

# Schemas Pydantic para API
class DocumentBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_contrato: Optional[str] = None
    valor_contrato: Optional[str] = None
    data_vencimento: Optional[datetime] = None
    observacoes: Optional[str] = None

class DocumentCreate(DocumentBase):
    nome_arquivo: str
    tipo_arquivo: str
    tamanho_arquivo: Optional[int] = None

class DocumentUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_contrato: Optional[str] = None
    valor_contrato: Optional[str] = None
    data_vencimento: Optional[datetime] = None
    observacoes: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    nome_arquivo: str
    caminho_arquivo: str
    tipo_arquivo: str
    tamanho_arquivo: Optional[int] = None
    status: str
    data_upload: datetime
    data_processamento: Optional[datetime] = None
    user_id: int
    
    class Config:
        from_attributes = True 
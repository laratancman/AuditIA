from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from .database import Base

class Report(Base):
    """Modelo para relatórios gerados pelo sistema"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo_relatorio = Column(String(100), nullable=False)  # compliance, analise, resumo, etc.
    categoria = Column(String(100), nullable=True)  # financeira, temporal, legal, etc.
    status = Column(String(50), default="gerado")  # gerado, processando, erro, arquivado
    formato = Column(String(50), default="pdf")  # pdf, docx, html, json
    caminho_arquivo = Column(String(1000), nullable=True)
    tamanho_arquivo = Column(Integer, nullable=True)  # em bytes
    parametros = Column(JSON, nullable=True)  # parâmetros usados na geração
    resumo_executivo = Column(Text, nullable=True)
    principais_achados = Column(Text, nullable=True)
    recomendacoes = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)
    data_geracao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    data_limite = Column(DateTime(timezone=True), nullable=True)
    prioridade = Column(String(50), default="media")  # baixa, media, alta, urgente
    publico = Column(Boolean, default=False)  # se pode ser compartilhado
    
    # Relacionamentos
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="reports")
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    document = relationship("Document", back_populates="reports")

# Schemas Pydantic para API
class ReportBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    tipo_relatorio: str
    categoria: Optional[str] = None
    formato: str = "pdf"
    resumo_executivo: Optional[str] = None
    principais_achados: Optional[str] = None
    recomendacoes: Optional[str] = None
    observacoes: Optional[str] = None
    data_limite: Optional[datetime] = None
    prioridade: str = "media"
    publico: bool = False

class ReportCreate(ReportBase):
    parametros: Optional[Dict[str, Any]] = None
    document_id: Optional[int] = None

class ReportUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    tipo_relatorio: Optional[str] = None
    categoria: Optional[str] = None
    status: Optional[str] = None
    formato: Optional[str] = None
    resumo_executivo: Optional[str] = None
    principais_achados: Optional[str] = None
    recomendacoes: Optional[str] = None
    observacoes: Optional[str] = None
    data_limite: Optional[datetime] = None
    prioridade: Optional[str] = None
    publico: Optional[bool] = None
    parametros: Optional[Dict[str, Any]] = None

class ReportResponse(ReportBase):
    id: int
    status: str
    caminho_arquivo: Optional[str] = None
    tamanho_arquivo: Optional[int] = None
    parametros: Optional[Dict[str, Any]] = None
    data_geracao: datetime
    data_atualizacao: Optional[datetime] = None
    user_id: int
    document_id: Optional[int] = None
    
    class Config:
        from_attributes = True 
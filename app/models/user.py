from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .database import Base

class User(Base):
    """Modelo para usuários do sistema"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    permissao = Column(String(50), default="usuario")  # admin, auditor, usuario
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_ultimo_acesso = Column(DateTime(timezone=True), nullable=True)
    telefone = Column(String(20), nullable=True)
    departamento = Column(String(100), nullable=True)
    cargo = Column(String(100), nullable=True)
    
    # Relacionamentos
    documents = relationship("Document", back_populates="user")
    compliance_flags = relationship("ComplianceFlag", back_populates="user")
    deadline_alerts = relationship("DeadlineAlert", back_populates="user")
    reports = relationship("Report", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")

# Schemas Pydantic para API
class UserBase(BaseModel):
    nome: str
    email: EmailStr
    permissao: str = "usuario"
    telefone: Optional[str] = None
    departamento: Optional[str] = None
    cargo: Optional[str] = None

class UserCreate(UserBase):
    senha: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    permissao: Optional[str] = None
    ativo: Optional[bool] = None
    telefone: Optional[str] = None
    departamento: Optional[str] = None
    cargo: Optional[str] = None

class UserResponse(UserBase):
    id: int
    ativo: bool
    data_criacao: datetime
    data_ultimo_acesso: Optional[datetime] = None
    
    class Config:
        from_attributes = True 
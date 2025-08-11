from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Configuração da base de dados
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./audit_ia.db"
)

# Configuração do engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in SQLALCHEMY_DATABASE_URL else None,
    echo=True  # Log das queries SQL (remover em produção)
)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()

# Função para obter a sessão da base de dados
def get_db():
    """
    Função para obter uma sessão da base de dados.
    Usar como dependency no FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar todas as tabelas
def create_tables():
    """
    Cria todas as tabelas no banco de dados.
    """
    from . import (
        User, Document, Clause, Entity, 
        ComplianceFlag, DeadlineAlert, Report, Feedback
    )
    Base.metadata.create_all(bind=engine)

# Função para dropar todas as tabelas (cuidado!)
def drop_tables():
    """
    Remove todas as tabelas do banco de dados.
    Usar apenas em desenvolvimento.
    """
    Base.metadata.drop_all(bind=engine) 
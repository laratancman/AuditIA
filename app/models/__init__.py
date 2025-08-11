# Importando configuração da base de dados
from .database import Base, get_db, create_tables, drop_tables

# Importando todos os modelos
from .user import User, UserBase, UserCreate, UserUpdate, UserResponse
from .document import Document, DocumentBase, DocumentCreate, DocumentUpdate, DocumentResponse
from .clause import Clause, ClauseBase, ClauseCreate, ClauseUpdate, ClauseResponse
from .entity import Entity, EntityBase, EntityCreate, EntityUpdate, EntityResponse
from .compliance_flag import ComplianceFlag, ComplianceFlagBase, ComplianceFlagCreate, ComplianceFlagUpdate, ComplianceFlagResponse
from .deadline_alert import DeadlineAlert, DeadlineAlertBase, DeadlineAlertCreate, DeadlineAlertUpdate, DeadlineAlertResponse
from .report import Report, ReportBase, ReportCreate, ReportUpdate, ReportResponse
from .feedback import Feedback, FeedbackBase, FeedbackCreate, FeedbackUpdate, FeedbackResponse

# Lista de todos os modelos SQLAlchemy
__all__ = [
    # Configuração da base de dados
    "Base", "get_db", "create_tables", "drop_tables",
    
    # Modelos SQLAlchemy
    "User",
    "Document", 
    "Clause",
    "Entity",
    "ComplianceFlag",
    "DeadlineAlert",
    "Report",
    "Feedback",
    
    # Schemas Pydantic
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    "DocumentBase", "DocumentCreate", "DocumentUpdate", "DocumentResponse",
    "ClauseBase", "ClauseCreate", "ClauseUpdate", "ClauseResponse",
    "EntityBase", "EntityCreate", "EntityUpdate", "EntityResponse",
    "ComplianceFlagBase", "ComplianceFlagCreate", "ComplianceFlagUpdate", "ComplianceFlagResponse",
    "DeadlineAlertBase", "DeadlineAlertCreate", "DeadlineAlertUpdate", "DeadlineAlertResponse",
    "ReportBase", "ReportCreate", "ReportUpdate", "ReportResponse",
    "FeedbackBase", "FeedbackCreate", "FeedbackUpdate", "FeedbackResponse"
]

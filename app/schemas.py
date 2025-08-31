import datetime
from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

# Usamos um Enum para padronizar os status
class DocumentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, unique=True, index=True, nullable=False)
    s3_url = Column(String, nullable=False)
    status = Column(Enum(DocumentStatus), nullable=False, default=DocumentStatus.PENDING)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
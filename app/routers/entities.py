from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import get_db, Entity, EntityCreate, EntityUpdate, EntityResponse, Document, Clause

router = APIRouter(prefix="/entities", tags=["entities"])

@router.post("/", response_model=EntityResponse, status_code=status.HTTP_201_CREATED)
def create_entity(entity: EntityCreate, db: Session = Depends(get_db)):
    """
    Criar uma nova entidade
    """
    # Verificar se o documento existe
    document = db.query(Document).filter(Document.id == entity.document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Verificar se a cláusula existe (se fornecida)
    if entity.clause_id:
        clause = db.query(Clause).filter(Clause.id == entity.clause_id).first()
        if not clause:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cláusula não encontrada"
            )
    
    db_entity = Entity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

@router.get("/", response_model=List[EntityResponse])
def get_entities(
    skip: int = 0,
    limit: int = 100,
    document_id: int = None,
    clause_id: int = None,
    tipo_entidade: str = None,
    categoria: str = None,
    status: str = None,
    relevancia: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar entidades com filtros opcionais
    """
    query = db.query(Entity)
    
    if document_id:
        query = query.filter(Entity.document_id == document_id)
    
    if clause_id:
        query = query.filter(Entity.clause_id == clause_id)
    
    if tipo_entidade:
        query = query.filter(Entity.tipo_entidade == tipo_entidade)
    
    if categoria:
        query = query.filter(Entity.categoria == categoria)
    
    if status:
        query = query.filter(Entity.status == status)
    
    if relevancia:
        query = query.filter(Entity.relevancia == relevancia)
    
    entities = query.offset(skip).limit(limit).all()
    return entities

@router.get("/{entity_id}", response_model=EntityResponse)
def get_entity(entity_id: int, db: Session = Depends(get_db)):
    """
    Obter uma entidade específica por ID
    """
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entidade não encontrada"
        )
    return entity

@router.put("/{entity_id}", response_model=EntityResponse)
def update_entity(entity_id: int, entity_update: EntityUpdate, db: Session = Depends(get_db)):
    """
    Atualizar uma entidade
    """
    db_entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if db_entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entidade não encontrada"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = entity_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_entity, field, value)
    
    db.commit()
    db.refresh(db_entity)
    return db_entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entity(entity_id: int, db: Session = Depends(get_db)):
    """
    Deletar uma entidade
    """
    db_entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if db_entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entidade não encontrada"
        )
    
    db.delete(db_entity)
    db.commit()
    
    return None

@router.patch("/{entity_id}/status", response_model=EntityResponse)
def update_entity_status(entity_id: int, status: str, db: Session = Depends(get_db)):
    """
    Atualizar status de uma entidade
    """
    db_entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if db_entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entidade não encontrada"
        )
    
    valid_statuses = ["detectada", "validada", "rejeitada"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
        )
    
    db_entity.status = status
    if status == "validada":
        from datetime import datetime
        db_entity.data_validacao = datetime.now()
    
    db.commit()
    db.refresh(db_entity)
    return db_entity

@router.get("/types/")
def get_entity_types(db: Session = Depends(get_db)):
    """
    Obter tipos de entidades disponíveis
    """
    types = db.query(Entity.tipo_entidade).distinct().all()
    return [t[0] for t in types if t[0]]

@router.get("/categories/")
def get_entity_categories(db: Session = Depends(get_db)):
    """
    Obter categorias de entidades disponíveis
    """
    categories = db.query(Entity.categoria).distinct().all()
    return [c[0] for c in categories if c[0]]

@router.get("/statistics/")
def get_entities_statistics(db: Session = Depends(get_db)):
    """
    Obter estatísticas das entidades
    """
    total_entities = db.query(Entity).count()
    entities_by_status = db.query(Entity.status, db.func.count(Entity.id)).group_by(Entity.status).all()
    entities_by_type = db.query(Entity.tipo_entidade, db.func.count(Entity.id)).group_by(Entity.tipo_entidade).all()
    entities_by_relevance = db.query(Entity.relevancia, db.func.count(Entity.id)).group_by(Entity.relevancia).all()
    
    return {
        "total": total_entities,
        "by_status": dict(entities_by_status),
        "by_type": dict(entities_by_type),
        "by_relevance": dict(entities_by_relevance)
    }

@router.get("/search/")
def search_entities(
    texto: str = None,
    tipo_entidade: str = None,
    categoria: str = None,
    db: Session = Depends(get_db)
):
    """
    Buscar entidades por texto ou critérios
    """
    query = db.query(Entity)
    
    if texto:
        query = query.filter(Entity.texto.ilike(f"%{texto}%"))
    
    if tipo_entidade:
        query = query.filter(Entity.tipo_entidade == tipo_entidade)
    
    if categoria:
        query = query.filter(Entity.categoria == categoria)
    
    entities = query.all()
    return entities 
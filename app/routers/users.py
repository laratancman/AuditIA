from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import bcrypt

from app.models import get_db, User, UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

# Função auxiliar para hash de senha
def hash_password(password: str) -> str:
    """Hash da senha usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Função auxiliar para verificar senha
def verify_password(password: str, hashed: str) -> bool:
    """Verifica se a senha está correta"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Criar um novo usuário
    """
    # Verificar se o email já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    # Criar hash da senha
    hashed_password = hash_password(user.senha)
    
    # Criar usuário
    db_user = User(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_password,
        permissao=user.permissao,
        telefone=user.telefone,
        departamento=user.departamento,
        cargo=user.cargo
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    ativo: bool = None,
    permissao: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar usuários com filtros opcionais
    """
    query = db.query(User)
    
    if ativo is not None:
        query = query.filter(User.ativo == ativo)
    
    if permissao:
        query = query.filter(User.permissao == permissao)
    
    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obter um usuário específico por ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Atualizar um usuário
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = user_update.dict(exclude_unset=True)
    
    # Se estiver atualizando o email, verificar se já existe
    if "email" in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletar um usuário (soft delete - apenas desativa)
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Soft delete - apenas desativa o usuário
    db_user.ativo = False
    db.commit()
    
    return None

@router.patch("/{user_id}/activate", response_model=UserResponse)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """
    Reativar um usuário
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    db_user.ativo = True
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}/documents")
def get_user_documents(user_id: int, db: Session = Depends(get_db)):
    """
    Obter documentos de um usuário
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user.documents 
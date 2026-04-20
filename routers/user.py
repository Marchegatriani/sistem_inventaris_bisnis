from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import user as models_user
from schemas import user as schemas_user
from auth.security import oauth2_scheme, get_password_hash
from auth.dependencies import get_current_user, get_current_superadmin

router = APIRouter(
    prefix="/users",
    tags=["Manajemen User"]
)

@router.post("/", response_model=schemas_user.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db), superadmin_user: models_user.User = Depends(get_current_superadmin)):
    db_user = db.query(models_user.User).filter(models_user.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    
    hashed_password = get_password_hash(user.password)
    
    new_user = models_user.User(
        username=user.username, 
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas_user.UserResponse])
def get_all_users(db: Session = Depends(get_db), superadmin_user: models_user.User = Depends(get_current_superadmin)):
    return db.query(models_user.User).all()

@router.get("/{id}", response_model=schemas_user.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db), superadmin_user: models_user.User = Depends(get_current_superadmin)):
    user = db.query(models_user.User).filter(models_user.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")
    return user

@router.put("/{id}", response_model=schemas_user.UserResponse)
def update_user(id: int, user_update: schemas_user.UserCreate, db: Session = Depends(get_db), superadmin_user: models_user.User = Depends(get_current_superadmin)):
    user = db.query(models_user.User).filter(models_user.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")
    
    if user.username != user_update.username:
        db_user_check = db.query(models_user.User).filter(models_user.User.username == user_update.username).first()
        if db_user_check:
            raise HTTPException(status_code=400, detail="Username sudah dipakai oleh user lain")
            
    user.username = user_update.username
    user.hashed_password = get_password_hash(user_update.password)
    user.role = user_update.role
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), superadmin_user: models_user.User = Depends(get_current_superadmin)):
    user = db.query(models_user.User).filter(models_user.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")
    
    db.delete(user)
    db.commit()
    return None
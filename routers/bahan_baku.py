from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import bahan_baku as models_bahan
from schemas import bahan_baku as schemas_bahan
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/bahan-baku",
    tags=["Manajemen Bahan Baku"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas_bahan.BahanBakuResponse, status_code=status.HTTP_201_CREATED)
def create_bahan(bahan: schemas_bahan.BahanBakuCreate, db: Session = Depends(get_db)):
    db_bahan = models_bahan.BahanBaku(**bahan.model_dump())
    db.add(db_bahan)
    db.commit()
    db.refresh(db_bahan)
    return db_bahan

@router.get("/", response_model=List[schemas_bahan.BahanBakuResponse])
def get_all_bahan(db: Session = Depends(get_db)):
    return db.query(models_bahan.BahanBaku).all()

@router.get("/{id}", response_model=schemas_bahan.BahanBakuResponse)
def get_bahan_by_id(id: int, db: Session = Depends(get_db)):
    bahan = db.query(models_bahan.BahanBaku).filter(models_bahan.BahanBaku.id == id).first()
    if not bahan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bahan baku tidak ditemukan")
    return bahan

@router.put("/{id}", response_model=schemas_bahan.BahanBakuResponse)
def update_bahan(id: int, bahan_update: schemas_bahan.BahanBakuCreate, db: Session = Depends(get_db)):
    bahan = db.query(models_bahan.BahanBaku).filter(models_bahan.BahanBaku.id == id).first()
    if not bahan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bahan baku tidak ditemukan")
    
    # Update data bahan baku (bisa digunakan untuk mengurangi/menyesuaikan stok)
    bahan.nama_bahan = bahan_update.nama_bahan
    bahan.stok_bahan = bahan_update.stok_bahan
    bahan.satuan = bahan_update.satuan
    
    db.commit()
    db.refresh(bahan)
    return bahan

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bahan(id: int, db: Session = Depends(get_db)):
    bahan = db.query(models_bahan.BahanBaku).filter(models_bahan.BahanBaku.id == id).first()
    if not bahan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bahan baku tidak ditemukan")
    
    db.delete(bahan)
    db.commit()
    return None
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import kategori as models_kategori
from schemas import kategori as schemas_kategori
from auth.dependencies import get_current_admin

router = APIRouter(
    prefix="/kategori",
    tags=["Kategori Produk"],
    dependencies=[Depends(get_current_admin)]
)

@router.post("/", response_model=schemas_kategori.KategoriResponse, status_code=status.HTTP_201_CREATED)
def create_kategori(kategori: schemas_kategori.KategoriCreate, db: Session = Depends(get_db)):
    db_kategori = db.query(models_kategori.Kategori).filter(models_kategori.Kategori.nama_kategori == kategori.nama_kategori).first()
    if db_kategori:
        raise HTTPException(status_code=400, detail="Kategori sudah terdaftar")
    
    kategori_baru = models_kategori.Kategori(**kategori.model_dump())
    db.add(kategori_baru)
    db.commit()
    db.refresh(kategori_baru)
    return kategori_baru

@router.get("/", response_model=List[schemas_kategori.KategoriResponse])
def get_all_kategori(db: Session = Depends(get_db)):
    return db.query(models_kategori.Kategori).all()

@router.get("/{id}", response_model=schemas_kategori.KategoriResponse)
def get_kategori_by_id(id: int, db: Session = Depends(get_db)):
    kategori = db.query(models_kategori.Kategori).filter(models_kategori.Kategori.id == id).first()
    if not kategori:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kategori tidak ditemukan")
    return kategori

@router.put("/{id}", response_model=schemas_kategori.KategoriResponse)
def update_kategori(id: int, kategori_update: schemas_kategori.KategoriCreate, db: Session = Depends(get_db)):
    kategori = db.query(models_kategori.Kategori).filter(models_kategori.Kategori.id == id).first()
    if not kategori:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kategori tidak ditemukan")
    
    kategori.nama_kategori = kategori_update.nama_kategori
    kategori.deskripsi = kategori_update.deskripsi
    db.commit()
    db.refresh(kategori)
    return kategori

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kategori(id: int, db: Session = Depends(get_db)):
    kategori = db.query(models_kategori.Kategori).filter(models_kategori.Kategori.id == id).first()
    if not kategori:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kategori tidak ditemukan")
    
    db.delete(kategori)
    db.commit()
    return None
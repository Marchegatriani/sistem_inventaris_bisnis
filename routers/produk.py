from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from database import get_db
from models import produk as models_produk
from models import kategori as models_kategori
from schemas import produk as schemas_produk
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/produk",
    tags=["Produk Kerajinan"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas_produk.ProdukResponse, status_code=status.HTTP_201_CREATED)
def create_produk(produk: schemas_produk.ProdukCreate, db: Session = Depends(get_db)):
    kategori = db.query(models_kategori.Kategori).filter(func.lower(models_kategori.Kategori.nama_kategori) == produk.nama_kategori.lower()).first()
    
    if not kategori:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Kategori '{produk.nama_kategori}' tidak ditemukan. Silakan buat kategori terlebih dahulu.")

    produk_data = produk.model_dump()
    produk_data.pop("nama_kategori")
    produk_data["kategori_id"] = kategori.id

    produk_baru = models_produk.Produk(**produk_data)
    db.add(produk_baru)
    db.commit()
    db.refresh(produk_baru)
    return produk_baru

@router.get("/", response_model=List[schemas_produk.ProdukResponse])
def get_all_produk(db: Session = Depends(get_db)):
    return db.query(models_produk.Produk).all()

@router.get("/{id}", response_model=schemas_produk.ProdukResponse)
def get_produk_by_id(id: int, db: Session = Depends(get_db)):
    produk = db.query(models_produk.Produk).filter(models_produk.Produk.id == id).first()
    if not produk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")
    return produk

@router.put("/{id}", response_model=schemas_produk.ProdukResponse)
def update_produk(id: int, produk_update: schemas_produk.ProdukCreate, db: Session = Depends(get_db)):
    produk = db.query(models_produk.Produk).filter(models_produk.Produk.id == id).first()
    if not produk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")
    
    # Cari kategori baru berdasarkan nama
    kategori = db.query(models_kategori.Kategori).filter(func.lower(models_kategori.Kategori.nama_kategori) == produk_update.nama_kategori.lower()).first()
    if not kategori:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Kategori '{produk_update.nama_kategori}' tidak ditemukan. Silakan buat kategori terlebih dahulu.")

    update_data = produk_update.model_dump()
    update_data.pop("nama_kategori")
    update_data["kategori_id"] = kategori.id
    
    for var, value in update_data.items():
        setattr(produk, var, value) if value is not None else None

    db.commit()
    db.refresh(produk)
    return produk

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produk(id: int, db: Session = Depends(get_db)):
    produk = db.query(models_produk.Produk).filter(models_produk.Produk.id == id).first()
    if not produk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")
    
    db.delete(produk)
    db.commit()
    return None
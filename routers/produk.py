from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import produk as models_produk
from models import kategori as models_kategori
from schemas import produk as schemas_produk

router = APIRouter(
    prefix="/produk",
    tags=["Produk Kerajinan"]
)

@router.post("/", response_model=schemas_produk.ProdukResponse, status_code=status.HTTP_201_CREATED)
def create_produk(produk: schemas_produk.ProdukCreate, db: Session = Depends(get_db)):
    # Cek dulu apakah kategori_id yang dimasukkan benar-benar ada di tabel kategori
    kategori_ada = db.query(models_kategori.Kategori).filter(models_kategori.Kategori.id == produk.kategori_id).first()
    if not kategori_ada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kategori ID tersebut tidak ditemukan")

    produk_baru = models_produk.Produk(**produk.model_dump())
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
    
    for var, value in vars(produk_update).items():
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
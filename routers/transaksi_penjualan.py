from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import transaksi_penjualan as models_transaksi
from models import produk as models_produk
from schemas import transaksi_penjualan as schemas_transaksi

from auth.security import oauth2_scheme

router = APIRouter(
    prefix="/transaksi-penjualan",
    tags=["Transaksi Penjualan"]
)

@router.post("/", response_model=schemas_transaksi.TransaksiPenjualanResponse, status_code=status.HTTP_201_CREATED)
def create_transaksi(transaksi: schemas_transaksi.TransaksiPenjualanCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    produk = db.query(models_produk.Produk).filter(models_produk.Produk.id == transaksi.produk_id).first()
    
    if not produk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")
    
    if produk.stok_produk < transaksi.jumlah_terjual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Stok tidak mencukupi. Sisa stok saat ini: {produk.stok_produk}"
        )

    transaksi_baru = models_transaksi.TransaksiPenjualan(**transaksi.model_dump())
    db.add(transaksi_baru)
    
    produk.stok_produk -= transaksi.jumlah_terjual
    
    db.commit()
    db.refresh(transaksi_baru)
    return transaksi_baru

@router.get("/", response_model=List[schemas_transaksi.TransaksiPenjualanResponse])
def get_all_transaksi(db: Session = Depends(get_db)):
    return db.query(models_transaksi.TransaksiPenjualan).all()
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

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
    # Cari produk berdasarkan nama, abaikan huruf besar/kecil
    produk = db.query(models_produk.Produk).filter(func.lower(models_produk.Produk.nama_produk) == transaksi.nama_produk.lower()).first()
    
    if not produk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produk dengan nama '{transaksi.nama_produk}' tidak ditemukan")
    
    if produk.stok_produk < transaksi.jumlah_terjual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Stok tidak mencukupi. Sisa stok saat ini: {produk.stok_produk}"
        )

    # Hitung total pemasukan otomatis
    total_pemasukan = produk.harga_jual * transaksi.jumlah_terjual
    
    transaksi_baru = models_transaksi.TransaksiPenjualan(
        produk_id=produk.id,
        jumlah_terjual=transaksi.jumlah_terjual,
        total_pemasukan=total_pemasukan
    )
    db.add(transaksi_baru)
    
    produk.stok_produk -= transaksi.jumlah_terjual
    
    db.commit()
    db.refresh(transaksi_baru)
    return transaksi_baru

@router.get("/", response_model=List[schemas_transaksi.TransaksiPenjualanResponse])
def get_all_transaksi(db: Session = Depends(get_db)):
    return db.query(models_transaksi.TransaksiPenjualan).all()
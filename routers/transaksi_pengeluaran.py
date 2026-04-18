from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import transaksi_pengeluaran as models_pengeluaran
from models import bahan_baku as models_bahan
from schemas import transaksi_pengeluaran as schemas_pengeluaran
from auth.security import oauth2_scheme

router = APIRouter(
    prefix="/transaksi-pengeluaran",
    tags=["Transaksi Pengeluaran"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/", response_model=schemas_pengeluaran.TransaksiPengeluaranResponse, status_code=status.HTTP_201_CREATED)
def create_pengeluaran(transaksi: schemas_pengeluaran.TransaksiPengeluaranCreate, db: Session = Depends(get_db)):
    bahan = db.query(models_bahan.BahanBaku).filter(models_bahan.BahanBaku.id == transaksi.bahan_baku_id).first()
    if not bahan:
        raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")

    transaksi_baru = models_pengeluaran.TransaksiPengeluaran(**transaksi.model_dump())
    db.add(transaksi_baru)
    
    bahan.stok_bahan += transaksi.jumlah_dibeli
    
    db.commit()
    db.refresh(transaksi_baru)
    return transaksi_baru
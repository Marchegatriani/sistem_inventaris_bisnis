from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from database import get_db
from models import transaksi_pengeluaran as models_pengeluaran
from models import bahan_baku as models_bahan
from models import user as models_user
from schemas import transaksi_pengeluaran as schemas_pengeluaran
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/transaksi-pengeluaran",
    tags=["Transaksi Pengeluaran"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas_pengeluaran.TransaksiPengeluaranResponse, status_code=status.HTTP_201_CREATED)
def create_pengeluaran(transaksi: schemas_pengeluaran.TransaksiPengeluaranCreate, db: Session = Depends(get_db), current_user: models_user.User = Depends(get_current_user)):
    # Cari bahan baku berdasarkan nama (abaikan huruf besar/kecil)
    bahan = db.query(models_bahan.BahanBaku).filter(func.lower(models_bahan.BahanBaku.nama_bahan) == transaksi.nama_bahan.lower()).first()
    
    # LOGIC BARU: Jika bahan baku belum ada, buat otomatis di database!
    if not bahan:
        bahan = models_bahan.BahanBaku(nama_bahan=transaksi.nama_bahan, stok_bahan=0, satuan=transaksi.satuan)
        db.add(bahan)
        db.commit()
        db.refresh(bahan)

    total_pengeluaran = transaksi.jumlah_dibeli * transaksi.harga_beli_satuan
    
    transaksi_baru = models_pengeluaran.TransaksiPengeluaran(
        bahan_baku_id=bahan.id,
        jumlah_dibeli=transaksi.jumlah_dibeli,
        harga_beli_satuan=transaksi.harga_beli_satuan,
        total_pengeluaran=total_pengeluaran,
        user_id=current_user.id # <-- SIMPAN ID USER YANG LOGIN
    )
    db.add(transaksi_baru)
    
    bahan.stok_bahan += transaksi.jumlah_dibeli
    
    db.commit()
    db.refresh(transaksi_baru)
    return transaksi_baru

@router.get("/", response_model=List[schemas_pengeluaran.TransaksiPengeluaranResponse])
def get_all_pengeluaran(db: Session = Depends(get_db)):
    return db.query(models_pengeluaran.TransaksiPengeluaran).all()
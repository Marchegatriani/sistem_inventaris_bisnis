from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransaksiPengeluaranBase(BaseModel):
    bahan_baku_id: int
    jumlah_dibeli: int
    harga_beli_satuan: int

class TransaksiPengeluaranCreate(BaseModel):
    nama_bahan: str
    satuan: str = "Pcs"  # Default satuan jika ternyata ini bahan baku baru
    jumlah_dibeli: int
    harga_beli_satuan: int

class TransaksiPengeluaranResponse(TransaksiPengeluaranBase):
    id: int
    total_pengeluaran: int
    user_id: int
    waktu_transaksi: datetime

    class Config:
        from_attributes = True
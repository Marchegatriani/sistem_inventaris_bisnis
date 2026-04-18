from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransaksiPengeluaranBase(BaseModel):
    bahan_baku_id: int
    jumlah_dibeli: int
    harga_beli_satuan: int
    total_pengeluaran: int

class TransaksiPengeluaranCreate(TransaksiPengeluaranBase):
    pass

class TransaksiPengeluaranResponse(TransaksiPengeluaranBase):
    id: int
    waktu_transaksi: datetime

    class Config:
        from_attributes = True
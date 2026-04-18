from pydantic import BaseModel
from datetime import datetime

class TransaksiPenjualanBase(BaseModel):
    produk_id: int
    jumlah_terjual: int

class TransaksiPenjualanCreate(BaseModel):
    nama_produk: str
    jumlah_terjual: int

class TransaksiPenjualanResponse(TransaksiPenjualanBase):
    id: int
    total_pemasukan: int
    waktu_transaksi: datetime

    class Config:
        from_attributes = True
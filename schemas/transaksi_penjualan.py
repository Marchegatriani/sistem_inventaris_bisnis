from pydantic import BaseModel
from datetime import datetime

class TransaksiPenjualanBase(BaseModel):
    produk_id: int
    jumlah_terjual: int
    total_pemasukan: int

class TransaksiPenjualanCreate(TransaksiPenjualanBase):
    pass

class TransaksiPenjualanResponse(TransaksiPenjualanBase):
    id: int
    waktu_transaksi: datetime

    class Config:
        from_attributes = True
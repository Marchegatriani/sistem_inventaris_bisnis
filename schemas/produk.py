from pydantic import BaseModel
from typing import Optional

class ProdukBase(BaseModel):
    nama_produk: str
    kategori_id: int
    stok_produk: int
    harga_jual: int
    deskripsi: Optional[str] = None

class ProdukCreate(ProdukBase):
    pass

class ProdukResponse(ProdukBase):
    id: int

    class Config:
        from_attributes = True
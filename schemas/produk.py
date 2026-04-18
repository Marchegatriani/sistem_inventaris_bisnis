from pydantic import BaseModel
from typing import Optional

class ProdukBase(BaseModel):
    nama_produk: str
    stok_produk: int
    harga_jual: int
    deskripsi: Optional[str] = None

class ProdukCreate(ProdukBase):
    nama_kategori: str

class ProdukResponse(ProdukBase):
    id: int
    kategori_id: int
    user_id: int

    class Config:
        from_attributes = True
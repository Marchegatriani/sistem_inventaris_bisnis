from pydantic import BaseModel
from typing import Optional

class KategoriBase(BaseModel):
    nama_kategori: str
    deskripsi: Optional[str] = None

class KategoriCreate(KategoriBase):
    pass

class KategoriResponse(KategoriBase):
    id: int

    class Config:
        from_attributes = True
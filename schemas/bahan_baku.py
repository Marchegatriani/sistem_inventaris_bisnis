from pydantic import BaseModel

class BahanBakuBase(BaseModel):
    nama_bahan: str
    stok_bahan: int
    satuan: str

class BahanBakuCreate(BahanBakuBase):
    pass

class BahanBakuResponse(BahanBakuBase):
    id: int

    class Config:
        from_attributes = True
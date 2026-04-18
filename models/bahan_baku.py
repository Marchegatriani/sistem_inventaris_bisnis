from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class BahanBaku(Base):
    __tablename__ = "bahan_baku"

    id = Column(Integer, primary_key=True, index=True)
    nama_bahan = Column(String(100), index=True)
    stok_bahan = Column(Integer, default=0)
    satuan = Column(String(50)) # Contoh: "Meter", "Gulung", "Pcs"

    transaksi_pengeluaran = relationship("TransaksiPengeluaran", back_populates="bahan_baku")
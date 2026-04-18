from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class TransaksiPengeluaran(Base):
    __tablename__ = "transaksi_pengeluaran"

    id = Column(Integer, primary_key=True, index=True)
    waktu_transaksi = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    bahan_baku_id = Column(Integer, ForeignKey("bahan_baku.id"))
    jumlah_dibeli = Column(Integer)
    harga_beli_satuan = Column(Integer)
    total_pengeluaran = Column(Integer)
    
    # Foreign key ke tabel user
    user_id = Column(Integer, ForeignKey("users.id"))

    bahan_baku = relationship("BahanBaku", back_populates="transaksi_pengeluaran")
    # Relasi ke tabel User
    user = relationship("User", back_populates="transaksi_pengeluaran")
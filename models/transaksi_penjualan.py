from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class TransaksiPenjualan(Base):
    __tablename__ = "transaksi_penjualan"

    id = Column(Integer, primary_key=True, index=True)
    # Waktu akan otomatis terisi saat transaksi dibuat
    waktu_transaksi = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Foreign key ke tabel produk
    produk_id = Column(Integer, ForeignKey("produk.id"))
    jumlah_terjual = Column(Integer)
    total_pemasukan = Column(Integer)
    
    # Foreign key ke tabel user
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relasi balik ke tabel Produk
    produk = relationship("Produk", back_populates="transaksi_penjualan")
    # Relasi ke tabel User
    user = relationship("User", back_populates="transaksi_penjualan")
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))

    # Relasi balik untuk melacak transaksi yang dibuat oleh user
    transaksi_penjualan = relationship("TransaksiPenjualan", back_populates="user")
    transaksi_pengeluaran = relationship("TransaksiPengeluaran", back_populates="user")
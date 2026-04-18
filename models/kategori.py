from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Kategori(Base):
    __tablename__ = "kategori_produk"

    id = Column(Integer, primary_key=True, index=True)
    nama_kategori = Column(String(50), unique=True, index=True)
    deskripsi = Column(String(255), nullable=True)

    # Relasi ke tabel produk (Satu kategori punya banyak produk)
    produk = relationship("Produk", back_populates="kategori")
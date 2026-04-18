from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Produk(Base):
    __tablename__ = "produk"

    id = Column(Integer, primary_key=True, index=True)
    nama_produk = Column(String(100), index=True)
    kategori_id = Column(Integer, ForeignKey("kategori_produk.id"))
    stok_produk = Column(Integer, default=0)
    harga_jual = Column(Integer)
    deskripsi = Column(String(255), nullable=True)

    # Foreign key ke tabel user
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relasi balik ke tabel Kategori
    kategori = relationship("Kategori", back_populates="produk")
    
    # Relasi ke tabel User
    user = relationship("User", back_populates="produk")

    # Relasi ke tabel Transaksi Penjualan (Satu produk bisa dijual berkali-kali)
    # Nanti kita buat file transaksi_penjualan.py
    # (Tambahkan ini di bagian bawah dalam class Produk)
    transaksi_penjualan = relationship("TransaksiPenjualan", back_populates="produk")
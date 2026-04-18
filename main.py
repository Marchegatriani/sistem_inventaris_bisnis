from fastapi import FastAPI
from database import engine, Base

# Urutan import diatur ulang untuk memastikan model dasar dimuat terlebih dahulu
# sebelum model yang memiliki relasi (ForeignKey) kepadanya.
from routers import auth as router_auth
from routers import user as router_user
from routers import kategori as router_kategori
from routers import bahan_baku as router_bahan
from routers import produk as router_produk
from routers import transaksi_penjualan as router_transaksi
from routers import transaksi_pengeluaran as router_pengeluaran

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Manajemen Produk dan Inventaris Bisnis Kerajinan Tangan (Crocheting)!",
    description="Sistem informasi manajemen stok dan pencatatan penjualan/pengeluaran",
    version="1.0.0"
)

# Urutan include_router tidak terlalu berpengaruh pada error ini,
# namun lebih rapi jika disamakan dengan urutan import.
app.include_router(router_auth.router)
app.include_router(router_user.router)
app.include_router(router_kategori.router)
app.include_router(router_bahan.router)
app.include_router(router_produk.router)
app.include_router(router_transaksi.router)
app.include_router(router_pengeluaran.router)

@app.get("/")
def root():
    return {"message": "Selamat datang di API Manajemen Produk dan Inventaris Bisnis Kerajinan Tangan!"}
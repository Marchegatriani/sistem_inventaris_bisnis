from fastapi import FastAPI
from database import engine, Base
from routers import produk as router_produk
from routers import transaksi_penjualan as router_transaksi
from routers import auth as router_auth
from routers import bahan_baku as router_bahan
from routers import transaksi_pengeluaran as router_pengeluaran
from routers import kategori as router_kategori

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Manajemen Produk dan Inventaris Bisnis",
    description="Sistem informasi manajemen stok dan pencatatan penjualan/pengeluaran",
    version="1.0.0"
)

app.include_router(router_kategori.router)
app.include_router(router_produk.router)
app.include_router(router_transaksi.router)
app.include_router(router_auth.router)
app.include_router(router_bahan.router)
app.include_router(router_pengeluaran.router)

@app.get("/")
def root():
    return {"message": "Selamat datang di API Manajemen Produk dan Inventaris Bisnis"}
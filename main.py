from fastapi import FastAPI
from database import engine, Base, SessionLocal
from sqlalchemy.exc import OperationalError
import sys
import time
import os
from dotenv import load_dotenv

from models import user as models_user
from auth.security import get_password_hash

from routers import auth as router_auth
from routers import user as router_user
from routers import kategori as router_kategori
from routers import bahan_baku as router_bahan
from routers import produk as router_produk
from routers import transaksi_penjualan as router_transaksi
from routers import transaksi_pengeluaran as router_pengeluaran

load_dotenv()

def create_super_admin_if_needed():
    """Fungsi untuk membuat super admin jika tidak ada user sama sekali di database."""
    db = SessionLocal()
    try:
        if db.query(models_user.User).first() is None:
            admin_username = os.getenv("SUPER_ADMIN_USERNAME", "admin")
            admin_password = os.getenv("SUPER_ADMIN_PASSWORD")

            if not admin_password:
                print("!!! PERINGATAN: Variabel SUPER_ADMIN_PASSWORD tidak diatur di .env. Super admin tidak dapat dibuat.")
                return

            hashed_password = get_password_hash(admin_password)
            super_admin = models_user.User(
                username=admin_username,
                hashed_password=hashed_password,
                role=models_user.UserRole.superadmin
            )
            db.add(super_admin)
            db.commit()
            print(f"--- Super admin '{admin_username}' berhasil dibuat secara otomatis. ---")
    finally:
        db.close()

try:
    time.sleep(2)
    Base.metadata.create_all(bind=engine)
    print("Koneksi database berhasil dan tabel telah disiapkan.")
    create_super_admin_if_needed()
except OperationalError as e:
    print("--- GAGAL TERHUBUNG KE DATABASE ---")
    print(f"Pastikan service MySQL (misal: dari XAMPP) sudah berjalan dan database '{engine.url.database}' sudah dibuat.")
    print("Detail error:", e)
    sys.exit(1)


app = FastAPI(
    title="API Manajemen Produk dan Inventaris Bisnis Kerajinan Tangan (Crocheting)!",
    description="Sistem informasi manajemen stok dan pencatatan penjualan/pengeluaran",
    version="1.0.0"
)

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
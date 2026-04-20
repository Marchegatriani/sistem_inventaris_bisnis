# 🧶 CrochetBiz - API Manajemen Inventaris

Sistem Backend API terintegrasi yang dibangun menggunakan **FastAPI** untuk mendukung digitalisasi operasional bisnis kerajinan tangan (*crochet*). Sistem ini mengotomatisasi pencatatan stok bahan baku, manajemen produk jadi, serta riwayat transaksi penjualan dan pengeluaran secara presisi.

## 🚀 Fitur Utama
* **Manajemen Inventaris:** CRUD lengkap untuk Produk, Kategori Produk, dan Bahan Baku.
* **Sistem Transaksi:** Otomasi pengurangan stok produk saat penjualan dan penambahan stok bahan baku saat pembelian.
* **Keamanan Berbasis JWT:** Implementasi *JSON Web Token (JWT)* untuk memastikan setiap aktivitas data hanya dapat diakses oleh pengguna terotorisasi.
* **Audit Trail:** Sistem dirancang untuk menjaga integritas data dan meminimalisir kesalahan pencatatan manual (*human error*).
* **Modular Monolith:** Struktur kode yang terbagi per modul (router) untuk memudahkan pemeliharaan dan pengembangan sistem di masa depan.

## 🛠 Tech Stack
* **Framework:** FastAPI
* **Database:** MySQL
* **ORM:** SQLAlchemy
* **Authentication:** PyJWT
* **Validation:** Pydantic
* **Documentation:** Swagger UI (/docs)

## ⚙️ Cara Menjalankan

1. **Clone Repositori:**
   ```bash
   git clone [https://github.com/Marchegatriani/sistem_inventaris_bisnis]
   cd sistem_inventaris_bisnis

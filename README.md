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

2. **Setup Virtual Environment:**
    ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Konfigurasi Database:**
- Pastikan MySQL server berjalan.
- Buat database baru bernama sistem_inventaris_bisnis.
- Sesuaikan connection string di file konfigurasi proyek kamu.

5. **Jalankan Server:**
    ```bash
   uvicorn main:app --reload

6. **Akses API:**
   Buka browser dan akses http://127.0.0.1:8000/docs untuk melihat dokumentasi API dan melakukan testing melalui Swagger UI.

Daftar Endpoint
<img width="392" height="654" alt="image" src="https://github.com/user-attachments/assets/04dc292a-31cc-42db-906c-b90a089c3102" />

👤 Author
Marche Gatriani Sude - Sistem Informasi, Universitas Hasanuddin

Proyek ini dikembangkan sebagai bagian dari Ujian Tengah Semester (UTS) mata kuliah Pemrograman Web Lanjutan.

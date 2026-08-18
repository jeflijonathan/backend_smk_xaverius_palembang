version python 1.11.3

# role user

1. TEACHER (guru)
2. STUDENT (Siswa)
3. ClassCaptain (Ketua kelas)
4. Secretary (Seketaris)
5. ADMIN (Admin sekolah)
6. CLASSADVISOR (Wali Kelas)
7. KURIKULUM (Kurikulum)
8. HEADMASTER (Kepala sekolah)

## Running the Application (Development)

To start the local FastAPI server with the auto-reload feature (the server automatically restarts every time a code change is made):

```bash
 python -m uvicorn main:router_instance.app --reload
```

## 🛠️ System & Installation Requirements

If this is your first time downloading or moving this project to a new device, install all the required libraries with the following command:

```bash
pip install -r requirements.txt
```

## 🛠️ Code Quality & Linting (Ruff)

Proyek ini menggunakan **Ruff** sebagai alat penjamin kualitas kode (_linter_ dan _code formatter_). Ruff bertugas untuk memindai seluruh basis kode Python secara otomatis guna memastikan kode tetap bersih, konsisten, aman, dan bebas dari _bug_ pasif.

### 🚀 Mengapa Menggunakan Ruff?

- **Super Cepat:** Ditulis menggunakan bahasa Rust, Ruff mampu mengecek kode puluhan hingga ratusan kali lebih cepat dibandingkan _linter_ tradisional seperti Flake8, Black, atau Pylint.
- **All-in-One:** Menggantikan peran berbagai _tools_ sekaligus (menggantikan Flake8, isort, Black, bandit, dan banyak lagi).
- **Auto-Fix:** Mampu memperbaiki mayoritas kesalahan penulisan kode secara instan.

```bash
python -m ruff check .
```

```bash
pip install ruff
```

## 📦 Manajemen Dependensi (pipreqs)

This project uses **pipreqs** to manage and update the `requirements.txt` file.

Unlike the default `pip freeze` command, which lists all packages in the virtual environment (including library dependencies from accidentally installed tools), **pipreqs** intelligently looks only at the `import` keywords actually written in your Python code.

### 🛠️ Cara Update `requirements.txt`

Jalankan perintah ini di terminal untuk memperbarui daftar library yang dipakai:

```bash
pip install pipreqs
pipreqs . --force
```

### 📊 Comparison: `pip freeze` vs `pipreqs`

| Features           | `pip freeze`                       | `pipreqs` (This Project)                   |
| :----------------- | :--------------------------------- | :----------------------------------------- |
| **How ​​It Works** | Emptying venv contents into a file | Scanning program code (`import`)           |
| **File Contents**  | Often bloated                      | Clean and essential                        |
| **Server Impact**  | Heavier & slower deployment        | Much faster container/server build process |

### 🚀 Why Use pipreqs?

- **Clean & Minimalist:** The `requirements.txt` file only contains the core libraries that are actually used by the application.
- **Lightweight Application Size:** Prevents bloating of container (Docker) image size or server memory during deployment because there are no unnecessary library installations.
- **Accurate Version Tracking:** Automatically detects the currently active library version on your local machine to avoid production mismatch issues.

---

### 💻 Local Usage Guide

#### A. For Developers (Updating New Dependencies)

If you've recently added or written new `import` code and want to update your `requirements.txt` list:

1. **Install pipreqs** (Just do it once at the start)

```bash
pip install pipreqs
```

2. **implement pipreqs**

```bash
python -m pipreqs.pipreqs . --force
```

## 🗄️ Database Migration & Synchronization

Proyek ini memiliki dua pendekatan dalam menangani perubahan struktur database:

### 1. Sinkronisasi Otomatis (Membuat Tabel Baru)
Secara bawaan, aplikasi akan mengecek dan membuat tabel secara otomatis jika tabel tersebut belum ada di database. Proses ini terjadi setiap kali Anda menjalankan file `run.py`:

```bash
python run.py
```
> **Catatan:** Fitur ini (melalui `Base.metadata.create_all()`) **hanya akan membuat tabel baru**. Fitur ini tidak dapat mendeteksi perubahan skema pada tabel yang sudah ada (misalnya menambah, menghapus, atau mengubah nama kolom).

### 2. Migrasi Manual (Mengubah Skema Tabel)
Jika Anda perlu melakukan perubahan pada tabel yang sudah ada (seperti menambah kolom baru, mengubah tipe data, dll), proyek ini menyediakan file `fix_db.py` untuk menjalankan _raw SQL_ secara langsung.

**Langkah-langkah Migrasi Manual:**
1. Buka file `fix_db.py`.
2. Ubah query SQL di dalam `conn.execute(text("..."))` sesuai dengan modifikasi tabel yang Anda butuhkan.
   Contoh penambahan kolom:
   ```python
   conn.execute(text("ALTER TABLE nama_tabel ADD COLUMN nama_kolom VARCHAR(255);"))
   ```
3. Jalankan script tersebut di terminal:
   ```bash
   python fix_db.py
   ```
> Jika ke depannya proyek menjadi lebih kompleks, disarankan untuk menginstal dan menginisialisasi **Alembic** agar riwayat migrasi struktur database dapat dikelola dengan lebih rapi (meskipun saat ini `alembic.ini` sudah ada, foldernya belum dikonfigurasi sepenuhnya).

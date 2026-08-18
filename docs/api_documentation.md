# API Documentation

Dokumen ini menjelaskan struktur Response API dan cara melakukan request untuk domain-domain yang tersedia di sistem ini (Employee, Subject, dan Student). 

Setiap endpoint API umumnya akan mengembalikan data dalam format JSON. Karena kita menggunakan FastAPI dan Pydantic, response akan tervalidasi secara otomatis berdasarkan schema yang telah dibuat di folder `dto`.

---

## 1. Domain: Employee

Base URL: `/api/employees`

### A. Create Employee
Mendaftarkan pegawai baru beserta akun *user* (untuk login).

- **Method**: `POST`
- **URL**: `/api/employees/`
- **Request Body** (`application/json`):
```json
{
  "user": {
    "username": "johndoe",
    "password": "password123"
  },
  "profile": {
    "first_name": "John",
    "last_name": "Doe",
    "niy": "12345678",
    "gender": "L",
    "birth_place": "Jakarta",
    "birth_date": "1990-01-01",
    "email": "johndoe@example.com",
    "address": "Jl. Sudirman",
    "phone_number": "081234567890"
  }
}
```

- **Success Response** (`200 OK`):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "profile_url": null,
  "niy": "12345678",
  "gender": "L",
  "birth_place": "Jakarta",
  "birth_date": "1990-01-01",
  "email": "johndoe@example.com",
  "address": "Jl. Sudirman",
  "RT": null,
  "RW": null,
  "zip_code": null,
  "phone_number": "081234567890",
  "description": null,
  "status": true,
  "id": "e44c2142-2d1c-4b5b-a612-e7f1234abcd5",
  "user_id": "u987c214-2d1c-4b5b-a612-e7f1234abcd5",
  "created_at": "2026-08-11T12:00:00Z",
  "updated_at": "2026-08-11T12:00:00Z"
}
```

### B. Get All Employees
Mengambil daftar seluruh pegawai.

- **Method**: `GET`
- **URL**: `/api/employees/`
- **Success Response** (`200 OK`):
```json
[
  {
    "id": "e44c2142-2d1c-4b5b-a612-e7f1234abcd5",
    "first_name": "John",
    "email": "johndoe@example.com",
    "niy": "12345678",
    "user_id": "u987c214-...",
    "...": "..."
  }
]
```

---

## 2. Domain: Subject (Mata Pelajaran)

Base URL: `/api/subjects`

### A. Create Category Subject
Membuat kategori mata pelajaran baru (contoh: IPA, IPS, Bahasa).

- **Method**: `POST`
- **URL**: `/api/subjects/categories`
- **Request Body**:
```json
{
  "name": "IPA"
}
```
- **Success Response** (`200 OK`):
```json
{
  "id": "c11c2142-...",
  "name": "IPA",
  "created_at": "2026-08-11T12:00:00Z",
  "updated_at": "2026-08-11T12:00:00Z",
  "deleted_at": null
}
```

### B. Create School Subject
Membuat mata pelajaran yang terhubung ke sebuah kategori.

- **Method**: `POST`
- **URL**: `/api/subjects/`
- **Request Body**:
```json
{
  "name": "Biologi",
  "category_subject_id": "c11c2142-..."
}
```
- **Success Response** (`200 OK`):
```json
{
  "id": "s22c2142-...",
  "name": "Biologi",
  "category_subject_id": "c11c2142-...",
  "created_at": "2026-08-11T12:00:00Z",
  "updated_at": "2026-08-11T12:00:00Z",
  "deleted_at": null
}
```

---

## 3. Domain: Student

Base URL: `/api/students` (berdasarkan `student_controller.py`)

### A. Create Student
- **Method**: `POST`
- **URL**: `/api/students/`
- **Request Body**:
*(Formatnya mirip dengan Employee, di mana ada `user_data` untuk akun login dan `profile_data` (nis, nisn, first_name, last_name, dsb) untuk biodata murid).*

```json
{
  "user": {
    "username": "siswa01",
    "password": "password123"
  },
  "profile": {
    "nis": "1001",
    "nisn": "0012345678",
    "first_name": "Budi",
    "last_name": "Santoso",
    "gender": "L",
    "birth_place": "Bandung",
    "birth_date": "2010-05-14"
  }
}
```
- **Success Response** (`200 OK`):
```json
{
  "id": "st33c2142-...",
  "user_id": "u555c214-...",
  "nis": "1001",
  "nisn": "0012345678",
  "first_name": "Budi",
  "last_name": "Santoso",
  "gender": "L",
  "created_at": "2026-08-11T12:00:00Z",
  "updated_at": "2026-08-11T12:00:00Z"
}
```

---

## Catatan
- Semua request update (mengubah data) menggunakan method **PATCH** (atau PUT) dengan menyertakan ID pada URL (`/api/domain/{id}`). Response kembaliannya akan sama dengan data ketika di-*create*.
- Method **DELETE** pada URL `/api/domain/{id}` akan menghapus data tersebut (beserta user login-nya apabila ada mekanisme *cascade*).
- Anda juga dapat melihat dokumentasi API interaktif (Swagger UI) yang digenerate otomatis oleh FastAPI dengan menjalankan server lalu membuka URL: `http://localhost:8000/docs`.

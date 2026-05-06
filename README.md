# Login Stealer — Flask CRUD Project

Aplikasi web CRUD berbasis Flask + Python dengan konsep OOP. Dibuat sebagai proyek pembelajaran yang mencakup frontend, backend, dan database dalam satu codebase yang bersih.

❗❗ **DO NOT USE THIS FOR CRIMINAL ACTIVITY, AUTHOR IS NOT RESPONSIBLE FOR YOUR MISBEHAVIOR**❗❗

---

## ✨ Fitur Utama

- Halaman utama dengan **6 image box** yang bisa diklik
- Semua box mengarah ke **satu form terpusat** (`/form`) dengan `box_id` tersimpan via hidden field
- Form menerima **email & password** lalu menyimpannya ke database
- Validasi form **custom JS** (tanpa validasi bawaan browser)
- Halaman konfirmasi setelah submit
- **Panel admin tersembunyi** dengan kredensial hardcoded
- Admin dapat **melihat, mengedit, dan menghapus** semua data yang masuk
- Password disimpan **plaintext** agar admin bisa membaca dan mengubahnya langsung
- **REST API endpoint** untuk integrasi dengan Postman / Insomnia

---

## 🗂️ Struktur Folder

```
project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── admin.py
│   │   └── api.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── form.html
│   │   ├── check_email.html
│   │   ├── admin_login.html
│   │   ├── admin_dashboard.html
│   │   └── admin_edit.html
│   └── static/
│       └── style.css
├── .env
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

---

## ⚙️ Instalasi

### 1. Clone repo

```bash
git clone https://github.com/username/login-stealer.git
cd login-stealer
```

### 2. Buat virtual environment (Optional)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Buat file `.env`

Salin dari `.env.example`:

```bash
cp .env.example .env
```

Lalu isi nilainya:

```env
SECRET_KEY=isi-dengan-string-random-panjang
ADMIN_USERNAME=admin
ADMIN_PASSWORD=passwordkamu
```

### 5. Jalankan aplikasi

```bash
python run.py
```

Buka di browser: `http://localhost:5000`

---

## 🧭 Halaman & Route

| Route | Keterangan |
|---|---|
| `/` | Halaman utama — 6 image box |
| `/form?box_id=<n>` | Form login (semua box mengarah ke sini) |
| `/check-email` | Halaman konfirmasi setelah submit |
| `/rahasia-admin/login` | Login panel admin |
| `/rahasia-admin/dashboard` | Dashboard — lihat semua data |
| `/rahasia-admin/edit/<id>` | Edit email & password user |
| `/rahasia-admin/delete/<id>` | Hapus data user |

---

## 🔌 API Endpoints

Semua endpoint berada di prefix `/api` dan menerima/mengembalikan **JSON**.

### Submit Data User

```
POST /api/submit
Content-Type: application/json

{
  "email": "test@email.com",
  "password": "abc123",
  "box_id": 2
}
```

### Login Admin

```
POST /api/admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "passwordkamu"
}
```

### Lihat Semua Data *(perlu login admin)*

```
GET /api/admin/users
```

### Edit Data *(perlu login admin)*

```
PUT /api/admin/users/<id>
Content-Type: application/json

{
  "email": "baru@email.com",
  "password": "passwordbaru"
}
```

### Hapus Data *(perlu login admin)*

```
DELETE /api/admin/users/<id>
```

> **Catatan:** Endpoint admin bergantung pada session cookie — pastikan API mengaktifkan **"Send Cookies"** dan **"Follow Redirects"**.

---

## 🏗️ Struktur OOP

```python
# UserSubmission — SQLAlchemy model
class UserSubmission(db.Model):
    id, email, password, box_id, created_at

# AdminUser — plain class, tidak disimpan di DB
class AdminUser:
    USERNAME, PASSWORD
    verify(username, password) → bool
```

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
|---|---|
| Backend | Python 3, Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Frontend | HTML, CSS, Vanilla JS |
| Environment | python-dotenv |

---

## 📦 Requirements

```
flask
flask-sqlalchemy
python-dotenv
```

---

## 🚀 Deployment

Project ini kompatibel untuk di-deploy ke **Vercel** dengan sedikit konfigurasi tambahan (`vercel.json`).

---

## ⚠️ Disclaimer

**Project ini dibuat murni untuk **tujuan pembelajaran** mata kuliah Praktikum Pemrograman Komputer. Tidak ditujukan untuk penggunaan produksi atau aktivitas yang melanggar hukum.**

---

## 👤 Author

Daffa Aqilah
Mata Kuliah : Praktikum Pemrograman Komputer

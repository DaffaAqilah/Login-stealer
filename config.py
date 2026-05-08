import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY     = os.environ.get('SECRET_KEY') or 'fallback-dev-key'
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'

    DB_HOST     = os.environ.get('DB_HOST')     or '127.0.0.1'
    DB_USER     = os.environ.get('DB_USER')     or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')   # default kosong
    DB_NAME     = os.environ.get('DB_NAME')     or 'login_stealer'

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
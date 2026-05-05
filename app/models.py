from app import db
from datetime import datetime
import os


class UserSubmission(db.Model):
    __tablename__ = 'submissions'

    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120), nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    box_id     = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, password, box_id):
        self.email    = email
        self.password = password  # disimpan plain
        self.box_id   = box_id

    def __repr__(self):
        return f'<UserSubmission {self.email}>'

    def to_dict(self):
        return {
            'id'        : self.id,
            'email'     : self.email,
            'password'  : self.password,
            'box_id'    : self.box_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }


import os

class AdminUser:
    USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'

    @staticmethod
    def verify(username: str, password: str) -> bool:
        return (
            username == AdminUser.USERNAME and
            password == AdminUser.PASSWORD
        )
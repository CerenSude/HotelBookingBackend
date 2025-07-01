from db import db
from sqlalchemy import LargeBinary

class User(db.Model):
    __tablename__ = 'users' #pg admindeki tablo

    user_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    photo_data = db.Column(db.LargeBinary)
    photo_mime_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
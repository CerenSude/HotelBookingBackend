import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'postgresql://postgres:ceren123@localhost:5432/HotelBooking')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")  # Kullanıcı oturumu vs. için

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

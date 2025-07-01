from db import db

class Amenity(db.Model):
    __tablename__ = 'amenities'

    amenity_id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.hotel_id'))
    name = db.Column(db.String(100), nullable=False)

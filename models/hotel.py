from db import db
from models.amenity import Amenity
from models.comment import Comment

hotel_amenities = db.Table('hotel_amenities',
    db.Column('hotel_id', db.Integer, db.ForeignKey('hotels.hotel_id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Hotel(db.Model):
    __tablename__ = 'hotels'

    hotel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    num_comments = db.Column(db.Integer, default=0)
    special_discount = db.Column(db.Integer, default=0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_flagged = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(120), nullable = True)
    amenities = db.relationship('Amenity', backref='hotel')
    comments = db.relationship('Comment', backref='hotel', lazy=True, cascade="all, delete-orphan")
    total_capacity = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'city': self.city,
            'country': self.country,
            'price': self.price,
            'rating': self.rating,
            'num_comments': self.num_comments,
            'discount': self.special_discount,
            "latitude": self.latitude,
            "longitude": self.longitude,
            'flagged': self.is_flagged,
            "image_url": self.image_url,
            "total_capacity": self.total_capacity,
            "amenities": [a.name for a in self.amenities],
            "comments": [c.to_dict() for c in self.comments]
        }

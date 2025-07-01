from db import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.hotel_id'), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='comments')


    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "user_id": self.user_id,
            "hotel_id": self.hotel_id,
            "service_name": self.service_name,
            "rating": self.rating,
            "comment_text": self.comment_text,
            "created_at": self.created_at.isoformat(),
            'user_name': self.user.name if self.user else None,
            'user_country': self.user.country if self.user else None
        }

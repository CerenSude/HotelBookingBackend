from db import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "hotel_id": self.hotel_id,
            "check_in_date": self.check_in_date.isoformat(),
            "check_out_date": self.check_out_date.isoformat(),
            "guest_count": self.guest_count,
            "total_price": float(self.total_price) if self.total_price else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

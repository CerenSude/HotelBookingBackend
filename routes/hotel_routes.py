from flask import Blueprint, request, jsonify
from models.hotel import Hotel
from datetime import datetime
from models.comment import Comment
from models.booking import Booking
from db import db
hotel_routes = Blueprint('hotels', __name__)

@hotel_routes.route('/hotels/search', methods=['GET'])
def search_hotels():
    try:
        city = request.args.get('city')
        guests = request.args.get('guests', type=int)
        check_in = request.args.get('checkIn')
        check_out = request.args.get('checkOut')

        query = Hotel.query

        if city:
            query = query.filter(Hotel.city.ilike(f"%{city}%"))

        if check_in and check_out and guests:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

            # Step 1: Get overlapping bookings and sum guest_count per hotel
            overlapping_subquery = db.session.query(
                Booking.hotel_id,
                db.func.sum(Booking.guest_count).label("total_guests")
            ).filter(
                Booking.check_in_date < check_out_date,
                Booking.check_out_date > check_in_date
            ).group_by(Booking.hotel_id).subquery()

            # Step 2: Join with hotels and filter those with enough capacity left
            query = query.outerjoin(
                overlapping_subquery,
                Hotel.hotel_id == overlapping_subquery.c.hotel_id
            ).filter(
                (Hotel.total_capacity - db.func.coalesce(overlapping_subquery.c.total_guests, 0)) >= guests
            )

        hotels = query.order_by(Hotel.rating.desc()).all()
        return jsonify([hotel.to_dict() for hotel in hotels])

    except Exception as e:
        print("💥 HATA:", e)
        return jsonify({'error': 'Sunucu hatası oluştu.'}), 500    
@hotel_routes.route('/hotels', methods=['GET'])
def list_all_hotels():
    hotels = Hotel.query.order_by(Hotel.rating.desc()).all()
    return jsonify([hotel.to_dict() for hotel in hotels])

@hotel_routes.route('/hotels/<int:hotel_id>', methods=['GET'])
def get_hotel_details(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(hotel.to_dict())

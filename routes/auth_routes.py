import os
from flask import Blueprint, request, jsonify, current_app, Response
from werkzeug.security import generate_password_hash,  check_password_hash
from werkzeug.utils import secure_filename
from models.user import User
from db import db
from flasgger import swag_from

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.form
    photo = request.files.get('photo')  # if user uploaded a file

    required_fields = ['email', 'password', 'name', 'country', 'city']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Eksik alanlar var.'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Bu e-posta zaten kayıtlı.'}), 409

    hashed_pw = generate_password_hash(data['password'])

    new_user = User(
        email=data['email'],
        password_hash=hashed_pw,
        name=data['name'],
        country=data['country'],
        city=data['city'],
        photo_data=photo.read() if photo else None,
        photo_mime_type=photo.mimetype if photo else None
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Kayıt başarılı 🎉'}), 201

@auth_routes.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Kullanıcı girişi',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'example': 'user@example.com'},
                    'password': {'type': 'string', 'example': '12345678!'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Giriş başarılı',
            'examples': {
                'application/json': {
                    'message': 'Hoş geldin Ayşe!'
                }
            }
        },
        400: {
            'description': 'Eksik email veya şifre',
            'examples': {
                'application/json': {
                    'error': 'Email ve şifre zorunludur'
                }
            }
        },
        401: {
            'description': 'Hatalı giriş',
            'examples': {
                'application/json': {
                    'error': 'Geçersiz email veya şifre'
                }
            }
        }
    }
})
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email ve şifre zorunludur'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Geçersiz email veya şifre'}), 401

    return jsonify({
    'message': f'Hoş geldin {user.name}!',
    'name': user.name,
    'email': user.email,
    'id': user.user_id,
}), 200

@auth_routes.route('/user-photo/<int:user_id>', methods=['GET'])
def get_user_photo(user_id):
    user = User.query.get_or_404(user_id)
    if not user.photo_data:
        return jsonify({'error': 'Fotoğraf yok'}), 404

    return Response(user.photo_data, mimetype=user.photo_mime_type)
    
    
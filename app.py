from flask import Flask
from flask_cors import CORS
from db import db
from config import DevelopmentConfig 
from models.user import User
from routes.auth_routes import auth_routes
from flasgger import Swagger
from routes.hotel_routes import hotel_routes

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(auth_routes)
app.register_blueprint(hotel_routes)

CORS(app, origins=["http://localhost:8080"], supports_credentials=True)
db.init_app(app)

Swagger(app)
@app.route('/ping')
def ping():
    return {"message": "pong"}

if __name__ == '__main__':
    app.run(port=5000)

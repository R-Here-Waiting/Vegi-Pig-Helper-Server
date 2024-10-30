from flask import Flask
from flask_cors import CORS
from app.controllers.pet_controller import pet_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(pet_bp, url_prefix='/api/pet')
    
    return app 
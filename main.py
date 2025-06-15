from flask import Flask
from flask_cors import CORS  
from app.routes import main
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  
    app.register_blueprint(main)
    return app

from flask import Flask
from flask_cors import CORS  
from app.routes import main
from dotenv import load_dotenv

print("Starting main.py...")

load_dotenv()
print("Loaded .env file")

def create_app():
    print("Creating Flask app...")
    app = Flask(_name_)
    CORS(app)  
    app.register_blueprint(main)
    print("Flask app created and blueprint registered")
    return app

if _name_ == "_main_":
    print("Entering main block...")
    app = create_app()
    print("Starting Flask server...")
    app.run(debug=True)
    print("Flask server started (this line should not print until the server stops)")
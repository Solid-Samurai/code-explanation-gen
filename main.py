from flask import Flask
from flask_cors import CORS  
from app.routes import main
from dotenv import load_dotenv

print("Starting main.py...")

load_dotenv()
print("Loaded .env file")

def create_app():
    print("Creating Flask app...")
    app = Flask(__name__)
    CORS(app)  
    app.register_blueprint(main)
    print("Flask app created and blueprint registered")
    return app

if __name__ == "__main__":
    print("Entering main block...")
    app = create_app()
    print("Starting Flask server...")
    app.run(debug=True)
    print("Flask server started (this line should not print until the server stops)")
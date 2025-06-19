
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask import Flask
from flask_cors import CORS  

from app.routes import main

def create_app():

    app = Flask(__name__, static_folder="static")
    CORS(app)
    app = Flask(__name__)
    CORS(app)  

    app.register_blueprint(main)

    @app.route("/")  # Serve the static index.html
    def serve_index():
        return send_from_directory("static", "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

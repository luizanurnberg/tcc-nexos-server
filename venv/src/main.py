import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from route.auth.route import auth_route
from route.next_release.route import release_route

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        methods=["GET", "POST", "OPTIONS"],
        allow_headers="*",
    )

    mongo_uri = os.getenv("MONGO_URI")
    app.config["MONGO_URI"] = mongo_uri

    mongo = PyMongo(app)

    app.register_blueprint(auth_route)
    app.register_blueprint(release_route)

    return app, mongo

app, mongo = create_app()

def run_http_server():
    app.run(host="0.0.0.0", port=3000)

if __name__ == "__main__":
    run_http_server()

#!/usr/bin/python3
"""Main module to start the Flask application"""

from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
swagger = Swagger(app)


@app.teardown_appcontext
def teardown_db(exception):
    """Teardown method to close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors with a JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=api_host, port=api_port, threaded=True)

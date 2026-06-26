from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password")
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "flask_db")

MONGODB_URI = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}"
    f"@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    "?authSource=admin"
)

client = MongoClient(MONGODB_URI)

db = client[MONGO_DB]
collection = db.data


@app.route("/")
def home():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


@app.route("/data", methods=["GET", "POST"])
def data():

    if request.method == "POST":
        body = request.get_json()
        collection.insert_one(body)
        return jsonify({"status": "Data inserted"}), 201

    docs = list(collection.find({}, {"_id": 0}))
    return jsonify(docs), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
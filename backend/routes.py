from flask import Blueprint, request, jsonify, send_file
from database import collection
from bson.objectid import ObjectId
from bson.binary import Binary
from datetime import datetime
import io

routes = Blueprint('routes', __name__)

# Create bottle
@routes.route("/create-bottle", methods=["POST"])
def create_bottle():
    name = request.form.get("name")
    location = request.form.get("location")
    file = request.files.get("file")

    if not name or not location or not file:
        return jsonify({"error": "name, location y file son requeridos"}), 400
    
    image_binary = Binary(file.read())
    
    doc = {
        "name": name,
        "location": location,
        "image": image_binary,
        "created_at": datetime.utcnow()
    }

    result = collection.insert_one(doc)
    return jsonify({"id": str(result.inserted_id), "name": name, "location": location})

# Get all bottles
@routes.route("/get-bottles", methods=["GET"])
def list_bottles():
    bottles = []
    for doc in collection.find():
        bottles.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "location": doc["location"]
        })
    return jsonify(bottles)

# Get only the imagen by id
@routes.route("/get-bottle-image/<id>", methods=["GET"])
def get_bottle_image(id):
    try:
        doc = collection.find_one({"_id": ObjectId(id)})
        if not doc:
            return jsonify({"error": "No encontrado"}), 404

        image_bytes = io.BytesIO(doc["image"])
        return send_file(image_bytes, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
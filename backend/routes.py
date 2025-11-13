from flask import Blueprint, request, jsonify, send_file
from database import collection
from bson.objectid import ObjectId
from bson.binary import Binary
from datetime import datetime
import subprocess
import os

routes = Blueprint('routes', __name__)

def runMattyConsole():
    exe_path = os.path.join(os.path.dirname(__file__), "bin", "src.exe")
    try:
        result = subprocess.run([exe_path], capture_output=True, text=True)
        return result.stdout.splitlines()[-1]
    except Exception as e:
        print(f"Error occurred: {e}")

# ENDPOINTS--------------------------------------------------------------------------

# Create bottle
@routes.route("/create-bottle/<location>", methods=["POST"])
def create_bottle(location):
    currentOwner = runMattyConsole()
    location = request.form.get("location")
    name = currentOwner
    #file = request.files.get("file")

    if not name or not location:
        return jsonify({"error": "name and location are required"}), 400
    
    #image_binary = Binary(file.read())
    
    doc = {
        "name": currentOwner,
        "location": location,
        "created_at": datetime.utcnow()
        #"image": image_binary,
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
            "location": doc["location"],
            "createdAt": doc["created_at"],
        })
    return jsonify(bottles)

# Get only the imagen by id
# @routes.route("/get-bottle-image/<id>", methods=["GET"])
# def get_bottle_image(id):
#     try:
#         doc = collection.find_one({"_id": ObjectId(id)})
#         if not doc:
#             return jsonify({"error": "Not found"}), 404
        
#         image_bytes = io.BytesIO(doc["image"])
#         return send_file(image_bytes, mimetype="image/png")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://angelfloorganise_db_user:admin@hackathon.3otqj5r.mongodb.net/?appName=Hackathon"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["mi_base"]
collection = db["bottles"]
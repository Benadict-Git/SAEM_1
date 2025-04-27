# app/database.py
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://benadictinfantofficial:DB7YLc1ajqWr4GeI@arun-tharkuri.vjzhzfs.mongodb.net/")
db = client.saem  # Use the 'saem' database
collection = db.get_collection("weather")
#collection.insert_one({"city": "Mumbai", "temperature": 25})
print("connected")

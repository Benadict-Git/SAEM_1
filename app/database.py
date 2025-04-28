# app/database.py
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://benadictinfantofficial:DB7YLc1ajqWr4GeI@arun-tharkuri.vjzhzfs.mongodb.net/")
db = client.saem

user_collection = db.users


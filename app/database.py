from dotenv import load_dotenv
import os
import motor.motor_asyncio

load_dotenv()  # Load from .env

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")  # Make sure to set DB_NAME in your .env file

if not MONGO_URL:
    raise ValueError("❌ MONGO_URL not loaded from .env")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["DB_NAME"]
user_collection = db["users"]

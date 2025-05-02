# test_db.py
import asyncio
from app.database import user_collection

async def check():
    print("Checking connection...")
    test_user = await user_collection.find_one()
    print("✅ MongoDB Connected:", test_user)

asyncio.run(check())

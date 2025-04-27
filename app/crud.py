# app/crud.py
from app.database import db
from app.models import SoilHealth, Weather, IrrigationSystem
from typing import List

def create_soil_health(data: SoilHealth):
    collection = db.soil_health
    result = collection.insert_one(data.dict())
    return str(result.inserted_id)

def get_soil_health() -> List[SoilHealth]:
    collection = db.soil_health
    data = collection.find()
    return [SoilHealth(**item) for item in data]

def create_weather(data: Weather):
    collection = db.weather
    result = collection.insert_one(data.dict())
    return str(result.inserted_id)

def get_weather() -> List[Weather]:
    collection = db.weather
    data = collection.find()
    return [Weather(**item) for item in data]

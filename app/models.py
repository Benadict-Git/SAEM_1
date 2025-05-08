# app/models.py
from pydantic import BaseModel
from typing import Dict

class SoilHealth(BaseModel):
    soil_type: str
    ph_level: float
    moisture_level: float
    nutrients: Dict[str, float]  # Assuming nutrients are key-value pairs
    date: str

class Weather(BaseModel):
    temperature: float
    humidity: float
    date: str
    city: str

class IrrigationSystem(BaseModel):
    status: str  # e.g., "on" or "off"
    last_activated: str
    next_scheduled: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

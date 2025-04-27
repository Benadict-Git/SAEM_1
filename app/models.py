# app/models.py
from pydantic import BaseModel

class SoilHealth(BaseModel):
    soil_type: str
    ph_level: float
    moisture_level: float
    nutrients: dict
    date: str

class Weather(BaseModel):
    temperature: float
    humidity: float
    date: str

class IrrigationSystem(BaseModel):
    status: str  # e.g., "on" or "off"
    last_activated: str
    next_scheduled: str

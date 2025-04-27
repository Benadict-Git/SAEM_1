# app/api/weather.py
from fastapi import APIRouter
from app.models import Weather
from app import crud

router = APIRouter()

@router.post("/weather/")
async def add_weather(data: Weather):
    return {"id": crud.create_weather(data)}

@router.get("/weather/")
async def get_weather():
    return crud.get_weather()

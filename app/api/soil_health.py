# app/api/soil_health.py
from fastapi import APIRouter
from app.models import SoilHealth
from app import crud

router = APIRouter()

@router.post("/soil_health/")
async def add_soil_health(data: SoilHealth):
    return {"id": crud.create_soil_health(data)}

@router.get("/soil_health/")
async def get_soil_health():
    return crud.get_soil_health()

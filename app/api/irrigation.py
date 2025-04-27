# app/api/irrigation.py
from fastapi import APIRouter
from app.models import IrrigationSystem
from app import crud

router = APIRouter()

@router.post("/irrigation/")
async def add_irrigation(data: IrrigationSystem):
    return {"id": crud.create_irrigation(data)}

@router.get("/irrigation/")
async def get_irrigation():
    return crud.get_irrigation()

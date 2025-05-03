from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from app.models import Weather
from app import crud
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/weather", response_class=HTMLResponse)
async def get_weather(request: Request):
    return templates.TemplateResponse("weather.html", {"request": request, "weather": None})

@router.post("/weather", response_class=HTMLResponse)
async def post_weather(request: Request, city: str = Form(...)):
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = await client.get(url)
            data = response.json()

        if response.status_code == 200:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "desc": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"]
            }
        else:
            weather = {"city": city, "temp": "--", "desc": "City not found", "humidity": "--"}

    except Exception as e:
        print("❌ Weather fetch failed:", e)
        weather = {"city": city, "temp": "--", "desc": "Error fetching data", "humidity": "--"}

    return templates.TemplateResponse("weather.html", {"request": request, "weather": weather})
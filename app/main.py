from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer

# Import routers
from app.api import weather, irrigation, soil_health, user, home

app = FastAPI()

# Mount static assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates directory setup
templates = Jinja2Templates(directory="app/templates")

# OAuth2 token flow (if needed in future)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Include all modular routers
app.include_router(weather.router)
app.include_router(irrigation.router)
app.include_router(soil_health.router)
app.include_router(user.router)
app.include_router(home.router)

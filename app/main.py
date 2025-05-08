from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from app.api import weather, irrigation, soil_health, user, home
from app import auth1
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.include_router(weather.router)
app.include_router(irrigation.router)
app.include_router(soil_health.router)
app.include_router(user.router)
app.include_router(home.router)

app.include_router(auth1.router)
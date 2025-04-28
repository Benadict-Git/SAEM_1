from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api import weather, irrigation, soil_health
from app.database import user_collection
from app.auth import hash_password, verify_password, create_access_token

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(weather.router)
app.include_router(irrigation.router)
app.include_router(soil_health.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/", response_class=HTMLResponse)
async def dashboard_redirect(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/soil-health", response_class=HTMLResponse)
async def soil_health_page(request: Request):
    return templates.TemplateResponse("soil_health.html", {"request": request})

@app.get("/weather", response_class=HTMLResponse)
async def weather_page(request: Request):
    return templates.TemplateResponse("weather.html", {"request": request})

@app.get("/irrigation", response_class=HTMLResponse)
async def irrigation_page(request: Request):
    return templates.TemplateResponse("irrigation.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
async def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    existing_user = await user_collection.find_one({"username": username})
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "Username already exists"})

    hashed_pw = hash_password(password)
    await user_collection.insert_one({"username": username, "password": hashed_pw})
    return RedirectResponse(url="/login", status_code=302)


@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await user_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid Credentials"})

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="user", value=username)
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    username = request.cookies.get("user")
    if not username:
        return RedirectResponse(url="/register")
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})

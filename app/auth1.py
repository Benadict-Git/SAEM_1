from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from fastapi.exceptions import HTTPException
from app.auth import hash_password, verify_password
from app.database import user_collection
import re

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def is_valid_password(password: str) -> bool:
    return (
        len(password) >= 8 and
        re.search(r"[A-Za-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

@router.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if not is_valid_password(password):
        return templates.TemplateResponse("signup.html", {"request": request, "msg": "Password too weak"})

    existing_user = await user_collection.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "msg": "Username or email already exists"})

    hashed_pw = hash_password(password)
    await user_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_pw
    })
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    user = await user_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie("user", user["username"])
        return response
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("user")
    return response

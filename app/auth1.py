# app/auth1.py
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth import  verify_password
from app.database import user_collection
import re
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Initialize the password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password validation function
def is_valid_password(password: str) -> bool:
    return (
        len(password) >= 8 and
        re.search(r"[A-Za-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

@router.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def post_signup(username: str = Form(...), password: str = Form(...)):
    # Check if the username already exists in the user collection
    if await user_collection.find_one({"username": username}):
        return {"error": "Username already exists"}

    # Hash the password and save the user to the database
    hashed_password = pwd_context.hash(password)
    await user_collection.insert_one({"username": username, "password": hashed_password})
    return {"message": "User created successfully"}

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    # Fetch user based on username (or email if applicable)
    user = await user_collection.find_one({"username": username})
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

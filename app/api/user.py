from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.auth import hash_password, verify_password
from app.database import user_collection
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("singup.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        existing_user = await user_collection.find_one({"username": username})
        if existing_user:
            return templates.TemplateResponse("singup.html", {"request": request, "msg": "Username already exists"})

        hashed_pw = hash_password(password)
        await user_collection.insert_one({"username": username, "password": hashed_pw})
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("singup.html", {"request": request, "msg": "Internal server error"})

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await user_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid Credentials"})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="user", value=username)
    return response

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    username = request.cookies.get("user")
    if not username:
        return RedirectResponse(url="/register")
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})

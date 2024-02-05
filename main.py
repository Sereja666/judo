import uuid
from datetime import datetime
from typing import Any

import uvicorn
from fastapi import FastAPI, Depends, Response, Cookie  # pip install fastapi[all]
from fastapi_users import FastAPIUsers
from sqlalchemy import create_engine
from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from scr.auth.database import User
from scr.auth.manager import get_user_manager
from scr.auth.module_auth import auth_backend
from scr.auth.schemas import UserRead, UserCreate

# from scr.pages.router import router as router_pages


app = FastAPI(title='Judo',
              description=f'подключена БД - {DB_HOST}:{DB_PORT}')

app.mount("/static", StaticFiles(directory="static"), name="static")

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@app.post("/hi", tags=['Мои API'])
async def get_percent():
    """ какая-то анатация """
    return 'Привет!'


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["auth"],
)

# app.include_router(router_pages)


current_user = fastapi_users.current_user()


# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


templates = Jinja2Templates(directory='scr/templates')


@app.get("/")
async def login_form(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})

@app.get("/auth/jwt/login")
async def login_form_jwt(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


# @app.post("/login")
# def login(request: Request, email: str = Form(...), password: str = Form(...), ):
#     redirect_url = f"/user?email={email}&password={password}"
#     return RedirectResponse(redirect_url)


# @app.post("/user")
# def user(email: str = Form(...), password: str = Form(...)):
#     # Здесь можно выполнить дополнительную логику, связанную с пользователем
#     return f"Привет, ваш email: {email}, ваш пароль: {password}"

# COOKIES: dict[str, dict[str, Any]] = {}
# COOKIE_SESSION_ID_KEY = 'web-app-session-id'
#
# def generate_session_id() -> str:
#     return uuid.uuid4().hex
#
# def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),) -> dict:
#     if session_id not in COOKIES:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='не залогинился')
#     return COOKIES[session_id]

@app.post("/protected-route")
def user(request: Request, response: Response, user: User = Depends(current_user), email: str = Form(...), password: str = Form(...)):
    # session_id = generate_session_id()
    # response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    # COOKIES[session_id] = {
    #     'username': auth_username,
    #     'login_at': datetime.now()
    # }

    # return f"Привет, ваш email: {email}, ваш пароль: {password} УРА!"
    return templates.TemplateResponse("main_page.html", context={ 'request':request, "email": email,
                                                         "password": password, 'username': user.username})

#
# @app.get('/check-cookie/')
# def demo_auth_chek_cookie(
#         user_session_data: dict = Depends(get_session_data)
# ):
#     username = user_session_data['username']
#     return {'message' : f'привет {username}', **user_session_data}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

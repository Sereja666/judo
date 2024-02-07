import uuid
from datetime import datetime
from typing import Any

import httpx
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
from scr.auth.jwt_auth import router as jwt_auth_router
# from scr.auth.schemas import UserRead, UserCreate

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
app.include_router(router=jwt_auth_router)

# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )
#
# # app.include_router(router_pages)


current_user = fastapi_users.current_user()


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


templates = Jinja2Templates(directory='scr/templates')


@app.get("/")
async def login_form(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


# @app.post("/send-data")
# async def send_data(email: str, password: str):
#     url = "http://localhost:8000/auth/jwt/login"
#     data = {
#         "email": email,
#         "password": password
#     }
#
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, data=data)
#
#         if response.status_code == 200:
#             # Обработка успешного ответа
#             return response.json()
#         else:
#             # Обработка ошибки
#             raise HTTPException(status_code=response.status_code, detail="Ошибка при отправке запроса")

# @app.get("/auth/jwt/login")
# async def login_form_jwt(request: Request):
#     return templates.TemplateResponse("sign_in.html", {"request": request})


# @app.post("/try-login")
# async def user(request: Request, response: Response, user: User = Depends(current_user), email: str = Form(...),
#          password: str = Form(...)):
#     url = "http://localhost:8000/auth/jwt/login"
#     data = {
#         "email": email,
#         "password": password
#     }
#
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, data=data)
#
#         if response.status_code == 200:
#             return templates.TemplateResponse("main_page.html", context={'request': request, "email": email,
#                                                                          "password": password,
#                                                                          'username': user.username})
#         else:
#             # Обработка ошибки
#             raise HTTPException(status_code=response.status_code, detail="Ошибка при отправке запроса")



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

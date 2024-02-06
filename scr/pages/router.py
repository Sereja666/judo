from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)


templates  = Jinja2Templates(directory='scr/templates')

@router.get("/jwt/login")
async def login_form(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


#
# @router.post("/login")
# def login(request: Request, email: str = Form(...), password: str = Form(...), ):
#     redirect_url = f"/user?email={email}&password={password}"
#     return RedirectResponse(redirect_url)



#
# @router.post("/pages/login")
# def login(request: Request, email: str = Form(...), password: str = Form(...),):
#     # Здесь можно выполнить логику проверки email и password
#     # и выполнить перенаправление на другую страницу
#     # В данном примере мы просто передаем значения в качестве параметров в URL
#     redirect_url = f"/pages/user?email={email}&password={password}"
#     return RedirectResponse(redirect_url)
#
# @router.get("/pages/user")
# def user(email: str, password: str):
#     # Здесь можно выполнить дополнительную логику, связанную с пользователем
#     return f"Привет, ваш email: {email}, ваш пароль: {password}"

#
#
# @router.post("/submitform")
# async def index(email: str = Form(...), password: str = Form(...)):
#     print('email:', email)
#     print('password:', password)
#     return RedirectResponse("/", status_code=303)


# @router.post("/")
# async def login(email: str = Form(...), password: str = Form(...)):
#     # Проверка email и password
#     print('email:', email)
#     print('password:', password)
#     if email == "a@a.ru" and password == "aaa":
#         # Выполнение перенаправления на другую страницу
#         return RedirectResponse('https://krasnodar.hh.ru')
#     else:
#         # Если email или password неверны, генерируем исключение
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")
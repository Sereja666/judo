import uvicorn
from fastapi import FastAPI #pip install fastapi[all]
from fastapi_users import  FastAPIUsers
from sqlalchemy import create_engine


from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from scr.auth.database import User
from scr.auth.manager import get_user_manager
from scr.auth.module_auth import auth_backend
from scr.auth.schemas import UserRead, UserCreate

app = FastAPI(title='Judo',
              description=f'подключена БД - {DB_HOST}:{DB_PORT}')


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










if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

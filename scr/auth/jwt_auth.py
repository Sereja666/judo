# from main import templates
from scr.auth import utils as auth_utils
from scr.auth.schemas import UserSchema
from pydantic import BaseModel
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status, Request, Response
)
from fastapi.security import (
    # HTTPBearer,
    # HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse


templates = Jinja2Templates(directory='scr/templates')

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-auth/jwt/login/",
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)
sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


def get_current_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        token: str = Depends(oauth2_scheme),
) -> dict:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload


def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.get("/login/", response_model=TokenInfo)
def auth_start(request: Request):

    return  templates.TemplateResponse("sign_in.html", {"request": request})


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        # subject
        "sub": user.username,
        "username": user.username,
        "email": user.email,
        # "logged_in_at"
    }
    token = auth_utils.encode_jwt(jwt_payload)
    TokenInfo(
        access_token=token,
        token_type="Bearer",
    ),
    # return TokenInfo(
    #     access_token=token,
    #     token_type="Bearer",
    # ), RedirectResponse("/users/me/")
    return  RedirectResponse("/jwt/mainpage/", status_code=302)


@router.get("/users/me/")
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }

@router.get("/mainpage/")
async def main_page(request: Request):

    # return HTMLResponse('main_page.html')
    return templates.TemplateResponse('main_page.html', {"request": request})
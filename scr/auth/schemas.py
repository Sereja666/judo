# import uuid
# from pathlib import Path
# from typing import Optional
#
# from fastapi_users import schemas
# from fastapi_users.schemas import PYDANTIC_V2
#
#
#
#
#
# class UserRead(schemas.BaseUser[int]):
#     id: int
#     email: str
#     username: str
#     role_id: int
#     is_active: bool = True
#     is_superuser: bool = False
#     is_verified: bool = False
#
#
#     class Config:
#         orm_mode = True
#
#
# class UserCreate(schemas.BaseUserCreate):
#     username: str
#     email: str
#     password: str
#     role_id: int
#     is_active: Optional[bool] = True
#     is_superuser: Optional[bool] = False
#     is_verified: Optional[bool] = False
#
#
# class UserUpdate(schemas.BaseUserUpdate):
#     pass

from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    # username: str = Field(..., min_length=3, max_length=20)
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
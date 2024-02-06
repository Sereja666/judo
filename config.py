from pathlib import Path

from dotenv import load_dotenv
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
SECRET = os.environ.get("SECRET")


class AuthJWT(BaseModel):
    print(BASE_DIR)

    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    print(private_key_path)
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    print(public_key_path)
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()

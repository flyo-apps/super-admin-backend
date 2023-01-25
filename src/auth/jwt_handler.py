from datetime import datetime, timedelta
from typing import List, Optional

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password, username):
    new_password = f'''{password}{username}'''
    return pwd_context.hash(new_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get("JWT_SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt

async def decode_access_token(
    token: str
) -> any:
    try:
        token = token[7:]
        encoded_jwt = jwt.decode(token, options={"verify_signature": False})
        return encoded_jwt
    except Exception as e:
        print(e)
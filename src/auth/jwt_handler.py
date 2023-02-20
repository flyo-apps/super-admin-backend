from typing import List, Optional

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

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

async def decode_access_token(
    token: str
) -> any:
    try:
        token = token[7:]
        encoded_jwt = jwt.decode(token, options={"verify_signature": False})
        return encoded_jwt
    except Exception as e:
        print(e)
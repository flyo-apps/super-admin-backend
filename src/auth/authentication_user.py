import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from users.crud.users import MongoDBUserDatabase
from users.models.users import UserInModel
from jwt import PyJWTError
from pydantic import ValidationError

from .jwt_handler import TokenData, pwd_context
import os

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


def verify_password(plain_password, hashed_password):
    data = pwd_context.verify(plain_password, hashed_password)
    return data

async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    user_db = MongoDBUserDatabase(UserInModel)
    user = await user_db.find_by_username(token_data.username)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: UserInModel = Depends(get_current_user),
):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif current_user.is_deleted:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

async def get_scope_list(
    user: UserInModel
):
    if user.is_admin:
        scopes = [
            "admin:read",
            "admin:write",
            "support:read",
            "support:write",
            "customer:read",
            "customer:write",
            "guest:read",
            "guest:write"
        ]
    elif user.is_support:
        scopes = [
            "support:read",
            "support:write",
            "customer:read",
            "customer:write",
            "guest:read",
            "guest:write"
        ]
    elif user.is_guest:
        scopes = [
            "guest:read",
            "guest:write"
        ]
    else:
        scopes = [
            "customer:read",
            "customer:write",
            "guest:read",
            "guest:write"
        ]

    return scopes


from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Security
from auth.authentication_user import get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from auth import authentication_user
from auth.jwt_handler import Token
from ..utils.constants import USER_ALREADY_EXISTS
from users.models.users import UserModel


router = APIRouter()


@router.post("/v1/login")
async def login_user(
    credentials: OAuth2PasswordRequestForm = Depends(),
    enable_user: Optional[bool] = False
):
    try:
        user, scopes = await authentication_user.authenticate(credentials, enable_user)
        if user == False:
            return {
                "internalResponseCode": 1,
                "details": "Username or Password is wrong"
            }

        if user.is_disabled is True:
            return {
                "internalResponseCode": 2,
                "details": "User is disabled"
            }

        if user.is_deleted is True:
            return {
                "internalResponseCode": 3,
                "details": "User is deleted"
            }
        
        access_token = await authentication_user.get_token(user=user, scopes=scopes)
        return {
            "internalResponseCode": 0,
            "access_token": access_token, 
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong while login ")


@router.post(
    "/v1/refresh_token", 
    response_model=Token,
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def refresh_token(
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["admin:write"],
    ),
):
    try:
        scopes, user = await authentication_user.get_user_and_scope(current_user)

        if user.is_disabled is True:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_ALREADY_EXISTS,
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = await  authentication_user.get_token(user=user, scopes=scopes)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong while fetching refresh token")
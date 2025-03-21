from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from src.users.schemas.auth import AuthSchema, CreateUserSchema
from src.users.schemas.token import Token
from src.users.services import UserService
from src.users.utils.password import create_access_token

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/register", response_model=AuthSchema)
async def create_user(data: Annotated[CreateUserSchema, Form()]):
    await user_service.check_if_user_exists(username=data.username, email=data.email)
    try:
        user = await user_service.create_user(data)
        return user

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
    )

    return Token(access_token=access_token, token_type="bearer")

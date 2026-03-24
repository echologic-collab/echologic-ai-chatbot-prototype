from datetime import timedelta
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.config import config
from src.core.container import Container
from src.core.security import create_access_token, get_current_user
from src.schemas.user_schema import Token, TokenData, User, UserCreate
from src.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

Service = Annotated[UserService, Depends(Provide[Container.user_service])]


@router.post("/register", response_model=User)
@inject
async def register(
    user_create: UserCreate,
    user_service: Service,
):
    try:
        user = await user_service.create_user(user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Service,
):
    user = await user_service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/verify", response_model=TokenData)
async def verify_token(
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    """
    Verify the validity of the access token.
    If valid, returns the token data (user email/id).
    """
    return current_user

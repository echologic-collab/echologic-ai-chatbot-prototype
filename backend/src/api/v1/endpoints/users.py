from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from src.core.container import Container
from src.core.security import get_current_user
from src.schemas.user_schema import TokenData, User, UserListResponse, UserUpdate
from src.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

Service = Annotated[UserService, Depends(Provide[Container.user_service])]


@inject
async def get_current_active_user(
    token_data: Annotated[TokenData, Depends(get_current_user)],
    user_service: Service,
) -> User:
    user = await user_service.get_by_email(token_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


@router.get("/me", response_model=User)
@inject
async def read_users_me(
    current_user: CurrentUser,
):
    return current_user


@router.patch("/me", response_model=User)
@inject
async def update_user_me(
    user_update: UserUpdate,
    current_user: CurrentUser,
    user_service: Service,
):
    return await user_service.patch(current_user.id, user_update)


@router.get("/", response_model=UserListResponse)
@inject
async def get_users(
    current_user: CurrentUser,
    user_service: Service,
):
    return await user_service.get_list()

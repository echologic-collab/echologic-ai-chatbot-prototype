from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from src.schemas.base_schema import ModelBaseInfo


class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    founds: list[User]
    search_options: dict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

from datetime import datetime

from src.core.security import get_password_hash, verify_password
from src.models.user_model import UserDb
from src.repository.user_repository import UserRepository
from src.schemas.user_schema import UserCreate
from src.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> UserDb:
        existing_user = await self.user_repository.get_by_email(user_create.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = get_password_hash(user_create.password)
        user = UserDb(
            email=user_create.email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name=user_create.name,
        )
        return await self.user_repository.create(user)

    async def authenticate(self, email: str, password: str) -> UserDb | None:
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_by_email(self, email: str) -> UserDb | None:
        return await self.user_repository.get_by_email(email)

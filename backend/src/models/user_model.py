from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.conversation_model import ConversationDb


class UserDb(BaseModel, table=True):
    __tablename__ = "users"
    name: Optional[str] = Field(default=None, nullable=True)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    hashed_password: str = Field(nullable=False)

    conversations: List["ConversationDb"] = Relationship(back_populates="user")

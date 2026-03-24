from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from src.core.enums import Role
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.conversation_model import ConversationDb


class MessageDb(BaseModel, table=True):
    __tablename__ = "messages"

    role: Role = Field(default=Role.USER, nullable=False)
    content: str = Field(nullable=False)
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversations.id")

    conversation: Optional["ConversationDb"] = Relationship(back_populates="messages")

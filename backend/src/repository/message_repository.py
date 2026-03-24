from typing import Any, Callable

from src.models.message_model import MessageDb
from src.repository.base_repository import BaseRepository


class MessageRepository(BaseRepository):
    """Message repository using MessageDb model with BaseRepository pattern."""

    def __init__(self, session_factory: Callable[..., Any]):
        super().__init__(session_factory, MessageDb)

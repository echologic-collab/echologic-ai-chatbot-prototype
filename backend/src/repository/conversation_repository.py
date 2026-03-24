from typing import Any, Callable

from sqlmodel import select

from src.models.conversation_model import ConversationDb
from src.repository.base_repository import BaseRepository
from src.util.query_builder import dict_to_sqlalchemy_filter_options


class ConversationRepository(BaseRepository):
    """Conversation repository using ConversationDb model with BaseRepository pattern."""

    def __init__(self, session_factory: Callable[..., Any]):
        super().__init__(session_factory, ConversationDb)

    async def get_existing_conversation(
        self, conversation_uuid: str, user_id: int
    ) -> ConversationDb | None:
        async with self.session_factory() as session:
            filter_options = dict_to_sqlalchemy_filter_options(
                self.model, {"uuid": conversation_uuid, "user_id": user_id}
            )
            query = select(self.model).where(filter_options)
            result = await session.execute(query)
            return result.scalars().first()

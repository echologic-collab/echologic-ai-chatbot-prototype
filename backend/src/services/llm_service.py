import logging
import os

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.postgres import PostgresSaver

from src.core.config import Config
from src.core.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, config: Config):
        self.config = config
        self.model = init_chat_model(config.MODEL_NAME)
        os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY

    def generate_response(self, message: str, thread_id: str) -> str:
        with PostgresSaver.from_conn_string(
            conn_string=self.config.SQLALCHEMY_DATABASE_URI.replace(
                "postgresql+asyncpg://", "postgresql://"
            )
        ) as checkpointer:
            checkpointer.setup()

            agent = create_agent(
                model=self.model,
                tools=[],
                checkpointer=checkpointer,
                debug=True if self.config.DEBUG else False,
                middleware=[
                    SummarizationMiddleware(
                        model=self.model,
                        trigger=("tokens", 2000),
                        keep=("messages", 10),
                    ),
                ],
            )

            response = agent.invoke(
                {"messages": [{"role": "user", "content": message}]},
                {"configurable": {"thread_id": thread_id}},
            )
            return response["messages"][-1].content

    def reset_thread(self, thread_id: str) -> None:
        try:
            with PostgresSaver.from_conn_string(
                conn_string=self.config.SQLALCHEMY_DATABASE_URI.replace(
                    "postgresql+asyncpg://", "postgresql://"
                )
            ) as checkpointer:
                checkpointer.delete_thread(thread_id)
        except Exception:
            logger.error(f"Failed to reset thread: {thread_id}")
            raise NotFoundError(detail=f"Thread {thread_id} not found")

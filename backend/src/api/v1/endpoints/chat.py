from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from src.core.container import Container
from src.core.enums import ConversationStatus, Role
from src.core.exceptions import NotFoundError, ValidationError
from src.core.security import get_current_user
from src.models.conversation_model import ConversationDb
from src.models.message_model import MessageDb
from src.repository.conversation_repository import ConversationRepository
from src.repository.message_repository import MessageRepository
from src.schemas.chat_schema import ChatRequest, ChatResponse
from src.schemas.user_schema import TokenData
from src.services.llm_service import LLMService
from src.services.user_service import UserService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
@inject
async def chat(
    chat_request: ChatRequest,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm_service])],
    conversation_repository: Annotated[
        ConversationRepository, Depends(Provide[Container.conversation_repository])
    ],
    message_repository: Annotated[
        MessageRepository, Depends(Provide[Container.message_repository])
    ],
):
    """
    Chat endpoint with authentication.
    Returns an echo of the user's message with their name.

    Raises:
        ValidationError: If message is empty or invalid
        NotFoundError: If authenticated user not found in database
    """
    # Validate message
    if not chat_request.message or not chat_request.message.strip():
        raise ValidationError(detail="Message cannot be empty")

    # Get user details from database
    user = await user_service.get_by_email(current_user.email)

    if not user:
        raise NotFoundError(detail=f"User {current_user.email} not found")

    conversation_uuid = chat_request.conversation_id
    conversation = None

    if conversation_uuid and conversation_uuid != "default":
        conversation = await conversation_repository.get_existing_conversation(
            conversation_uuid=conversation_uuid, user_id=user.id
        )

    if not conversation:
        conversation = await conversation_repository.create(
            schema=ConversationDb(
                user_id=user.id,
                title=chat_request.message[:12] + "...",  # Simple title generation
                status=ConversationStatus.ACTIVE,
            )
        )

    await message_repository.create(
        schema=MessageDb(
            conversation_id=conversation.id,
            content=chat_request.message,
            role=Role.USER,
        )
    )

    thread_id = conversation.uuid
    response_text = await run_in_threadpool(
        llm_service.generate_response, chat_request.message, thread_id
    )

    await message_repository.create(
        schema=MessageDb(
            conversation_id=conversation.id,
            content=response_text,
            role=Role.ASSISTANT,
        )
    )

    user_name = user.name if user.name else "User"

    return ChatResponse(
        user_email=current_user.email,
        user_name=user_name,
        message=chat_request.message,
        response=response_text,
        conversation_id=conversation.uuid,
    )


@router.post("/reset", response_model=ChatResponse)
@inject
async def reset_thread(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm_service])],
    conversation_repository: Annotated[
        ConversationRepository, Depends(Provide[Container.conversation_repository])
    ],
    conversation_id: str = "default",
):
    """
    Reset conversation thread for the user.
    """
    user = await user_service.get_by_email(current_user.email)

    if not user:
        raise NotFoundError(detail=f"User {current_user.email} not found")

    llm_service.reset_thread(conversation_id)

    await conversation_repository.update(
        conversation_id=conversation_id,
        status=ConversationStatus.INACTIVE,
    )

    return ChatResponse(
        user_email=current_user.email,
        user_name=user.name or "User",
        message="System",
        response="Conversation memory reset.",
        conversation_id=conversation_id,
    )

from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.chat_repository import ChatRepository


class ChatService:
    """
    Orchestrates the flow between the API, the Database, and Gemini AI.
    This service fulfills the 'Day 2' integration requirements.
    """

    @staticmethod
    async def handle_user_request(session: AsyncSession, conversation_id: int, user_text: str):
        # 1. Save user message (Sub-task: Save to DB)
        await ChatRepository.save_message(
            session=session, 
            conversation_id=conversation_id, 
            content=user_text, 
            is_bot=False
        )

        # 2. Get history for context (Sub-task: Fetch last N messages)
        history = await ChatRepository.get_chat_history(session, conversation_id, limit=5)
        
        # 3. Format history for the AI (Sub-task: Attach messages to conversation)
        # For now, we'll create a simple list of messages
        chat_context = [{"role": "user" if not m.is_bot else "model", "content": m.content} for m in history]

        # 4. Call Gemini (Sub-task: Call Gemini)
        # bot_response = await gemini_client.generate(chat_context)
        bot_response = "I am Echo Logic, your security-focused assistant." # Placeholder

        # 5. Save bot response (Sub-task: Save bot response)
        await ChatRepository.save_message(
            session=session, 
            conversation_id=conversation_id, 
            content=bot_response, 
            is_bot=True
        )

        return bot_response
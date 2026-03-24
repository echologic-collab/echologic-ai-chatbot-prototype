from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    user_email: str
    user_name: Optional[str] = None
    message: str
    response: str
    conversation_id: str

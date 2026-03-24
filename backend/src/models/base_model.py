import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(
        default_factory=lambda: str(uuid.uuid4()), unique=True, index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


class BaseUUIDModel(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

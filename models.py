# backend/models.py
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Elder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    elder_id: int = Field(foreign_key="elder.id")
    type: str
    payload: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

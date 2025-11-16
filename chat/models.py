"""Pydantic models for chat functionality."""
from pydantic import BaseModel
from datetime import datetime
from typing import List


class ChatMessage(BaseModel):
    id: str
    username: str
    role: str  # "user" or "bot"
    content: str
    timestamp: datetime


class ChatMessageCreate(BaseModel):
    content: str


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessage]
    total: int

"""Utility functions for chat functionality."""
from datetime import datetime
from typing import List
import uuid
from .models import ChatMessage
from .database import chat_history_db


def generate_bot_response(user_message: str) -> str:
    """
    Simple bot response generator.
    In production, replace with actual chatbot logic (LLM, rule-based, etc.)
    """
    # Simple echo bot for demonstration
    responses = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hi there! What can I do for you?",
        "how are you": "I'm doing great! Thanks for asking. How can I assist you?",
        "help": "I'm here to help! You can ask me questions or just chat with me.",
        "bye": "Goodbye! Have a great day!",
    }

    user_message_lower = user_message.lower().strip()

    # Check for exact matches
    if user_message_lower in responses:
        return responses[user_message_lower]

    # Default response
    return f"You said: '{user_message}'. I'm a simple bot, but I heard you!"


def save_chat_message(username: str, role: str, content: str) -> ChatMessage:
    """Save a chat message to the in-memory database."""
    message = ChatMessage(
        id=str(uuid.uuid4()),
        username=username,
        role=role,
        content=content,
        timestamp=datetime.utcnow()
    )

    if username not in chat_history_db:
        chat_history_db[username] = []

    chat_history_db[username].append(message)
    return message


def get_user_chat_history(username: str) -> List[ChatMessage]:
    """Retrieve all chat messages for a user."""
    return chat_history_db.get(username, [])

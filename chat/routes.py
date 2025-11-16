"""Chat routes."""
from fastapi import APIRouter, Depends
from typing import Optional
from auth.models import User
from auth.dependencies import get_current_active_user
from .models import ChatMessage, ChatMessageCreate, ChatHistoryResponse
from .utils import generate_bot_response, save_chat_message, get_user_chat_history
from .database import chat_history_db

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatMessage)
async def send_message(
    message: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Send a message to the chatbot and get a response.
    Both the user message and bot response are saved to chat history.
    """
    # Save user message
    user_message = save_chat_message(
        username=current_user.username,
        role="user",
        content=message.content
    )

    # Generate and save bot response
    bot_response_content = generate_bot_response(message.content)
    bot_message = save_chat_message(
        username=current_user.username,
        role="bot",
        content=bot_response_content
    )

    # Return the bot's response
    return bot_message


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    current_user: User = Depends(get_current_active_user),
    limit: Optional[int] = None
):
    """
    Retrieve chat history for the current user.
    Optionally limit the number of messages returned.
    """
    messages = get_user_chat_history(current_user.username)

    # Apply limit if specified
    if limit and limit > 0:
        messages = messages[-limit:]

    return ChatHistoryResponse(
        messages=messages,
        total=len(messages)
    )


@router.delete("/history")
async def clear_chat_history(current_user: User = Depends(get_current_active_user)):
    """
    Clear all chat history for the current user.
    """
    if current_user.username in chat_history_db:
        deleted_count = len(chat_history_db[current_user.username])
        chat_history_db[current_user.username] = []
        return {
            "message": "Chat history cleared successfully",
            "deleted_messages": deleted_count
        }
    return {
        "message": "No chat history found",
        "deleted_messages": 0
    }

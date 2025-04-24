"""Tests for the AI Conversation Client API."""

import pytest
from datetime import datetime
from typing import List, Any

from ai_conversation_client import (
    Message, MessageRole, Conversation, AIClient, AIBackend
)


class DummyAIBackend(AIBackend):
    """A dummy backend for testing."""
    
    async def generate_response(self, messages: List[Message], **kwargs: Any) -> Message:
        """Generate a simple echo response."""
        last_message = messages[-1]
        return Message(
            f"Echo: {last_message.content}",
            MessageRole.ASSISTANT
        )


@pytest.fixture
def backend():
    return DummyAIBackend()


@pytest.fixture
def client(backend):
    return AIClient(backend)


# ...existing TestMessage and TestConversation classes...

class TestAIClient:
    """Tests for the AIClient class."""
    
    def test_create_conversation(self, client):
        """Test that a conversation can be created and stored in the client."""
        title = "Test Conversation"
        
        conversation = client.create_conversation(title)
        
        assert conversation.title == title
        assert client.get_conversation(conversation.id) == conversation
    
    @pytest.mark.asyncio
    async def test_send_message(self, client):
        """Test that messages can be sent and responses received."""
        conversation = client.create_conversation("Test Conversation")
        message_content = "Hello, AI!"
        
        response = await client.send_message(conversation.id, message_content)
        
        assert len(conversation.messages) == 2
        assert conversation.messages[0].content == message_content
        assert conversation.messages[0].role == MessageRole.USER
        assert response.content == f"Echo: {message_content}"
        assert response.role == MessageRole.ASSISTANT
    
    def test_get_nonexistent_conversation(self, client):
        """Test that getting a nonexistent conversation returns None."""
        assert client.get_conversation("nonexistent_id") is None
    
    @pytest.mark.asyncio
    async def test_send_message_nonexistent_conversation(self, client):
        """Test that sending a message to a nonexistent conversation raises an error."""
        with pytest.raises(ValueError):
            await client.send_message("nonexistent_id", "Hello, AI!")
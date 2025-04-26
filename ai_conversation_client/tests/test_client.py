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
        if not messages:
            raise ValueError("Messages list cannot be empty")
        last_message = messages[-1]
        return Message(
            f"Echo: {last_message.content}",
            MessageRole.ASSISTANT
        )


class ErrorAIBackend(AIBackend):
    """A backend that always raises an error."""
    
    async def generate_response(self, messages: List[Message], **kwargs: Any) -> Message:
        """Always raises an error."""
        raise RuntimeError("Backend error")


@pytest.fixture
def backend():
    return DummyAIBackend()


@pytest.fixture
def error_backend():
    return ErrorAIBackend()


@pytest.fixture
def client(backend):
    return AIClient(backend)


# ...existing TestMessage and TestConversation classes...

class TestMessage:
    """Tests for the Message class."""
    
    def test_message_properties(self):
        """Test that all message properties work correctly."""
        content = "Test message"
        role = MessageRole.USER
        message = Message(content, role)
        
        assert message.content == content
        assert message.role == role
        assert message.id is not None
        assert isinstance(message.timestamp, datetime)
    
    def test_custom_message_id(self):
        """Test message creation with custom ID."""
        custom_id = "custom_123"
        message = Message("content", message_id=custom_id)
        assert message.id == custom_id
    
    def test_custom_timestamp(self):
        """Test message creation with custom timestamp."""
        custom_time = datetime(2024, 1, 1)
        message = Message("content", timestamp=custom_time)
        assert message.timestamp == custom_time
    
    def test_message_immutability(self):
        """Test that message properties cannot be modified."""
        message = Message("test")
        with pytest.raises(AttributeError):
            message.content = "new content"
        with pytest.raises(AttributeError):
            message.role = MessageRole.ASSISTANT
        with pytest.raises(AttributeError):
            message.id = "new_id"
        with pytest.raises(AttributeError):
            message.timestamp = datetime.now()
    
    def test_empty_message_content(self):
        """Test that empty message content is not allowed."""
        with pytest.raises(ValueError):
            Message("")
        with pytest.raises(ValueError):
            Message("   ")
    
    def test_invalid_role_type(self):
        """Test that role must be a MessageRole enum."""
        with pytest.raises(TypeError):
            Message("test", role="user")
    
    def test_content_whitespace_handling(self):
        """Test that leading/trailing whitespace is stripped."""
        message = Message("  test  ")
        assert message.content == "test"


class TestConversation:
    """Tests for the Conversation class."""
    
    def test_conversation_properties(self):
        """Test that all conversation properties work correctly."""
        title = "Test Conv"
        conv = Conversation(title=title)
        assert conv.title == title
        assert conv.id is not None
        assert isinstance(conv.messages, list)
    
    def test_system_prompt(self):
        """Test conversation creation with system prompt."""
        system_prompt = "You are a helpful assistant"
        conv = Conversation(system_prompt=system_prompt)
        assert len(conv.messages) == 1
        assert conv.messages[0].role == MessageRole.SYSTEM
        assert conv.messages[0].content == system_prompt
    
    def test_add_multiple_messages(self):
        """Test adding multiple messages maintains order."""
        conv = Conversation()
        messages = [
            Message("msg1", MessageRole.USER),
            Message("msg2", MessageRole.ASSISTANT),
            Message("msg3", MessageRole.USER)
        ]
        for msg in messages:
            conv.add_message(msg)
            
        assert len(conv.messages) == len(messages)
        for orig, stored in zip(messages, conv.messages):
            assert orig.content == stored.content
            assert orig.role == stored.role
    
    def test_conversation_immutability(self):
        """Test that conversation properties cannot be modified."""
        conv = Conversation("conv_123", "Test")
        with pytest.raises(AttributeError):
            conv.id = "new_id"
        with pytest.raises(AttributeError):
            conv.title = "New Title"
        
        # Messages list should be a copy
        messages = conv.messages
        messages.append(Message("test"))
        assert len(conv.messages) == 0
    
    def test_empty_system_prompt(self):
        """Test that empty system prompt is not allowed."""
        with pytest.raises(ValueError):
            Conversation(system_prompt="")
        with pytest.raises(ValueError):
            Conversation(system_prompt="   ")
    
    def test_invalid_message_type(self):
        """Test that only Message instances can be added."""
        conv = Conversation()
        with pytest.raises(TypeError):
            conv.add_message("not a message")
    
    def test_title_whitespace_handling(self):
        """Test that title whitespace is handled correctly."""
        conv = Conversation(title="  Test Title  ")
        assert conv.title == "Test Title"


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
    
    def test_create_multiple_conversations(self, client):
        """Test creating multiple conversations."""
        conv1 = client.create_conversation("Conv 1")
        conv2 = client.create_conversation("Conv 2")
        
        assert conv1.id != conv2.id
        assert client.get_conversation(conv1.id) == conv1
        assert client.get_conversation(conv2.id) == conv2
    
    @pytest.mark.asyncio
    async def test_conversation_history(self, client):
        """Test that conversation history is maintained correctly."""
        conv = client.create_conversation()
        messages = ["Hello", "How are you?", "What's the weather?"]
        
        for msg in messages:
            await client.send_message(conv.id, msg)
            
        # Each message should have a user message and AI response
        assert len(conv.messages) == len(messages) * 2
        
        # Verify alternating user/assistant pattern
        for i in range(0, len(conv.messages), 2):
            assert conv.messages[i].role == MessageRole.USER
            assert conv.messages[i+1].role == MessageRole.ASSISTANT
    
    def test_invalid_backend_type(self):
        """Test that backend must implement AIBackend."""
        with pytest.raises(TypeError):
            AIClient("not a backend")
    
    @pytest.mark.asyncio
    async def test_backend_error_handling(self, error_backend):
        """Test that backend errors are properly handled."""
        client = AIClient(error_backend)
        conv = client.create_conversation()
        
        with pytest.raises(RuntimeError) as exc_info:
            await client.send_message(conv.id, "Hello")
        assert "Backend error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_empty_message_content(self, client):
        """Test that empty messages are not allowed."""
        conv = client.create_conversation()
        with pytest.raises(ValueError):
            await client.send_message(conv.id, "")
        with pytest.raises(ValueError):
            await client.send_message(conv.id, "   ")
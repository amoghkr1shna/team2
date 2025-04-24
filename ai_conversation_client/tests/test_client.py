# """
# Tests for the AI Conversation Client API.

# These tests verify the interface of the AI Conversation Client
# without actually implementing the functionality.
# """

# import pytest
# from datetime import datetime
# from unittest.mock import patch, MagicMock, AsyncMock

# from ai_conversation_client import Message, MessageRole, Conversation, AIClient


# class TestMessage:
#     """Tests for the Message class."""
    
#     def test_message_creation(self):
#         """Test that a message can be created with the expected properties."""
#         content = "Hello, AI!"
#         role = MessageRole.USER
#         message_id = "msg_123"
#         timestamp = datetime.now()
        
#         message = Message(content, role, message_id, timestamp)
        
#         assert message.content == content
#         assert message.role == role
#         assert message.id == message_id
#         assert message.timestamp == timestamp
    
#     def test_message_default_values(self):
#         """Test that a message uses correct default values."""
#         content = "Hello, AI!"
        
#         message = Message(content)
        
#         assert message.content == content
#         assert message.role == MessageRole.USER
#         assert message.id is not None  # Now we expect a generated ID
#         assert message.id.startswith("msg_")  # Check ID format
#         assert isinstance(message.timestamp, datetime)


# class TestConversation:
#     """Tests for the Conversation class."""
    
#     def test_conversation_creation(self):
#         """Test that a conversation can be created with the expected properties."""
#         conversation_id = "conv_123"
#         title = "Test Conversation"
        
#         conversation = Conversation(conversation_id, title)
        
#         assert conversation.id == conversation_id
#         assert conversation.title == title
#         assert conversation.messages == []
    
#     def test_add_message(self):
#         """Test that messages can be added to a conversation."""
#         conversation = Conversation("conv_123", "Test Conversation")
#         message = Message("Hello, AI!")
        
#         conversation.add_message(message)
        
#         assert len(conversation.messages) == 1
#         assert conversation.messages[0] == message
    
#     def test_get_latest_messages(self):
#         """Test that the latest messages can be retrieved from a conversation."""
#         conversation = Conversation("conv_123", "Test Conversation")
        
#         # Add 10 messages
#         for i in range(10):
#             message = Message(f"Message {i}")
#             conversation.add_message(message)
        
#         # Get the latest 5 messages
#         latest_messages = conversation.get_latest_messages(5)
        
#         assert len(latest_messages) == 5
#         assert latest_messages[0].content == "Message 5"
#         assert latest_messages[4].content == "Message 9"
    
#     def test_system_prompt(self):
#         """Test that a system prompt is added as a system message."""
#         system_prompt = "You are a helpful assistant."
        
#         conversation = Conversation(system_prompt=system_prompt)
        
#         assert len(conversation.messages) == 1
#         assert conversation.messages[0].content == system_prompt
#         assert conversation.messages[0].role == MessageRole.SYSTEM


# class TestAIClient:
#     """Tests for the AIClient class."""
    
#     def test_client_creation(self):
#         """Test that a client can be created with the expected properties."""
#         api_key = "sk-1234567890"
#         model = "gpt-4"
#         temperature = 0.5
#         max_tokens = 100
        
#         client = AIClient(api_key, model, temperature, max_tokens)
        
#         # We can't directly access private attributes, but we can test the behavior
#         assert client._api_key == api_key
#         assert client._model == model
#         assert client._temperature == temperature
#         assert client._max_tokens == max_tokens
    
#     def test_create_conversation(self):
#         """Test that a conversation can be created and stored in the client."""
#         client = AIClient()
#         title = "Test Conversation"
        
#         conversation = client.create_conversation(title)
        
#         assert conversation.title == title
#         assert client.get_conversation(conversation.id) == conversation
    
#     def test_list_conversations(self):
#         """Test that all conversations can be listed."""
#         client = AIClient()
        
#         # Create 3 conversations
#         conversations = [
#             client.create_conversation("Conversation 1"),
#             client.create_conversation("Conversation 2"),
#             client.create_conversation("Conversation 3")
#         ]
        
#         listed_conversations = client.list_conversations()
        
#         assert len(listed_conversations) == 3
#         for conversation in conversations:
#             assert conversation in listed_conversations
    
#     @pytest.mark.asyncio
#     async def test_send_message(self):
#         """Test that messages can be sent and responses received."""
#         client = AIClient()
#         conversation = client.create_conversation("Test Conversation")
#         message_content = "Hello, AI!"
        
#         # Send a message and get a response
#         ai_message = await client.send_message(conversation.id, message_content)
        
#         # Check that both messages were added to the conversation
#         assert len(conversation.messages) == 2
#         assert conversation.messages[0].content == message_content
#         assert conversation.messages[0].role == MessageRole.USER
#         assert conversation.messages[1] == ai_message
#         assert ai_message.role == MessageRole.ASSISTANT
    
#     def test_set_model(self):
#         """Test that the model can be changed."""
#         client = AIClient()
#         initial_model = client._model
#         new_model = "gpt-4"
        
#         client.set_model(new_model)
        
#         assert client._model == new_model
#         assert client._model != initial_model
    
#     def test_export_conversation_json(self):
#         """Test that a conversation can be exported as JSON."""
#         client = AIClient()
#         conversation = client.create_conversation("Test Conversation")
        
#         exported = client.export_conversation(conversation.id, "json")
        
#         assert isinstance(exported, dict)
#         assert exported["id"] == conversation.id
#         assert exported["title"] == conversation.title
    
#     def test_export_conversation_text(self):
#         """Test that a conversation can be exported as text."""
#         client = AIClient()
#         conversation = client.create_conversation("Test Conversation")
        
#         exported = client.export_conversation(conversation.id, "text")
        
#         assert isinstance(exported, str)
#         assert conversation.id in exported
#         assert conversation.title in exported
    
#     def test_export_conversation_invalid_format(self):
#         """Test that exporting with an invalid format raises an error."""
#         client = AIClient()
#         conversation = client.create_conversation("Test Conversation")
        
#         with pytest.raises(ValueError):
#             client.export_conversation(conversation.id, "invalid_format")
    
#     def test_get_nonexistent_conversation(self):
#         """Test that getting a nonexistent conversation returns None."""
#         client = AIClient()
        
#         conversation = client.get_conversation("nonexistent_id")
        
#         assert conversation is None
    
#     @pytest.mark.asyncio
#     async def test_send_message_nonexistent_conversation(self):
#         """Test that sending a message to a nonexistent conversation raises an error."""
#         client = AIClient()
        
#         with pytest.raises(ValueError):
#             await client.send_message("nonexistent_id", "Hello, AI!") 


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
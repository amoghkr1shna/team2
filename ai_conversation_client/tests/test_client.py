"""
Tests for the AI Conversation Client API.

These tests verify the implementation of the AI Conversation Client
by mocking external dependencies.
"""

import pytest
import json
import os
from datetime import datetime
from unittest.mock import patch, MagicMock, AsyncMock

from ai_conversation_client import Message, MessageRole, Conversation, AIClient


class TestMessage:
    """Tests for the Message class."""
    
    def test_message_creation(self):
        """Test that a message can be created with the expected properties."""
        content = "Hello, AI!"
        role = MessageRole.USER
        message_id = "msg_123"
        timestamp = datetime.now()
        
        message = Message(content, role, message_id, timestamp)
        
        assert message.content == content
        assert message.role == role
        assert message.id == message_id
        assert message.timestamp == timestamp
    
    def test_message_default_values(self):
        """Test that a message uses correct default values."""
        content = "Hello, AI!"
        
        message = Message(content)
        
        assert message.content == content
        assert message.role == MessageRole.USER
        assert message.id is not None
        assert message.id.startswith("msg_")
        assert isinstance(message.timestamp, datetime)
    
    def test_message_to_dict(self):
        """Test that a message can be converted to a dictionary."""
        content = "Hello, AI!"
        role = MessageRole.USER
        
        message = Message(content, role)
        message_dict = message.to_dict()
        
        assert message_dict["role"] == role.value
        assert message_dict["content"] == content
    
    def test_message_from_dict(self):
        """Test that a message can be created from a dictionary."""
        message_data = {
            "role": "user",
            "content": "Hello, AI!",
            "id": "msg_123",
            "timestamp": datetime.now().isoformat()
        }
        
        message = Message.from_dict(message_data)
        
        assert message.content == message_data["content"]
        assert message.role == MessageRole.USER
        assert message.id == message_data["id"]


class TestConversation:
    """Tests for the Conversation class."""
    
    def test_conversation_creation(self):
        """Test that a conversation can be created with the expected properties."""
        conversation_id = "conv_123"
        title = "Test Conversation"
        
        conversation = Conversation(conversation_id, title)
        
        assert conversation.id == conversation_id
        assert conversation.title == title
        assert conversation.messages == []
    
    def test_add_message(self):
        """Test that messages can be added to a conversation."""
        conversation = Conversation("conv_123", "Test Conversation")
        message = Message("Hello, AI!")
        
        conversation.add_message(message)
        
        assert len(conversation.messages) == 1
        assert conversation.messages[0] == message
    
    def test_get_latest_messages(self):
        """Test that the latest messages can be retrieved from a conversation."""
        conversation = Conversation("conv_123", "Test Conversation")
        
        # Add 10 messages
        for i in range(10):
            message = Message(f"Message {i}")
            conversation.add_message(message)
        
        # Get the latest 5 messages
        latest_messages = conversation.get_latest_messages(5)
        
        assert len(latest_messages) == 5
        assert latest_messages[0].content == "Message 5"
        assert latest_messages[4].content == "Message 9"
    
    def test_system_prompt(self):
        """Test that a system prompt is added as a system message."""
        system_prompt = "You are a helpful assistant."
        
        conversation = Conversation(system_prompt=system_prompt)
        
        assert len(conversation.messages) == 1
        assert conversation.messages[0].content == system_prompt
        assert conversation.messages[0].role == MessageRole.SYSTEM
    
    def test_conversation_to_dict(self):
        """Test that a conversation can be converted to a dictionary."""
        conversation = Conversation("conv_123", "Test Conversation")
        conversation.add_message(Message("Hello!", MessageRole.USER))
        conversation.add_message(Message("Hi there!", MessageRole.ASSISTANT))
        
        conv_dict = conversation.to_dict()
        
        assert conv_dict["id"] == "conv_123"
        assert conv_dict["title"] == "Test Conversation"
        assert len(conv_dict["messages"]) == 2
        assert conv_dict["messages"][0]["content"] == "Hello!"
        assert conv_dict["messages"][1]["content"] == "Hi there!"
    
    def test_conversation_from_dict(self):
        """Test that a conversation can be created from a dictionary."""
        now = datetime.now().isoformat()
        conv_data = {
            "id": "conv_123",
            "title": "Test Conversation",
            "messages": [
                {
                    "id": "msg_1",
                    "content": "Hello!",
                    "role": "user",
                    "timestamp": now
                },
                {
                    "id": "msg_2",
                    "content": "Hi there!",
                    "role": "assistant",
                    "timestamp": now
                }
            ]
        }
        
        conversation = Conversation.from_dict(conv_data)
        
        assert conversation.id == "conv_123"
        assert conversation.title == "Test Conversation"
        assert len(conversation.messages) == 2
        assert conversation.messages[0].content == "Hello!"
        assert conversation.messages[0].role == MessageRole.USER
        assert conversation.messages[1].content == "Hi there!"
        assert conversation.messages[1].role == MessageRole.ASSISTANT


class TestAIClient:
    """Tests for the AIClient class."""
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_client_creation(self, mock_openai):
        """Test that a client can be created with the expected properties."""
        api_key = "sk-1234567890"
        model = "gpt-4"
        temperature = 0.5
        max_tokens = 100
        
        client = AIClient(api_key, model, temperature, max_tokens)
        
        assert client._api_key == api_key
        assert client._model == model
        assert client._temperature == temperature
        assert client._max_tokens == max_tokens
        mock_openai.assert_called_once_with(api_key=api_key)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_create_conversation(self, mock_openai):
        """Test that a conversation can be created and stored in the client."""
        client = AIClient()
        title = "Test Conversation"
        
        conversation = client.create_conversation(title)
        
        assert conversation.title == title
        assert client.get_conversation(conversation.id) == conversation
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_list_conversations(self, mock_openai):
        """Test that all conversations can be listed."""
        client = AIClient()
        
        # Create 3 conversations
        conversations = [
            client.create_conversation("Conversation 1"),
            client.create_conversation("Conversation 2"),
            client.create_conversation("Conversation 3")
        ]
        
        listed_conversations = client.list_conversations()
        
        assert len(listed_conversations) == 3
        for conversation in conversations:
            assert conversation in listed_conversations
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    @pytest.mark.asyncio
    async def test_send_message(self, mock_openai):
        """Test that messages can be sent and responses received."""
        # Create mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is the AI's response."
        
        # Setup the mock OpenAI client
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client
        
        client = AIClient()
        conversation = client.create_conversation("Test Conversation")
        message_content = "Hello, AI!"
        
        # Send a message and get a response
        ai_message = await client.send_message(conversation.id, message_content)
        
        # Check that both messages were added to the conversation
        assert len(conversation.messages) == 2
        assert conversation.messages[0].content == message_content
        assert conversation.messages[0].role == MessageRole.USER
        assert conversation.messages[1] == ai_message
        assert ai_message.role == MessageRole.ASSISTANT
        assert ai_message.content == "This is the AI's response."
        
        # Verify the API was called with the expected parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == client._model
        assert call_args["temperature"] == client._temperature
        assert len(call_args["messages"]) == 1
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == message_content
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_set_model(self, mock_openai):
        """Test that the model can be changed."""
        client = AIClient()
        initial_model = client._model
        new_model = "gpt-4"
        
        client.set_model(new_model)
        
        assert client._model == new_model
        assert client._model != initial_model
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_export_conversation_json(self, mock_openai):
        """Test that a conversation can be exported as JSON."""
        client = AIClient()
        conversation = client.create_conversation("Test Conversation")
        
        exported = client.export_conversation(conversation.id, "json")
        
        assert isinstance(exported, dict)
        assert exported["id"] == conversation.id
        assert exported["title"] == conversation.title
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_export_conversation_text(self, mock_openai):
        """Test that a conversation can be exported as text."""
        client = AIClient()
        conversation = client.create_conversation("Test Conversation")
        
        exported = client.export_conversation(conversation.id, "text")
        
        assert isinstance(exported, str)
        assert conversation.title in exported
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_export_conversation_invalid_format(self, mock_openai):
        """Test that exporting with an invalid format raises an error."""
        client = AIClient()
        conversation = client.create_conversation("Test Conversation")
        
        with pytest.raises(ValueError):
            client.export_conversation(conversation.id, "invalid_format")
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_get_nonexistent_conversation(self, mock_openai):
        """Test that getting a nonexistent conversation returns None."""
        client = AIClient()
        
        conversation = client.get_conversation("nonexistent_id")
        
        assert conversation is None
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    @pytest.mark.asyncio
    async def test_send_message_nonexistent_conversation(self, mock_openai):
        """Test that sending a message to a nonexistent conversation raises an error."""
        client = AIClient()
        
        with pytest.raises(ValueError):
            await client.send_message("nonexistent_id", "Hello, AI!")
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("ai_conversation_client.AsyncOpenAI")
    def test_save_and_load_conversations(self, mock_openai, tmp_path):
        """Test that conversations can be saved to and loaded from a file."""
        client = AIClient()
        
        # Create a conversation with messages
        conversation = client.create_conversation("Test Conversation")
        conversation.add_message(Message("Hello!", MessageRole.USER))
        conversation.add_message(Message("Hi there!", MessageRole.ASSISTANT))
        
        # Save the conversations to a temporary file
        file_path = tmp_path / "test_conversations.json"
        client.save_conversations(str(file_path))
        
        # Create a new client and load the conversations
        new_client = AIClient()
        new_client.load_conversations(str(file_path))
        
        # Check that the conversation was loaded correctly
        loaded_conversations = new_client.list_conversations()
        assert len(loaded_conversations) == 1
        loaded_conversation = loaded_conversations[0]
        assert loaded_conversation.id == conversation.id
        assert loaded_conversation.title == conversation.title
        assert len(loaded_conversation.messages) == 2
        assert loaded_conversation.messages[0].content == "Hello!"
        assert loaded_conversation.messages[1].content == "Hi there!" 
"""
AI Conversation Client

A Python client for interacting with AI language models.
This module provides an interface for sending messages, managing conversations,
and handling responses from various AI providers.

Usage:
    from ai_conversation_client import BaseAIClient, Message, MessageRole
    from ai_conversation_client.providers import OpenAIClient
    
    # Create a client with your preferred provider
    client = OpenAIClient(api_key="your_api_key")
    
    # Create a conversation
    conversation = client.create_conversation(title="My Chat", 
                                             system_prompt="You are a helpful assistant.")
    
    # Send a message and get a response
    response = await client.send_message(conversation.id, "Hello, AI!")
    print(response.content)
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
import uuid
import os
import json
import asyncio
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MessageRole(Enum):
    """
    Roles for conversation messages.
    
    Attributes:
        SYSTEM: Messages that instruct or inform the AI about its behavior
        USER: Messages from the human user
        ASSISTANT: Messages from the AI assistant
        FUNCTION: Messages used for function calling (advanced feature)
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class Message:
    """Represents a message in a conversation with the AI."""
    
    def __init__(self, content: str, role: MessageRole = MessageRole.USER, 
                 message_id: Optional[str] = None, timestamp: Optional[datetime] = None):
        """
        Initialize a new message.
        
        Args:
            content: The content of the message
            role: The role of the message sender (default: USER)
            message_id: Optional unique identifier for the message
            timestamp: Optional timestamp for the message
        """
        self._content = content
        self._role = role
        self._id = message_id or f"msg_{uuid.uuid4().hex[:8]}"
        self._timestamp = timestamp or datetime.now()
    
    @property
    def id(self) -> str:
        """Return the id of the message."""
        return self._id
    
    @property
    def content(self) -> str:
        """Return the content of the message."""
        return self._content
    
    @property
    def role(self) -> MessageRole:
        """Return the role of the message sender."""
        return self._role
    
    @property
    def timestamp(self) -> datetime:
        """Return the timestamp of the message."""
        return self._timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary for API requests."""
        return {
            "role": self._role.value,
            "content": self._content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create a message from a dictionary."""
        role = MessageRole(data.get("role", "user"))
        content = data.get("content", "")
        message_id = data.get("id")
        timestamp_str = data.get("timestamp")
        
        timestamp = None
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except ValueError:
                timestamp = datetime.now()
        
        return cls(content, role, message_id, timestamp)


class Conversation:
    """Represents a conversation with the AI."""
    
    def __init__(self, conversation_id: Optional[str] = None, 
                 title: Optional[str] = None, 
                 system_prompt: Optional[str] = None):
        """
        Initialize a new conversation.
        
        Args:
            conversation_id: Optional unique identifier for the conversation
            title: Optional title for the conversation
            system_prompt: Optional system prompt to set the AI's behavior
        """
        self._id = conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        self._title = title or f"Conversation {self._id}"
        self._messages: List[Message] = []
        
        # Add system message if provided
        if system_prompt:
            self.add_message(Message(system_prompt, MessageRole.SYSTEM))
    
    @property
    def id(self) -> str:
        """Return the id of the conversation."""
        return self._id
    
    @property
    def title(self) -> str:
        """Return the title of the conversation."""
        return self._title
    
    @property
    def messages(self) -> List[Message]:
        """Return all messages in the conversation."""
        return self._messages.copy()
    
    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation.
        
        Args:
            message: The message to add
        """
        self._messages.append(message)
    
    def get_latest_messages(self, count: int = 5) -> List[Message]:
        """
        Get the most recent messages from the conversation.
        
        Args:
            count: The number of messages to retrieve (default: 5)
            
        Returns:
            A list of the most recent messages
        """
        return self._messages[-count:] if self._messages else []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the conversation to a dictionary for storage/serialization."""
        return {
            "id": self._id,
            "title": self._title,
            "messages": [
                {
                    "id": msg.id,
                    "content": msg.content,
                    "role": msg.role.value,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in self._messages
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create a conversation from a dictionary."""
        conversation_id = data.get("id")
        title = data.get("title")
        
        conversation = cls(conversation_id, title)
        
        # Add messages
        for msg_data in data.get("messages", []):
            role = MessageRole(msg_data.get("role", "user"))
            content = msg_data.get("content", "")
            message_id = msg_data.get("id")
            
            timestamp = None
            timestamp_str = msg_data.get("timestamp")
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except ValueError:
                    timestamp = datetime.now()
            
            message = Message(content, role, message_id, timestamp)
            conversation.add_message(message)
        
        return conversation


class BaseAIClient(ABC):
    """Abstract base class for AI conversation clients."""
    
    def __init__(self):
        """Initialize a new AI client."""
        self._conversations: Dict[str, Conversation] = {}
    
    def create_conversation(self, title: Optional[str] = None, 
                          system_prompt: Optional[str] = None) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            title: Optional title for the conversation
            system_prompt: Optional system prompt to set the AI's behavior
            
        Returns:
            A new Conversation object
        """
        conversation = Conversation(title=title, system_prompt=system_prompt)
        self._conversations[conversation.id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Retrieve a conversation by ID.
        
        Args:
            conversation_id: The ID of the conversation to retrieve
            
        Returns:
            The Conversation if found, None otherwise
        """
        return self._conversations.get(conversation_id)
    
    def list_conversations(self) -> List[Conversation]:
        """
        List all available conversations.
        
        Returns:
            A list of all conversations managed by this client
            
        Usage:
            conversations = client.list_conversations()
            for conv in conversations:
                print(f"{conv.title} (ID: {conv.id})")
        """
        return list(self._conversations.values())
    
    @abstractmethod
    async def send_message(self, conversation_id: str, message_content: str) -> Message:
        """
        Send a user message to the AI and get a response.
        
        This is the main method for interacting with the AI. It sends a message to
        the specified conversation and returns the AI's response.
        
        Args:
            conversation_id: The ID of the conversation to send the message to
            message_content: The content of the message to send
            
        Returns:
            A Message object containing the AI's response
            
        Raises:
            ValueError: If the conversation ID is not found
            Exception: If there is an error communicating with the AI provider
            
        Usage:
            response = await client.send_message(conversation.id, "Hello, AI!")
            print(response.content)
        """
        pass
    
    @abstractmethod
    def set_model(self, model: str) -> None:
        """
        Change the AI model used for generating responses.
        
        Args:
            model: The name of the model to use
            
        Usage:
            client.set_model("gpt-4")
        """
        pass
    
    def export_conversation(self, conversation_id: str, 
                          format: str = "json") -> Union[str, Dict[str, Any]]:
        """
        Export a conversation to a specified format.
        
        Args:
            conversation_id: The ID of the conversation to export
            format: The format to export to ("json" or "text")
            
        Returns:
            A string (for "text" format) or dictionary (for "json" format)
            representing the conversation
            
        Raises:
            ValueError: If the conversation ID is not found or if the format is invalid
            
        Usage:
            # Export as text
            text_export = client.export_conversation(conversation.id, "text")
            print(text_export)
            
            # Export as JSON
            json_export = client.export_conversation(conversation.id, "json")
            import json
            print(json.dumps(json_export, indent=2))
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        if format.lower() == "json":
            return conversation.to_dict()
        elif format.lower() == "text":
            # Format as text
            text_output = f"# {conversation.title}\n\n"
            
            for msg in conversation.messages:
                timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                role_name = msg.role.name.capitalize()
                text_output += f"[{timestamp}] {role_name}: {msg.content}\n\n"
            
            return text_output
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def save_conversations(self, file_path: str) -> None:
        """
        Save all conversations to a JSON file.
        
        Args:
            file_path: The path to save the conversations to
            
        Raises:
            IOError: If there's an error writing to the file
            
        Usage:
            client.save_conversations("conversations.json")
        """
        try:
            data = {
                "conversations": [conv.to_dict() for conv in self._conversations.values()]
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise IOError(f"Error saving conversations: {str(e)}") from e
    
    def load_conversations(self, file_path: str) -> None:
        """
        Load conversations from a JSON file.
        
        Args:
            file_path: The path to load the conversations from
            
        Raises:
            IOError: If there's an error reading from the file
            ValueError: If the file contains invalid data
            
        Usage:
            client.load_conversations("conversations.json")
            
        Note:
            This will replace any existing conversations with the same IDs.
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for conv_data in data.get("conversations", []):
                conversation = Conversation.from_dict(conv_data)
                self._conversations[conversation.id] = conversation
        except Exception as e:
            raise IOError(f"Error loading conversations: {str(e)}") from e 
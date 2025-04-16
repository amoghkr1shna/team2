"""
AI Conversation Client

A Python client for interacting with OpenAI's ChatGPT API.
This module provides an interface for sending messages, managing conversations,
and handling responses from the OpenAI API.
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
import uuid


class MessageRole(Enum):
    """Roles for conversation messages."""
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
        self._title = title
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


class AIClient:
    """Client for interacting with OpenAI's ChatGPT API."""
    
    def __init__(self, api_key: Optional[str] = None, 
                 model: str = "gpt-3.5-turbo", 
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None):
        """
        Initialize a new AI client.
        
        Args:
            api_key: OpenAI API key (can be None if set in environment)
            model: The OpenAI model to use (default: gpt-3.5-turbo)
            temperature: Controls randomness (0-1, default: 0.7)
            max_tokens: Maximum tokens in response (None for model default)
        """
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
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
        List all conversations.
        
        Returns:
            A list of all conversations
        """
        return list(self._conversations.values())
    
    async def send_message(self, conversation_id: str, message_content: str) -> Message:
        """
        Send a message to the AI and get a response.
        
        Args:
            conversation_id: The ID of the conversation
            message_content: The content of the message to send
            
        Returns:
            The AI's response message
            
        Raises:
            ValueError: If the conversation doesn't exist
            ConnectionError: If there's an issue with the API connection
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        # Add user message to conversation
        user_message = Message(message_content, MessageRole.USER)
        conversation.add_message(user_message)
        
        # In a real implementation, this would make an API call to OpenAI
        # For now, we'll create a placeholder response
        response_content = f"This is a placeholder response to: {message_content}"
        ai_message = Message(response_content, MessageRole.ASSISTANT)
        
        # Add AI response to conversation
        conversation.add_message(ai_message)
        
        return ai_message
    
    def set_model(self, model: str) -> None:
        """
        Change the AI model being used.
        
        Args:
            model: The name of the model to use
        """
        self._model = model
    
    def export_conversation(self, conversation_id: str, 
                           format: str = "json") -> Union[str, Dict[str, Any]]:
        """
        Export a conversation in the specified format.
        
        Args:
            conversation_id: The ID of the conversation to export
            format: The format to export to (json, text, etc.)
            
        Returns:
            The exported conversation
            
        Raises:
            ValueError: If the conversation doesn't exist or format is invalid
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        # This is a placeholder - a real implementation would format accordingly
        if format.lower() == "json":
            return {"id": conversation.id, "title": conversation.title}
        elif format.lower() == "text":
            return f"Conversation {conversation.id}: {conversation.title}"
        else:
            raise ValueError(f"Unsupported export format: {format}") 
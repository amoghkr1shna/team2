#updated code, after TA Feedback on dependency injection and class structure

from abc import ABC, abstractmethod
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
    """Represents a message in a conversation.
    
    Attributes:
        content (str): The content of the message
        role (MessageRole): The role of the message sender (user, assistant, system, function)
        id (str): Unique identifier for the message
        timestamp (datetime): When the message was created
    """
    
    def __init__(self, content: str, role: MessageRole = MessageRole.USER, 
                 message_id: Optional[str] = None, timestamp: Optional[datetime] = None):
        """Initialize a new message.
        
        Args:
            content (str): The content of the message
            role (MessageRole, optional): The role of the sender. Defaults to USER.
            message_id (str, optional): Unique identifier. If None, one will be generated.
            timestamp (datetime, optional): Message timestamp. If None, current time is used.
        """
        self._content = content
        self._role = role
        self._id = message_id or f"msg_{uuid.uuid4().hex[:8]}"
        self._timestamp = timestamp or datetime.now()
    
    @property
    def id(self) -> str:
        """Get the message's unique identifier.
        
        Returns:
            str: The message ID
        """
        return self._id
    
    @property
    def content(self) -> str:
        return self._content
    
    @property
    def role(self) -> MessageRole:
        return self._role
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp


class AIBackend(ABC):
    """Abstract base class for AI backends."""
    
    @abstractmethod
    async def generate_response(self, messages: List[Message], **kwargs: Any) -> Message:
        """Generate a response from the AI backend."""
        pass


class Conversation:
    """Represents a conversation with message history.
    
    Attributes:
        id (str): Unique identifier for the conversation
        title (str, optional): Title of the conversation
        messages (List[Message]): List of messages in the conversation
    """
    
    def __init__(self, conversation_id: Optional[str] = None, 
                 title: Optional[str] = None, 
                 system_prompt: Optional[str] = None):
        """Initialize a new conversation.
        
        Args:
            conversation_id (str, optional): Unique identifier. If None, one will be generated.
            title (str, optional): Title of the conversation
            system_prompt (str, optional): Initial system prompt to set conversation context
        """
        self._id = conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        self._title = title
        self._messages: List[Message] = []
        
        if system_prompt:
            self.add_message(Message(system_prompt, MessageRole.SYSTEM))
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def title(self) -> Optional[str]:
        return self._title
    
    @property
    def messages(self) -> List[Message]:
        return self._messages.copy()
    
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation.
        
        Args:
            message (Message): The message to add
        """
        self._messages.append(message)


class AIClient:
    """Generic AI client using dependency injection for backend implementation."""
    
    def __init__(self, backend: AIBackend):
        """
        Initialize the client with a backend implementation.
        
        Args:
            backend: An implementation of AIBackend
        """
        self._backend = backend
        self._conversations: Dict[str, Conversation] = {}
    
    def create_conversation(self, title: Optional[str] = None, 
                          system_prompt: Optional[str] = None) -> Conversation:
        """Create a new conversation.
        
        Args:
            title (str, optional): Title for the conversation
            system_prompt (str, optional): Initial system prompt
            
        Returns:
            Conversation: The newly created conversation
        """
        conversation = Conversation(title=title, system_prompt=system_prompt)
        self._conversations[conversation.id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self._conversations.get(conversation_id)
    
    async def send_message(self, conversation_id: str, message_content: str) -> Message:
        """Send a message and get an AI response.
        
        Args:
            conversation_id (str): ID of the conversation to send message to
            message_content (str): Content of the message to send
            
        Returns:
            Message: The AI's response message
            
        Raises:
            ValueError: If conversation_id doesn't exist
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        user_message = Message(message_content, MessageRole.USER)
        conversation.add_message(user_message)
        
        response = await self._backend.generate_response(conversation.messages)
        conversation.add_message(response)
        
        return response

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
    """Represents a message in a conversation."""
    
    def __init__(self, content: str, role: MessageRole = MessageRole.USER, 
                 message_id: Optional[str] = None, timestamp: Optional[datetime] = None):
        self._content = content
        self._role = role
        self._id = message_id or f"msg_{uuid.uuid4().hex[:8]}"
        self._timestamp = timestamp or datetime.now()
    
    @property
    def id(self) -> str:
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
    """Represents a conversation."""
    
    def __init__(self, conversation_id: Optional[str] = None, 
                 title: Optional[str] = None, 
                 system_prompt: Optional[str] = None):
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
        self._messages.append(message)


class AIClient:
    """Generic AI client using dependency injection."""
    
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
        conversation = Conversation(title=title, system_prompt=system_prompt)
        self._conversations[conversation.id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self._conversations.get(conversation_id)
    
    async def send_message(self, conversation_id: str, message_content: str) -> Message:
        """Send a message and get an AI response."""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        user_message = Message(message_content, MessageRole.USER)
        conversation.add_message(user_message)
        
        response = await self._backend.generate_response(conversation.messages)
        conversation.add_message(response)
        
        return response
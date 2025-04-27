#updated code, after TA Feedback on dependency injection and class structure

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
import uuid


class MessageRole(Enum):
    """Roles for conversation messages.
    
    Defines the possible roles a message sender can have in a conversation:
    - SYSTEM: System messages that define behavior or context
    - USER: Messages from the user
    - ASSISTANT: Messages from the AI assistant
    - FUNCTION: Messages from function calls
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class Message:
    """Represents a message in a conversation.
    
    A message is an immutable object that contains content, sender role,
    and metadata like timestamp and ID.
    
    Attributes:
        content (str): The content of the message
        role (MessageRole): The role of the message sender
        id (str): Unique identifier for the message
        timestamp (datetime): When the message was created
    
    Raises:
        ValueError: If content is empty or role is invalid
    """
    
    def __init__(self, content: str, role: MessageRole = MessageRole.USER, 
                 message_id: Optional[str] = None, timestamp: Optional[datetime] = None):
        """Initialize a new message.
        
        Args:
            content (str): The content of the message
            role (MessageRole, optional): The role of the sender. Defaults to USER.
            message_id (str, optional): Unique identifier. If None, one will be generated.
            timestamp (datetime, optional): Message timestamp. If None, current time is used.
            
        Raises:
            ValueError: If content is empty
            TypeError: If role is not a MessageRole
        """
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")
        if not isinstance(role, MessageRole):
            raise TypeError("Role must be a MessageRole enum value")
            
        self._content = content.strip()
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
        """Get the message content.
        
        Returns:
            str: The content of the message
        """
        return self._content
    
    @property
    def role(self) -> MessageRole:
        """Get the message sender's role.
        
        Returns:
            MessageRole: The role of the sender
        """
        return self._role
    
    @property
    def timestamp(self) -> datetime:
        """Get the message timestamp.
        
        Returns:
            datetime: When the message was created
        """
        return self._timestamp


class AIBackend(ABC):
    """Abstract base class for AI backends.
    
    This class defines the interface that any AI backend implementation
    must follow to be compatible with the AIClient.
    """
    
    @abstractmethod
    async def generate_response(self, messages: List[Message], **kwargs: Any) -> Message:
        """Generate a response from the AI backend.
        
        Args:
            messages (List[Message]): The conversation history
            **kwargs: Additional backend-specific parameters
            
        Returns:
            Message: The AI's response message
            
        Raises:
            ValueError: If messages list is empty
            RuntimeError: If response generation fails
        """
        pass


class Conversation:
    """Represents a conversation with message history.
    
    A conversation is a collection of messages with metadata like title
    and optional system prompt.
    
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
            
        Raises:
            ValueError: If system_prompt is empty when provided
        """
        if system_prompt is not None and not system_prompt.strip():
            raise ValueError("System prompt cannot be empty when provided")
            
        self._id = conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        self._title = title.strip() if title else None
        self._messages: List[Message] = []
        
        if system_prompt:
            self.add_message(Message(system_prompt, MessageRole.SYSTEM))
    
    @property
    def id(self) -> str:
        """Get the conversation's unique identifier.
        
        Returns:
            str: The conversation ID
        """
        return self._id
    
    @property
    def title(self) -> Optional[str]:
        """Get the conversation title.
        
        Returns:
            Optional[str]: The title of the conversation, if set
        """
        return self._title
    
    @property
    def messages(self) -> List[Message]:
        """Get the conversation messages.
        
        Returns a copy of the messages list to prevent modification.
        
        Returns:
            List[Message]: Copy of the conversation messages
        """
        return self._messages.copy()
    
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation.
        
        Args:
            message (Message): The message to add
            
        Raises:
            TypeError: If message is not a Message instance
        """
        if not isinstance(message, Message):
            raise TypeError("Message must be an instance of Message class")
        self._messages.append(message)


class AIClient:
    """Generic AI client using dependency injection for backend implementation.
    
    This client manages conversations and delegates AI interactions to a backend.
    It uses dependency injection to remain backend-agnostic.
    """
    
    def __init__(self, backend: AIBackend):
        """Initialize the client with a backend implementation.
        
        Args:
            backend (AIBackend): An implementation of AIBackend
            
        Raises:
            TypeError: If backend is not an AIBackend instance
        """
        if not isinstance(backend, AIBackend):
            raise TypeError("Backend must implement AIBackend")
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
            
        Raises:
            ValueError: If title or system_prompt is empty when provided
        """
        conversation = Conversation(title=title, system_prompt=system_prompt)
        self._conversations[conversation.id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by its ID.
        
        Args:
            conversation_id (str): The ID of the conversation to retrieve
            
        Returns:
            Optional[Conversation]: The conversation if found, None otherwise
        """
        return self._conversations.get(conversation_id)
    
    async def send_message(self, conversation_id: str, message_content: str) -> Message:
        """Send a message and get an AI response.
        
        Args:
            conversation_id (str): ID of the conversation to send message to
            message_content (str): Content of the message to send
            
        Returns:
            Message: The AI's response message
            
        Raises:
            ValueError: If conversation_id doesn't exist or message_content is empty
            RuntimeError: If AI response generation fails
        """
        if not message_content or not message_content.strip():
            raise ValueError("Message content cannot be empty")
            
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        user_message = Message(message_content, MessageRole.USER)
        conversation.add_message(user_message)
        
        try:
            response = await self._backend.generate_response(conversation.messages)
            conversation.add_message(response)
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to generate AI response: {str(e)}") from e
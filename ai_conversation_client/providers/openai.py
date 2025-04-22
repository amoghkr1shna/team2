"""
OpenAI Implementation of the AI Conversation Client

This module provides an implementation of the BaseAIClient interface
using OpenAI's API.
"""

import os
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

from ai_conversation_client import BaseAIClient, Message, MessageRole, Conversation

# Load environment variables
load_dotenv()

class OpenAIClient(BaseAIClient):
    """Client for interacting with OpenAI's ChatGPT API."""
    
    def __init__(self, api_key: Optional[str] = None, 
                 model: str = "gpt-3.5-turbo", 
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None):
        """
        Initialize a new OpenAI client.
        
        Args:
            api_key: OpenAI API key (can be None if set in environment)
            model: The OpenAI model to use (default: gpt-3.5-turbo)
            temperature: Controls randomness (0-1, default: 0.7)
            max_tokens: Maximum tokens in response (None for model default)
        """
        super().__init__()
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError("OpenAI API key is required. Provide it as a parameter or set it in the OPENAI_API_KEY environment variable.")
        
        self._model = model or os.getenv("MODEL", "gpt-3.5-turbo")
        self._temperature = temperature if temperature is not None else float(os.getenv("TEMPERATURE", "0.7"))
        self._max_tokens = max_tokens or (int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None)
        
        # Initialize the OpenAI client
        self._client = AsyncOpenAI(api_key=self._api_key)
    
    async def send_message(self, conversation_id: str, message_content: str) -> Message:
        """
        Send a user message to OpenAI and get a response.
        
        This method sends a message to the specified conversation using the OpenAI API
        and returns the AI's response.
        
        Args:
            conversation_id: The ID of the conversation to send the message to
            message_content: The content of the message to send
            
        Returns:
            A Message object containing the AI's response
            
        Raises:
            ValueError: If the conversation ID is not found
            ConnectionError: If there is an error communicating with the OpenAI API
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        # Add user message to conversation
        user_message = Message(message_content, MessageRole.USER)
        conversation.add_message(user_message)
        
        # Prepare messages for the API request
        messages = [msg.to_dict() for msg in conversation.messages]
        
        try:
            # Call the OpenAI API
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens
            )
            
            # Extract the response content
            response_content = response.choices[0].message.content
            
            # Create a message from the response
            ai_message = Message(response_content, MessageRole.ASSISTANT)
            
            # Add AI response to conversation
            conversation.add_message(ai_message)
            
            return ai_message
        except Exception as e:
            # Handle API errors
            error_message = f"Error communicating with OpenAI API: {str(e)}"
            raise ConnectionError(error_message) from e
    
    def set_model(self, model: str) -> None:
        """
        Change the OpenAI model being used.
        
        Args:
            model: The name of the OpenAI model to use (e.g., "gpt-3.5-turbo", "gpt-4")
        """
        self._model = model 
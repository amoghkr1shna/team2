#!/usr/bin/env python3
"""
Example usage of the AI Conversation Client.

This script demonstrates how to use the AI Conversation Client to:
1. Create a new conversation with a system prompt
2. Send messages to the AI and receive responses
3. Send follow-up messages in the same conversation
4. Export a conversation as text
5. Save conversations to a file for later use

Usage:
    python -m ai_conversation_client.example
    
Requirements:
    - OpenAI API key set in .env file or environment variables
    - AI Conversation Client package installed
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_conversation_client.providers import OpenAIClient

async def main():
    """
    Run the example AI conversation workflow.
    
    This function demonstrates a complete workflow for using the AI Conversation Client:
    - Setting up the client with environment variables
    - Creating a conversation with a custom system prompt
    - Sending an initial message and receiving a response
    - Sending a follow-up message in the same conversation
    - Exporting the conversation as text
    - Saving the conversation to a file
    
    Returns:
        None
        
    Note:
        Requires an OpenAI API key to be set in the environment or .env file.
    """
    # Load environment variables
    load_dotenv()
    
    # Check if API key is provided
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OpenAI API key in the .env file or environment variables.")
        print("Example: OPENAI_API_KEY=your-key-here")
        return
    
    # Create an AI client
    client = OpenAIClient()
    
    # Create a conversation with a system prompt
    conversation = client.create_conversation(
        title="Python Programming Help",
        system_prompt="You are a helpful Python programming assistant. You provide clear, concise, and accurate information about Python programming."
    )
    
    print(f"Created conversation: {conversation.title} (ID: {conversation.id})")
    
    # First message
    message_content = "What's the difference between a list and a tuple in Python?"
    print(f"\nSending message: {message_content}")
    
    response = await client.send_message(conversation.id, message_content)
    print(f"\nResponse: {response.content}")
    
    # Second message - follow-up
    message_content = "Can you show me an example of when to use each one?"
    print(f"\nSending follow-up: {message_content}")
    
    response = await client.send_message(conversation.id, message_content)
    print(f"\nResponse: {response.content}")
    
    # Export the conversation as text
    text_export = client.export_conversation(conversation.id, "text")
    print("\n----- Conversation Export (Text) -----")
    print(text_export)
    
    # Save all conversations to a file
    client.save_conversations("conversations.json")
    print("\nConversations saved to conversations.json")

if __name__ == "__main__":
    asyncio.run(main()) 
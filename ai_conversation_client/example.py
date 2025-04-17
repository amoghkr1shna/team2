#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from ai_conversation_client import AIClient

async def main():
    """Run the example."""
    # Load environment variables
    load_dotenv()
    
    # Check if API key is provided
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OpenAI API key in the .env file or environment variables.")
        print("Example: OPENAI_API_KEY=your-key-here")
        return
    
    # Create an AI client
    client = AIClient()
    
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
#!/usr/bin/env python3
"""
Command-line interface for the AI Conversation Client.

This module provides a simple command-line interface for interacting
with the AI Conversation Client.

Usage:
    # Start a new chat session
    python -m ai_conversation_client.cli chat
    
    # Continue an existing conversation
    python -m ai_conversation_client.cli chat --conversation-id CONV_ID
    
    # List all saved conversations
    python -m ai_conversation_client.cli list
    
    # Export a conversation
    python -m ai_conversation_client.cli export CONV_ID --format text
    
    # Load conversations from a file
    python -m ai_conversation_client.cli load conversations.json
"""

import asyncio
import argparse
import os
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath('..'))
from ai_conversation_client import AIClient, MessageRole, Message

async def chat_mode(client, conversation_id=None, system_prompt=None):
    """
    Start an interactive chat session with the AI.
    
    This function provides a REPL (Read-Eval-Print Loop) interface for chatting with
    the AI. It either creates a new conversation or continues an existing one.
    
    Special commands:
        exit, quit: End the chat session
        save: Save all conversations to a file
        export json/text: Export the current conversation
    
    Args:
        client: An instance of AIClient
        conversation_id: Optional ID of an existing conversation to continue
        system_prompt: Optional system prompt for a new conversation
        
    Returns:
        None
    """
    # Create or load a conversation
    if conversation_id:
        conversation = client.get_conversation(conversation_id)
        if not conversation:
            print(f"Conversation with ID {conversation_id} not found.")
            return
        print(f"Continuing conversation: {conversation.title}")
    else:
        title = input("Enter a title for the conversation (or press Enter for default): ")
        if not title:
            title = None
        
        if not system_prompt:
            system_prompt = input("Enter a system prompt (or press Enter for default): ")
            if not system_prompt:
                system_prompt = "You are a helpful assistant."
        
        conversation = client.create_conversation(title, system_prompt)
        print(f"Created new conversation: {conversation.title} (ID: {conversation.id})")
    
    # Show the most recent messages
    messages = conversation.messages
    if messages:
        print("\nRecent messages:")
        for msg in messages[-5:]:
            role_name = msg.role.name.capitalize()
            print(f"{role_name}: {msg.content}")
    
    # Start the chat loop
    print("\nType 'exit' or 'quit' to end the conversation.")
    print("Type 'save' to save the conversation to a file.")
    print("Type 'export json' or 'export text' to export the conversation.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ("exit", "quit"):
                break
            elif user_input.lower() == "save":
                file_path = input("Enter file path to save: ")
                if not file_path:
                    file_path = "conversations.json"
                client.save_conversations(file_path)
                print(f"Saved conversations to {file_path}")
                continue
            elif user_input.lower().startswith("export"):
                parts = user_input.lower().split()
                format_type = parts[1] if len(parts) > 1 else "text"
                if format_type not in ("json", "text"):
                    print("Unsupported format. Use 'export json' or 'export text'.")
                    continue
                
                result = client.export_conversation(conversation.id, format_type)
                if format_type == "json":
                    import json
                    print(json.dumps(result, indent=2))
                else:
                    print(result)
                continue
            
            print("Waiting for response...")
            response = await client.send_message(conversation.id, user_input)
            print(f"\nAI: {response.content}")
            
        except KeyboardInterrupt:
            print("\nExiting chat mode...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

async def main():
    """
    Main entry point for the CLI application.
    
    This function parses command-line arguments and executes the appropriate
    command based on user input. Available commands:
    
    - chat: Start an interactive chat session
    - list: List all saved conversations
    - export: Export a conversation to text or JSON
    - load: Load conversations from a file
    
    Returns:
        None
        
    Raises:
        SystemExit: If the OpenAI API key is missing
    """
    parser = argparse.ArgumentParser(description="AI Conversation Client CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start an interactive chat")
    chat_parser.add_argument("--conversation-id", "-c", help="ID of an existing conversation")
    chat_parser.add_argument("--system-prompt", "-s", help="System prompt for a new conversation")
    
    # List conversations command
    list_parser = subparsers.add_parser("list", help="List all conversations")
    
    # Export conversation command
    export_parser = subparsers.add_parser("export", help="Export a conversation")
    export_parser.add_argument("conversation_id", help="ID of the conversation to export")
    export_parser.add_argument("--format", "-f", choices=["json", "text"], default="text", 
                              help="Export format (default: text)")
    export_parser.add_argument("--output", "-o", help="Output file path")
    
    # Load conversations command
    load_parser = subparsers.add_parser("load", help="Load conversations from a file")
    load_parser.add_argument("file_path", help="Path to the conversations file")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is provided
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OpenAI API key is required.")
        print("Set it in the OPENAI_API_KEY environment variable or in a .env file.")
        sys.exit(1)
    
    # Create an AI client
    client = AIClient()
    
    if args.command == "chat":
        await chat_mode(client, args.conversation_id, args.system_prompt)
    elif args.command == "list":
        conversations = client.list_conversations()
        if not conversations:
            print("No conversations found.")
        else:
            print(f"Found {len(conversations)} conversations:")
            for i, conv in enumerate(conversations, 1):
                msg_count = len(conv.messages)
                print(f"{i}. {conv.title} (ID: {conv.id}) - {msg_count} messages")
    elif args.command == "export":
        try:
            result = client.export_conversation(args.conversation_id, args.format)
            
            if args.output:
                with open(args.output, "w") as f:
                    if args.format == "json":
                        import json
                        json.dump(result, f, indent=2)
                    else:
                        f.write(result)
                print(f"Exported conversation to {args.output}")
            else:
                if args.format == "json":
                    import json
                    print(json.dumps(result, indent=2))
                else:
                    print(result)
        except ValueError as e:
            print(f"Error: {str(e)}")
    elif args.command == "load":
        try:
            client.load_conversations(args.file_path)
            conversations = client.list_conversations()
            print(f"Loaded {len(conversations)} conversations from {args.file_path}")
        except Exception as e:
            print(f"Error loading conversations: {str(e)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main()) 
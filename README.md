# AI Conversation Client

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python client for interacting with AI language models, providing a clean and simple interface for managing AI conversations with different providers.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
- [API Reference](#api-reference)
- [Implementation Details](#implementation-details)
- [Testing](#testing)
- [License](#license)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-conversation-client.git
cd ai-conversation-client

# Install using pip in development mode
pip install -e ".[dev]"

# Create a .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-openai-api-key-here" > ai_conversation_client/.env
```

## Quick Start

### Using the CLI

```bash
# Start an interactive chat
python -m ai_conversation_client.cli chat

# List all conversations
python -m ai_conversation_client.cli list

# Export a conversation
python -m ai_conversation_client.cli export <conversation_id> --format json
```

### Using the Python API

```python
import asyncio
from ai_conversation_client.providers import OpenAIClient

async def main():
    # Initialize client with your API key
    client = OpenAIClient()

    # Create a new conversation
    conversation = client.create_conversation(
        title="My First Conversation",
        system_prompt="You are a helpful assistant."
    )

    # Send a message and get a response
    response = await client.send_message(
        conversation.id,
        "What can you tell me about Python?"
    )

    # Print the response
    print(f"AI: {response.content}")

    # Export conversation
    json_export = client.export_conversation(conversation.id, "json")
    print(f"Conversation exported: {json_export}")

# Run the example
asyncio.run(main())
```

## Features

- **Provider Abstraction**: Interface-based design that separates AI provider implementations from the core conversation logic
- **Conversation Management**: Create, retrieve, and manage multiple AI conversations
- **Message Handling**: Send messages to AI models and process responses
- **Customizable Settings**: Configure model, temperature, and other parameters
- **Export/Import**: Save conversations to JSON or formatted text output
- **Command-line Interface**: Interact with the client via a simple CLI
- **Persistent Storage**: Save and load conversations from disk

## Usage

### Command Line Interface

The client includes a command-line interface for easy interaction:

```bash
# Start a new conversation and chat interactively
python -m ai_conversation_client.cli chat

# Continue an existing conversation
python -m ai_conversation_client.cli chat --conversation-id <id>

# List all saved conversations
python -m ai_conversation_client.cli list

# Export a conversation in text format
python -m ai_conversation_client.cli export <id> --format text --output conversation.txt

# Load conversations from a file
python -m ai_conversation_client.cli load conversations.json
```

During interactive chat, you can use these commands:

- Type `exit` or `quit` to end the chat
- Type `save` to save all conversations to a file
- Type `export json` or `export text` to see the current conversation in different formats

### Python API

Here's how to use the client in your Python code:

```python
import asyncio
from ai_conversation_client.providers import OpenAIClient
from ai_conversation_client import MessageRole

async def example():
    # Create a client
    client = OpenAIClient()

    # Create a conversation
    conversation = client.create_conversation(
        title="Python Help",
        system_prompt="You are a Python expert."
    )

    # Send messages and get responses
    response = await client.send_message(conversation.id, "How do I read a file in Python?")
    print(response.content)

    follow_up = await client.send_message(conversation.id, "What about writing to a file?")
    print(follow_up.content)

    # Save conversations for later
    client.save_conversations("my_conversations.json")

    # Load conversations in another session
    new_client = OpenAIClient()
    new_client.load_conversations("my_conversations.json")

    # List all conversations
    for conv in new_client.list_conversations():
        print(f"{conv.title} (ID: {conv.id}) - {len(conv.messages)} messages")

asyncio.run(example())
```

## API Reference

### MessageRole

An enum defining the possible roles for a message in a conversation:

- `MessageRole.SYSTEM`: System messages that define the AI's behavior
- `MessageRole.USER`: Messages from the user
- `MessageRole.ASSISTANT`: Messages from the AI assistant
- `MessageRole.FUNCTION`: Messages from function calls

### Message

Represents a single message within a conversation.

```python
from ai_conversation_client import Message, MessageRole
from datetime import datetime

message = Message(
    content="Hello!",
    role=MessageRole.USER,
    message_id="msg_123",  # Optional
    timestamp=datetime.now()  # Optional
)
```

**Properties:**

- `id`: Unique identifier of the message
- `content`: Text content of the message
- `role`: Role of the sender (user, assistant, etc.)
- `timestamp`: When the message was created

**Methods:**

- `to_dict()`: Convert the message to a dictionary
- `from_dict(data)`: Create a message from a dictionary

### Conversation

Represents a conversation consisting of multiple messages.

```python
from ai_conversation_client import Conversation

conversation = Conversation(
    conversation_id="conv_123",  # Optional
    title="My Conversation",  # Optional
    system_prompt="You are a helpful assistant."  # Optional
)
```

**Properties:**

- `id`: Unique identifier of the conversation
- `title`: Display title of the conversation
- `messages`: List of all messages in the conversation

**Methods:**

- `add_message(message)`: Add a message to the conversation
- `get_latest_messages(count=5)`: Get the most recent messages
- `to_dict()`: Convert the conversation to a dictionary
- `from_dict(data)`: Create a conversation from a dictionary

### BaseAIClient

The abstract base class that defines the interface for AI clients.

**Methods:**

- `create_conversation(title=None, system_prompt=None)`: Create a new conversation
- `get_conversation(conversation_id)`: Get a conversation by ID
- `list_conversations()`: List all conversations
- `async send_message(conversation_id, message_content)`: Send a message and get AI response
- `set_model(model)`: Change the AI model being used
- `export_conversation(conversation_id, format="json")`: Export a conversation
- `save_conversations(file_path)`: Save all conversations to a file
- `load_conversations(file_path)`: Load conversations from a file

### OpenAIClient

A concrete implementation of BaseAIClient that uses the OpenAI API.

```python
from ai_conversation_client.providers import OpenAIClient

client = OpenAIClient(
    api_key="your-openai-api-key",  # Optional if set in environment
    model="gpt-3.5-turbo",  # Optional, default shown
    temperature=0.7,  # Optional, default shown
    max_tokens=None  # Optional
)
```

## Implementation Details

The AI Conversation Client is built using:

- **Python 3.8+**: For modern language features
- **Abstract Base Classes**: For provider-agnostic interfaces
- **OpenAI API**: For AI chat completions using AsyncOpenAI client (one of several possible providers)
- **Asyncio**: For asynchronous API calls
- **Dotenv**: For environment variable management
- **JSON**: For conversation storage and serialization
- **UUID**: For generating unique IDs for messages and conversations
- **Argparse**: For command-line interface parsing

The implementation includes:

1. **Interface Definition**: Abstract BaseAIClient class for multiple providers
2. **Core Classes**: Message, Conversation, and provider implementations
3. **API Integration**: Full integration with OpenAI's Chat Completions API via OpenAIClient
4. **Serialization**: Complete to_dict/from_dict methods for persistence
5. **Command-line Interface**: A full-featured CLI with multiple commands
6. **Error Handling**: Comprehensive error handling for API failures
7. **Environment Config**: Support for configuration via environment variables

### Architecture

The client follows a clean interface-based architecture:

```
ai_conversation_client/
├── __init__.py          # Core interfaces and classes
├── cli.py               # Command-line interface
├── example.py           # Example usage
├── providers/
│   ├── __init__.py      # Provider exports
│   └── openai.py        # OpenAI implementation
```

### Extending with New Providers

You can create additional providers by implementing the BaseAIClient interface:

```python
from ai_conversation_client import BaseAIClient, Message, MessageRole

class CustomAIClient(BaseAIClient):
    def __init__(self, api_key, **kwargs):
        super().__init__()
        # Initialize your client

    async def send_message(self, conversation_id, message_content):
        # Implement message sending for your provider
        pass

    def set_model(self, model):
        # Implement model switching for your provider
        pass
```

## Testing

The project includes comprehensive tests using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_conversation_client
```

Tests are structured to mock the API calls, allowing for thorough testing without making actual API requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

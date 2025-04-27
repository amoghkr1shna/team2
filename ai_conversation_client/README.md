# AI Conversation Client

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python client for interacting with OpenAI's ChatGPT API, providing a clean and simple interface for managing AI conversations.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Project Scope](#project-scope)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-conversation-client.git
cd ai-conversation-client

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
import asyncio
from ai_conversation_client import AIClient

async def main():
    # Initialize client with your API key
    client = AIClient(api_key="your-openai-api-key")

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

### Conversation

Represents a conversation consisting of multiple messages.

```python
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

### AIClient

The main client for interacting with the OpenAI API.

```python
client = AIClient(
    api_key="your-openai-api-key",  # Optional if set in environment
    model="gpt-3.5-turbo",  # Optional, default shown
    temperature=0.7,  # Optional, default shown
    max_tokens=None  # Optional
)
```

**Methods:**

- `create_conversation(title=None, system_prompt=None)`: Create a new conversation
- `get_conversation(conversation_id)`: Get a conversation by ID
- `list_conversations()`: List all conversations
- `async send_message(conversation_id, message_content)`: Send a message and get AI response
- `set_model(model)`: Change the AI model being used
- `export_conversation(conversation_id, format="json")`: Export a conversation

## Project Scope

### Minimum Viable Version (MVV)

This project's minimum viable version includes:

1. **Conversation Management**

   - Create, retrieve, and list conversations
   - Add messages to conversations
   - Retrieve conversation history

2. **OpenAI Integration**

   - Connect to OpenAI API using API key
   - Send messages to OpenAI
   - Process AI responses

3. **Configuration**

   - Support for different OpenAI models
   - Customizable parameters (temperature, tokens)

4. **Export Options**
   - JSON and text export formats

### Out of Scope

Features intentionally excluded from the initial version:

1. **Authentication & Authorization**

   - User management and authentication
   - Access control systems

2. **Advanced OpenAI Features**

   - Fine-tuning models
   - Streaming responses
   - Function calling
   - Image generation

3. **User Interfaces**

   - Web, mobile, or desktop UIs

4. **Data Persistence**

   - Database integration
   - Backup functionality

5. **Analytics**
   - Usage tracking
   - Performance monitoring

## Testing

The project uses pytest for testing. Run the tests with:

```bash
pytest ai_conversation_client/tests/
```

The test suite verifies the interface definitions without requiring actual API calls to OpenAI.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

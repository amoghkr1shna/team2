# Email-AI Integration

This project integrates Team 8's email inbox client with an AI conversation client to create a spam detection application.

## Overview

The integration:

- Accesses emails from a mailbox (real or mock)
- Analyzes each email with AI to determine spam probability
- Outputs results to a CSV file

## Setup

```bash
# Clone the repository with submodules
git clone --recursive https://github.com/yourusername/repo-name.git
cd repo-name

# If you already cloned without submodules:
git submodule update --init --recursive
```

## Usage

### Command Line Interface

```bash
# Basic usage with mock emails
python spam_detection.py --populate

# Specify output location
python spam_detection.py --output results.csv --populate

# Limit number of emails processed
python spam_detection.py --populate --limit 10

# Use a specific AI model
python spam_detection.py --populate --model gpt-4
```

### Programmatic API

```python
from spam_detection import SpamDetector
import asyncio

async def analyze_emails():
    # Create detector instance (handles all components)
    detector = SpamDetector()

    # Optional: Populate with test data
    detector.populate_inbox_with_mock_data(count=10)

    # Process emails and save results
    await detector.analyze_and_save(output_file='results.csv')

# Run the async function
asyncio.run(analyze_emails())
```

## Output

The integration produces a CSV file with two columns:

```
mail_id,Pct_spam
c1a94df7-73e9-4d63-afba-812496b2d18d,2.0
9f02f669-0e12-4f37-a1a0-d7f548c8b026,5.0
```

## How It Works

1. The `SpamDetector` class integrates both components:

   - Email Client: Fetches and manages emails
   - AI Client: Analyzes email content for spam probability

2. System prompts and configuration are handled internally

3. Emails are processed sequentially and analyzed for spam

4. Results are collected and saved to CSV

Third parties can use the application directly without defining prompts, managing connections between components, or handling technical implementation details.

## API Reference

### SpamDetector

```python
detector = SpamDetector(
    api_key=None,        # Optional: OpenAI API key
    model="gpt-3.5-turbo", # Optional: AI model to use
    email_data_dir=None  # Optional: Directory for email data
)
```

#### Methods:

- `populate_inbox_with_mock_data(count=15)`: Adds mock emails to the inbox
- `async analyze_email(email_body)`: Analyzes a single email for spam probability
- `async analyze_inbox(folder="INBOX", limit=None)`: Processes emails and returns results
- `async analyze_and_save(output_file='spam_results.csv', folder="INBOX", limit=None)`: Analyzes emails and saves to CSV

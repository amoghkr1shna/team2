import os
import sys
import csv
import asyncio
import pytest

# Add the email client implementation and API to sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_impl', 'src'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_api', 'src'))

from ai_conversation_client.providers.openai import OpenAIClient
from my_inbox_impl.mail_fetcher import MockFetcher
from my_inbox_impl import ClientImpl

@pytest.mark.asyncio
async def test_email_ai_integration(tmp_path, monkeypatch):
    # Setup: use a temp directory for the CSV output
    csv_path = tmp_path / "spam_results.csv"

    # Patch OpenAIClient to return a fixed spam probability
    class DummyAIClient(OpenAIClient):
        async def send_message(self, conversation_id, prompt):
            class DummyResponse:
                content = "42.0"
            return DummyResponse()

    # Email client setup
    email_client = ClientImpl(data_dir=str(tmp_path))
    fetcher = MockFetcher()
    fetcher.set_client(email_client)
    fetcher.fetch_messages(count=3)

    ai_client = DummyAIClient(api_key="dummy")
    conversation = ai_client.create_conversation(
        title="Spam Detection",
        system_prompt="You are an AI that returns the probability that an email is spam. Respond with a number between 0 and 100."
    )

    results = []
    for message in email_client.get_messages(folder="INBOX", limit=20):
        mail_id = message.id
        body = message.body
        pct_spam = await ai_client.send_message(conversation.id, body)
        results.append({'mail_id': mail_id, 'Pct_spam': float(pct_spam.content)})

    # Write to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['mail_id', 'Pct_spam']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    # Assert CSV is correct
    with open(csv_path) as f:
        lines = f.readlines()
        assert lines[0].strip() == "mail_id,Pct_spam"
        assert len(lines) == 4  # header + 3 emails
        for line in lines[1:]:
            assert line.strip().endswith("42.0") 
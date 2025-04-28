import os
import sys
import asyncio
import csv

# Dynamically find the repo root (assumes this script is always at the repo root)
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_impl', 'src'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_api', 'src'))

from my_inbox_impl import get_client as get_email_client
from ai_conversation_client.providers.openai import OpenAIClient
from my_inbox_impl.mail_fetcher import MockFetcher

async def get_spam_probability(ai_client, conversation_id, email_body):
    prompt = (
        "You are an AI that returns the probability that an email is spam. "
        "Respond with a number between 0 and 100.\n"
        f"Email: {email_body}"
    )
    response = await ai_client.send_message(conversation_id, prompt)
    # Try to extract a number from the response
    try:
        pct = float(response.content.strip().split()[0])
    except Exception:
        pct = 0.0
    return pct

async def main():
    # Email client setup
    email_client = get_email_client()
    # AI client setup (ensure OPENAI_API_KEY is set in your environment)
    ai_client = OpenAIClient()
    conversation = ai_client.create_conversation(
        title="Spam Detection",
        system_prompt="You are an AI that returns the probability that an email is spam. Respond with a number between 0 and 100."
    )

    # Populate inbox with mock messages
    fetcher = MockFetcher()
    fetcher.set_client(email_client)
    fetcher.fetch_messages(count=15)

    results = []
    for message in email_client.get_messages(folder="INBOX", limit=20):
        mail_id = message.id
        body = message.body
        pct_spam = await get_spam_probability(ai_client, conversation.id, body)
        results.append({'mail_id': mail_id, 'Pct_spam': pct_spam})

    output_csv = os.environ.get('SPAM_RESULTS_CSV', 'spam_results.csv')
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['mail_id', 'Pct_spam']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == '__main__':
    asyncio.run(main()) 
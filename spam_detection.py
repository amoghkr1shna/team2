#!/usr/bin/env python3
"""
Spam Detection Integration

This module integrates the email inbox client with the AI conversation client
to analyze emails for spam probability.
"""

import os
import sys
import asyncio
import csv
import argparse
import re
from typing import List, Dict, Optional, Union, Any

# Ensure imports work regardless of where script is run from
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_impl', 'src'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_api', 'src'))

from my_inbox_impl import get_client as get_email_client, ClientImpl
from my_inbox_impl.mail_fetcher import MockFetcher
from ai_conversation_client.providers.openai import OpenAIClient


class SpamDetector:
    """Integrates email client with AI to detect spam probability in emails."""
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: str = "gpt-3.5-turbo",
                 email_data_dir: Optional[str] = None):
        """
        Initialize the spam detector.
        
        Args:
            api_key: OpenAI API key (uses environment variable if None)
            model: AI model to use
            email_data_dir: Directory for email client data (uses default if None)
        """
        self.email_client = ClientImpl(data_dir=email_data_dir) if email_data_dir else get_email_client()
        self.ai_client = OpenAIClient(api_key=api_key, model=model)
        
        # Create a conversation with a specific system prompt for spam detection
        self.conversation = self.ai_client.create_conversation(
            title="Spam Detection",
            system_prompt="You are an AI that determines the probability that an email is spam. "
                         "Analyze the content, subject, and sender of emails. "
                         "Return ONLY a number between 0 and 100 representing the percentage "
                         "probability that the email is spam."
        )
    
    async def analyze_email(self, email_body: str) -> float:
        """
        Analyze an email to get its spam probability.
        
        Args:
            email_body: The content of the email
            
        Returns:
            A float between 0 and 100 representing spam probability
        """
        prompt = f"Email content: {email_body}\n\nBased on this email, what is the probability (0-100) that this is spam?"
        
        try:
            response = await self.ai_client.send_message(self.conversation.id, prompt)
            
            # Extract number from response using regex to find numbers, including those with percentage signs
            numbers = re.findall(r'\d+(?:\.\d+)?', response.content)
            if numbers:
                # Take the first number found
                pct = float(numbers[0])
                
                # Ensure it's in the 0-100 range
                pct = max(0, min(100, pct))
                
                return pct
            
            return 0.0  # No numbers found
            
        except Exception as e:
            # Log the error if desired
            print(f"Error analyzing email: {str(e)}")
            return 0.0  # Return conservative estimate on failure
    
    def populate_inbox_with_mock_data(self, count: int = 15) -> None:
        """
        Populate the inbox with mock emails for testing.
        
        Args:
            count: Number of mock emails to generate
        """
        fetcher = MockFetcher()
        fetcher.set_client(self.email_client)
        fetcher.fetch_messages(count=count)
    
    async def analyze_inbox(self, folder: str = "INBOX", limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Analyze all emails in the specified folder.
        
        Args:
            folder: Email folder to analyze
            limit: Maximum number of emails to analyze
            
        Returns:
            List of dictionaries with mail_id and Pct_spam
        """
        results = []
        
        for message in self.email_client.get_messages(folder=folder, limit=limit):
            mail_id = message.id
            body = message.body
            
            try:
                # Analyze the email with error handling
                pct_spam = await self.analyze_email(body)
                
                results.append({
                    'mail_id': mail_id, 
                    'Pct_spam': pct_spam
                })
            except Exception as e:
                # If analysis fails for any reason, use default value
                print(f"Error analyzing email {mail_id}: {str(e)}")
                results.append({
                    'mail_id': mail_id, 
                    'Pct_spam': 0.0
                })
        
        return results
    
    async def analyze_and_save(self, 
                             output_file: str = 'spam_results.csv',
                             folder: str = "INBOX", 
                             limit: Optional[int] = None) -> str:
        """
        Analyze inbox emails and save results to a CSV file.
        
        Args:
            output_file: Path to output CSV file
            folder: Email folder to analyze
            limit: Maximum number of emails to analyze
            
        Returns:
            Path to the created CSV file
        """
        results = await self.analyze_inbox(folder=folder, limit=limit)
        
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['mail_id', 'Pct_spam']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        
        return output_file


async def main(args: argparse.Namespace) -> int:
    """
    Main function to run the spam detection application.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code
    """
    try:
        # Create the spam detector
        detector = SpamDetector(api_key=args.api_key, model=args.model)
        
        # Populate inbox if requested
        if args.populate:
            detector.populate_inbox_with_mock_data(count=args.email_count)
        
        # Analyze emails and save to CSV
        output_file = await detector.analyze_and_save(
            output_file=args.output,
            folder=args.folder,
            limit=args.limit
        )
        
        print(f"Analysis complete. Results saved to: {output_file}")
        return 0
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze emails for spam probability')
    parser.add_argument('--output', default='spam_results.csv', help='Output CSV file path')
    parser.add_argument('--api-key', help='OpenAI API key (uses env var if not provided)')
    parser.add_argument('--model', default='gpt-3.5-turbo', help='AI model to use')
    parser.add_argument('--folder', default='INBOX', help='Email folder to analyze')
    parser.add_argument('--limit', type=int, help='Max number of emails to analyze')
    parser.add_argument('--populate', action='store_true', help='Populate inbox with mock data')
    parser.add_argument('--email-count', type=int, default=15, help='Number of mock emails to generate')
    
    args = parser.parse_args()
    
    exit_code = asyncio.run(main(args))
    sys.exit(exit_code) 
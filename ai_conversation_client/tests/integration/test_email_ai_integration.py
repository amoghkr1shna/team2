import os
import sys
import csv
import asyncio
import pytest
from unittest.mock import MagicMock, patch

# Add the email client implementation and API to sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_impl', 'src'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'external', 'email-client', 'my_inbox_api', 'src'))
sys.path.insert(0, REPO_ROOT)  # To import spam_detection

from my_inbox_impl import ClientImpl
from my_inbox_impl.mail_fetcher import MockFetcher
from ai_conversation_client.providers.openai import OpenAIClient
from spam_detection import SpamDetector

# Test fixtures and utility functions
class DummyEmailMessage:
    """Mock email message for testing."""
    def __init__(self, message_id, body, subject="Test Subject", from_="test@example.com", is_spam=False):
        self.id = message_id
        self.body = body
        self.subject = subject
        self.from_ = from_
        self._is_spam = is_spam
        self._is_read = False
        
    @property
    def is_read(self):
        return self._is_read
        
    def mark_as_read(self):
        self._is_read = True

class DummyClientImpl:
    """Mock email client implementation for testing."""
    def __init__(self, messages=None):
        self.messages = messages or []
        
    def get_messages(self, folder="INBOX", limit=None):
        msgs = self.messages[:limit] if limit else self.messages
        for msg in msgs:
            yield msg

class DummyAIClient:
    """Mock AI client for testing."""
    def __init__(self, response_content="42.0", should_fail=False):
        self.response_content = response_content
        self.should_fail = should_fail
        self.conversation_id = "test_conv_123"
    
    def create_conversation(self, title, system_prompt):
        class DummyConversation:
            def __init__(self, conv_id):
                self.id = conv_id
        return DummyConversation(self.conversation_id)
        
    async def send_message(self, conversation_id, prompt):
        if self.should_fail:
            raise ConnectionError("Simulated AI client failure")
            
        class DummyResponse:
            def __init__(self, content):
                self.content = content
        return DummyResponse(self.response_content)


@pytest.mark.asyncio
async def test_basic_spam_detection(tmp_path):
    """Test the basic spam detection flow with mock data."""
    # Setup: use a temp directory for the CSV output
    csv_path = tmp_path / "spam_results.csv"
    
    # Setup a SpamDetector with dummy implementations
    detector = SpamDetector(api_key="dummy_key", email_data_dir=str(tmp_path))
    
    # Replace the real clients with our dummies
    detector.email_client = DummyClientImpl([
        DummyEmailMessage("1", "Buy cheap watches!", is_spam=True),
        DummyEmailMessage("2", "Meeting tomorrow at 10am", is_spam=False),
        DummyEmailMessage("3", "You've won a million dollars!", is_spam=True)
    ])
    
    detector.ai_client = DummyAIClient("42.0")
    
    # Use the SpamDetector to analyze and save
    await detector.analyze_and_save(output_file=str(csv_path))
    
    # Assert CSV is correct
    with open(csv_path) as f:
        lines = f.readlines()
        assert lines[0].strip() == "mail_id,Pct_spam"
        assert len(lines) == 4  # header + 3 emails
        for line in lines[1:]:
            assert line.strip().endswith("42.0")


@pytest.mark.asyncio
async def test_analyze_empty_inbox(tmp_path):
    """Test analyzing an empty inbox."""
    csv_path = tmp_path / "spam_results.csv"
    
    detector = SpamDetector(api_key="dummy_key", email_data_dir=str(tmp_path))
    detector.email_client = DummyClientImpl([])  # Empty inbox
    detector.ai_client = DummyAIClient("42.0")
    
    await detector.analyze_and_save(output_file=str(csv_path))
    
    # Assert CSV has only the header
    with open(csv_path) as f:
        lines = f.readlines()
        assert lines[0].strip() == "mail_id,Pct_spam"
        assert len(lines) == 1  # only header, no emails


@pytest.mark.asyncio
async def test_analyze_email_handles_non_numeric_response(tmp_path):
    """Test that analyze_email can handle non-numeric AI responses."""
    detector = SpamDetector(api_key="dummy_key", email_data_dir=str(tmp_path))
    
    # AI client returns text that's not a number
    detector.ai_client = DummyAIClient("This email does not appear to be spam.")
    
    # Should return 0.0 for non-numeric responses
    result = await detector.analyze_email("Hello world")
    assert result == 0.0


@pytest.mark.asyncio
async def test_analyze_email_handles_percentage_response(tmp_path):
    """Test that analyze_email can handle responses with percentage signs."""
    detector = SpamDetector(api_key="dummy_key", email_data_dir=str(tmp_path))
    
    # AI client returns a percentage
    detector.ai_client = DummyAIClient("75% probability of spam")
    
    # Should extract the number 75
    result = await detector.analyze_email("Free money now!")
    assert result == 75.0


@pytest.mark.asyncio
async def test_analyze_inbox_with_ai_failure(tmp_path):
    """Test recovery when the AI client fails."""
    detector = SpamDetector(api_key="dummy_key", email_data_dir=str(tmp_path))
    
    detector.email_client = DummyClientImpl([
        DummyEmailMessage("1", "Test email")
    ])
    
    # Configure AI client to fail
    detector.ai_client = DummyAIClient(should_fail=True)
    
    # Should handle the error and return 0.0 as fallback
    results = await detector.analyze_inbox()
    assert len(results) == 1
    assert results[0]['mail_id'] == "1"
    assert results[0]['Pct_spam'] == 0.0


@pytest.mark.asyncio
async def test_analyze_large_inbox(tmp_path):
    """Test analyzing a large inbox."""
    csv_path = tmp_path / "spam_results.csv"
    
    # Create 100 test emails
    test_emails = [
        DummyEmailMessage(f"{i}", f"Test email {i}")
        for i in range(100)
    ]
    
    detector = SpamDetector(api_key="dummy_key", email_data_dir=str(tmp_path))
    detector.email_client = DummyClientImpl(test_emails)
    detector.ai_client = DummyAIClient("42.0")
    
    # Analyze with a limit of 10 emails
    await detector.analyze_and_save(output_file=str(csv_path), limit=10)
    
    # Assert CSV has only 10 emails + header
    with open(csv_path) as f:
        lines = f.readlines()
        assert len(lines) == 11  # header + 10 emails


@pytest.mark.asyncio
async def test_real_dependencies_mocked(tmp_path, monkeypatch):
    """Test with more realistic dependency mocking."""
    csv_path = tmp_path / "spam_results.csv"
    
    # Create a mock for ClientImpl that returns our test messages
    test_messages = [
        DummyEmailMessage("1", "Test email 1"),
        DummyEmailMessage("2", "Test email 2"),
        DummyEmailMessage("3", "Test email 3"),
    ]
    
    mock_client = MagicMock()
    mock_client.get_messages.return_value = test_messages
    
    # Create a mock for OpenAIClient
    mock_ai = MagicMock()
    mock_ai.create_conversation.return_value = MagicMock(id="test_conv_123")
    
    # Mock the async send_message method
    async def mock_send_message(*args, **kwargs):
        return MagicMock(content="42.0")
    
    mock_ai.send_message = mock_send_message
    
    # Path real implementations with mocks
    with patch('spam_detection.ClientImpl', return_value=mock_client), \
         patch('spam_detection.OpenAIClient', return_value=mock_ai):
        
        detector = SpamDetector(api_key="dummy_key", email_data_dir=str(tmp_path))
        await detector.analyze_and_save(output_file=str(csv_path))
    
    # Assert CSV has the expected content
    with open(csv_path) as f:
        lines = f.readlines()
        assert lines[0].strip() == "mail_id,Pct_spam"
        assert len(lines) == 4  # header + 3 emails 
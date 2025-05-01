import os
import sys
import subprocess
import csv
import tempfile

def test_spam_detection_e2e():
    """End-to-end test of the spam detection application."""
    # Find the repo root and script path
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    script_path = os.path.join(repo_root, 'spam_detection.py')
    env_path = os.path.join(repo_root, 'ai_conversation_client', '.env')

    # Use a temp directory for output
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'spam_results.csv')
        # Set environment so the script writes to our temp CSV
        env = os.environ.copy()
        
        # If a .env file exists, copy its contents to the environment
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        env[key] = value

        # Run the script from the repo root with --populate to generate mock data
        result = subprocess.run(
            [sys.executable, script_path, '--output', csv_path, '--populate', '--email-count', '5'],
            cwd=repo_root,
            env=env,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Check that the CSV was created
        assert os.path.exists(csv_path), "spam_results.csv was not created"

        # Check the CSV content
        with open(csv_path) as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert rows[0] == ['mail_id', 'Pct_spam']
            assert len(rows) > 1, "No emails were processed"


def test_spam_detection_e2e_with_custom_model():
    """Test the spam detection with a custom model parameter."""
    # Find the repo root and script path
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    script_path = os.path.join(repo_root, 'spam_detection.py')
    env_path = os.path.join(repo_root, 'ai_conversation_client', '.env')

    # Use a temp directory for output
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'spam_results.csv')
        # Set environment so the script writes to our temp CSV
        env = os.environ.copy()
        
        # If a .env file exists, copy its contents to the environment
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        env[key] = value

        # Run the script with a custom model parameter
        result = subprocess.run(
            [
                sys.executable, 
                script_path, 
                '--output', csv_path, 
                '--populate', 
                '--email-count', '3',
                '--model', 'gpt-4'  # Use a different model
            ],
            cwd=repo_root,
            env=env,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Check that the CSV was created
        assert os.path.exists(csv_path), "spam_results.csv was not created"


def test_spam_detection_e2e_with_limit():
    """Test the spam detection with a limit on the number of emails to process."""
    # Find the repo root and script path
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    script_path = os.path.join(repo_root, 'spam_detection.py')
    env_path = os.path.join(repo_root, 'ai_conversation_client', '.env')

    # Use a temp directory for output
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'spam_results.csv')
        env = os.environ.copy()

        # If a .env file exists, copy its contents to the environment
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        env[key] = value

        # Generate 10 mock emails but process only 2
        result = subprocess.run(
            [
                sys.executable, 
                script_path, 
                '--output', csv_path, 
                '--populate', 
                '--email-count', '10',
                '--limit', '2'  # Process only 2 emails
            ],
            cwd=repo_root,
            env=env,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Check that the CSV has only 3 rows (header + 2 emails)
        with open(csv_path) as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 3, f"Expected 3 rows (header + 2 emails), got {len(rows)}" 
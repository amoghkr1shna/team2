import os
import sys
import subprocess
import csv
import tempfile

def test_email_ai_e2e():
    # Find the repo root and script path
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    script_path = os.path.join(repo_root, 'integrate_email_ai.py')
    env_path = os.path.join(repo_root, 'ai_conversation_client', '.env')

    # Use a temp directory for output
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'spam_results.csv')
        # Set environment so the script writes to our temp CSV
        env = os.environ.copy()
        env['SPAM_RESULTS_CSV'] = csv_path
        if os.path.exists(env_path):
            env['DOTENV_PATH'] = env_path  # if you want to control dotenv loading

        # Run the script from the repo root
        result = subprocess.run(
            [sys.executable, script_path],
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
            assert len(rows) > 1  # At least one email processed 
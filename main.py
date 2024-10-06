import requests
import json
import os
from git import Repo
import jira_utils
import github_utils
import gemini_utils
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_API_VERSION = os.getenv("JIRA_API_VERSION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def main():
    # 1. Get latest Jira ticket
    ticket_data = jira_utils.get_latest_ticket()
    ticket_id = ticket_data['issues'][0]['key']
    ticket_name = ticket_data['issues'][0]['fields']['summary']
    repo_url = ticket_data['issues'][0]['fields']['customfield_13410'][0]

    # 2. Generate branch name using Gemini
    shortened_branch_name = gemini_utils.get_gemini_branch_name(ticket_name)
    branch_name = f"{ticket_id}-{shortened_branch_name}"

    # 3. Clone repository
    repo_path = os.path.join(os.getcwd(), "repo")
    if not os.path.exists(repo_path):
        github_utils.clone_repo(repo_url, repo_path)

    # 4. Checkout new branch and push
    repo = Repo(repo_path)
    repo.git.checkout("-b", branch_name)
    repo.git.push("--set-upstream", "origin", branch_name)

    # 5. Get repo data
    repo_data = gemini_utils.get_repo_data(repo_path)

    # 6. Generate code changes from Gemini
    code_changes = gemini_utils.get_gemini_code_changes(ticket_data, repo_data)

    # 7. Apply code changes (TODO)
    # ... (Parse code_changes and apply changes to the repo) ...

    # 8. Update Jira status
    jira_utils.update_jira_status(ticket_id, "In Development")

    # 9. Update Jira status to "Code Review" (TODO)
    # ... (After applying code changes) ...

if __name__ == "__main__":
    main()
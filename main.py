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

    # 5. Update Jira status
    jira_utils.update_jira_status(ticket_id, "In Development")

    # 6. Get repo data
    repo_data = gemini_utils.get_repo_data(repo_path)

    # 7. Generate code changes from Gemini
    code_changes = gemini_utils.get_gemini_code_changes(ticket_data, repo_data)

    # 8. Apply code changes
    code_changes = code_changes.strip()  # Remove leading/trailing whitespace

    if code_changes:
        # **1. Validation:** Check for valid JSON format
        try:
            code_changes_dict = json.loads(code_changes)
        except json.JSONDecodeError:
            print("Error: Unable to decode Gemini response. Please check the format.")
            return  # Exit if JSON is invalid

        # **2. Validation:** Check if the response contains any changes
        if not code_changes_dict:
            print("Info: Gemini did not provide any code changes.")
            return  # Exit if no changes are provided

        # **3. Apply changes**
        repo = Repo(repo_path)
        for file_path, file_content in code_changes_dict.items():
            # **4. Error Handling: Invalid File Paths**
            # Adjust file_path to be relative to the repository root if needed
            file_path = os.path.join(repo_path, file_path)

            try:
                # **5. Error Handling: Permission Errors**
                with open(file_path, "w") as f:
                    f.write(file_content)
                repo.git.add(file_path)  # Stage the changes
            except PermissionError as e:
                print(f"Error: Permission error while writing to file: {file_path}")
                print(f"Error message: {e}")
            except FileNotFoundError as e:
                print(f"Error: File not found: {file_path}")
                print(f"Error message: {e}")

        # **6. Error Handling: Commit and Push**
        try:
            repo.git.commit(m=f"Completed Jira ticket {ticket_id}")
            repo.git.push()
        except Exception as e:
            print(f"Error: Committing and pushing changes failed.")
            print(f"Error message: {e}")
            return  # Exit if commit/push fails

    # 9. Update Jira status to "Code Review" (TODO)
    jira_utils.update_jira_status(ticket_id, "Code Review")
    # ... (After applying code changes) ...

if __name__ == "__main__":
    main()
import os
import subprocess
import requests
import json
import base64
import gzip
from jira_utils import *
from github_utils import *
from gemini_utils import *
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def main():
    # Attempt to change to the git root
    git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
    if git_root:
        print(f"Changing to Git root directory: {git_root}")
        os.chdir(git_root)
    else:
        print("Error: Not inside a Git repository.")
        exit(1)

    # Get the most recent ticket info with the jira rest api
    ticket = get_latest_ticket()

    # Extract ticket information
    ticket_number = ticket['issues'][0]['key']
    ticket_name = ticket['issues'][0]['fields']['summary']
    description = ticket['issues'][0]['fields']['description']['content'][0]['content'][0]['text']
    acceptance_requirements = ticket['issues'][0]['fields']['customfield_12700']['content'][0]['content'][0]['text']

    print(f"Ticket Number: {ticket_number}")
    print(f"Ticket Name: {ticket_name}")
    print(f"Ticket Description: {description}")
    print(f"Acceptance Requirements: {acceptance_requirements}")

    # Generate branch name using Gemini
    ticket_name_short = generate_branch_name(ticket_name)

    # Trim whitespace from the ticket name
    ticket_name_short = ticket_name_short.strip()

    branch_name = f"{ticket_number}-{ticket_name_short}"

    print(f"Branch Name: {branch_name}")

    # Create a new branch
    create_branch(branch_name)

    # Push the new branch to the remote repository
    push_branch(branch_name)

    # Update ticket status to "In Progress"
    # update_jira_status(ticket_number, "In Progress")

    # Get the repo context and encode it
    repo_context = get_repo_context()

    # Send the prompt to Gemini with the cached content ID
    gemini_response = get_gemini_changes(ticket_name, description, acceptance_requirements, repo_context)

    # Parse and apply the Gemini response
    apply_gemini_changes(gemini_response)

    # Commit and push changes
    # commit_and_push()

    # Update ticket status to "Code Review"
    update_jira_status(ticket_number, "Code Review")

if __name__ == "__main__":
    main()
import requests
import json
import os
import git

# Replace with your actual API keys and credentials
JIRA_USERNAME = "your_jira_username"
JIRA_API_TOKEN = "your_jira_api_token"
JIRA_BASE_URL = "https://your-jira-instance.atlassian.net"
JIRA_API_VERSION = "rest/api/3"
GEMINI_API_KEY = "your_gemini_api_key"

def get_jira_ticket_details(ticket_id):
    """Fetches and parses Jira ticket details."""
    url = f"{JIRA_BASE_URL}/{JIRA_API_VERSION}/issue/{ticket_id}"
    headers = {"Authorization": f"Basic {JIRA_USERNAME}:{JIRA_API_TOKEN}", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_latest_ticket():
    """Gets the most recent Jira ticket for the current user."""
    url = f"{JIRA_BASE_URL}/{JIRA_API_VERSION}/search"
    params = {
        "jql": f"assignee=\"{JIRA_USERNAME}\" ORDER BY created DESC",
        "maxResults": 1
    }
    headers = {"Authorization": f"Basic {JIRA_USERNAME}:{JIRA_API_TOKEN}", "Accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_gemini_branch_name(ticket_name):
    """Generates a branch name using the Gemini API."""
    gemini_request = {
        "contents": [{"parts": [{"text": f"Write a valid git branch title (no more than 20 characters total) using this ticket name: '{ticket_name}'. Valid branch names are connected with dashes <branch-name>. The repository name can only contain ASCII letters, digits, and the characters ., -, and _. Do not include any other text in the repsonse."}]}],
        "safetySettings": [{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 20
        }
    }
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=gemini_request, params={"key": GEMINI_API_KEY})
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def get_repo_data(repo_path):
    """Generates a JSON string representing the repo's file content."""
    repo_data = "["
    for file in git.Repo(repo_path).git.ls_tree("-r", "--name-only", "HEAD").splitlines():
        content = git.Repo(repo_path).git.show("HEAD:" + file)
        repo_data += f'{{ "{file}": "{content}" }},'
    repo_data = repo_data[:-1]  # Remove trailing comma
    repo_data += "]"
    return repo_data

def get_gemini_code_changes(ticket_data, repo_data):
    """Sends a prompt to Gemini API for code generation based on ticket details and repo content."""
    ticket_name = ticket_data['issues'][0]['fields']['summary']
    description = ticket_data['issues'][0]['fields']['description']
    acceptance_requirements = ticket_data['issues'][0]['fields']['customfield_12700']
    comments = ticket_data['issues'][0]['fields']['comment']['comments']
    comments_text = "\n".join([comment['body'] for comment in comments if comment['body']])

    gemini_prompt = {
        "contents": [{"parts": [{"text": f"Using the ticket name, description, acceptance requirements, and comments, send git changes (with file names) to complete the Jira ticket. '{ticket_name}' -- '{description}' -- '{acceptance_requirements}' -- '{comments_text}' -- '{repo_data}'"}]}],
        "safetySettings": [{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=gemini_prompt, params={"key": GEMINI_API_KEY})
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def update_jira_status(ticket_id, status):
    """Updates the status of a Jira ticket."""
    url = f"{JIRA_BASE_URL}/{JIRA_API_VERSION}/issue/{ticket_id}"
    headers = {"Authorization": f"Basic {JIRA_USERNAME}:{JIRA_API_TOKEN}", "Content-Type": "application/json"}
    data = {"fields": {"status": {"name": status}}}
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

def main():
    """Main function to execute the workflow."""
    ticket_data = get_latest_ticket()
    ticket_id = ticket_data['issues'][0]['key']
    ticket_name = ticket_data['issues'][0]['fields']['summary']
    repo_url = ticket_data['issues'][0]['fields']['customfield_13410'][0]  # Assuming 'customfield_13410' holds the repo URL

    # Get branch name from Gemini
    shortened_branch_name = get_gemini_branch_name(ticket_name)
    branch_name = f"{ticket_id}-{shortened_branch_name}"

    # Clone the repository
    repo_path = os.path.join(os.getcwd(), "repo")  # Or choose a different location
    if not os.path.exists(repo_path):
        git.Repo.clone_from(repo_url, repo_path)

    # Checkout new branch and push
    repo = git.Repo(repo_path)
    repo.git.checkout("-b", branch_name)
    repo.git.push("--set-upstream", "origin", branch_name)

    # Get repo data
    repo_data = get_repo_data(repo_path)

    # Generate code changes from Gemini
    code_changes = get_gemini_code_changes(ticket_data, repo_data)

    # **TODO: Implement parsing and applying code changes to the repo based on the 'code_changes' response. 
    #  You'll need to extract file names and their content from the 'code_changes' response.
    #  Use 'repo.git.add()' to add files, 'repo.git.commit()' to commit, and 'repo.git.push()' to push.

    # Update Jira status to "In Development"
    update_jira_status(ticket_id, "In Development")

    # **TODO: After code changes are applied and pushed, update Jira status to "Code Review" 
    # update_jira_status(ticket_id, "Code Review")

if __name__ == "__main__":
    main()
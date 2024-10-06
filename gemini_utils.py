import requests
import json
from git import Repo
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
    for file in Repo(repo_path).git.ls_tree("-r", "--name-only", "HEAD").splitlines():
        content = Repo(repo_path).git.show("HEAD:" + file)
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
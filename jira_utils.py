import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_API_VERSION = os.getenv("JIRA_API_VERSION")

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

def update_jira_status(ticket_id, status):
    """Updates the status of a Jira ticket."""
    url = f"{JIRA_BASE_URL}/{JIRA_API_VERSION}/issue/{ticket_id}"
    headers = {"Authorization": f"Basic {JIRA_USERNAME}:{JIRA_API_TOKEN}", "Content-Type": "application/json"}
    data = {"fields": {"status": {"name": status}}}
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
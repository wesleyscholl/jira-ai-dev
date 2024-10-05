import requests
import config

class JiraClient:
    def __init__(self):
        self.base_url = config.JIRA_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {config.JIRA_API_TOKEN}",
            "Content-Type": "application/json"
        }

    def get_ticket(self, ticket_key):
        """Fetches a Jira ticket by its key."""
        url = f"{self.base_url}/issue/{ticket_key}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch ticket: {response.text}")
from jira_integration import JiraClient
from github_integration import GitHubClient

def main():
    ticket_key = input("Enter Jira ticket key: ")
    repo_url = input("Enter GitHub repository URL: ") 

    # 1. Fetch Jira Ticket
    jira = JiraClient()
    ticket_data = jira.get_ticket(ticket_key)

    # 2. Extract Relevant Information (for later use with LLM)
    ticket_summary = ticket_data['fields']['summary']
    ticket_description = ticket_data['fields']['description']
    # ... extract other details ...

    # 3. Clone the GitHub Repository 
    github = GitHubClient()
    github.clone_repo(repo_url, f"./repos/{ticket_key}") # Clone into a 'repos' folder

    # (Next steps: Branching, LLM interaction, code modification)

if __name__ == "__main__":
    main()
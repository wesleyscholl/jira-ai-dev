from git import Repo
import config

class GitHubClient:
    def __init__(self):
        self.api_token = config.GITHUB_API_TOKEN

    def clone_repo(self, repo_url, local_path):
        """Clones a GitHub repository to a local path."""
        try:
            Repo.clone_from(repo_url, local_path, credentials=(self.api_token, 'x-oauth-basic')) 
            print(f"Successfully cloned repository to: {local_path}")
        except Exception as e:
            raise Exception(f"Failed to clone repository: {e}")

    # Add more functions for branching, pushing, pull requests, etc. later
import os
from git import Repo

def clone_repo(repo_url, repo_path):
    """Clones a GitHub repository."""
    if not os.path.exists(repo_path):
        Repo.clone_from(repo_url, repo_path)
import os
import subprocess
from git import Repo
from git.exc import GitCommandError

def create_branch(branch_name):
    """Creates a new branch in the Git repository or checks out an existing one."""
    repo = Repo('.')
    current_branch = repo.active_branch.name

    if current_branch == branch_name:
        print(f"Already on branch '{branch_name}'")
        return

    try:
        # Try to create and checkout the new branch
        repo.git.checkout('-b', branch_name)
        print(f"Created and checked out new branch '{branch_name}'")
    except GitCommandError as e:
        if "already exists" in str(e):
            # Branch already exists, so just check it out
            repo.git.checkout(branch_name)
            print(f"Checked out existing branch '{branch_name}'")
        else:
            # Re-raise the exception if it's not about an existing branch
            raise

def push_branch(branch_name):
    """Pushes the new branch to the remote repository."""
    repo = Repo('.')
    repo.git.push('--set-upstream', 'origin', branch_name)

def commit_and_push():
    """Commits and pushes the changes to the remote repository."""
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Updated files based on Gemini\'s suggestions'], check=True)
    subprocess.run(['git', 'push'], check=True)
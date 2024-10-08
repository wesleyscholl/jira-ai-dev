# gemini_utils.py
import requests
import json
import subprocess
import base64
import gzip
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_branch_name(ticket_name):
    """Generates a branch name using the Gemini API."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Write a valid git branch title (no more than 20 characters total) using this ticket name: '{ticket_name}'. Valid branch names are connected with dashes <branch-name>. The repository name can only contain ASCII letters, digits, and the characters ., -, and _. Do not include any other text in the repsonse."
    response = model.generate_content(prompt)
    return response.text.strip()

def get_repo_context():
    """Generates a JSON string representing the repo's file content."""
    repo_context = {}
    for file in subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'HEAD']).decode().splitlines():
        try:
            content = subprocess.check_output(['git', 'show', 'HEAD:' + file]).decode()
            repo_context[file] = content
        except subprocess.CalledProcessError:
            # Handle the case where a file can't be read
            repo_context[file] = "Error: Unable to read file content"
        except UnicodeDecodeError:
            # Handle binary files
            repo_context[file] = "Binary file"
    return json.dumps(repo_context)

def get_gemini_changes(ticket_name, description, acceptance_requirements, repo_context):
    """Sends a prompt to Gemini API for code generation based on ticket details and repo content."""
    gemini_prompt = f"Using the ticket name, description, acceptance requirements, and repo data send git changes (with file names) to complete the Jira ticket in a structured json format. For each file, provide the file path (filepath), a diff that represents the changes, and the updated_content for the entire file. Do not use backticks like a code block. Ensuring all properties and values are quoted, respond with valid json in this format: {{changes: [{{filepath: file1.py, diff: git diff, updated_content: updates}}, {{filepath: file2.txt, diff: git diff, updated_content: updates}}]}}. -- Ticket name: '{ticket_name}' -- Ticket Description: '{description}' -- Acceptance Requirements: '{acceptance_requirements}' -- Repo Context: '{repo_context}' -- Do not include any other text in the repsonse."
    model = genai.GenerativeModel("gemini-1.5-pro-exp-0827")
    response = model.generate_content(gemini_prompt)
    return response.text

def apply_gemini_changes(gemini_response):
    """Parses and applies the code changes returned by Gemini."""
    changes_array = gemini_response
    changes_array = changes_array.strip()
    changes_array = changes_array.replace("```json\n", "")
    changes_array = changes_array.replace("```diff\n", "")
    changes_array = changes_array.replace("```", "")
    
    # Parse the JSON string, if errors occur, print the error message and fix the JSON string
    try:
        changes_array = json.loads(changes_array)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("Fixing JSON string...")
        changes_array = changes_array.replace("\n", "")
        changes_array = changes_array.replace("}{", "},{")
        changes_array = json.loads(changes_array)

    for change in changes_array["changes"]:
        print("Processing file changes...")
        print(change)
        filepath = change["filepath"]
        diff = change["diff"].replace("\\r\\n", "\n")  # Replace Windows-style line endings
        updated_content = change["updated_content"].replace("\\r\\n", "\n")  # Replace Windows-style line endings

        print(f"Processing file: {filepath}")

        # Check if the file exists
        if not os.path.exists(filepath):
            print(f"File does not exist: {filepath}. Creating it.")
            with open(filepath, "w") as f:
                pass  # Create an empty file

        # Apply the diff
        subprocess.run(["patch", "-p1", "--forward", "-i", "-"], input=diff.encode(), check=True)
        print("Patch applied successfully.")

        # Write the updated content to the file
        with open(filepath, "w") as f:
            f.write(updated_content)
        print(f"Updated content written to {filepath}")
        print("------------------------")
            
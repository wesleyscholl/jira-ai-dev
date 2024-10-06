# jira-ai-dev
Automating software development with AI 


## Agent workflow:

- Get Jira ticket information via API (JSON), using the Jira CLI, or other library.
- Parse the ticket description, acceptance criteria, name, github repo link, and other relevant details for development.
- Clone corresponding GitHub repo from Jira ticket info.
- Update Jira ticket status from "Open" to "In Development".
- Send the ticket number and title to the Gemini 1.5 Flash API to create the GitHub branch name, shorten it to 40 characters total including the ticket number (Example - "CRS-5437-Project-New-Feature-Description").
- Checkout new branch using the shortened branch title and push the new branch to origin (remote).
- Send ticket details and repo context to Gemini 1.5 Flash API with specific instructions.
- Specific instructions, to return file names to modify, full code for files to modify (with new code) to complete the Jira ticket. 
- The response structure and format needs to be predictable to parse and make file changes to the git repo.
- If necessary, query Gemini 1.5 Flash API multiple times until next action is certain, use memory and or local storage to store all requests and responses. 
- If the response is not in right format or structure, validation should send another query. 
- Use the response to make changes to the GitHub repo (adding new files, modifying existing files, etc.).
- Stage, commit, push, and create a pull request from the new branch into the "develop" branch.
- Update Jira ticket status from "In Development" to "Code Review".

## 1. Project Setup & Tools

Programming Language: Python is a great choice for its versatility and extensive libraries.

Libraries:

Jira API: https://developer.atlassian.com/cloud/jira/software/rest/api-group-issues - Use the official Jira API to interact with Jira tickets.

GitHub API: https://docs.github.com/en/rest - Use the GitHub API to manage repositories, branches, and commits.

Gemini 1.5 Flash API: https://developers.google.com/generativeai/reference/rest - Access the Gemini API for code generation and assistance.

Other Useful Libraries:

requests - for making HTTP requests to APIs.

json - for parsing JSON data.

os - for interacting with the operating system (file management).

git - for managing Git repositories.

Environment: Set up a virtual environment (e.g., using venv) to isolate your project dependencies.

## 2. Agent Logic

Jira Ticket Retrieval:

Utilize the Jira API to fetch ticket details by ID or other criteria.

Parse JSON data to extract the ticket's description, acceptance criteria, name, GitHub repo link, and other relevant information.

GitHub Repository Management:

Use the GitHub API to clone the repository specified in the Jira ticket.

Create a new branch using the Gemini 1.5 Flash API's response.

Check out the new branch and push it to the remote repository.

Gemini 1.5 Flash API Interactions:

Construct requests to the Gemini 1.5 Flash API, providing context from the Jira ticket and repository.

Specify clear instructions for code generation, including:

Desired file names and locations.

Specific code modifications (new code, additions, deletions).

Target programming language and framework.

Handle response validation and re-querying if the structure is incorrect.

Utilize memory or local storage to keep track of requests and responses for context.

Code Modification & Git Operations:

Parse the Gemini 1.5 Flash API response to identify file changes.

Apply the changes to the cloned repository (e.g., create new files, modify existing files).

Use the git library to stage changes, commit with a descriptive message, and push to the remote repository.

Create a pull request from the new branch to the "develop" branch on GitHub.

Jira Ticket Update:

Use the Jira API to update the ticket status to "In Development" and finally to "Code Review".

## 3. Code Structure

Modular Design: Break your code into functions for better organization and reusability.

Error Handling: Implement robust error handling mechanisms to catch exceptions and provide informative error messages.

Logging: Use a logging system (e.g., logging module) to track important events and debug issues.

## 4. Advanced Features (Optional)

Chat Interface: Consider adding a chat interface (e.g., using a chatbot library) to allow developers to interact with the agent more naturally.

Automated Testing: Integrate automated testing into your workflow to ensure the quality of the generated code.

Performance Optimization: Optimize your code for speed and efficiency, especially for frequent API calls.

Security: Implement security measures to protect your code and prevent unauthorized access to your systems.

## 5. Considerations

API Limits: Be aware of the limitations of the Jira, GitHub, and Gemini APIs (e.g., rate limits).

Gemini Model Usage: Remember to properly manage your Gemini API usage (e.g., token management, billing).

Training and Tuning: You may need to train the Gemini model further (e.g., fine-tuning) to improve code generation accuracy for your specific development context.

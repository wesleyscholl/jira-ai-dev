import unittest
import gemini_utils

class GeminiUtilsTest(unittest.TestCase):

    def test_get_gemini_branch_name(self):
        ticket_name = "My Ticket"
        branch_name = gemini_utils.get_gemini_branch_name(ticket_name)
        # Assert that the branch name is valid and meets your expected length/format
        self.assertTrue(len(branch_name) <= 20)
        self.assertIn("-", branch_name)

    def test_get_repo_data(self):
        # You'll need to provide a path to a test repository for this test
        repo_path = "path/to/your/test/repo" 
        repo_data = gemini_utils.get_repo_data(repo_path)
        self.assertTrue(isinstance(repo_data, str))
        # You can add more specific assertions based on the expected structure of repo_data

    def test_get_gemini_code_changes(self):
        # You'll need to provide sample ticket data and repository data for this test
        ticket_data = {
            "issues": [
                {
                    "key": "YOUR_TICKET_ID",
                    "fields": {
                        "summary": "Test Ticket",
                        # ... other fields
                    }
                }
            ]
        }
        repo_data = "[...]"  # Replace with sample repo data
        code_changes = gemini_utils.get_gemini_code_changes(ticket_data, repo_data)
        self.assertTrue(isinstance(code_changes, str))
        # You can add more specific assertions based on the expected structure of code_changes
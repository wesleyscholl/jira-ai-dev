import unittest
import jira_utils

# You will need to add your own test credentials to the .env file for these tests to work
class JiraUtilsTest(unittest.TestCase):

    def test_get_jira_ticket_details(self):
        # You'll need to replace this with a valid ticket ID from your Jira instance
        ticket_id = "YOUR_TICKET_ID"  
        ticket_data = jira_utils.get_jira_ticket_details(ticket_id)
        self.assertIsNotNone(ticket_data)
        self.assertIn("key", ticket_data)

    def test_get_latest_ticket(self):
        latest_ticket = jira_utils.get_latest_ticket()
        self.assertIsNotNone(latest_ticket)
        self.assertIn("issues", latest_ticket)

    def test_update_jira_status(self):
        # You'll need to replace this with a valid ticket ID and status 
        ticket_id = "YOUR_TICKET_ID"
        status = "In Progress"  
        jira_utils.update_jira_status(ticket_id, status)
        # You may want to add a check here to verify the status update was successful
        # This might require an additional API call to retrieve the ticket details after the update
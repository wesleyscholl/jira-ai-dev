import unittest
import github_utils
import os
import shutil

class GithubUtilsTest(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_repo_path = "test_repo"
        os.makedirs(self.test_repo_path, exist_ok=True)

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.test_repo_path)

    def test_clone_repo(self):
        # You'll need to replace this with a valid repository URL
        repo_url = "https://github.com/YOUR_USER/YOUR_REPOSITORY.git"  
        github_utils.clone_repo(repo_url, self.test_repo_path)
        self.assertTrue(os.path.exists(os.path.join(self.test_repo_path, ".git")))
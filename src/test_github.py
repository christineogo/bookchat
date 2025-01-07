#!/usr/bin/env python3

import unittest
from datetime import datetime
import os
import json
from github_manager import GitHubManager

class TestGitHubManager(unittest.TestCase):
    """Test cases for GitHub integration."""
    
    def setUp(self):
        """Set up test environment."""
        self.github_manager = GitHubManager()
        self.test_message_id = int(datetime.utcnow().timestamp())  # Use timestamp as unique ID
    
    def test_message_lifecycle(self):
        """Test creating, pushing, and retrieving a message."""
        # Create test message
        test_message = {
            "content": "Test message created at " + datetime.utcnow().isoformat(),
            "author": "Test Suite",
            "metadata": {
                "test_run": True,
                "type": "integration_test"
            }
        }
        
        try:
            # Test pushing message
            message_url = self.github_manager.push_message(test_message, self.test_message_id)
            self.assertIsNotNone(message_url)
            self.assertTrue(message_url.startswith("https://github.com/"))
            print(f"\nMessage pushed successfully to: {message_url}")
            
            # Test retrieving message
            retrieved_message = self.github_manager.get_message(self.test_message_id)
            self.assertIsNotNone(retrieved_message)
            self.assertEqual(retrieved_message["content"], test_message["content"])
            self.assertEqual(retrieved_message["author"], test_message["author"])
            self.assertEqual(retrieved_message["metadata"], test_message["metadata"])
            print("\nMessage retrieved successfully:")
            print(json.dumps(retrieved_message, indent=2))
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")
    
    def test_file_path_generation(self):
        """Test message file path generation."""
        path = self.github_manager._generate_message_path(self.test_message_id)
        
        # Path should follow pattern: messages/YYYY/MM/message_ID.json
        self.assertTrue(path.startswith("messages/"))
        self.assertTrue(path.endswith(f"message_{self.test_message_id}.json"))
        print(f"\nGenerated file path: {path}")
    
    def test_error_handling(self):
        """Test error handling for invalid operations."""
        # Test with invalid message ID
        retrieved_message = self.github_manager.get_message(-1)
        self.assertIsNone(retrieved_message)
        print("\nError handling test passed")

def run_tests():
    """Run the test suite."""
    print("\nRunning GitHub integration tests...")
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()

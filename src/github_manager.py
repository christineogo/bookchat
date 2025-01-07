#!/usr/bin/env python3

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
import base64
from dotenv import load_dotenv

class GitHubManager:
    """Manages GitHub operations for the messaging application."""
    
    def __init__(self):
        """Initialize GitHub manager with credentials from environment variables."""
        load_dotenv()
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('GITHUB_REPO')
        
        if not self.token or not self.repo_name:
            raise ValueError("GitHub token and repository name must be set in .env file")
        
        self.github = Github(self.token)
        self.repo = self.github.get_repo(self.repo_name)
        self.messages_dir = "messages"
    
    def _generate_message_path(self, message_id: int) -> str:
        """Generate a path for a message file.
        
        Args:
            message_id: Unique identifier for the message
            
        Returns:
            Path where the message should be stored in the repository
        """
        timestamp = datetime.utcnow()
        year_month = timestamp.strftime("%Y/%m")
        return f"{self.messages_dir}/{year_month}/message_{message_id}.json"
    
    def push_message(self, message_data: Dict[str, Any], message_id: int) -> str:
        """Push a message to GitHub.
        
        Args:
            message_data: Dictionary containing message data
            message_id: Unique identifier for the message
            
        Returns:
            The commit URL
        """
        try:
            # Add timestamp if not present
            if 'timestamp' not in message_data:
                message_data['timestamp'] = datetime.utcnow().isoformat()
            
            # Convert message data to JSON
            content = json.dumps(message_data, indent=2)
            
            # Generate file path
            file_path = self._generate_message_path(message_id)
            
            # Create commit message
            commit_message = f"Add message {message_id}"
            
            try:
                # Try to get existing file
                existing_file = self.repo.get_contents(file_path)
                # Update file if it exists
                self.repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha
                )
            except Exception:
                # Create new file if it doesn't exist
                self.repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content
                )
            
            return f"https://github.com/{self.repo_name}/blob/main/{file_path}"
            
        except Exception as e:
            raise Exception(f"Failed to push message to GitHub: {str(e)}")
    
    def get_message(self, message_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a message from GitHub.
        
        Args:
            message_id: ID of the message to retrieve
            
        Returns:
            Message data as a dictionary, or None if not found
        """
        try:
            # Search through year/month directories
            current_time = datetime.utcnow()
            year_month = current_time.strftime("%Y/%m")
            
            # Try to get the file from the current month
            file_path = self._generate_message_path(message_id)
            
            try:
                file_content = self.repo.get_contents(file_path)
                content = base64.b64decode(file_content.content).decode('utf-8')
                return json.loads(content)
            except Exception:
                # If not found, could implement a search through other months
                return None
                
        except Exception as e:
            print(f"Error retrieving message from GitHub: {str(e)}")
            return None

def test_github_integration():
    """Test the GitHub integration."""
    try:
        # Initialize the GitHub manager
        github_manager = GitHubManager()
        
        # Create a test message
        test_message = {
            "content": "Test message from GitHub integration",
            "author": "System Test",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Push the message
        message_url = github_manager.push_message(test_message, 1)
        print(f"Message pushed successfully. URL: {message_url}")
        
        # Retrieve the message
        retrieved_message = github_manager.get_message(1)
        if retrieved_message:
            print("Message retrieved successfully:")
            print(json.dumps(retrieved_message, indent=2))
        else:
            print("Failed to retrieve message")
            
    except Exception as e:
        print(f"Test failed: {str(e)}")

if __name__ == '__main__':
    test_github_integration()

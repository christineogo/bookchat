#!/usr/bin/env python3

import http.server
import socketserver
import json
import os
from urllib.parse import parse_qs, urlparse
from http import HTTPStatus
from typing import Dict, Any, Optional
from init_db import DatabaseManager
from github_manager import GitHubManager

class MessageHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the messaging application."""
    
    # Define the directory for static files
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

    def __init__(self, *args, **kwargs):
        """Initialize the handler with database and GitHub managers."""
        # Initialize managers
        self.db_manager = DatabaseManager()
        self.github_manager = GitHubManager()
        
        # Initialize the parent class
        super().__init__(*args, directory=self.static_dir, **kwargs)

    def do_GET(self) -> None:
        """Handle GET requests.
        
        Routes:
        / - Serves the main page
        /static/* - Serves static files
        /messages - Returns list of messages
        """
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve the main page
            self.serve_file('index.html', content_type='text/html')
        elif parsed_path.path == '/messages':
            try:
                # Get messages from database
                messages = self.db_manager.get_messages(limit=50)
                self.send_json_response({'messages': messages})
            except Exception as e:
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
        elif parsed_path.path.startswith('/static/'):
            # Handle static file requests
            super().do_GET()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Path not found")

    def do_POST(self) -> None:
        """Handle POST requests.
        
        Routes:
        /messages - Accept new messages
        """
        if self.path == '/messages':
            try:
                # Get the content length from headers
                content_length = int(self.headers.get('Content-Length', 0))
                # Read the request body
                post_data = self.rfile.read(content_length)
                message_data = json.loads(post_data.decode('utf-8'))
                
                # Validate message data
                if 'content' not in message_data:
                    raise ValueError("Message must contain 'content' field")
                
                # Save message to database
                message_id = self.db_manager.add_message(
                    content=message_data['content'],
                    author=message_data.get('author'),
                    git_commit_hash=None  # Will be updated after GitHub push
                )
                
                # Push to GitHub
                github_url = self.github_manager.push_message(message_data, message_id)
                
                # Send success response
                self.send_json_response({
                    'status': 'success',
                    'message': 'Message saved and pushed to GitHub',
                    'message_id': message_id,
                    'github_url': github_url
                })
            except json.JSONDecodeError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON data")
            except ValueError as e:
                self.send_error(HTTPStatus.BAD_REQUEST, str(e))
            except Exception as e:
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Path not found")

    def serve_file(self, filename: str, content_type: str) -> None:
        """Serve a file from the template directory."""
        try:
            file_path = os.path.join(self.template_dir, filename)
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND, f"File {filename} not found")

    def send_json_response(self, data: Dict[str, Any], status: int = 200) -> None:
        """Helper method to send JSON responses."""
        response = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

def run_server(port: int = 8081) -> None:
    """Run the HTTP server on the specified port."""
    with socketserver.TCPServer(("", port), MessageHandler) as httpd:
        print(f"Server running on port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()

if __name__ == '__main__':
    run_server()

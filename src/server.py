#!/usr/bin/env python3

import http.server
import socketserver
import json
import os
from urllib.parse import parse_qs, urlparse
from http import HTTPStatus
from typing import Dict, Any, Optional

class MessageHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the messaging application."""
    
    # Define the directory for static files
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

    def __init__(self, *args, **kwargs):
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
            # Return list of messages (to be implemented)
            self.send_json_response({'messages': []})
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
                
                # TODO: Implement message storage
                
                # Send success response
                self.send_json_response({
                    'status': 'success',
                    'message': 'Message received'
                })
            except json.JSONDecodeError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON data")
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

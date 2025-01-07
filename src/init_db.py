#!/usr/bin/env python3

import sqlite3
import os
from typing import Optional
from datetime import datetime

class DatabaseManager:
    """Manages database operations for the messaging application."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file. If None, uses default path.
        """
        if db_path is None:
            # Get the project root directory (parent of src)
            project_root = os.path.dirname(os.path.dirname(__file__))
            db_path = os.path.join(project_root, 'database', 'messages.db')
            
            # Ensure database directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        
    def init_db(self) -> None:
        """Initialize the database schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create messages table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    author TEXT,
                    git_commit_hash TEXT,
                    UNIQUE(id)
                )
                ''')
                
                # Create index on timestamp for faster querying
                cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_messages_timestamp 
                ON messages(timestamp)
                ''')
                
                conn.commit()
                print(f"Database initialized successfully at {self.db_path}")
                
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise
    
    def add_message(self, content: str, author: Optional[str] = None,
                   git_commit_hash: Optional[str] = None) -> int:
        """Add a new message to the database.
        
        Args:
            content: The message content
            author: Optional author name
            git_commit_hash: Optional Git commit hash for version tracking
            
        Returns:
            The ID of the newly inserted message
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                timestamp = datetime.utcnow().isoformat()
                
                cursor.execute('''
                INSERT INTO messages (content, timestamp, author, git_commit_hash)
                VALUES (?, ?, ?, ?)
                ''', (content, timestamp, author, git_commit_hash))
                
                conn.commit()
                return cursor.lastrowid
                
        except sqlite3.Error as e:
            print(f"Error adding message: {e}")
            raise
    
    def get_messages(self, limit: int = 100, offset: int = 0) -> list:
        """Retrieve messages from the database.
        
        Args:
            limit: Maximum number of messages to retrieve
            offset: Number of messages to skip
            
        Returns:
            List of message dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Configure connection to return dictionaries
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                SELECT id, content, timestamp, author, git_commit_hash
                FROM messages
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
                ''', (limit, offset))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            print(f"Error retrieving messages: {e}")
            raise

def init_database():
    """Initialize the database with the schema."""
    db_manager = DatabaseManager()
    db_manager.init_db()

if __name__ == '__main__':
    init_database()

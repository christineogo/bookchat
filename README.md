# Git-Backed Messaging Application

A simple web-based messaging application that uses Git as a backend storage system. Messages are stored and versioned using GitHub, with a lightweight Python backend and a clean HTML/CSS/JavaScript frontend.

## Features

- Real-time messaging interface
- Git-based message storage and versioning
- SQLite for local data caching
- Simple and clean web interface
- No heavy frameworks - pure Python, HTML, CSS, and JavaScript

## Prerequisites

- Python 3.8 or higher (make sure to use `python3` command or the appropriate Python 3 executable)
- Git installed and configured
- GitHub account with personal access token
- SQLite3

## Project Structure

```
bookchat/
├── README.md
├── .env                 # Environment variables (GitHub token, etc.)
├── .gitignore          # Git ignore file
├── static/             # Static files
│   ├── css/           # CSS styles
│   └── js/            # JavaScript files
├── templates/          # HTML templates
├── database/          # SQLite database
└── src/               # Python source code
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd bookchat
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   GITHUB_TOKEN=your_github_token
   GITHUB_REPO=your_repository_name
   ```

5. Initialize the database:
   ```bash
   python src/init_db.py
   ```

6. Run the application:
   ```bash
   python src/app.py
   ```

## Usage

1. Open your web browser and navigate to `http://localhost:8080`
2. Start sending and receiving messages
3. All messages are automatically versioned and stored in the configured GitHub repository

## Technical Details

- Backend: Python with built-in `http.server` module
- Database: SQLite3 for local caching
- Version Control: Git/GitHub API
- Frontend: Vanilla JavaScript, HTML5, CSS3

## Security Notes

- Store your GitHub token securely and never commit it to the repository
- The application uses HTTPS for GitHub API communication
- All sensitive data is stored in the `.env` file

## License

MIT License - Feel free to use, modify, and distribute this code.

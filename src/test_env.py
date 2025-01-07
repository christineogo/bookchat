#!/usr/bin/env python3

import os
from dotenv import load_dotenv

def test_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    print(f"Looking for .env file at: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            print("\nContents of .env file:")
            print(f.read())
    
    load_dotenv(dotenv_path=env_path)
    
    print("\nEnvironment variables:")
    print(f"GITHUB_TOKEN: {os.getenv('GITHUB_TOKEN')}")
    print(f"GITHUB_REPO: {os.getenv('GITHUB_REPO')}")

if __name__ == '__main__':
    test_env()

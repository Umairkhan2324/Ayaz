#!/usr/bin/env python
import sys
import warnings
import getpass
import os
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv

from ayaz.crew import Ayaz

# Load environment variables
load_dotenv()

# Get Watson configurations
MODEL = os.getenv('MODEL')
WATSONX_URL = os.getenv('WATSONX_URL')
WATSONX_APIKEY = os.getenv('WATSONX_APIKEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')

# Validate required environment variables
if not all([MODEL, WATSONX_URL, WATSONX_APIKEY, WATSONX_PROJECT_ID]):
    raise ValueError("Missing required Watson environment variables in .env file")

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def get_user_input() -> Dict[str, str]:
    """
    Get all required inputs from the user at runtime.
    Returns:
        Dict containing all user inputs and credentials
    """
    print("\n=== User Information ===")
    
    # Get email
    while True:
        email = input("Email: ").strip()
        if '@' in email and '.' in email:
            break
        print("Please enter a valid email address.")
    
    # Get password/auth token
    auth_token = getpass.getpass("Password/Auth Token: ").strip()
    
    # Get action
    print("\n=== Task Description ===")
    print("Examples of what you can ask:")
    print("- Schedule a team meeting for next Tuesday at 2 PM")
    print("- Process all unread emails from yesterday")
    print("- Create a project proposal document")
    print("- Update the Q4 budget spreadsheet")
    print("- Any other task you need help with")
    
    action = input("\nWhat would you like me to do? ").strip()
    
    # Get any additional context if needed
    print("\nAny additional details or requirements? (Optional, press Enter to skip)")
    context = input("Additional context: ").strip()
    
    return {
        "email": email,
        "auth_token": auth_token,
        "action": action,
        "context": context if context else None
    }

def run():
    """Run the crew with user inputs"""
    try:
        # Get user inputs
        user_inputs = get_user_input()
        
        # Prepare inputs for the crew
        inputs = {
            'current_year': str(datetime.now().year),
            'action': user_inputs['action'],
            'user_email': user_inputs['email'],
            'auth_token': user_inputs['auth_token']
        }
        
        # Add context if provided
        if user_inputs['context']:
            inputs['context'] = user_inputs['context']
        
        print("\n=== Starting Workflow ===")
        print(f"Processing request: {user_inputs['action']}")
        
        # Run the crew
        result = Ayaz().crew().kickoff(inputs=inputs)
        
        print("\n=== Workflow Complete ===")
        print(result)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print("\n=== Error ===")
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def train():
    """Train the crew with user inputs"""
    try:
        user_inputs = get_user_input()
        Ayaz().crew().train(
            n_iterations=int(sys.argv[2]),
            filename=sys.argv[3],
            inputs=user_inputs
        )
    except Exception as e:
        print(f"Training error: {str(e)}")
        sys.exit(1)

def replay():
    """Replay the crew with user inputs"""
    try:
        user_inputs = get_user_input()
        Ayaz().crew().replay(
            task_id=sys.argv[2],
            inputs=user_inputs
        )
    except Exception as e:
        print(f"Replay error: {str(e)}")
        sys.exit(1)

def test():
    """Test the crew with user inputs"""
    try:
        user_inputs = get_user_input()
        Ayaz().crew().test(
            n_iterations=int(sys.argv[2]),
            inputs=user_inputs
        )
    except Exception as e:
        print(f"Test error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "train":
            train()
        elif command == "replay":
            replay()
        elif command == "test":
            test()
        else:
            print(f"Unknown command: {command}")
    else:
        run()

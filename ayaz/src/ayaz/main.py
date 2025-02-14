#!/usr/bin/env python
import sys
import warnings
import getpass
from datetime import datetime
from typing import Dict, Optional

from ayaz.crew import Ayaz

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def get_user_credentials() -> Dict[str, str]:
    """
    Get user email and authentication details.
    Returns:
        Dict containing user credentials
    """
    print("\n=== User Authentication ===")
    email = input("Please enter your email: ").strip()
    password = getpass.getpass("Please enter your password: ").strip()
    
    return {
        "email": email,
        "auth_token": password  # In a real application, you might want to handle this more securely
    }

def get_user_action() -> str:
    """
    Get the action that the user wants to perform.
    Returns:
        String containing the user's requested action
    """
    print("\n=== Action Input ===")
    print("What would you like me to do? Examples:")
    print("1. Schedule a meeting with the team")
    print("2. Process emails from yesterday")
    print("3. Create a document for project X")
    print("4. Update the project spreadsheet")
    
    action = input("\nPlease describe your request: ").strip()
    return action

def run(credentials: Optional[Dict[str, str]] = None, action: Optional[str] = None):
    """
    Run the crew with the given credentials and action.
    
    Args:
        credentials: Optional dictionary containing user credentials
        action: Optional string containing the user's requested action
    """
    if credentials is None:
        credentials = get_user_credentials()
    
    if action is None:
        action = get_user_action()
    
    inputs = {
        'current_year': str(datetime.now().year),
        'action': action,
        'user_email': credentials['email'],
        'auth_token': credentials['auth_token']
    }
    
    print("\n=== Starting Workflow ===")
    print(f"Processing request: {action}")
    
    try:
        result = Ayaz().crew().kickoff(inputs=inputs)
        print("\n=== Workflow Complete ===")
        print(result)
    except Exception as e:
        print("\n=== Error ===")
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    credentials = get_user_credentials()
    action = get_user_action()
    
    inputs = {
        "action": action,
        "user_email": credentials['email'],
        "auth_token": credentials['auth_token']
    }
    
    try:
        Ayaz().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    credentials = get_user_credentials()
    action = get_user_action()
    
    try:
        Ayaz().crew().replay(task_id=sys.argv[1], action=action)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    credentials = get_user_credentials()
    action = get_user_action()
    
    inputs = {
        "action": action,
        "user_email": credentials['email'],
        "auth_token": credentials['auth_token']
    }
    
    try:
        Ayaz().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
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

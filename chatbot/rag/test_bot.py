# rag/test_bot.py
"""
Interactive testing script for the installation chatbot.
"""
import os
import sys
import json
import argparse

# Add parent directory to path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.bot import InstallationBot
from config import STRUCTURED_DIR

def interactive_chat(kb_path, user_id="test_user"):
    """
    Run an interactive chat session with the bot.
    
    Args:
        kb_path (str): Path to the knowledge base file
        user_id (str): User ID for session tracking
    """
    # Initialize the bot
    bot = InstallationBot(kb_path)
    
    # Print a welcome message
    print("\n" + "="*50)
    print("ProAxion Sensor Installation Assistant - Test Mode")
    print("="*50)
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'reset' to restart the conversation")
    print("="*50 + "\n")
    
    # Process the welcome message
    response = bot.process_message(user_id, "hello")
    print(f"🤖 Assistant: {response}\n")
    
    # Start the conversation loop
    while True:
        # Get user input
        user_input = input("👤 You: ")
        
        # Check for exit commands
        if user_input.lower() in ["exit", "quit"]:
            print("\nEnding chat session. Goodbye!")
            break
        
        # Process the message
        response = bot.process_message(user_id, user_input)
        
        # Print the response
        print(f"\n🤖 Assistant: {response}\n")

def list_knowledge_bases():
    """List available knowledge base files."""
    kb_files = []
    for filename in os.listdir(STRUCTURED_DIR):
        if filename.startswith("kb_") and filename.endswith(".json"):
            kb_files.append(os.path.join(STRUCTURED_DIR, filename))
    
    return kb_files

def main():
    """Main function to parse arguments and start the chatbot."""
    parser = argparse.ArgumentParser(description="Interactive Installation Chatbot Tester")
    
    # Add arguments
    parser.add_argument("--kb", help="Knowledge base file path")
    parser.add_argument("--user", default="test_user", help="User ID for session")
    parser.add_argument("--list", action="store_true", help="List available knowledge bases")
    
    # Parse arguments
    args = parser.parse_args()
    
    # List knowledge bases if requested
    if args.list:
        kb_files = list_knowledge_bases()
        if kb_files:
            print("\nAvailable knowledge bases:")
            for i, kb_file in enumerate(kb_files, 1):
                # Try to get the title from the file
                try:
                    with open(kb_file, 'r') as f:
                        data = json.load(f)
                        title = data.get('title', 'Untitled')
                except Exception:
                    title = "Could not load"
                
                print(f"{i}. {os.path.basename(kb_file)} - {title}")
        else:
            print("No knowledge base files found. Please run the document processor first.")
        return
    
    # Get knowledge base path
    kb_path = args.kb
    if not kb_path:
        # Find the latest knowledge base
        kb_files = list_knowledge_bases()
        if kb_files:
            kb_path = max(kb_files, key=os.path.getmtime)
            print(f"Using latest knowledge base: {os.path.basename(kb_path)}")
        else:
            print("No knowledge base files found. Please run the document processor first.")
            return
    
    # Start interactive chat
    interactive_chat(kb_path, args.user)

if __name__ == "__main__":
    main()
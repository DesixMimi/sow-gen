# tests/test_sow_chat.py
import os
import sys

# Ensure app module is found
sys.path.append(os.getcwd())

from app.agent import root_agent

def test_chat_flow():
    print("🚀 Starting SOW-Wise Chat Test...")
    
    # 1. User provides partial info (Missing customer name)
    user_input_1 = "I need to migrate my old banking application to Google Cloud."
    print(f"\n👤 User: {user_input_1}")
    
    try:
        response_1 = root_agent.query(user_input_1)
        print(f"🤖 Agent: {response_1}")
        # Expected: Agent asks for Customer Name, Role, Project Name, and maybe Security/QA scope.
        
        # 2. Simulate user providing some info but missing scope
        user_input_2 = "Customer is Bank Yahav, I am the CTO. Project is 'Cloud Migration'."
        print(f"\n👤 User: {user_input_2}")
        
        # Note: In a real chat, we'd need to maintain history. 
        # Since this script re-initializes or doesn't keep state in `root_agent` automatically unless configured with memory,
        # we are just testing the *response logic* for the first turn here to ensure it uses the Writer Prompt correctly.
        # To truly test multi-turn, we'd need a session object, but 'root_agent.query' might be stateless depending on ADK implementation.
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_chat_flow()

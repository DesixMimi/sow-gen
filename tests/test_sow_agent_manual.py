# test_sow_agent.py
import os
import sys

# Ensure app module is found
sys.path.append(os.getcwd())

from app.agent import root_agent

def test_agent():
    print("🚀 Starting SOW-Wise Agent Test...")
    user_input = "I need to migrate my old banking application to Google Cloud. It needs strict security."
    
    try:
        # standard ADK agent usually has .query() or .generate()
        # We'll try .query() first as it's common in ADK
        response = root_agent.query(user_input)
        
        print("\n✅ Agent Response:")
        print(response)
        
    except AttributeError:
        print("❌ 'query' method not found. Trying 'generate'...")
        try:
            response = root_agent.generate(user_input)
            print("\n✅ Agent Response:")
            print(response.text if hasattr(response, 'text') else response)
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"Agent methods: {dir(root_agent)}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    test_agent()

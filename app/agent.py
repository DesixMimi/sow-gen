import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from zoneinfo import ZoneInfo

# Import our custom components
# Import our custom components
from app.sow_generator import generate_sow
from app.prompts import SYSTEM_INSTRUCTION, ARCHITECTURE_INSTRUCTION

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# --- Architecture Agent Definition ---
arch_agent = Agent(
    name="architecture_agent",
    model=Gemini(
        model="gemini-3-flash-preview", 
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=ARCHITECTURE_INSTRUCTION,
)

def consult_architecture_agent(project_details: str) -> str:
    """
    Generates detailed architecture diagram instructions based on the project details.
    Call this tool AFTER the SOW is generated and the user agrees to the scope.
    
    Args:
        project_details: A summary of the project, including technical components and flow.
        
    Returns:
        A detailed text description of the architecture diagram instructions.
    """
    print(f"🎨 Calling Architecture Agent for: {project_details[:50]}...")
    response = arch_agent.query(project_details)
    return response.text if hasattr(response, 'text') else str(response)

# --- Main SOW-Wise Agent Definition ---
root_agent = Agent(
    name="sow_wise_agent",
    model=Gemini(
        model="gemini-3-flash-preview", 
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[generate_sow, consult_architecture_agent],
)

app = App(
    root_agent=root_agent,
    name="sow_wise_app",
)

import sys
import os

# Add the current directory to sys.path so we can import app modules if needed
sys.path.append(os.getcwd())

from app.sow_generator import generate_sow

phases = [
    {"name": "Phase 1 - Discovery", "description": "Requirements gathering", "role": "Analyst", "hours": 10, "rate": 100},
    {"name": "Phase 2 - Development", "description": "Coding the solution", "role": "Developer", "hours": 40, "rate": 150}
]

maintenance = [
    {"description": "Monthly Server upkeep", "cost": 500},
    {"description": "Support hours", "cost": 1000}
]

output = generate_sow(
    customer_name="Test Customer",
    customer_role="CEO",
    customer_company="Test Company",
    project_name="Test Project",
    project_description="This is a test project to verify the SOW generator.",
    phases=phases,
    maintenance_items=maintenance,
    output_path="test_sow.html"
)

print(output)

import os
import datetime
from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Any

def generate_sow(
    customer_name: str,
    customer_role: str,
    customer_company: str,
    project_name: str,
    project_description: str,
    phases: List[Dict[str, Any]],
    maintenance_items: List[Dict[str, Any]] = None,
    output_path: str = "output_sow.html"
) -> str:
    """
    Generates a SOW HTML document.
    
    Args:
        customer_name: Name of the customer.
        customer_role: Role of the customer.
        customer_company: Name of the customer's company.
        project_name: Name of the project.
        project_description: Description of the project.
        phases: List of phases. Each phase is a dict with:
            - name
            - description
            - role
            - hours
            - rate
        maintenance_items: List of maintenance items. Each item is a dict with:
            - description
            - cost
        output_path: Path to save the generated HTML.
    
    Returns:
        The path to the generated file.
    """
    
    # Calculate totals for phases
    total_hours = 0
    total_cost = 0
    
    processed_phases = []
    for phase in phases:
        hours = float(phase.get('hours', 0))
        rate = float(phase.get('rate', 0))
        total = hours * rate
        
        total_hours += hours
        total_cost += total
        
        processed_phases.append({
            **phase,
            'hours': f"{hours:g}",
            'rate': f"{rate:g}",
            'total': f"{total:,.0f}"
        })
        
    # Calculate totals for maintenance
    total_monthly_cost = 0
    processed_maintenance = []
    if maintenance_items:
        for item in maintenance_items:
            cost = float(item.get('cost', 0))
            total_monthly_cost += cost
            processed_maintenance.append(item)
    
    today = datetime.date.today().strftime("%d/%m/%Y")
    
    data = {
        'date': today,
        'customer_name': customer_name,
        'customer_role': customer_role,
        'customer_company': customer_company,
        'project_name': project_name,
        'project_description': project_description,
        'phases': processed_phases,
        'total_hours': f"{total_hours:g}",
        'total_cost': f"{total_cost:,.0f}",
        'maintenance_items': processed_maintenance,
        'total_monthly_cost': f"{total_monthly_cost:,.0f}"
    }
    
    # Setup Jinja2 environment
    # Assuming templates are in ../templates relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('sow_template.html')
    
    rendered_html = template.render(data)
    

    # Save to file
    # If output_path is relative, make it relative to base_dir
    if not os.path.isabs(output_path):
        output_path = os.path.join(base_dir, output_path)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
    if output_path.endswith('.docx'):
        try:
            import pypandoc
            # Use convert_text to avoid issues with glob and special characters in paths
            pypandoc.convert_text(rendered_html, 'docx', format='html', outputfile=str(output_path))
        except ImportError:
            return "Error: pypandoc not installed. Cannot generate DOCX."
        except Exception as e:
            return f"Error generating DOCX: {str(e)}"
            
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
    return f"SOW generated at: {output_path}"

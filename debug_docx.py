import sys
import os
sys.path.append(os.getcwd())
try:
    from app.sow_generator import generate_sow
    # Added Hebrew test data to verify RTL
    result = generate_sow(
        'ישראל ישראלי', 'מנכ״ל', 'חברה בע״מ', 
        'מיגרציה לענן', 'תיאור הפרויקט בעברית לקוח יקר', 
        [{'name': 'שלב א', 'description': 'אפיון', 'role': 'ארכיטקט', 'hours': 10, 'rate': 100}], 
        [{'description': 'תמיכה חודשית', 'cost': 500}],
        output_path='test_rtl_output.docx'
    )
    print(f"Result: {result}")
except Exception as e:
    print(f"Script Error: {e}")

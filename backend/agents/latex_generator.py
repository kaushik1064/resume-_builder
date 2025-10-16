from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import re
import os

def sanitize_for_latex(text):
    """
    Sanitize text for LaTeX by escaping special characters
    """
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    
    # Replace problematic Unicode characters
    replacements = {
        'â€"': '--',  # en-dash
        'â€"': '---',  # em-dash
        ''': "'",   # left single quote
        ''': "'",   # right single quote
        '"': "``",  # left double quote
        '"': "''",  # right double quote
        'â€¦': '...',  # ellipsis
        'â‚¬': r'\euro',
        'Â£': r'\pounds',
        'Â°': r'$^\circ$',
        '—': '--',  # em dash
        '–': '--',  # en dash
        '"': "``",
        '"': "''",
        ''': "'",
        ''': "'",
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Escape LaTeX special characters (but not if already escaped)
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    
    # Build result character by character to avoid double-escaping
    result = []
    i = 0
    while i < len(text):
        # Check if already escaped
        if i > 0 and text[i-1] == '\\':
            result.append(text[i])
            i += 1
            continue
        
        # Check for special characters
        char = text[i]
        if char in special_chars:
            result.append(special_chars[char])
        else:
            result.append(char)
        i += 1
    
    return ''.join(result)

def sanitize_dict(data):
    """
    Recursively sanitize all strings in a dictionary
    """
    if isinstance(data, dict):
        return {k: sanitize_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_dict(item) for item in data]
    elif isinstance(data, str):
        return sanitize_for_latex(data)
    else:
        return data

def validate_user_info(user_info):
    """
    Validate and ensure user_info has proper structure with defaults
    """
    if not isinstance(user_info, dict):
        user_info = {}
    
    # Set required defaults
    defaults = {
        'name': 'YOUR NAME',
        'email': 'email@example.com',
        'phone': '+00-0000000000',
        'title': 'Job Title',
        'location': '',
        'linkedin': '',
        'github': '',
        'education': [],
        'experience': [],
        'projects': [],
        'certifications': [],
        'skills': []
    }
    
    # Merge with defaults
    for key, default_value in defaults.items():
        if key not in user_info or user_info[key] is None:
            user_info[key] = default_value
        # Ensure lists are actually lists
        elif isinstance(default_value, list) and not isinstance(user_info[key], list):
            user_info[key] = default_value
    
    # Validate nested structures
    if user_info['education']:
        for edu in user_info['education']:
            if not isinstance(edu, dict):
                continue
            edu.setdefault('degree', '')
            edu.setdefault('specialization', '')
            edu.setdefault('institute', '')
            edu.setdefault('year', '')
            edu.setdefault('gpa', '')
    
    if user_info['experience']:
        for exp in user_info['experience']:
            if not isinstance(exp, dict):
                continue
            exp.setdefault('title', '')
            exp.setdefault('company', '')
            exp.setdefault('duration', '')
            exp.setdefault('details', [])
    
    if user_info['projects']:
        for proj in user_info['projects']:
            if not isinstance(proj, dict):
                continue
            proj.setdefault('name', '')
            proj.setdefault('link', '')
            proj.setdefault('duration', '')
            proj.setdefault('details', [])
    
    if user_info['certifications']:
        for cert in user_info['certifications']:
            if not isinstance(cert, dict):
                continue
            cert.setdefault('name', '')
            cert.setdefault('issuer', '')
            cert.setdefault('date', '')
            cert.setdefault('details', [])
    
    if user_info['skills']:
        for skill in user_info['skills']:
            if not isinstance(skill, dict):
                continue
            skill.setdefault('category', '')
            skill.setdefault('items', '')
    
    return user_info

def fill_latex_resume(user_info, output_path="resume.tex"):
    """
    Generate LaTeX resume from user info with proper sanitization and validation
    """
    try:
        # Validate input structure
        user_info = validate_user_info(user_info)
        
        # Sanitize all input data
        sanitized_info = sanitize_dict(user_info)
        
        # Find template
        template_path = Path(__file__).parent.parent / "templates"
        
        # Also check if templates is in current directory (for Colab)
        if not template_path.exists():
            template_path = Path("templates")
        
        if not template_path.exists():
            raise FileNotFoundError(
                f"Templates directory not found. Checked: {template_path.absolute()}"
            )
        
        template_file = template_path / "latex_template.tex"
        if not template_file.exists():
            raise FileNotFoundError(
                f"Template file not found: {template_file.absolute()}"
            )
        
        print(f"✓ Using template: {template_file}")
        
        # Load and render template
        env = Environment(loader=FileSystemLoader(str(template_path)))
        template = env.get_template("latex_template.tex")
        
        tex_code = template.render(**sanitized_info)
        
        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(tex_code)
        
        print(f"✓ LaTeX template rendered to {output_path}")
        print(f"  File size: {output_path.stat().st_size} bytes")
        
        return tex_code, str(output_path)
    
    except Exception as e:
        print(f"✗ Error in fill_latex_resume: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
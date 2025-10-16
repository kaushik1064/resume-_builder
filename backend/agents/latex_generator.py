from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import re

def sanitize_for_latex(text):
    """
    Sanitize text for LaTeX by escaping special characters
    """
    if not isinstance(text, str):
        return text
    
    # Replace problematic Unicode characters
    replacements = {
        '–': '--',  # en-dash
        '—': '---',  # em-dash
        ''': "'",   # left single quote
        ''': "'",   # right single quote
        '"': "``",  # left double quote
        '"': "''",  # right double quote
        '…': '...',  # ellipsis
        '€': r'\euro',
        '£': r'\pounds',
        '°': r'$^\circ$',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Escape LaTeX special characters
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
    
    # Don't escape if already escaped
    for old, new in special_chars.items():
        text = re.sub(f'(?<!\\\\){re.escape(old)}', new, text)
    
    return text

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

def fill_latex_resume(user_info, output_path="resume.tex"):
    """
    Generate LaTeX resume from user info with proper sanitization
    """
    # Sanitize all input data
    sanitized_info = sanitize_dict(user_info)
    
    template_path = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_path)))
    template = env.get_template("latex_template.tex")
    
    tex_code = template.render(**sanitized_info)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tex_code)
    
    return tex_code, output_path
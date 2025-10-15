# LaTeX resume generator logic here
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def fill_latex_resume(user_info, output_path="resume.tex"):
    template_path = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_path)))
    template = env.get_template("latex_template.tex")
    tex_code = template.render(**user_info)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tex_code)
    return tex_code, output_path

import os

# Define the project structure
structure = {
    "resume-ai-app": {
        "backend": {
            "agents": {
                "__init__.py": "",
                "dynamic_scraper.py": "# Dynamic scraping logic here\n",
                "job_matcher.py": "# Job matching logic here\n",
                "latex_generator.py": "# LaTeX resume generator logic here\n"
            },
            "utils": {
                "__init__.py": "",
                "pdf_generator.py": "# PDF generation utilities\n"
            },
            "templates": {
                "latex_template.tex": "% Your LaTeX resume template here\n"
            },
            "temp": {},  # created at runtime
            "main.py": "# Entry point for backend FastAPI or Flask app\n",
            "requirements.txt": "# List your backend dependencies here\n"
        },
        "frontend": {
            "pages": {
                "index.tsx": "// Next.js main page\n"
            },
            "components": {
                "PlaceholdersAndVanishInput.tsx": "// Component for animated input\n",
                "InteractiveGradientBackground.tsx": "// Background effect component\n"
            },
            "styles": {
                "globals.css": "/* Global CSS styles */\n"
            },
            "public": {},
            "package.json": "{\n  \"name\": \"frontend\",\n  \"version\": \"1.0.0\"\n}\n",
            "next.config.js": "// Next.js configuration\n"
        }
    }
}


def create_structure(base_path, structure_dict):
    """Recursively create folders and files based on the given structure."""
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


# Run the structure creation
base_dir = os.getcwd()  # current working directory
create_structure(base_dir, structure)

print("✅ Project structure created successfully!")

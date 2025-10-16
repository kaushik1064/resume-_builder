# Job matching logic here
import google.generativeai as genai
import os
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

def match_resume_to_job(user_resume_text, jobdesc_text):
    prompt = (
        "Given the following RESUME and JOB DESCRIPTION, extract and optimize resume fields to match the job requirements. "
        "Return ONLY valid JSON with this EXACT structure:\n"
        "{\n"
        '  "name": "Full Name",\n'
        '  "email": "email@example.com",\n'
        '  "phone": "+1-234-567-8900",\n'
        '  "title": "Job Title/Role",\n'
        '  "location": "City, Country",\n'
        '  "linkedin": "linkedin.com/in/profile",\n'
        '  "github": "github.com/username",\n'
        '  "education": [{"degree": "B.Tech", "specialization": "Computer Science", "institute": "University Name", "year": "2022", "gpa": "8.5"}],\n'
        '  "experience": [{"title": "Role Title", "company": "Company Name", "duration": "Jan 2023-Present", "details": ["Achievement 1", "Achievement 2"]}],\n'
        '  "projects": [{"name": "Project Name", "link": "github.com/link", "duration": "Jan 2024", "details": ["Detail 1", "Detail 2"]}],\n'
        '  "certifications": [{"name": "Cert Name", "issuer": "Issuer", "date": "2023", "details": ["Detail"]}],\n'
        '  "skills": [{"category": "Languages", "items": "Python, Java"}, {"category": "Tools", "items": "Docker, Git"}]\n'
        "}\n\n"
        "RESUME:\n" + (user_resume_text or "") +
        "\n\nJOB DESCRIPTION:\n" + (jobdesc_text or "") +
        "\n\nReturn ONLY the JSON, no markdown, no explanation."
    )
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)
    import json
    try:
        # Remove markdown code blocks if present
        text = resp.text.strip()
        if text.startswith('```'):
            text = re.sub(r'^```(?:json)?\n', '', text)
            text = re.sub(r'\n```$', '', text)
        return json.loads(text)
    except Exception as e:
        print(f"JSON parse error: {e}")
        block = re.search(r'\{.*\}', resp.text, re.DOTALL)
        if block:
            try:
                return json.loads(block.group())
            except:
                pass
        # Return default structure if parsing fails
        return {
            "name": "Name Not Found",
            "email": "email@example.com",
            "phone": "+00-0000000000",
            "title": "Job Title",
            "education": [],
            "experience": [],
            "projects": [],
            "skills": []
        }

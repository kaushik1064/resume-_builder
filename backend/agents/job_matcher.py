# Job matching logic here
import google.generativeai as genai
import os
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

def match_resume_to_job(user_resume_text, jobdesc_text):
    prompt = (
        "Given the following RESUME and JOB DESCRIPTION, extract resume fields (name, email, phone, education, experience, projects, skills, summary) and rewrite them to match the job requirements. "
        "If data is missing, infer or omit. Output a JSON with each section, optimizing for ATS."
        "\n\nRESUME:\n" + (user_resume_text or "") +
        "\n\nJOB DESCRIPTION:\n" + (jobdesc_text or "") +
        "\n\nOutput JSON only."
    )
    model = genai.GenerativeModel("gemini-pro")
    resp = model.generate_content(prompt)
    import json
    try:
        return json.loads(resp.text)
    except Exception:
        block = re.search(r'\{.*\}', resp.text, re.DOTALL)
        return json.loads(block.group()) if block else {}

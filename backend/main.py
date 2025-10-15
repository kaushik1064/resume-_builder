import sys
import asyncio

# Fix for Windows + Playwright + asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import shutil
import os
import tempfile
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from agents.dynamic_scraper import process_sources
from agents.job_matcher import match_resume_to_job
from agents.latex_generator import fill_latex_resume
from utils.pdf_generator import tex_to_pdf
from starlette.responses import FileResponse

TEMP = "./temp"
os.makedirs(TEMP, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process/")
async def process_resume(
    job_urls: str = Form(""),
    basic_details: str = Form(""),
    resume_file: UploadFile = None,
):
    sources = {'urls': [], 'pdfs': [], 'txts': []}
    if job_urls:
        sources['urls'] = [j.strip() for j in job_urls.split(",") if j.strip()]
    temp_fp = ""
    if resume_file:
        suffix = resume_file.filename.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(suffix=f'.{suffix}', delete=False) as tmpf:
            tmpf.write(await resume_file.read())
            temp_fp = tmpf.name
        if suffix == "pdf":
            sources['pdfs'].append(temp_fp)
        elif suffix == "txt":
            sources['txts'].append(temp_fp)
    elif basic_details.strip():
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as tmpf:
            tmpf.write(basic_details)
            sources['txts'].append(tmpf.name)
    
    results = await process_sources(sources)
    resume_text = ""
    job_desc_text = ""
    if results.get('pdfs'):
        resume_text = next(iter(results['pdfs'].values()))
    elif results.get('txts'):
        resume_text = next(iter(results['txts'].values()))
    if results.get('urls'):
        job_desc_text = next(iter(results['urls'].values()))
    
    ai_resume = match_resume_to_job(resume_text, job_desc_text)
    tex_code, tex_fp = fill_latex_resume(ai_resume, output_path=os.path.join(TEMP, "resume.tex"))
    pdf_fp = tex_to_pdf(tex_fp, TEMP)
    return FileResponse(str(pdf_fp), media_type="application/pdf", filename="resume.pdf")

@app.get("/")
def alive():
    return {"hello": "world"}

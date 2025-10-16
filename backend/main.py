import sys
import asyncio

# Fix for Windows + Playwright + asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import shutil
import os
import tempfile
import traceback
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.dynamic_scraper import process_sources
from agents.job_matcher import match_resume_to_job
from agents.latex_generator import fill_latex_resume
from utils.pdf_generator import tex_to_pdf
from starlette.responses import FileResponse, JSONResponse

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
    try:
        print("=" * 60)
        print("Starting resume processing...")
        print("=" * 60)
        
        sources = {'urls': [], 'pdfs': [], 'txts': []}
        
        # Parse job URLs
        if job_urls:
            sources['urls'] = [j.strip() for j in job_urls.split(",") if j.strip()]
            print(f"✓ Job URLs: {sources['urls']}")
        
        # Handle resume file upload
        temp_fp = ""
        if resume_file:
            suffix = resume_file.filename.split(".")[-1].lower()
            with tempfile.NamedTemporaryFile(suffix=f'.{suffix}', delete=False) as tmpf:
                tmpf.write(await resume_file.read())
                temp_fp = tmpf.name
            
            if suffix == "pdf":
                sources['pdfs'].append(temp_fp)
                print(f"✓ Resume PDF uploaded: {temp_fp}")
            elif suffix == "txt":
                sources['txts'].append(temp_fp)
                print(f"✓ Resume TXT uploaded: {temp_fp}")
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")
        
        # Handle basic details as text
        elif basic_details.strip():
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w', encoding='utf-8') as tmpf:
                tmpf.write(basic_details)
                sources['txts'].append(tmpf.name)
                print(f"✓ Basic details saved: {tmpf.name}")
        
        # Validate that we have at least something to process
        if not sources['urls'] and not sources['pdfs'] and not sources['txts']:
            raise HTTPException(
                status_code=400, 
                detail="Please provide either a job URL, resume file, or basic details"
            )
        
        # Process sources (scraping/extraction)
        print("\n" + "=" * 60)
        print("Processing sources...")
        print("=" * 60)
        results = await process_sources(sources)
        
        # Extract resume text
        resume_text = ""
        if results.get('pdfs'):
            resume_text = next(iter(results['pdfs'].values()))
            print(f"✓ Resume text extracted from PDF ({len(resume_text)} chars)")
        elif results.get('txts'):
            resume_text = next(iter(results['txts'].values()))
            print(f"✓ Resume text extracted from TXT ({len(resume_text)} chars)")
        
        if not resume_text:
            resume_text = "No resume provided"
            print("⚠ Warning: No resume text found, using placeholder")
        
        # Extract job description
        job_desc_text = ""
        if results.get('urls'):
            job_desc_text = next(iter(results['urls'].values()))
            print(f"✓ Job description extracted ({len(job_desc_text)} chars)")
        else:
            job_desc_text = "No job description provided"
            print("⚠ Warning: No job description found, using placeholder")
        
        # Match resume to job using AI
        print("\n" + "=" * 60)
        print("Matching resume to job description...")
        print("=" * 60)
        ai_resume = match_resume_to_job(resume_text, job_desc_text)
        print(f"✓ AI processing complete")
        print(f"  Name: {ai_resume.get('name', 'N/A')}")
        print(f"  Email: {ai_resume.get('email', 'N/A')}")
        print(f"  Title: {ai_resume.get('title', 'N/A')}")
        
        # Generate LaTeX
        print("\n" + "=" * 60)
        print("Generating LaTeX...")
        print("=" * 60)
        tex_output_path = os.path.join(TEMP, "resume.tex")
        
        try:
            tex_code, tex_fp = fill_latex_resume(ai_resume, output_path=tex_output_path)
            print(f"✓ LaTeX generated: {tex_fp}")
        except Exception as e:
            print(f"✗ LaTeX generation failed: {str(e)}")
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"LaTeX generation failed: {str(e)}"
            )
        
        # Compile to PDF
        print("\n" + "=" * 60)
        print("Compiling PDF...")
        print("=" * 60)
        try:
            pdf_fp = tex_to_pdf(tex_fp, TEMP)
            print(f"✓ PDF compiled: {pdf_fp}")
        except Exception as e:
            print(f"✗ PDF compilation failed: {str(e)}")
            traceback.print_exc()
            
            # Return the .tex file for debugging if PDF fails
            if os.path.exists(tex_fp):
                return FileResponse(
                    str(tex_fp), 
                    media_type="application/x-tex",
                    filename="debug_resume.tex",
                    headers={
                        "X-Error": "PDF compilation failed. Returning .tex file for debugging.",
                        "X-Error-Detail": str(e)
                    }
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"PDF compilation failed: {str(e)}"
                )
        
        # Clean up temp files
        try:
            if temp_fp and os.path.exists(temp_fp):
                os.remove(temp_fp)
        except:
            pass
        
        print("\n" + "=" * 60)
        print("✓ Resume generation complete!")
        print("=" * 60)
        
        # Return PDF
        return FileResponse(
            str(pdf_fp), 
            media_type="application/pdf", 
            filename="resume.pdf"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ FATAL ERROR")
        print("=" * 60)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/")
def alive():
    return {"status": "ok", "message": "Resume Builder API is running"}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "temp_dir": TEMP,
        "temp_exists": os.path.exists(TEMP)
    }
# Dynamic scraping logic here
import nest_asyncio
import asyncio
nest_asyncio.apply()
import os
import base64
from pathlib import Path
from PIL import Image as PILImage
import google.generativeai as genai
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

def gemini_vision_extract(image_path):
    pil_img = PILImage.open(image_path).convert("RGB")
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = (
        "Extract ALL visible text as a human would see it from this image or screenshot. "
        "Return as much continuous text as possible in document order."
    )
    resp = model.generate_content([prompt, pil_img])
    return resp.text if hasattr(resp, "text") else resp

def extract_text_from_pdf(pdf_path):
    if not Path(pdf_path).exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return ""
    try:
        reader = PdfReader(pdf_path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        if text and len(text) > 1000:
            return text
    except Exception as e:
        print(f"PDF direct text extraction error: {e}")

    try:
        pages = convert_from_path(pdf_path, first_page=1, last_page=1)
        img_path = "pdfpage.png"
        pages[0].save(img_path, "PNG")
        print("Falling back to OCR/Gemini Vision for PDF first page...")
        return gemini_vision_extract(img_path)
    except Exception as e:
        print(f"PDF to image/Gemini Vision error: {e}")
        return ""

def extract_text_from_txt(txt_path):
    if not Path(txt_path).exists():
        print(f"Error: TXT file not found at {txt_path}")
        return ""
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ""

async def crawl_or_screenshot(url):
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        screenshot=True,
        wait_for='js:() => document.body.innerText.includes("Data Scientist II")'
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if result.success:
            text = ""
            try:
                text = result.markdown.raw_markdown
            except AttributeError:
                text = str(result.markdown)
            if text and len(text) > 15000 and ("content" in text.lower() or "role" in text.lower()):
                return text, None
            else:
                return "", result.screenshot
        else:
            raise Exception(f"Crawl error: {result.error_message}")

async def process_sources(sources_dict):
    results = {}
    # URLs
    if sources_dict.get('urls'):
        results['urls'] = {}
        for url in sources_dict['urls']:
            text, screenshot_b64 = await crawl_or_screenshot(url)
            if text:
                results['urls'][url] = text
            elif screenshot_b64:
                try:
                    img_bytes = base64.b64decode(screenshot_b64)
                    img_path = f"screenshot_{len(results['urls'])}.png"
                    with open(img_path, "wb") as f:
                        f.write(img_bytes)
                    vision_text = gemini_vision_extract(img_path)
                    results['urls'][url] = vision_text
                except Exception as e:
                    results['urls'][url] = ""
            else:
                results['urls'][url] = ""
    # PDFs
    if sources_dict.get('pdfs'):
        results['pdfs'] = {}
        for pdf_path in sources_dict['pdfs']:
            text = extract_text_from_pdf(pdf_path)
            results['pdfs'][pdf_path] = text or ""
    # TXTs
    if sources_dict.get('txts'):
        results['txts'] = {}
        for txt_path in sources_dict['txts']:
            text = extract_text_from_txt(txt_path)
            results['txts'][txt_path] = text or ""
    return results

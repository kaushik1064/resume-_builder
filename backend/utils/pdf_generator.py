# PDF generation utilities
import subprocess
from pathlib import Path

def tex_to_pdf(tex_file, output_dir):
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    pdf_path = outdir / (Path(tex_file).stem + ".pdf")
    cmd = ["pdflatex", "-output-directory", str(outdir), tex_file]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return pdf_path

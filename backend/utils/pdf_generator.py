import subprocess
from pathlib import Path
import os

def tex_to_pdf(tex_path, output_dir):
    """
    Compile LaTeX to PDF in Colab environment
    """
    tex_path = Path(tex_path)
    output_dir = Path(output_dir)
    
    # Ensure paths exist
    if not tex_path.exists():
        raise FileNotFoundError(f"TeX file not found: {tex_path}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run pdflatex with proper settings for Colab
    cmd = [
        'pdflatex',
        '-interaction=nonstopmode',  # Don't stop on errors
        '-output-directory', str(output_dir),
        str(tex_path)
    ]
    
    try:
        # First pass
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=30  # 30 second timeout
        )
        
        # Second pass for references (optional, ignore errors)
        subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=30
        )
        
        # Find the generated PDF
        pdf_name = tex_path.stem + '.pdf'
        pdf_path = output_dir / pdf_name
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not generated at: {pdf_path}")
            
        return pdf_path
        
    except subprocess.CalledProcessError as e:
        # Capture and log the actual LaTeX error
        stderr_output = e.stderr.decode('utf-8', errors='ignore') if e.stderr else ""
        stdout_output = e.stdout.decode('utf-8', errors='ignore') if e.stdout else ""
        
        print("=" * 60)
        print("LATEX COMPILATION ERROR")
        print("=" * 60)
        print("STDERR:", stderr_output[:500])
        print("STDOUT:", stdout_output[:500])
        
        # Check log file for detailed error
        log_file = output_dir / (tex_path.stem + '.log')
        if log_file.exists():
            print("\n" + "=" * 60)
            print("LOG FILE ERRORS:")
            print("=" * 60)
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                log_lines = f.readlines()
                # Print last 50 lines which usually contain the error
                for line in log_lines[-50:]:
                    if line.startswith('!') or 'Error' in line:
                        print(line.strip())
        
        raise Exception(f"LaTeX compilation failed. Check the log at {log_file}")
    
    except subprocess.TimeoutExpired:
        raise Exception("LaTeX compilation timed out after 30 seconds")
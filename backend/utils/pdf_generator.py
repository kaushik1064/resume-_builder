import subprocess
from pathlib import Path
import os
import re

def tex_to_pdf(tex_path, output_dir):
    """
    Compile LaTeX to PDF in Colab environment with enhanced debugging
    """
    tex_path = Path(tex_path)
    output_dir = Path(output_dir)
    
    # Ensure paths exist
    if not tex_path.exists():
        raise FileNotFoundError(f"TeX file not found: {tex_path}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read the .tex file to check for obvious issues
    print(f"\n📄 Reading LaTeX file: {tex_path}")
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            tex_content = f.read()
        print(f"  Size: {len(tex_content)} bytes")
        print(f"  Lines: {len(tex_content.splitlines())}")
        
        # Check for common issues
        if '{{' in tex_content and '|default' in tex_content:
            print("  ⚠ WARNING: Found unprocessed Jinja2 syntax!")
            print("  This means the template wasn't rendered correctly")
        
        # Show first few lines for debugging
        lines = tex_content.splitlines()
        print("\n  First 10 lines:")
        for i, line in enumerate(lines[:10], 1):
            print(f"    {i:2}: {line[:80]}")
        
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
    
    # Run pdflatex with proper settings for Colab
    cmd = [
        'pdflatex',
        '-interaction=nonstopmode',  # Don't stop on errors
        '-halt-on-error',  # But halt on critical errors
        '-output-directory', str(output_dir),
        str(tex_path)
    ]
    
    print(f"\n🔨 Running pdflatex...")
    print(f"  Command: {' '.join(cmd)}")
    
    try:
        # First pass
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            cwd=str(output_dir.parent)  # Run from parent directory
        )
        
        stdout_output = result.stdout.decode('utf-8', errors='ignore')
        stderr_output = result.stderr.decode('utf-8', errors='ignore')
        
        # Check if compilation succeeded
        if result.returncode != 0:
            print(f"  ✗ First pass failed with return code {result.returncode}")
            raise subprocess.CalledProcessError(result.returncode, cmd, stdout_output, stderr_output)
        
        print(f"  ✓ First pass completed")
        
        # Second pass for references (optional, ignore errors)
        print(f"  Running second pass...")
        subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            cwd=str(output_dir.parent)
        )
        
        # Find the generated PDF
        pdf_name = tex_path.stem + '.pdf'
        pdf_path = output_dir / pdf_name
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not generated at: {pdf_path}")
        
        print(f"  ✓ PDF generated: {pdf_path}")
        print(f"  Size: {pdf_path.stat().st_size} bytes")
        
        return pdf_path
        
    except subprocess.CalledProcessError as e:
        # Detailed error reporting
        print("\n" + "=" * 70)
        print("❌ LATEX COMPILATION ERROR")
        print("=" * 70)
        
        stderr_output = e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='ignore')
        stdout_output = e.stdout if isinstance(e.stdout, str) else e.stdout.decode('utf-8', errors='ignore')
        
        # Parse stdout for actual LaTeX errors
        errors = []
        warnings = []
        
        for line in stdout_output.splitlines():
            if line.startswith('!'):
                errors.append(line)
            elif 'Error' in line or 'error' in line:
                errors.append(line)
            elif 'Warning' in line and 'Font' not in line:
                warnings.append(line)
        
        if errors:
            print("\n🔴 LaTeX Errors Found:")
            print("-" * 70)
            for error in errors[:10]:  # Show first 10 errors
                print(f"  {error}")
        
        if warnings:
            print("\n⚠️  Warnings:")
            print("-" * 70)
            for warning in warnings[:5]:  # Show first 5 warnings
                print(f"  {warning}")
        
        # Check log file for detailed error info
        log_file = output_dir / (tex_path.stem + '.log')
        if log_file.exists():
            print("\n" + "=" * 70)
            print("📋 LOG FILE ANALYSIS")
            print("=" * 70)
            
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                log_content = f.read()
            
            # Extract key error information
            error_patterns = [
                r'! (.+)',  # Error lines starting with !
                r'l\.(\d+) (.+)',  # Line number references
                r'LaTeX Error: (.+)',
                r'Missing (.+)',
                r'Undefined (.+)'
            ]
            
            found_errors = []
            for pattern in error_patterns:
                matches = re.findall(pattern, log_content, re.MULTILINE)
                found_errors.extend(matches)
            
            if found_errors:
                print("\n🎯 Key Issues:")
                print("-" * 70)
                for i, error in enumerate(found_errors[:15], 1):  # Show top 15
                    error_str = error if isinstance(error, str) else ' '.join(str(x) for x in error)
                    print(f"  {i}. {error_str[:100]}")
            
            # Check for specific common issues
            if 'Undefined control sequence' in log_content:
                print("\n💡 Possible cause: Undefined LaTeX command")
                print("   Check for special characters that weren't properly escaped")
            
            if 'Missing } inserted' in log_content:
                print("\n💡 Possible cause: Unmatched braces in template")
                print("   Check Jinja2 template syntax")
            
            if 'Font' in log_content and 'not found' in log_content:
                print("\n💡 Possible cause: Missing font package")
                print("   Try installing additional LaTeX packages")
            
            # Save log excerpt for manual inspection
            log_excerpt_file = output_dir / 'latex_error_excerpt.log'
            with open(log_excerpt_file, 'w', encoding='utf-8') as f:
                f.write("LAST 100 LINES OF LOG:\n")
                f.write("=" * 70 + "\n")
                f.write('\n'.join(log_content.splitlines()[-100:]))
            
            print(f"\n📄 Full log excerpt saved to: {log_excerpt_file}")
        
        # Print the problematic .tex file location
        print("\n" + "=" * 70)
        print(f"📁 Files for debugging:")
        print(f"   LaTeX source: {tex_path}")
        print(f"   Log file: {log_file}")
        print(f"   Working directory: {output_dir}")
        print("=" * 70)
        
        # Create a simplified test
        print("\n🧪 Debugging tip:")
        print("   Run manually: cd temp && pdflatex resume.tex")
        print("   This will show interactive error messages")
        
        raise Exception(
            f"LaTeX compilation failed.\n"
            f"Check files:\n"
            f"  - {log_file}\n"
            f"  - {tex_path}\n"
            f"Run 'cd {output_dir.parent} && pdflatex {tex_path.name}' for interactive debugging"
        )
    
    except subprocess.TimeoutExpired:
        raise Exception("LaTeX compilation timed out after 30 seconds")
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        raise
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

LATEX_TEMPLATE = r"""
\documentclass[a4paper,10pt]{article}
%-----------------------------------------------------------
\usepackage[top=0.75in, bottom=0.75in, left=0.55in, right=0.85in]{geometry}
\usepackage{graphicx}
\usepackage{url}
\usepackage{palatino}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{xcolor} % Added this package
\fontfamily{SansSerif}
\selectfont

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=cyan,
    pdftitle={Resume},
    pdfpagemode=FullScreen,
}
    
\urlstyle{same}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{color}
\definecolor{mygrey}{gray}{0.75}
\textheight=9.8in
\raggedbottom

\setlength{\tabcolsep}{0in}
\newcommand{\isep}{-2 pt}
\newcommand{\lsep}{-0.5cm}
\newcommand{\psep}{-0.6cm}
\renewcommand{\labelitemii}{$\circ$}

\pagestyle{empty}
%-----------------------------------------------------------
%Custom commands - FIXED THIS SECTION
\newcommand{\resheading}[1]{%
  \par\noindent%
  \small%
  \colorbox{mygrey}{%
    \parbox{\dimexpr\linewidth-2\fboxsep\relax}{%
      \textbf{#1}%
    }%
  }%
  \par\nobreak%
}
\newcommand{\ressubheading}[3]{
\begin{tabular*}{6.62in}{l @{\extracolsep{\fill}} r}
    \textsc{{\textbf{#1}}} & \textsc{\textit{[#2]}} \\
\end{tabular*}\vspace{-8pt}}

\begin{document}

\hspace{0.5cm}\\[-1.8cm]

\textbf{SRI KAUSHIK AYALURI} \hspace{9.6cm} {\bf srinukaus@gmail.com}\\
\indent {\bf Machine Learning Engineer}  \hspace{10.3 cm} {\bf +91-9381880485} \\
\indent {\bf Visakhapatnam, India}  \hspace{7.9 cm} {\bf linkedin.com/in/sri-kaushik-ayaluri} \\
\indent {\bf github.com/kaushik1064} \\


\vspace{-2mm}
\resheading{\textbf{EDUCATION} }\\[\lsep]\\ \\
%\begin{table}[ht!]
%\begin{center}
\indent \begin{tabular}{ p{2.5cm} @{\hskip 0.15in} p{5.5cm} @{\hskip 0.15in} p{3.5cm} @{\hskip 0.15in} p{2.5cm} @{\hskip 0.15in} p{1.5cm} }
\toprule
\textbf{Degree} & \textbf{Specialization} & \textbf{Institute} & \textbf{Year} & \textbf{CPI} \\
\midrule
B.Tech & \textit{Mechanical Engineering} & SCE College & 2022 & 7.01 \\
Intermediate & \textit{Physics, Chemistry, \& Mathematics} & Chaitanya College & 2018 & 8.5 \\
10th Grade & - & S.F.S High School & 2016 & 8.7 \\
\bottomrule
\end{tabular}

%\end{center}
%\end{table}
\\ \\

%\resheading{\textbf{FIELDS OF INTEREST} }\\[\lsep]
%\begin{itemize}
%\item \noindent Wireless Network and Network Security, Another one, a third one
%\end{itemize}

\vspace{1mm}

\resheading{\textbf{WORK EXPERIENCE} }


\begin{itemize}

\vspace{-1mm}
\item {\bf Machine Learning \& Data Analytics Intern } \textit{[VELOXIVISION EDU TECH]}
\textit{\hfill 
{Feb 2024–Aug 2024}
}
\vspace{-1mm}

\begin{itemize}

\item Engineered a \textbf{transaction analysis pipeline}, processing \textbf{50,000+ transactions} using \textbf{Pandas \& SQL}, reducing data processing time by \textbf{40\%}.

\item Developed a \textbf{K-Means clustering model} that segmented customers into \textbf{3 distinct groups}, improving personalized banking product recommendations by \textbf{30\%}.

\item Implemented an \textbf{anomaly detection system} (\textbf{Isolation Forest}) that flagged \textbf{98\% of fraudulent transactions}, and Built an interactive \textbf{Power BI dashboard}, utilized for \textbf{strategic banking decisions}.

\vspace{-1mm}

\end{itemize}
\end{itemize}


\begin{itemize}

\vspace{-1mm}
\item {\bf Junior ML Engineer } \textit{[Omdena Organization]}
\textit{\hfill 
{Oct 2023-Jan 2024}
}
\vspace{-1mm}

\begin{itemize}

\item Engineered an \textbf{automated web scraping pipeline} for \textbf{Nepali news sites}, collecting and processing over \textbf{500,000+ news articles} using \textbf{Selenium \& BeautifulSoup}, reducing data acquisition time by \textbf{70\%}.

\item Fine-tuned a \textbf{BERT-based Named Entity Recognition (NER) model}, improving accuracy from \textbf{65\% to 90\%}, enabling more precise detection of abusive content in news articles.

\item Deployed the \textbf{ML model} using \textbf{MLOps (Dagshub, Docker, CI/CD)}, automating model training and deployment, reducing manual intervention by \textbf{60\%}.

\item Implemented a \textbf{real-time API endpoint} for extracting and analyzing entity relationships in news data, supporting \textbf{100+ concurrent requests} with an average response time of \textbf{1.2s}.

\vspace{-1mm}

\end{itemize}
\end{itemize}



\begin{itemize}

\vspace{-0.5mm}
\item {\bf Data Scientist Intern } \textit{[Omdena Global Projects]}
\textit{\hfill 
{May 2023-June 2023}
}
\vspace{-1mm}

\begin{itemize}

\item Developed a high-accuracy recommendation model for \textbf{Berlin grocery stores}, achieving \textbf{90\% precision}.

\item Optimized data collection, preprocessing, and web scraping of \textbf{10,000+ grocery listings}.

\item Devised innovative machine learning solutions for personalized recommendations through \textbf{NLP technology, resulting in over 1,500 unique interactions per day} and fostering sustained increases in daily usage among frequent shoppers.

\vspace{-1mm}

\end{itemize}
\end{itemize}



\resheading{\textbf{PROJECTS} }

\begin{itemize}

\vspace{-0.5mm}
\item {\bf Conversational AI Chatbot with Real-Time Web Scraping and Vector Retrieval}  
\href{https://github.com/kaushik1064/Conversational-AI-Chatbot}{Project Link}  
\textit{\hfill {Nov 2024-Dec 2024}}

\begin{itemize}

\vspace{-2mm}
\item Built an \textbf{end-to-end Flask-based chatbot} integrating \textbf{LangChain} and Hugging Face’s \textbf{Mistral-7B} model, improving inference speed by \textbf{40\%} and handling over \textbf{1,000 user requests daily}.  
\item Implemented a \textbf{real-time Google Search \& Selenium scraping pipeline}, increasing relevant data coverage by \textbf{60\%} and reducing manual research time by \textbf{35\%}.  
\item Optimized \textbf{vector storage with FAISS} and \textbf{HuggingFace Bge Embeddings}, cutting retrieval latency by \textbf{30\%} and achieving a \textbf{90\% accuracy} in relevant document retrieval.  

\vspace{-2mm}
\end{itemize}
\end{itemize}

\begin{itemize}

\vspace{-0.5mm}
\item {\bf AI Pipeline for Image Detection, Classification, and Captioning}  
\href{https://github.com/kaushik1064/INFLIECT_AI_PIPELINE-PROJECT.git}{Project Link}  
\textit{\hfill {Sep 2024-Oct 2024}}

\begin{itemize}

\vspace{-2mm}
\item Constructed an advanced AI pipeline with \textbf{Google ViT and YOLOv5}, facilitating real-time data processing and \textbf{enabling the analysis of 500+ data points per second}, which streamlined operations for the analytics team.  
\item Improved object detection speed by \textbf{50\%} and classification accuracy by \textbf{60\%}.  
\item Deployed via \textbf{Flask}, enabling \textbf{80+ users} to interact with the AI pipeline.  

\vspace{-2mm}
\end{itemize}
\end{itemize}


\resheading{\textbf{CERTIFICATIONS} }\\[\lsep]
\begin{itemize}
\item {\bf Data Science with AI} - Veloxivision Edu Tech \hfill \textit{Oct 2022 - Oct 2023}
\begin{itemize}  
\item Completed a comprehensive course covering \textbf{end-to-end ML pipelines}, including ETL, feature engineering, model training, and deployment using Python, TensorFlow, and MLOps tools (Docker, CI/CD). Gained hands-on experience in \textbf{NLP} (BERT, Transformers) for text classification and entity recognition, achieving 90\%+ accuracy in projects. Also worked on \textbf{computer vision} applications using OpenCV and CNNs, deploying models via Flask/REST APIs.
\end{itemize}



\resheading{\textbf{TECHNICAL SKILLS} }
\begin{itemize}
\vspace{-1mm}

\item \textbf{Languages:} Python, SQL  

\vspace{-1mm}
\item \textbf{Tools:} TensorFlow, PyTorch, LangChain, Docker, Git, CI/CD, MLOps, AWS, Jupiter Notebook, LaTeX  

\vspace{-1mm}
\item \textbf{Libraries \& Databases:} Pandas, NumPy, SciPy, OpenCV, MySQL, PostgreSQL

\vspace{-1mm}
\item \textbf{AI \& ML:} Langchain, NLP, Machine Learning, Deep
Learning

\vspace{-4mm}
\end{itemize}


\end{document}

"""

def generate_latex_resume(user_info, job_description):
    """
    Use Gemini to generate a customized LaTeX resume
    """
    prompt = f"""You are an expert resume writer and LaTeX formatting specialist.

I have a LaTeX resume template with placeholder sections. Your task is to:
1. Replace HEADER_SECTION with the user's contact information formatted like:
   \textbf{{NAME}} \hspace{{9.6cm}} {{\bf EMAIL}}\\
   \indent {{\bf TITLE}} \hspace{{10.3cm}} {{\bf PHONE}} \\
   \indent {{\bf LOCATION}} \hspace{{7.9cm}} {{\bf LINKEDIN}} \\
   \indent {{\bf GITHUB}} \\

2. Replace EDUCATION_SECTION with a table of education (degree, specialization, institute, year, GPA)
   Use the same tabular format as shown in the template. Skip if no education data.

3. Replace WORK_EXPERIENCE_SECTION with experience entries using:
   \item {{\bf TITLE }} \textit{{[COMPANY]}}
   \textit{{\hfill {{DURATION}}}}
   With bullet points for each achievement. Skip if no experience.

4. Replace PROJECTS_SECTION with project entries including project name, link, duration, and details.
   Skip if no projects.

5. Replace CERTIFICATIONS_SECTION with certification entries.
   Skip if no certifications.

6. Replace TECHNICAL_SKILLS_SECTION with skills grouped by category.
   Skip if no skills.

IMPORTANT:
- Preserve ALL LaTeX commands, backslashes, and special formatting
- Escape special characters properly (_#$%&^~)
- Keep exact spacing commands (\\vspace, \\hspace, \\indent, \\textbf, \\textit, \\href)
- NEVER use double curly braces or percent-curly-brace markers - these are template markers, not LaTeX
- Use regular ASCII characters only: use - (hyphen) not – (en-dash), use ' not ' or '
- Only include sections that have data
- Return ONLY the complete, compilable LaTeX code
- Do NOT include markdown code blocks or any explanation

USER INFORMATION:
{format_user_info(user_info)}

LATEX TEMPLATE WITH PLACEHOLDERS:
{LATEX_TEMPLATE}

Return the complete LaTeX resume now:"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    
    # Extract LaTeX code
    latex_code = response.text.strip()
    
    # Remove markdown code blocks if present
    if latex_code.startswith('```'):
        latex_code = latex_code.split('```')[1]
        if latex_code.startswith('latex'):
            latex_code = latex_code[5:]
        latex_code = latex_code.strip()
    
    # Sanitize smart quotes and dashes to ASCII equivalents
    replacements = {
        ''': "'",          # Left single quote
        ''': "'",          # Right single quote
        '"': '"',          # Left double quote
        '"': '"',          # Right double quote
        '–': '-',          # En-dash
        '—': '-',          # Em-dash
        'â€™': "'",        # Corrupted apostrophe
        'â€œ': '"',        # Corrupted left quote
        'â€\x9d': '"',     # Corrupted right quote
    }
    
    for old, new in replacements.items():
        latex_code = latex_code.replace(old, new)
    
    return latex_code

def format_user_info(user_info):
    """Format user info as readable text for the LLM prompt"""
    text = f"""
Name: {user_info.get('name', 'N/A')}
Email: {user_info.get('email', 'N/A')}
Phone: {user_info.get('phone', 'N/A')}
Title: {user_info.get('title', 'N/A')}
Location: {user_info.get('location', 'N/A')}
LinkedIn: {user_info.get('linkedin', 'N/A')}
GitHub: {user_info.get('github', 'N/A')}

EDUCATION:
"""
    for edu in user_info.get('education', []):
        text += f"- {edu.get('degree', '')} in {edu.get('specialization', '')} from {edu.get('institute', '')} ({edu.get('year', '')}) - GPA: {edu.get('gpa', '')}\n"
    
    text += "\nEXPERIENCE:\n"
    for exp in user_info.get('experience', []):
        text += f"- {exp.get('title', '')} at {exp.get('company', '')} ({exp.get('duration', '')})\n"
        for detail in exp.get('details', []):
            text += f"  * {detail}\n"
    
    text += "\nPROJECTS:\n"
    for proj in user_info.get('projects', []):
        text += f"- {proj.get('name', '')} ({proj.get('duration', '')})\n"
        if proj.get('link'):
            text += f"  Link: {proj.get('link')}\n"
        for detail in proj.get('details', []):
            text += f"  * {detail}\n"
    
    text += "\nCERTIFICATIONS:\n"
    for cert in user_info.get('certifications', []):
        text += f"- {cert.get('name', '')} from {cert.get('issuer', '')} ({cert.get('date', '')})\n"
    
    text += "\nSKILLS:\n"
    for skill in user_info.get('skills', []):
        text += f"- {skill.get('category', '')}: {skill.get('items', '')}\n"
    
    return text
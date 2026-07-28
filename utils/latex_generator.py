
import re

from utils.resume_structure import extract_resume_structure
from utils.header_parser import extract_header_details


def escape_latex(text):

    if text is None:
        return ""

    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    return text


def format_skills(items):

    if not items:
        return "N/A"

    return ", ".join(
        escape_latex(i)
        for i in items
    )


def format_projects(items):

    if not items:
        return "N/A"

    latex = ""

    for item in items:

        latex += (
            "\\textbf{"
            + escape_latex(item)
            + "}\\\\[4pt]\n"
        )

    return latex


def format_experience(items):

    if not items:
        return "N/A"

    latex = ""

    for item in items:

        latex += (
            "\\textbf{"
            + escape_latex(item)
            + "}\\\\[3pt]\n"
        )

    return latex


def format_education(items):

    if not items:
        return "N/A"

    latex = ""

    for item in items:

        latex += (
            escape_latex(item)
            + "\\\\\n"
        )

    return latex


def format_certifications(items):

    if not items:
        return "N/A"

    latex = "\\begin{itemize}[leftmargin=*]\n"

    for item in items:

        latex += (
            "\\item "
            + escape_latex(item)
            + "\n"
        )

    latex += "\\end{itemize}\n"

    return latex


def generate_latex_resume(candidate_name, rewritten_resume):

    header = extract_header_details(rewritten_resume)

    structure = extract_resume_structure(rewritten_resume)

    candidate_name = escape_latex(candidate_name)

    phone = escape_latex(header["phone"])

    email = escape_latex(header["email"])

    linkedin = header["linkedin"]

    github = header["github"]

    leetcode = header["leetcode"]

    summary = escape_latex(
        structure["summary"]
    )

    skills = format_skills(
        structure["skills"]
    )

    experience = format_experience(
        structure["experience"]
    )

    projects = format_projects(
        structure["projects"]
    )

    education = format_education(
        structure["education"]
    )

    certifications = format_certifications(
        structure["certifications"]
    )

    latex = rf"""
\documentclass[10pt]{{article}}

\usepackage[a4paper,margin=0.45in]{{geometry}}
\usepackage{{titlesec}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{parskip}}
\usepackage{{xcolor}}

\pagestyle{{empty}}

\hypersetup{{
colorlinks=true,
urlcolor=blue
}}

\titleformat{{\section}}
{{\large\bfseries}}
{{}}
{{0em}}
{{}}

\titlespacing{{\section}}
{{0pt}}
{{8pt}}
{{4pt}}

\begin{{document}}

\begin{{center}}

{{\Huge\textbf{{{candidate_name}}}}}

\vspace{{3pt}}

{phone}
\hspace{{10pt}}|\hspace{{10pt}}
{email}
\hspace{{10pt}}|\hspace{{10pt}}
\href{{{linkedin}}}{{LinkedIn}}

\hspace{{10pt}}|\hspace{{10pt}}
\href{{{github}}}{{GitHub}}

\hspace{{10pt}}|\hspace{{10pt}}
\href{{{leetcode}}}{{LeetCode}}

\end{{center}}

\vspace{{6pt}}

\hrule

\vspace{{8pt}}

\section*{{Professional Summary}}

{summary}

\section*{{Technical Skills}}

\begin{{itemize}}[leftmargin=*]

\item {skills}

\end{{itemize}}

\section*{{Professional Experience}}

{experience}

\section*{{Projects}}

{projects}

\section*{{Education}}

{education}

\section*{{Certifications}}

{certifications}

\end{{document}}
"""

    return latex
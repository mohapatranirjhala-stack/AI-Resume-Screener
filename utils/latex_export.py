
import os
import subprocess


def save_latex_file(latex_code, output_file):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(latex_code)


def compile_latex_to_pdf(tex_file):

    try:

        subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                tex_file
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        pdf_file = tex_file.replace(".tex", ".pdf")

        if os.path.exists(pdf_file):
            return pdf_file

        return None

    except Exception as e:

        print(e)
        return None
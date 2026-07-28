
import subprocess
import os


def compile_latex_to_pdf(tex_file):

    try:

        output_dir = os.path.dirname(
            os.path.abspath(tex_file)
        )

        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                output_dir,
                tex_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:

            print("\n========== LATEX COMPILATION ERROR ==========\n")
            print(result.stdout)
            print(result.stderr)
            print("\n=============================================\n")

            return None

        pdf_file = tex_file.replace(
            ".tex",
            ".pdf"
        )

        if os.path.exists(pdf_file):

            return pdf_file

        return None

    except Exception as e:

        print("\n========== PYTHON ERROR ==========\n")
        print(e)
        print("\n==================================\n")

        return None
import io
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
#Libraries pour gerer le pdf
import pdfkit
import markdown2
#Libraries pour gerer les fichiers docx
from docx.shared import Pt
from docx import Document
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
import subprocess       # used to convert markdown to docx
from markdown import markdown
from bs4 import BeautifulSoup

#Libraries pour gerer les fichiers pptx
from pptx import Presentation
from pptx.util import Inches
#Local functions


def download_pdf(markdown_content):
    html_content = markdown2.markdown(markdown_content)
    html_content_final = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Document</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    path_to_wkhtmltopdf = '.././wkhtmltopdf/bin/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdf_data = pdfkit.from_string(html_content_final, configuration=config)
    return pdf_data

def convert_markdown_to_docx(input_file, output_file):
    path=".././Pandoc/pandoc.exe"
    try:
        subprocess.run([path, input_file, '-o', output_file], check=True)
        print(f"Conversion successful! {output_file} has been created.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")


import subprocess

def convert_markdown_to_pptx_using_template(markdown_file, output_pptx, template_pptx):
    try:
        path="./Pandoc/pandoc.exe"

        subprocess.run(
            [path, markdown_file, '-o', output_pptx, '--reference-doc', template_pptx],
            check=True
        )
        print(f"Conversion with template successful! Output saved to {output_pptx}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")



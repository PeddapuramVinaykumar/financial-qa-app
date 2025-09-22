# parsers.py
import pdfplumber
import pandas as pd

def parse_pdf(file):
    chunks = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                chunks.append(text)
    return chunks

def parse_excel(file):
    df = pd.read_excel(file)
    return [df.to_csv(index=False)]

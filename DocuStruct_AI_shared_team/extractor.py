

import json
import requests
from pypdf import PdfReader

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3.5:4b"


def extract_pdf_text(pdf_source):
    from io import BytesIO
    from pypdf import PdfReader

    if isinstance(pdf_source, (str, bytes)) or hasattr(pdf_source, "__fspath__"):
        reader = PdfReader(pdf_source)
    else:
        pdf_source.seek(0)
        pdf_bytes = pdf_source.read()
        reader = PdfReader(BytesIO(pdf_bytes))

    text = "\n".join(
        page.extract_text() or "" for page in reader.pages
    )

    if not text.strip():
        raise ValueError(
            "No readable text found. This PDF may be scanned."
        )

    return text



def extract_invoice_fields(pdf_text):
    prompt = f"""
Extract these fields from the invoice text:
invoice_number, vendor, invoice_date, due_date,
subtotal, tax, total.

Return one JSON object with exactly these keys.
Use null for missing values.
Amounts must be numbers or null.
Do not guess or calculate missing values.
Dates must use YYYY-MM-DD format.
For example, write 2026-10-20, not 20 October 2026.

Invoice text:
{pdf_text[:4000]}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "think": False,
            "options": {
                "num_predict": 250
            }
        },
        timeout=300
    )

    response.raise_for_status()
    answer = response.json().get("response", "").strip()

    if not answer:
        raise ValueError("The AI returned an empty response.")

    data = json.loads(answer)

    required_fields = [
        "invoice_number", "vendor", "invoice_date",
        "due_date", "subtotal", "tax", "total"
    ]

    for field in required_fields:
        data.setdefault(field, None)

    return data



def analyze_invoice(pdf_path):
    text = extract_pdf_text(pdf_path)
    return extract_invoice_fields(text)

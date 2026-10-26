# DocuStruct AI — PDF to Validated Data

**DocuStruct AI** is a local AI-powered document processing tool that extracts structured information from invoice PDFs, validates the extracted data, and allows users to review and export the results.
Our goal is to reduce manual data entry and make invoice processing faster and more reliable.

## Problem Statement
Invoices and other business documents often contain information that must be manually copied into spreadsheets or databases. This process can be time-consuming and may introduce errors.
DocuStruct AI addresses this problem by converting invoice PDF content into structured data and checking it before export.

## Features
- **PDF Upload:** Upload an invoice PDF for processing.
- **Text Extraction:** Extract text from PDF documents using `pypdf`.
- **AI-Powered Extraction:** Use a locally running Ollama model to identify important invoice fields.
- **Data Validation:** Check required fields, dates, numeric amounts, and invoice total consistency.
- **Human Review:** Review and correct extracted values before exporting.
- **JSON Export:** Download structured invoice data in JSON format.
- **CSV Export:** Export invoice data for use in spreadsheets and data analysis.
- **Local Processing:** Run AI inference locally using Ollama rather than relying on a hosted AI API.

## Technologies Used
| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Ollama | Local AI model execution |
| Qwen3.5 4B | AI-powered invoice field extraction |
| pypdf | PDF text extraction |
| pandas | Structured data handling and CSV export |
| requests | Communication with the local Ollama API |

## How It Works
1. Upload an invoice PDF.
2. Extract text from the document.
3. Send the extracted text to the local AI model.
4. Convert the model's response into structured invoice fields.
5. Validate required fields, dates, and monetary values.
6. Review and correct the extracted information.
7. Export the final data as JSON or CSV.

## Extracted Fields
The application extracts the following invoice information:
- Invoice number
- Vendor name
- Invoice date
- Due date
- Subtotal
- Tax
- Total amount
The validation process checks for missing fields, invalid dates, negative or nonnumeric amounts, and inconsistencies between the subtotal, tax, and total.

## Prerequisites
Before running the project, install:
- Python
- Git
- Ollama
- The `qwen3.5:4b` model
The model must be downloaded in Ollama before using AI-powered extraction.

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/nandinipatnaik9017-jpg/docustruct-ai.git
cd docustruct-ai
```
If the project files are inside `DocuStruct_AI_shared_team`, enter that folder:
```bash
cd DocuStruct_AI_shared_team
```

### 2. Create a virtual environment
```bash
py -m venv .venv
```
Activate it on Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
py -m pip install -r requirements.txt
```

### 4. Install and start the local AI model
Install Ollama from its official website:
https://ollama.com/

Download the model:
```bash
ollama pull qwen3.5:4b
```

Make sure Ollama is running. You can check the installed models with:
```bash
ollama list
```

### 5. Run the application
From the folder containing `app.py`, run:
```bash
py -m streamlit run app.py
```
Open the local URL displayed in your terminal, usually:
http://localhost:8501

## Testing
Test the application with a sample, text-based invoice PDF.
Verify that:
- Invoice fields are extracted correctly.
- Missing or invalid values are flagged.
- Incorrect invoice totals are identified.
- Extracted values can be reviewed and corrected.
- JSON and CSV exports contain the expected information.
AI extraction can produce mistakes, so always review the results before using them.

## Privacy and Limitations
AI inference is performed locally through Ollama. Invoice text is sent to the local model for extraction rather than to a hosted AI service in the current implementation.
The application currently focuses on text-based invoice PDFs. Scanned documents may require OCR support. Extraction accuracy can vary depending on document layout and text quality.
This project is a prototype and is not a replacement for professional financial verification.

## Future Improvements
- Add OCR support for scanned PDFs.
- Support additional document types, including forms and reports.
- Improve extraction accuracy for complex tables and layouts.
- Add automated testing and document-level evaluation.
- Support batch processing of multiple documents.
- Improve error handling and validation reporting.

## Contributors
Built collaboratively as a hackathon project.

## License
Add the license selected for this repository here. If you intend to release the project as open source, choose an appropriate license and include its license file in the repository.

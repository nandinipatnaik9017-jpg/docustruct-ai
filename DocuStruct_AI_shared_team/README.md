# DocuStruct AI — Shared Team Project

This folder contains the main application files for DocuStruct AI, including the Streamlit interface, invoice validation, human review, data export, and Ollama-based PDF extraction.

## Requirements

- Python
- Ollama
- The `qwen3.5:4b` model

## Run the Application on Windows

Open PowerShell in this folder and run each command separately.

**1. Create a virtual environment**

```powershell
py -m venv .venv
```

**2. Activate the environment**

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```powershell
py -m pip install -r requirements.txt
```

**4. Download the AI model**

```powershell
ollama pull qwen3.5:4b
```

**5. Start the application**

```powershell
py -m streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Testing

Run these commands from this folder to test the Ollama connection and PDF extraction:

```powershell
py test_ollama.py
py test_extractor.py
```

Ollama must be running, and the model must be installed before testing AI extraction.

## Team Workflow

We use GitHub to share our project files and keep our work updated. We divide tasks between team members, test our changes locally, and share completed updates through GitHub. Each of us maintains a separate Python virtual environment. We also avoid uploading unnecessary files such as `.venv` and `__pycache__`.

Before continuing development, we check the latest shared changes and make sure the application still works after updates.

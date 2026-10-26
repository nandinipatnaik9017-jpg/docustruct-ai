# DocuStruct AI — Shared Team Project

This folder combines the Streamlit UI/validation/review/export app with the backend Ollama PDF extractor.

## Before running
- Install Python.
- Install Ollama and pull the model: `ollama pull qwen3.5:4b`
- Start Ollama if it is not running.

## Run on Windows
Open a terminal in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Team workflow
- Keep `app.py` (UI, validation, review, exports) and `extractor.py` (PDF text + Ollama AI) in the same folder.
- Do not send or share the `.venv` folder; each teammate creates their own environment.
- Use GitHub to collaborate on one live codebase. A ZIP is only a snapshot and does not sync changes between computers.
- Before editing, pull the latest changes; after editing, commit and push your changes.
- Do not overwrite a working copy until the shared version has been tested.

## Tests
`python test_ollama.py` checks the local Ollama API.
`python test_extractor.py` extracts the included sample invoice (requires Ollama running and model installed).

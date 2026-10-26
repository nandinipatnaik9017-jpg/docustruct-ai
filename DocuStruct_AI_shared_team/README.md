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

## Team Workflow
- We use GitHub to share our project files and keep both our work updated.
- Before making changes, we check for the latest updates from our teammate.
- We divide the work between us so that we can develop different parts of the project.
- Each of us tests our changes locally before sharing them.
- Once the changes are ready, we push them to GitHub and update the shared project.
- We check the updated version together to make sure everything works properly.
- We keep our Python virtual environments separate on our own computers.
- We avoid uploading unnecessary files such as `.venv` and `__pycache__`.
- If something goes wrong after an update, we check the changes and fix the issue before continuing.

## Tests
`python test_ollama.py` checks the local Ollama API.
`python test_extractor.py` extracts the included sample invoice (requires Ollama running and model installed).

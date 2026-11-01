# DreamWeaver-AI

> A small research/prototype project for generating and serving AI-generated art.

### Repository structure

- `backend/` — Python backend services and scripts (art generation, model list, event tracker).
- `frontend/` — Streamlit frontend app (web UI/app entrypoint).
- `unity_world/` — Unity assets and world export (if used).
- `assets/` — Shared assets used by the project.
- `artifacts/` — Generated outputs and intermediate files.
- `requirements.txt` — Python dependencies for the project.

### Quick start (Windows)

1. Clone the repo and open a terminal in the project root.

2. Create and activate a Python virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

Backend: run locally

1. Change to the backend folder and start the backend services or run scripts.

```powershell
cd backend
# Run the development server (if present)
python manage.py runserver

# Or run the art generation script directly
python art_generator.py
```

Frontend: run locally

1. Open a new terminal, activate the virtualenv, then run the Streamlit app:

```powershell
cd frontend
streamlit run app.py
```

2. Open the local URL printed by Streamlit in your browser.

### Notes on `art_generator.py`

- The script at `backend/art_generator.py` is the main art generation entrypoint. If you see a `SyntaxError` referencing a stray `dfrom` or similar, open the file and correct the import to `from ... import ...` (there's a known typo in older versions).
- Depending on the models used (Hugging Face Diffusers, etc.), you may need additional system packages (CUDA, GPU drivers) and larger dependency installs. Review any top-of-file comments in `backend/art_generator.py` for model-specific setup.

Configuration and secrets

- Any API keys or model access tokens should be provided via environment variables or a local config file (not checked into source control). Add them before running scripts that contact external model services.

Development tips

- Use the virtual environment to avoid dependency conflicts.
- Keep generated outputs in `artifacts/` and add them to `.gitignore` if appropriate.

Troubleshooting

- If `pip install -r requirements.txt` fails on Windows, ensure you have a supported Python version and build tools (for packages with native extensions).
- For GPU-accelerated model runs, verify CUDA and driver versions match the installed PyTorch/CUDA wheel.

Contributing

1. Open an issue describing the change or bug.
2. Create a branch, make changes, and submit a pull request.

License

This repository does not include a license file. Add a `LICENSE` at the repo root if you intend to publish or share.



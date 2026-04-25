# Backend

FastAPI backend for the Knowledge Navigator website.

## Run locally

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Server runs at http://localhost:8000

## Endpoints

- GET /health
- POST /api/chat

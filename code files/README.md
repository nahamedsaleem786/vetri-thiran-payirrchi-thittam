# LegalEase — AI-Assisted Legal Document Generator

LegalEase is a Streamlit + FastAPI application for generating editable AI-assisted drafts of common legal documents with Google's Gemini API.

## What's fixed in this version

- Uses Google's current `google-genai` Python SDK instead of the legacy `google-generativeai` package.
- Uses `gemini-2.5-flash` by default, a stable Gemini API model.
- Backend starts even when the API key is missing; `/health` clearly reports configuration status.
- Better FastAPI validation and error messages.
- Streamlit backend connection can be configured with `BACKEND_URL`.
- DOCX export is kept self-contained and does not require a logo.
- PDF export includes bundled Unicode fonts so Tamil/Unicode text is less likely to break.
- Added `/health` and `/docs` endpoints.

## Requirements

- Python 3.10 or newer
- A Gemini API key for AI generation

## Windows setup

Open Command Prompt or PowerShell in this folder:

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set:

```text
GEMINI_API_KEY=YOUR_REAL_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Start the backend in **Terminal 1**:

```powershell
venv\Scripts\activate
uvicorn main:app --reload
```

Start the frontend in **Terminal 2**:

```powershell
venv\Scripts\activate
streamlit run app.py
```

Open the Streamlit URL shown in the terminal, normally `http://localhost:8501`.

## Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`, then run:

```bash
uvicorn main:app --reload
```

In another terminal:

```bash
source venv/bin/activate
streamlit run app.py
```

## Check the backend

Open:

- `http://127.0.0.1:8000/` — API status
- `http://127.0.0.1:8000/health` — Gemini configuration status
- `http://127.0.0.1:8000/docs` — interactive FastAPI docs

## Document workflow

1. Select a document type.
2. Enter the parties.
3. Enter the terms and conditions.
4. Select an effective date.
5. Click **Generate Document**.
6. Edit the generated text if needed.
7. Download TXT, DOCX, or PDF.

## Project structure

```text
LegalEase/
├── app.py
├── main.py
├── routes.py
├── requirements.txt
├── .env.example
├── README.md
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── assets/
│   └── fonts/
│       ├── DejaVuSerif.ttf
│       └── DejaVuSerif-Bold.ttf
└── utils/
    ├── __init__.py
    ├── document_formatter.py
    └── pdf_formatter.py
```

## Notes

Do not commit `.env` or your API key to GitHub. The application produces AI-assisted drafts, not legal advice. Have an appropriately qualified legal professional review a document before using it for an actual legal matter.

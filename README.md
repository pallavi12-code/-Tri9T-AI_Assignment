# CT200 Document Parser & Versioning API

A Python/FastAPI document-processing system that extracts document structure, validates heading hierarchy, and tracks document versions and changes.

> Originally developed for an AI engineering internship assignment; the repository is presented here as a standalone engineering project.

## What it does

### Document parsing
- Accepts PDF/text content for processing
- Extracts document text and structural headings
- Represents detected headings as structured JSON

### Structure validation
Checks for:
- Duplicate headings
- Incorrect heading hierarchy
- Skipped heading levels

Example:

```text
H1
 └── H2
      └── H3    valid

H1
 └── H3         warning: skipped level
```

### Version management
The application stores document versions and supports change comparison, including added, removed, and changed headings.

### REST API

| Endpoint | Purpose |
|---|---|
| `/api/parse` | Parse document content and return structure |
| `/api/versions` | Create/manage document versions |
| `/api/versions/{id}` | Retrieve version history |
| `/api/compare` | Compare document versions |

## Architecture

```text
Document
   ↓
Text extraction
   ↓
Heading parser
   ↓
Optional LLM-assisted structure extraction
   ↓
Validation
   ↓
Version manager
   ↓
SQLite / SQLAlchemy
   ↓
FastAPI
```

## Repository structure

```text
.
├── app/
│   ├── database.py
│   ├── models.py
│   ├── parser.py
│   ├── validator.py
│   ├── versioning.py
│   ├── llm.py
│   ├── routes.py
│   ├── schemas.py
│   ├── utils.py
│   └── main.py
├── tests/
├── requirements.txt
├── approach.md
└── README.md
```

## Run locally

```bash
git clone https://github.com/pallavi12-code/-Tri9T-AI_Assignment.git
cd -Tri9T-AI_Assignment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API documentation is available at `http://127.0.0.1:8000/docs` while the server is running.

## Tests

```bash
pytest
```

## Example parse request

```json
{
  "text": "INTRODUCTION\nMachine Learning Overview"
}
```

Example structured response:

```json
{
  "headings": [
    {"title": "INTRODUCTION", "level": 1}
  ],
  "valid": true,
  "warnings": []
}
```

## Tech stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- PyPDF
- Pytest
- Optional LLM integration

## Future improvements

- Add authentication and authorization
- Add PostgreSQL support
- Containerize the API
- Add broader document-format support
- Add deployment and observability

## Author

**Pallavi Reddy**  
Artificial Intelligence & Machine Learning Engineering Student, CBIT

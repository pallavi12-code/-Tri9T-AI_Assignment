# CT200 Document Parser API

This FastAPI service extracts headings from plain text and text-based PDFs,
reports heading validation warnings, and stores document versions in SQLite for
heading-level comparison.

## Architecture

Requests enter `app/main.py` and are routed through `app/routes.py`. The
`DocumentParser` extracts numbered, title-case, and uppercase headings.
`DocumentValidator` reports duplicate headings and skipped levels. Versions
are persisted with SQLAlchemy through a request-scoped session dependency, and
`VersionManager` compares their extracted heading structures.

## Setup and run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; interactive documentation is
at `/docs`. Set `DATABASE_URL` to use another SQLAlchemy-supported database.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Service status |
| GET | `/health` | Health status |
| POST | `/api/parse` | Parse JSON text into headings and validation results |
| POST | `/api/upload` | Parse an uploaded text-based PDF |
| POST | `/api/versions` | Create the next version for a document |
| GET | `/api/versions/{document_id}` | List stored versions |
| POST | `/api/compare?document_id=...&old_version=1&new_version=2` | Compare two stored versions |

Invalid file types return `415`, malformed PDFs return `400`, PDFs without
extractable text return `422`, missing versions return `404`, and invalid
request bodies return FastAPI's standard `422` response.

## Examples

Parse text:

```bash
curl -X POST http://127.0.0.1:8000/api/parse \
  -H 'content-type: application/json' \
  -d '{"text":"INTRODUCTION\n1. Background\nDetails"}'
```

Response:

```json
{
  "headings": [
    {"title": "INTRODUCTION", "level": 1},
    {"title": "Background", "level": 1}
  ],
  "valid": true,
  "warnings": []
}
```

Create and compare versions:

```bash
curl -X POST http://127.0.0.1:8000/api/versions \
  -H 'content-type: application/json' \
  -d '{"document_id":"manual-1","content":"INTRODUCTION"}'
curl -X POST http://127.0.0.1:8000/api/versions \
  -H 'content-type: application/json' \
  -d '{"document_id":"manual-1","content":"INTRODUCTION\nCONCLUSION"}'
curl -X POST 'http://127.0.0.1:8000/api/compare?document_id=manual-1&old_version=1&new_version=2'
```

## Testing

```bash
python -m pytest -q
```

GitHub Actions runs the same test command after installing `requirements.txt`.

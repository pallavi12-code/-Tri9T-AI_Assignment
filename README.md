# CT200 AI Document Parser & Versioning System

An AI-powered document processing system developed for the **Tri9T AI Engineering Internship Assignment**.

The system extracts document structure from PDFs, identifies heading hierarchy, validates document formatting, and maintains document versions with change tracking.

---

## 🚀 Features

### 1. PDF Document Processing

* Upload and process PDF documents
* Extract raw text from documents
* Convert unstructured documents into structured data

### 2. Intelligent Heading Extraction

* Detect document headings
* Identify heading levels (H1, H2, H3...)
* Generate structured JSON output

Example:

```json
{
  "headings": [
    {
      "title": "Introduction",
      "level": 1
    },
    {
      "title": "Overview",
      "level": 2
    }
  ]
}
```

---

### 3. Document Validation

The validation layer checks:

* Duplicate headings
* Incorrect heading hierarchy
* Skipped heading levels

Example:

```
H1
 |
 H2
 |
 H3   ✅ Valid


H1
 |
 H3   ❌ Skipped level
```

---

### 4. Version Management

The system supports:

* Creating document versions
* Maintaining version history
* Comparing document changes

Tracks:

* Added headings
* Removed headings
* Modified heading levels

Example:

```json
{
 "added": [
    "Conclusion"
 ],
 "removed": [],
 "changed": []
}
```

---

### 5. FastAPI REST API

Provides API endpoints for:

| Endpoint             | Description                |
| -------------------- | -------------------------- |
| `/api/parse`         | Extract document structure |
| `/api/versions`      | Create document version    |
| `/api/versions/{id}` | View version history       |
| `/api/compare`       | Compare versions           |

---

# 🏗️ Project Architecture

```
PDF Document

      |
      v

Text Extraction

      |
      v

Heading Parser

      |
      v

LLM Structure Extraction

      |
      v

Validation Layer

      |
      v

Version Manager

      |
      v

Database

      |
      v

FastAPI API
```

---

# 📂 Project Structure

```
CT200-AI-Parser

│
├── app/
│
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
│
├── tests/
│   ├── test_parser.py
│   └── test_validator.py
│
├── requirements.txt
├── approach.md
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

Clone repository:

```bash
git clone <your-github-link>
```

Move into project:

```bash
cd CT200-AI-Parser
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate:

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Application runs at:

```
http://127.0.0.1:8000
```

Swagger API documentation:

```
http://127.0.0.1:8000/docs
```

---

# 🧪 Running Tests

Run all tests:

```bash
pytest
```

Expected:

```
====================
passed
====================
```

---

# 📌 API Testing

## Parse Document

POST:

```
/api/parse
```

Request:

```json
{
"text":"INTRODUCTION\nMachine Learning Overview"
}
```

Response:

```json
{
"headings":[
 {
  "title":"INTRODUCTION",
  "level":1
 }
],
"valid":true,
"warnings":[]
}
```

---

## Create Version

POST:

```
/api/versions
```

Request:

```json
{
"document_id":"CT200",
"content":"Introduction"
}
```

---

## Compare Versions

POST:

```
/api/compare
```

Returns:

```json
{
"added":[],
"removed":[],
"changed":[]
}
```

---

# 🛠️ Technologies Used

## Backend

* Python
* FastAPI
* SQLAlchemy

## AI / NLP

* LLM Integration
* Prompt Engineering
* Structured JSON Extraction

## Database

* SQLite
* SQLAlchemy ORM

## Testing

* Pytest

## Development Tools

* Git
* GitHub
* VS Code

---

# Future Improvements

* Connect production LLM API
* Add PostgreSQL support
* Add authentication
* Add Docker deployment
* Add cloud hosting

---

# Author

**Pallavi Reddy**

Artificial Intelligence & Machine Learning Engineering Student

---

## Internship Assignment

Developed as part of the **Tri9T AI Engineering Internship Assignment (CT200)**.

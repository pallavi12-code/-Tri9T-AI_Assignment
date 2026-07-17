# Technical Approach — CT200 AI Document Parser

## 1. Problem Statement

The objective of this project is to build an AI-powered document processing system capable of extracting document structure from PDFs, validating heading hierarchy, and managing document versions.

---

# 2. System Architecture

The application follows a modular backend architecture.

```
PDF Document

      |
      v

Text Extraction Layer

      |
      v

Document Parser

      |
      v

LLM Structure Extraction

      |
      v

Validation Layer

      |
      v

Version Management

      |
      v

Database Storage

      |
      v

FastAPI REST API
```

---

# 3. PDF Processing

PDF documents are processed using PyPDF.

The extracted text is passed to the parser module for structure analysis.

---

# 4. Heading Extraction

The parser identifies:

* Heading titles
* Heading hierarchy
* Heading levels

The output is converted into structured JSON format.

Example:

```json
{
 "title":"Introduction",
 "level":1
}
```

---

# 5. Validation System

The validation layer checks:

## Duplicate Headings

Detects repeated heading names.

## Skipped Heading Levels

Detects invalid hierarchy:

```
H1
 |
 H3
```

---

# 6. Version Management

The system maintains multiple document versions.

Each version stores:

* Document ID
* Version number
* Content
* Timestamp

The comparison engine identifies:

* Added headings
* Removed headings
* Changed headings

---

# 7. Database Design

SQLite database with SQLAlchemy ORM is used.

Main table:

```
DocumentVersion

id
document_id
version
content
created_at
```

---

# 8. API Layer

FastAPI provides REST endpoints:

| Endpoint           | Purpose          |
| ------------------ | ---------------- |
| POST /parse        | Parse document   |
| POST /upload       | Upload PDF       |
| POST /versions     | Create version   |
| GET /versions/{id} | Version history  |
| POST /compare      | Compare versions |

---

# 9. Testing Strategy

Unit tests cover:

* Parser functionality
* Validation rules
* Version comparison

Pytest is used as the testing framework.

---

# 10. Future Improvements

* Production LLM integration
* PostgreSQL deployment
* Authentication
* Docker support
* Cloud deployment

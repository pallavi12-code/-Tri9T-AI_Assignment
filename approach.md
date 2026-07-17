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
# Decision Log

## 1. What part of this system is most likely to silently give wrong results without erroring? How would you catch it?

The heading extraction/parser layer is the most likely component to silently produce incorrect results because PDFs have inconsistent formatting and a heading may be interpreted as normal text or vice versa. I would catch this using validation rules, unit tests with different document structures, and manual comparison of extracted headings against sample PDFs.

---

## 2. Where did you choose simplicity over correctness because of time? What would break first in production?
I chose a lightweight rule-based heading parser and simplified version comparison instead of implementing a more advanced document understanding model. In production, the parser would be the first component to fail on complex PDFs with tables, images, unusual layouts, or inconsistent heading styles.

---

## 3. Name one input you did not handle, and what your system does when it sees it.
One input I did not fully handle is scanned PDFs containing only images without selectable text. Currently, the PDF extraction step returns empty text or incomplete content. A production system would need OCR support before sending the document to the parser.

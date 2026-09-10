"""FastAPI routes for parsing, uploads, and document versioning."""

from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DocumentVersion
from app.parser import DocumentParser
from app.schemas import (
    CompareResponse,
    DocumentRequest,
    ParseResponse,
    UploadResponse,
    VersionCreate,
    VersionHistoryResponse,
    VersionResponse,
)
from app.validator import DocumentValidator
from app.versioning import VersionManager

router = APIRouter()
parser = DocumentParser()
validator = DocumentValidator()
version_manager = VersionManager()


def _parse(text: str) -> dict:
    headings = parser.extract_headings(text)
    validation = validator.validate(headings)
    return {
        "headings": headings,
        "valid": validation["valid"],
        "warnings": validation["warnings"],
    }


@router.post("/parse", response_model=ParseResponse)
def parse_document(request: DocumentRequest) -> dict:
    return _parse(request.text)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> dict:
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF files are supported")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded PDF is empty")

    try:
        reader = PdfReader(BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except (PdfReadError, OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Unable to read the PDF") from exc

    if not text:
        raise HTTPException(status_code=422, detail="The PDF contains no extractable text")
    return {"filename": filename, **_parse(text)}


@router.post(
    "/versions",
    response_model=VersionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_version(request: VersionCreate, db: Session = Depends(get_db)) -> DocumentVersion:
    latest = db.scalar(
        select(DocumentVersion.version)
        .where(DocumentVersion.document_id == request.document_id)
        .order_by(DocumentVersion.version.desc())
    )
    record = DocumentVersion(
        document_id=request.document_id,
        version=(latest or 0) + 1,
        content=request.content,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/versions/{document_id}", response_model=VersionHistoryResponse)
def get_history(document_id: str, db: Session = Depends(get_db)) -> dict:
    versions = db.scalars(
        select(DocumentVersion)
        .where(DocumentVersion.document_id == document_id)
        .order_by(DocumentVersion.version)
    ).all()
    return {"document_id": document_id, "versions": versions}


@router.post("/compare", response_model=CompareResponse)
def compare_versions(
    document_id: str,
    old_version: int = Query(..., ge=1),
    new_version: int = Query(..., ge=1),
    db: Session = Depends(get_db),
) -> dict:
    records = db.scalars(
        select(DocumentVersion).where(
            DocumentVersion.document_id == document_id,
            DocumentVersion.version.in_([old_version, new_version]),
        )
    ).all()
    by_version = {record.version: record for record in records}
    if old_version not in by_version or new_version not in by_version:
        raise HTTPException(status_code=404, detail="Requested version not found")

    return version_manager.compare(
        parser.extract_headings(by_version[old_version].content),
        parser.extract_headings(by_version[new_version].content),
    )

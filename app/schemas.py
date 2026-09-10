"""Pydantic request and response models for the public API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1_000_000)


class Heading(BaseModel):
    title: str
    level: int = Field(..., ge=1, le=6)


class ParseResponse(BaseModel):
    headings: list[Heading]
    valid: bool
    warnings: list[str]


class VersionCreate(BaseModel):
    document_id: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1, max_length=1_000_000)


class VersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: str
    version: int
    created_at: datetime


class VersionHistoryResponse(BaseModel):
    document_id: str
    versions: list[VersionResponse]


class CompareResponse(BaseModel):
    added: list[str]
    removed: list[str]
    changed: list[str]


class UploadResponse(ParseResponse):
    filename: str

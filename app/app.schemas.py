"""
Pydantic schemas for request and response validation.

Compatible with:
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x ORM Models

These schemas provide serialization/deserialization for API requests,
responses, nested document trees, version comparison, selections,
and QA generation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models import MatchType, SelectionStatus


# ==========================================================
# Base Schema
# ==========================================================


class ORMBase(BaseModel):
    """Base schema enabling ORM serialization."""

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Document Schemas
# ==========================================================


class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class DocumentResponse(ORMBase):
    id: int
    title: str
    created_at: datetime


# ==========================================================
# Document Version Schemas
# ==========================================================


class DocumentVersionCreate(BaseModel):
    document_id: int
    version_number: int
    source_filename: str


class DocumentVersionResponse(ORMBase):
    id: int
    document_id: int
    version_number: int
    source_filename: str
    uploaded_at: datetime
    root_node_id: Optional[int] = None


# ==========================================================
# Node Schemas
# ==========================================================


class NodeBase(BaseModel):
    heading: str
    level: int
    order_index: int
    content_text: str
    content_hash: str
    structural_path: str


class NodeCreate(NodeBase):
    version_id: int
    parent_id: Optional[int] = None


class NodeSummary(ORMBase):
    id: int
    heading: str
    level: int
    structural_path: str


class NodeResponse(ORMBase):
    id: int
    version_id: int
    parent_id: Optional[int]

    heading: str
    level: int
    order_index: int

    content_text: str
    content_hash: str
    structural_path: str

    children: list["NodeResponse"] = Field(default_factory=list)


NodeResponse.model_rebuild()


# ==========================================================
# Tree Response
# ==========================================================


class TreeResponse(BaseModel):
    document_id: int
    version_id: int
    root: NodeResponse


# ==========================================================
# Search Schemas
# ==========================================================


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    version_id: Optional[int] = None


class SearchResult(ORMBase):
    node_id: int
    heading: str
    structural_path: str
    score: float


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int


# ==========================================================
# Browse API
# ==========================================================


class TopLevelSection(ORMBase):
    id: int
    heading: str
    level: int


class BrowseResponse(BaseModel):
    document_id: int
    version_id: int
    sections: list[TopLevelSection]


# ==========================================================
# Node Detail API
# ==========================================================


class NodeDetailResponse(NodeResponse):
    version: DocumentVersionResponse
  # ==========================================================
# Node Match Schemas
# ==========================================================


class NodeMatchResponse(ORMBase):
    id: int
    old_node_id: int | None
    new_node_id: int | None
    match_type: MatchType
    similarity_score: float
    matched_at: datetime


class VersionDiffResponse(BaseModel):
    node_id: int
    changed: bool
    match_type: MatchType | None = None
    similarity_score: float | None = None
    old_hash: str | None = None
    new_hash: str | None = None
    summary: str


# ==========================================================
# Selection Schemas
# ==========================================================


class SelectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    node_ids: list[int] = Field(..., min_length=1)
    version_id: int
    selected_by: str = Field(..., min_length=1, max_length=255)


class SelectionResponse(ORMBase):
    id: int
    node_id: int
    selected_by: str
    created_at: datetime
    status: SelectionStatus


class SelectionDetail(SelectionResponse):
    node: NodeSummary


# ==========================================================
# QA Reference Schemas
# ==========================================================


class QAReferenceResponse(ORMBase):
    id: int
    selection_id: int
    node_id: int
    mongo_doc_id: str
    is_stale: bool
    generated_at: datetime


# ==========================================================
# QA Generation Schemas
# ==========================================================


class TestCase(BaseModel):
    title: str
    objective: str
    preconditions: list[str]
    steps: list[str]
    expected_result: str
    requirement_reference: str


class GenerateQARequest(BaseModel):
    selection_id: int


class GenerateQAResponse(BaseModel):
    selection_id: int
    generated_at: datetime
    version_id: int
    test_cases: list[TestCase]


class RetrieveQAResponse(BaseModel):
    selection_id: int
    is_stale: bool
    generated_at: datetime
    test_cases: list[TestCase]


# ==========================================================
# Search / Filter
# ==========================================================


class SearchFilter(BaseModel):
    heading: str | None = None
    body: str | None = None
    version_id: int | None = None


# ==========================================================
# Generic API Responses
# ==========================================================


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


class HealthResponse(BaseModel):
    status: str
    database: str
    llm: str
    document_store: str


# ==========================================================
# Ingestion
# ==========================================================


class IngestResponse(BaseModel):
    document_id: int
    version_id: int
    title: str
    nodes_created: int
    processing_time_seconds: float


# ==========================================================
# Staleness
# ==========================================================


class StalenessResponse(BaseModel):
    selection_id: int
    is_stale: bool
    changed_nodes: list[int]
    message: str


# ==========================================================
# API Pagination
# ==========================================================


class Pagination(BaseModel):
    page: int = 1
    size: int = 20
    total: int


class PaginatedNodes(BaseModel):
    pagination: Pagination
    items: list[NodeSummary]
from pydantic import BaseModel
from typing import List



class DocumentRequest(BaseModel):

    text: str



class Heading(BaseModel):

    title: str

    level: int



class DocumentResponse(BaseModel):

    headings: List[Heading]
from pydantic import BaseModel


class VersionCreate(BaseModel):

    document_id: str

    content: str



class VersionCompare(BaseModel):

    old_version: int

    new_version: int
    valid: bool

    warnings: list
from pydantic import BaseModel

from datetime import datetime



class VersionCreate(BaseModel):

    document_id: str

    content: str



class VersionResponse(BaseModel):

    document_id: str

    version: int

    created_at: datetime



class CompareResponse(BaseModel):

    added: list

    removed: list

    changed: list

# app/models.py
"""SQLAlchemy ORM models.

Defines the relational schema described in the approved architecture:
Document -> DocumentVersion -> Node (self-referential tree), plus the
cross-version NodeMatch bridge table, Selection, and QAReference (the
SQLite-side pointer into the Mongo/JSON Q&A store).

All models inherit from `Base` (app.database) and use SQLAlchemy 2.x's
`Mapped` / `mapped_column` declarative style throughout.
"""

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.database import Base



class DocumentVersion(Base):

    __tablename__ = "document_versions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    document_id = Column(
        String,
        index=True
    )


    version = Column(
        Integer
    )


    content = Column(
        Text
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class MatchType(str, enum.Enum):
    """Classification of how a node relates across two document versions."""

    UNCHANGED = "unchanged"
    MODIFIED = "modified"
    ADDED = "added"
    DELETED = "deleted"


class SelectionStatus(str, enum.Enum):
    """Lifecycle status of a user-created selection."""

    PENDING = "pending"
    GENERATED = "generated"
    STALE = "stale"


class Document(Base):
    """A logical document tracked across one or more parsed versions."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    versions: Mapped[list["DocumentVersion"]] = relationship(
        "DocumentVersion",
        back_populates="document",
        cascade="all, delete-orphan",
        foreign_keys="DocumentVersion.document_id",
        order_by="DocumentVersion.version_number",
    )

    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r})"


class DocumentVersion(Base):
    """A single parsed snapshot (version) of a Document."""

    __tablename__ = "document_versions"
    __table_args__ = (
        UniqueConstraint(
            "document_id", "version_number", name="uq_document_version_number"
        ),
        Index("ix_document_versions_document_id", "document_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    # Nullable + use_alter: root_node_id points into `nodes`, which itself
    # points back to `document_versions` via Node.version_id. use_alter
    # breaks the circular DDL dependency by adding this FK constraint in a
    # separate ALTER TABLE statement after both tables exist; post_update
    # on the relationship (below) tells the ORM to set this column in a
    # second UPDATE after the row insert, avoiding an insert-order deadlock.
    root_node_id: Mapped[int | None] = mapped_column(
        ForeignKey("nodes.id", use_alter=True, name="fk_version_root_node"),
        nullable=True,
    )

    document: Mapped["Document"] = relationship(
        "Document", back_populates="versions", foreign_keys=[document_id]
    )
    root_node: Mapped["Node | None"] = relationship(
        "Node",
        foreign_keys=[root_node_id],
        post_update=True,
        viewonly=False,
    )
    nodes: Mapped[list["Node"]] = relationship(
        "Node",
        back_populates="version",
        cascade="all, delete-orphan",
        foreign_keys="Node.version_id",
        order_by="Node.order_index",
    )

    def __repr__(self) -> str:
        return (
            f"DocumentVersion(id={self.id!r}, document_id={self.document_id!r}, "
            f"version_number={self.version_number!r})"
        )


class Node(Base):
    """A single node in a document version's hierarchical section tree."""

    __tablename__ = "nodes"
    __table_args__ = (
        Index("ix_nodes_version_id", "version_id"),
        Index("ix_nodes_parent_id", "parent_id"),
        Index("ix_nodes_structural_path", "structural_path"),
        Index("ix_nodes_content_hash", "content_hash"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version_id: Mapped[int] = mapped_column(
        ForeignKey("document_versions.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=True
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    heading: Mapped[str] = mapped_column(String(512), nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    structural_path: Mapped[str] = mapped_column(String(64), nullable=False)

    version: Mapped["DocumentVersion"] = relationship(
        "DocumentVersion", back_populates="nodes", foreign_keys=[version_id]
    )
    parent: Mapped["Node | None"] = relationship(
        "Node",
        remote_side=[id],
        back_populates="children",
        foreign_keys=[parent_id],
    )
    children: Mapped[list["Node"]] = relationship(
        "Node",
        back_populates="parent",
        cascade="all, delete-orphan",
        foreign_keys=[parent_id],
        order_by="Node.order_index",
    )
    selections: Mapped[list["Selection"]] = relationship(
        "Selection",
        back_populates="node",
        cascade="all, delete-orphan",
        foreign_keys="Selection.node_id",
    )
    matches_as_old: Mapped[list["NodeMatch"]] = relationship(
        "NodeMatch",
        back_populates="old_node",
        foreign_keys="NodeMatch.old_node_id",
        cascade="all, delete-orphan",
    )
    matches_as_new: Mapped[list["NodeMatch"]] = relationship(
        "NodeMatch",
        back_populates="new_node",
        foreign_keys="NodeMatch.new_node_id",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Node(id={self.id!r}, structural_path={self.structural_path!r}, "
            f"heading={self.heading!r})"
        )


class NodeMatch(Base):
    """Cross-version linkage between an old node and a new node.

    This is not a tree edge — it records how the versioning algorithm
    matched (or failed to match) nodes between two consecutive document
    versions. Exactly one of old_node_id / new_node_id is null for
    `added` / `deleted` matches; both are populated for `unchanged` and
    `modified` matches.
    """

    __tablename__ = "node_matches"
    __table_args__ = (
        Index("ix_node_matches_old_node_id", "old_node_id"),
        Index("ix_node_matches_new_node_id", "new_node_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    old_node_id: Mapped[int | None] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=True
    )
    new_node_id: Mapped[int | None] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=True
    )
    match_type: Mapped[MatchType] = mapped_column(
        SAEnum(MatchType, name="match_type_enum", native_enum=False, length=16),
        nullable=False,
    )
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    matched_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    old_node: Mapped["Node | None"] = relationship(
        "Node", back_populates="matches_as_old", foreign_keys=[old_node_id]
    )
    new_node: Mapped["Node | None"] = relationship(
        "Node", back_populates="matches_as_new", foreign_keys=[new_node_id]
    )

    def __repr__(self) -> str:
        return (
            f"NodeMatch(id={self.id!r}, match_type={self.match_type!r}, "
            f"old_node_id={self.old_node_id!r}, new_node_id={self.new_node_id!r})"
        )


class Selection(Base):
    """A user's selection of a node for Q&A generation."""

    __tablename__ = "selections"
    __table_args__ = (
        Index("ix_selections_node_id", "node_id"),
        Index("ix_selections_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    node_id: Mapped[int] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False
    )
    selected_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    status: Mapped[SelectionStatus] = mapped_column(
        SAEnum(
            SelectionStatus, name="selection_status_enum", native_enum=False, length=16
        ),
        nullable=False,
        default=SelectionStatus.PENDING,
    )

    node: Mapped["Node"] = relationship(
        "Node", back_populates="selections", foreign_keys=[node_id]
    )
    qa_reference: Mapped["QAReference | None"] = relationship(
        "QAReference",
        back_populates="selection",
        cascade="all, delete-orphan",
        uselist=False,
        foreign_keys="QAReference.selection_id",
    )

    def __repr__(self) -> str:
        return (
            f"Selection(id={self.id!r}, node_id={self.node_id!r}, "
            f"status={self.status!r})"
        )


class QAReference(Base):
    """SQLite-side pointer into the Mongo/JSON store for a generated Q&A payload.

    Keeps relational integrity (FK cascades, joins) on the SQL side while
    the variable-shape LLM output itself lives in the document store,
    referenced here by `mongo_doc_id`.
    """

    __tablename__ = "qa_references"
    __table_args__ = (
        UniqueConstraint("selection_id", name="uq_qa_reference_selection"),
        Index("ix_qa_references_node_id", "node_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    selection_id: Mapped[int] = mapped_column(
        ForeignKey("selections.id", ondelete="CASCADE"), nullable=False
    )
    node_id: Mapped[int] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False
    )
    mongo_doc_id: Mapped[str] = mapped_column(String(64), nullable=False)
    is_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    selection: Mapped["Selection"] = relationship(
        "Selection", back_populates="qa_reference", foreign_keys=[selection_id]
    )
    node: Mapped["Node"] = relationship("Node", foreign_keys=[node_id])

    def __repr__(self) -> str:
        return (
            f"QAReference(id={self.id!r}, selection_id={self.selection_id!r}, "
            f"is_stale={self.is_stale!r})"
        )
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.database import Base



class DocumentVersion(Base):

    __tablename__ = "document_versions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    document_id = Column(
        String,
        index=True
    )


    version = Column(
        Integer
    )


    content = Column(
        Text
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

"""
Utility functions for the Tri9T AI Engineering Internship project.

Shared helpers for:

- SHA256 content hashing
- Heading normalization
- Text normalization
- Structural path generation
- Tree traversal
- Lightweight text diff summaries
"""

from __future__ import annotations

import hashlib
import re
from difflib import SequenceMatcher
from typing import Iterable

from app.models import Node


# ==========================================================
# Hashing
# ==========================================================


def compute_content_hash(text: str) -> str:
    """
    Generate a stable SHA256 hash for node content.

    Used for:
    - change detection
    - staleness detection
    - version comparison
    """

    normalized = normalize_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


# ==========================================================
# Text Normalization
# ==========================================================


def normalize_text(text: str) -> str:
    """
    Normalize text before hashing or comparison.
    """

    text = text.replace("\r", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_heading(text: str) -> str:
    """
    Normalize headings for fuzzy matching.

    Example:

    "1.2 Blood Pressure"

    becomes

    "blood pressure"
    """

    text = text.lower()

    text = re.sub(r"^\d+(\.\d+)*", "", text)

    text = re.sub(r"[^a-z0-9 ]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# Structural Paths
# ==========================================================


def build_structural_path(parent_path: str | None, order: int) -> str:
    """
    Build deterministic structural paths.

    Examples

    Root

    0001

    Child

    0001/0003

    Grandchild

    0001/0003/0002
    """

    current = f"{order:04d}"

    if parent_path:
        return f"{parent_path}/{current}"

    return current


# ==========================================================
# Similarity
# ==========================================================


def similarity(a: str, b: str) -> float:
    """
    Compute similarity score.

    Returns float between 0 and 1.
    """

    return SequenceMatcher(
        None,
        normalize_text(a),
        normalize_text(b),
    ).ratio()


# ==========================================================
# Diff Summary
# ==========================================================


def diff_summary(old: str, new: str) -> str:
    """
    Produce a lightweight human-readable diff summary.
    """

    if old == new:
        return "No changes."

    ratio = similarity(old, new)

    if ratio > 0.95:
        return "Minor wording changes."

    if ratio > 0.75:
        return "Section modified."

    if ratio > 0.40:
        return "Major content updated."

    return "Content substantially changed."


# ==========================================================
# Tree Traversal
# ==========================================================


def walk_tree(root: Node) -> Iterable[Node]:
    """
    Depth-first traversal of a document tree.
    """

    yield root

    for child in root.children:
        yield from walk_tree(child)


# ==========================================================
# Heading Utilities
# ==========================================================


def is_heading(text: str) -> bool:
    """
    Heuristic heading detector.

    Used during PDF parsing.
    """

    text = text.strip()

    if len(text) > 120:
        return False

    if text.endswith("."):
        return False

    return True


# ==========================================================
# Safe String
# ==========================================================


def safe_strip(value: str | None) -> str:
    """
    Convert None to empty string and strip whitespace.
    """

    if value is None:
        return ""

    return value.strip()

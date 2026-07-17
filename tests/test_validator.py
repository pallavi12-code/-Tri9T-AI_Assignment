import pytest

from app.validator import DocumentValidator
from app.utils import create_heading



def test_duplicate_heading_detection():

    headings = [

        create_heading(
            "Introduction",
            1
        ),

        create_heading(
            "Introduction",
            1
        )

    ]


    validator = DocumentValidator()

    result = validator.validate(headings)


    assert result["valid"]


    assert (
        "Duplicate heading detected: Introduction"
        in result["warnings"]
    )



def test_skipped_heading_detection():

    headings = [

        create_heading(
            "Introduction",
            1
        ),

        create_heading(
            "Details",
            3
        )

    ]


    validator = DocumentValidator()


    result = validator.validate(headings)


    assert (
        "Skipped heading level before Details (H3)"
        in result["warnings"]
    )



def test_valid_heading_structure():

    headings = [

        create_heading(
            "Introduction",
            1
        ),

        create_heading(
            "Overview",
            2
        ),

        create_heading(
            "Conclusion",
            1
        )

    ]


    validator = DocumentValidator()


    result = validator.validate(headings)


    assert result["valid"]



def test_duplicate_helper():

    headings = [

        create_heading(
            "AI",
            1
        ),

        create_heading(
            "AI",
            2
        )

    ]


    validator = DocumentValidator()


    assert validator.has_duplicate(
        headings,
        "AI"
    ) 

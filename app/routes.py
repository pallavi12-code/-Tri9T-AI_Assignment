from fastapi import APIRouter

from app.llm import LLMService
from app.validator import DocumentValidator

from app.schemas import (
    DocumentRequest,
    DocumentResponse
)


router = APIRouter()


llm = LLMService()

validator = DocumentValidator()



@router.post(
    "/parse",
    response_model=DocumentResponse
)
def parse_document(
    request: DocumentRequest
):


    result = llm.extract_structure(
        request.text
    )


    headings = result["headings"]


    validation = validator.validate(
        headings
    )


    return {

        "headings": headings,

        "valid":
        validation["valid"],

        "warnings":
        validation["warnings"]

    }

"""
API routes for CT200 document parser.
"""


from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)


from app.parser import DocumentParser

from app.validator import DocumentValidator

from app.versioning import VersionManager

from app.llm import LLMService

from app.schemas import (
    DocumentRequest,
    VersionCreate
)


from pypdf import PdfReader

from io import BytesIO



router = APIRouter()



parser = DocumentParser()

validator = DocumentValidator()

version_manager = VersionManager()

llm = LLMService()



# Temporary storage
# Later replaced by database persistence

documents = {}



# -----------------------------
# Parse Text Document
# -----------------------------


@router.post("/parse")
def parse_document(
        request: DocumentRequest
):


    headings = parser.extract_headings(
        request.text
    )


    validation = validator.validate(
        headings
    )


    return {


        "headings":
        headings,


        "valid":
        validation["valid"],


        "warnings":
        validation["warnings"]

    }





# -----------------------------
# Upload PDF
# -----------------------------


@router.post("/upload")
async def upload_pdf(
        file: UploadFile = File(...)
):


    if not file.filename.endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="Only PDF files allowed"

        )


    content = await file.read()



    try:

        reader = PdfReader(
            BytesIO(content)
        )


        text = ""


        for page in reader.pages:

            text += (
                page.extract_text()
                or ""
            )


    except Exception:


        raise HTTPException(

            status_code=400,

            detail="Invalid PDF"

        )



    headings = parser.extract_headings(
        text
    )


    validation = validator.validate(
        headings
    )



    return {


        "filename":
        file.filename,


        "headings":
        headings,


        "warnings":
        validation["warnings"]

    }





# -----------------------------
# Create Version
# -----------------------------


@router.post("/versions")
def create_version(
        request: VersionCreate
):


    doc_id = request.document_id



    if doc_id not in documents:

        documents[doc_id] = []



    version = len(
        documents[doc_id]
    ) + 1



    documents[doc_id].append(

        {

            "version":
            version,


            "content":
            request.content

        }

    )


    return {


        "document_id":
        doc_id,


        "version":
        version

    }





# -----------------------------
# Version History
# -----------------------------


@router.get(
    "/versions/{document_id}"
)
def get_history(
        document_id:str
):


    return {


        "document_id":
        document_id,


        "versions":
        documents.get(
            document_id,
            []
        )

    }





# -----------------------------
# Compare Versions
# -----------------------------


@router.post("/compare")
def compare_versions(

        document_id:str,

        old_version:int,

        new_version:int

):


    if document_id not in documents:

        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )



    versions = documents[document_id]



    old_doc = versions[
        old_version - 1
    ]


    new_doc = versions[
        new_version - 1
    ]



    old_structure = parser.extract_headings(

        old_doc["content"]

    )


    new_structure = parser.extract_headings(

        new_doc["content"]

    )



    comparison = version_manager.compare(

        old_structure,

        new_structure

    )


    return comparison

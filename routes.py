from fastapi import Depends

from app.versioning import VersionManager


version_manager = VersionManager()



versions = {}



@router.post(
    "/versions"
)
def create_version(
    request: VersionCreate
):


    doc_id = request.document_id


    if doc_id not in versions:

        versions[doc_id] = []



    new_version = (
        len(versions[doc_id])
        + 1
    )


    versions[doc_id].append(

        {
            "version":
            new_version,

            "content":
            request.content
        }

    )


    return {

        "document_id":
        doc_id,

        "version":
        new_version

    }





@router.get(
    "/versions/{document_id}"
)
def history(
    document_id:str
):


    return {

        "document_id":
        document_id,


        "versions":
        versions.get(
            document_id,
            []
        )

    }




@router.post(
    "/compare"
)
def compare_versions(
    document_id:str,
    old_version:int,
    new_version:int
):


    docs = versions.get(
        document_id,
        []
    )


    old_doc = docs[
        old_version-1
    ]


    new_doc = docs[
        new_version-1
    ]



    old_structure = (
        llm.extract_structure(
            old_doc["content"]
        )
    )


    new_structure = (
        llm.extract_structure(
            new_doc["content"]
        )
    )



    return version_manager.compare(

        old_structure["headings"],

        new_structure["headings"]

    )

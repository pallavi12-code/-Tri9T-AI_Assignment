"""
Main FastAPI application.

Starts the CT200 AI Document Parser API.
"""


from fastapi import FastAPI

from app.routes import router

from app.database import Base, engine

from app import models



# Create database tables

Base.metadata.create_all(
    bind=engine
)



app = FastAPI(

    title="CT200 AI Document Parser",

    description="""
    AI powered document parser with:
    
    - PDF text extraction
    - Heading detection
    - Validation
    - Version management
    
    """,

    version="1.0.0"

)



# Register routes

app.include_router(

    router,

    prefix="/api",

    tags=["Document Parser"]

)



@app.get("/")
def home():

    return {

        "application":
        "CT200 AI Document Parser",

        "status":
        "running"

    }



@app.get("/health")
def health_check():

    return {

        "status":
        "healthy"

    }

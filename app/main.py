"""Application entry point."""

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CT200 Document Parser",
    description="Parse document headings, validate structure, and compare versions.",
    version="1.0.0",
)
app.include_router(router, prefix="/api", tags=["Document Parser"])


@app.get("/")
def home() -> dict[str, str]:
    return {"application": "CT200 Document Parser", "status": "running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

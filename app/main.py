from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.models import PresentationRequest, SlideConfig, PresentationMetadata, PresentationCreatedResponse
from app.slide_generator import generate_presentation
from app.presentation_store import store, get_metadata
import os

app = FastAPI(title="Slide Generator API", version="1.0")

@app.post("/api/v1/presentations", response_model=PresentationCreatedResponse, summary="Create a new presentation")
def create_presentation(payload: PresentationRequest):
    """
    Generates a new .pptx presentation using GPT or custom content.
    """
    pres_id, file_path = generate_presentation(payload)
    return {
        "id": pres_id,
        "download_url": f"/api/v1/presentations/{pres_id}/download"
    }

@app.get("/api/v1/presentations/{id}", response_model=PresentationMetadata, summary="Get presentation metadata")
def get_presentation(id: str):
    """
    Fetches metadata (topic, config) for a specific presentation.
    """
    meta = get_metadata(id)
    if not meta:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return meta

@app.get(
    "/api/v1/presentations/{id}/download",
    summary="Download .pptx file (hidden from Swagger UI)",
    response_class=FileResponse,
    include_in_schema=False  # avoid Swagger rendering issue
)
def download_presentation(id: str):
    """
    Returns the .pptx file as a binary download.
    """
    meta = get_metadata(id)
    if not meta or not os.path.exists(meta["file_path"]):
        raise HTTPException(status_code=404, detail="Presentation not found or file missing")

    return FileResponse(
        path=meta["file_path"],
        filename=f"{id}.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

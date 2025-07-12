from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import FileResponse
from anyio import to_thread
from app.models.models import PresentationRequest, SlideConfig, PresentationMetadata, PresentationCreatedResponse
from app.utils.slide_generator import generate_presentation
from app.stores.presentation_store import get_metadata
from app.utils.auth import get_current_user
from app.utils.limiter import limiter
import os

router = APIRouter()

@router.post("", response_model=PresentationCreatedResponse)
@limiter.limit("1/hour")
async def create_presentation(payload: PresentationRequest, request: Request, user_id: str = Depends(get_current_user)):
    pres_id, file_path = await to_thread.run_sync(generate_presentation, payload)
    return {"id": pres_id, "download_url": f"/api/v1/presentations/{pres_id}/download"}

@router.get("/{id}", response_model=PresentationMetadata)
@limiter.limit("1/minute")
async def get_presentation(id: str, request: Request, user_id: str = Depends(get_current_user)):
    meta = await to_thread.run_sync(get_metadata, id)
    if not meta:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return meta

@router.get("/{id}/download", response_class=FileResponse)
@limiter.limit("1/minute")
async def download_presentation(id: str, request: Request):
    meta = await to_thread.run_sync(get_metadata, id)
    if not meta or not os.path.exists(meta["file_path"]):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(meta["file_path"], filename=f"{id}.pptx")

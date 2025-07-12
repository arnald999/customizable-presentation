from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.requests import Request
from fastapi import Header, HTTPException, Request, Depends
from app.user_store import get_or_create_user_id
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.models import PresentationRequest, SlideConfig, PresentationMetadata, PresentationCreatedResponse
from app.slide_generator import generate_presentation
from app.presentation_store import store, get_metadata
from app.auth import get_current_user
import os

# def get_current_user(request: Request, x_api_key: str = Header(...)):
#     user_id = get_or_create_user_id(x_api_key)
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Invalid or missing API key")
    
#     request.state.user_id = user_id
#     return user_id

# Create limiter
"""API rate limiting by anyone"""
# limiter = Limiter(key_func=get_remote_address)

def user_key_func(request: Request):
    return getattr(request.state, "user_id", "anonymous")

"""API rate limiting per user"""
limiter = Limiter(key_func=user_key_func)

# Create FastAPI app with middleware
app = FastAPI(title="Slide Generator API", version="1.0")
app.state.limiter = limiter

# Attach rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Try again later."},
    )

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": exc.status_code}
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


@app.post("/api/v1/presentations", response_model=PresentationCreatedResponse, summary="Create a new presentation")
@limiter.limit("1/hour")
def create_presentation(payload: PresentationRequest, request: Request, user_id: str = Depends(get_current_user)):
    """
    Generates a new .pptx presentation using GPT or custom content.
    """
    try:
        pres_id, file_path = generate_presentation(payload)
        return {
            "id": pres_id,
            "download_url": f"/api/v1/presentations/{pres_id}/download"
        }
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected server error")
        

@app.get("/api/v1/presentations/{id}", response_model=PresentationMetadata, summary="Get presentation metadata")
@limiter.limit("1/minute")
def get_presentation(id: str, request: Request, user_id: str = Depends(get_current_user)):
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
@limiter.limit("1/minute")
def download_presentation(id: str, request: Request, user_id: str = Depends(get_current_user)):
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

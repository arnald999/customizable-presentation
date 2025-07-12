from pydantic import BaseModel
from typing import List, Optional

### Request Models

class SlideConfig(BaseModel):
    num_slides: int = 5
    font: Optional[str] = "Arial"
    color_theme: Optional[str] = "blue"

class PresentationRequest(BaseModel):
    topic: str
    custom_content: Optional[str] = None
    config: SlideConfig

### Response Models

class PresentationMetadata(BaseModel):
    topic: str
    config: SlideConfig

class PresentationCreatedResponse(BaseModel):
    id: str
    download_url: str
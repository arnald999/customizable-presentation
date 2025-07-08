from pydantic import BaseModel
from typing import List, Optional

class SlideConfig(BaseModel):
    num_slides: int = 5
    font: Optional[str] = "Arial"
    color_theme: Optional[str] = "blue"

class PresentationRequest(BaseModel):
    topic: str
    custom_content: Optional[str] = None
    config: SlideConfig

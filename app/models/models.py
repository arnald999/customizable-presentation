from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


### Request Models
class LLMModel(str, Enum):
    mistral = "mistral"
    llama3 = "llama3"
    gpt4 = "gpt4"
    gemma = "gemma"

class SlideConfig(BaseModel):
    num_slides: int = Field(..., ge=1, le=20, description="Number of slides (1 to 20)")
    font: Optional[str] = "Arial"
    color_theme: Optional[str] = "#0D47A1"
    llm_model: LLMModel = LLMModel.mistral

class SlideStyleConfig(BaseModel):
    font: Optional[str] = "Arial"
    color_theme: Optional[str] = "#0D47A1"
    llm_model: LLMModel = LLMModel.mistral

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
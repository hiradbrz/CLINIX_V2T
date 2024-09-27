# backend/models.py
from pydantic import BaseModel
from typing import Optional, List

class TranscriptionRequest(BaseModel):
    email: str
    audio_file: str  # Base64 encoded string

class SummaryRequest(BaseModel):
    email: str
    transcription_text: str
    summary_type: str
    solution_types: List[str]

class SaveRequest(BaseModel):
    email: str
    summary: Optional[str] = None
    full_text: Optional[str] = None
    template: Optional[str] = None

class TemplateRequest(BaseModel):
    email: str
    template: str

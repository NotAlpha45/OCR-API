from pydantic import BaseModel


class OcrOutput(BaseModel):
    success: bool
    text: str
    processing_time_ms: float
    confidence: float


class ImageValidationOutput(BaseModel):
    is_valid: bool
    reason: str | None = None

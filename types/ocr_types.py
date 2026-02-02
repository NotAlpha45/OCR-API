from pydantic import BaseModel


class OcrOutput(BaseModel):
    texts: list[str]
    processing_time: float
    average_confidence: float

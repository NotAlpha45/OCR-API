from abc import ABC, abstractmethod
from data_types.ocr_types import OcrOutput


class BaseOcrService(ABC):
    """Abstract base class for OCR services."""

    @abstractmethod
    def extract_text(self, image_content: bytes) -> OcrOutput:
        """
        Extract text from image bytes.

        Args:
            image_content: Image data as bytes

        Returns:
            OcrOutput containing extracted text, confidence, and processing time
        """
        pass

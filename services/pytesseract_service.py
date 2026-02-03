import time
import json
from io import BytesIO
from PIL import Image
import pytesseract

from data_types.ocr_types import OcrOutput
from exceptions.ocr_exceptions import OcrConfigException
from services.base_ocr_service import BaseOcrService


try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise OcrConfigException("Configuration file 'config.json' not found.")
except json.JSONDecodeError:
    raise OcrConfigException("Configuration file 'config.json' contains invalid JSON.")


class PytesseractOcrService(BaseOcrService):
    """Pytesseract implementation of OCR service using Tesseract engine."""

    def __init__(self):
        # Verify tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise OcrConfigException(
                f"Tesseract is not installed or not found in PATH: {str(e)}"
            ) from e

    def extract_text(self, image_content: bytes) -> OcrOutput:

        start_time = time.time()

        try:
            # Convert bytes to PIL Image
            image = Image.open(BytesIO(image_content))

            # Get language configuration
            lang = config["TESSERACT"]["LANGUAGE"] or "eng"

            # Extract text with confidence data
            data = pytesseract.image_to_data(
                image, lang=lang, output_type=pytesseract.Output.DICT
            )

            # Filter out empty text and calculate average confidence
            confidences = [
                float(conf)
                for conf, text in zip(data["conf"], data["text"])
                if text.strip() and conf != "-1"
            ]

            # Extract full text
            text = pytesseract.image_to_string(image, lang=lang).strip()

            processing_time_ms = (time.time() - start_time) * 1000

            if not text:
                return OcrOutput(
                    success=False,
                    text="",
                    processing_time_ms=processing_time_ms,
                    confidence=0.0,
                )

            average_confidence = (
                sum(confidences) / len(confidences) / 100.0 if confidences else 0.0
            )

            return OcrOutput(
                success=True,
                text=text,
                processing_time_ms=processing_time_ms,
                confidence=average_confidence,
            )

        except Exception as e:
            raise OcrConfigException(f"Failed to process image with Tesseract: {str(e)}")

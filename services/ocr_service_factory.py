import json
from services.base_ocr_service import BaseOcrService
from services.easyocr_service import EasyOcrService
from services.pytesseract_service import PytesseractOcrService
from exceptions.ocr_exceptions import OcrConfigException


try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise OcrConfigException("Configuration file 'config.json' not found.")
except json.JSONDecodeError:
    raise OcrConfigException("Configuration file 'config.json' contains invalid JSON.")


class OcrServiceFactory:
    """Factory class for creating OCR service instances based on configuration."""

    _service_instance: BaseOcrService | None = None

    @classmethod
    def get_service(cls) -> BaseOcrService:
        """
        Get the configured OCR service instance (singleton).

        Returns:
            BaseOcrService instance based on OCR_ENGINE configuration

        Raises:
            OcrConfigException: If OCR engine is not configured or unsupported
        """
        if cls._service_instance is not None:
            return cls._service_instance

        try:
            engine = config["OCR_ENGINE"].lower()
        except KeyError:
            raise OcrConfigException(
                "OCR_ENGINE not found in configuration file. "
                "Please specify 'easyocr' or 'tesseract'."
            )

        if engine == "easyocr":
            cls._service_instance = EasyOcrService()
        elif engine == "tesseract":
            cls._service_instance = PytesseractOcrService()
        else:
            raise OcrConfigException(
                f"Unsupported OCR engine: '{engine}'. "
                "Supported engines: 'easyocr', 'tesseract'."
            )

        return cls._service_instance

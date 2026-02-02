import time
import easyocr
import json

from data_types.ocr_types import OcrOutput
from exceptions.ocr_exceptions import OcrConfigException


try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise OcrConfigException("Configuration file 'config.json' not found.")
except json.JSONDecodeError:
    raise OcrConfigException("Configuration file 'config.json' contains invalid JSON.")


class OcrService:

    __easy_ocr_reader = None

    def __init__(self):
        if OcrService.__easy_ocr_reader is None:
            try:
                OcrService.__easy_ocr_reader = easyocr.Reader(
                    lang_list=config["EASY_OCR"]["LANGUAGES"],
                    gpu=config["EASY_OCR"]["GPU"],
                    model_storage_directory=config["EASY_OCR"][
                        "MODEL_STORAGE_DIRECTORY"
                    ],
                )
            except Exception as e:
                raise OcrConfigException(
                    f"Failed to initialize EasyOCR Reader: {str(e)}"
                ) from e

        self.__easy_ocr_reader = OcrService.__easy_ocr_reader

    def extract_text(self, image_content: bytes) -> OcrOutput:

        start_time = time.time()

        image_read_results = self.__easy_ocr_reader.readtext(
            image=image_content,
            batch_size=config["EASY_OCR"]["BATCH_SIZE"] or 1,
        )

        if not image_read_results:
            return OcrOutput(
                success=False,
                text="",
                processing_time_ms=(time.time() - start_time) * 1000,
                confidence=0.0,
            )

        text = "\n".join([text for (_, text, _) in image_read_results])
        confidences = [conf for (_, _, conf) in image_read_results]
        average_confidence = sum(confidences) / len(confidences)
        processing_time_ms = (time.time() - start_time) * 1000

        return OcrOutput(
            success=True,
            text=text,
            processing_time_ms=processing_time_ms,
            confidence=average_confidence,
        )

from time import time
import easyocr
import json

from exceptions.ocr_exceptions import OcrConfigException
from types.ocr_types import OcrOutput

with open("config.json", "r") as config_file:
    config = json.load(config_file)


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
                texts=[],
                processing_time=time.time() - start_time,
                average_confidence=0.0,
            )

        texts = [text for (_, text, _) in image_read_results]
        confidences = [conf for (_, _, conf) in image_read_results]
        average_confidence = sum(confidences) / len(confidences)
        processing_time = time.time() - start_time

        return OcrOutput(
            texts=texts,
            processing_time=processing_time,
            average_confidence=average_confidence,
        )

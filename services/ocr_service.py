from time import time
from typing import Dict
import easyocr
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)


class OcrService:

    __easy_ocr_reader = None

    def __init__(self):
        if OcrService.__easy_ocr_reader is None:
            OcrService.__easy_ocr_reader = easyocr.Reader(
                lang_list=config["EASY_OCR"]["LANGUAGES"],
                gpu=config["EASY_OCR"]["GPU"],
                model_storage_directory=config["EASY_OCR"]["MODEL_STORAGE_DIRECTORY"],
            )
        self.__easy_ocr_reader = OcrService.__easy_ocr_reader

    def extract_text(self, image_content: bytes) -> Dict[str, str | float]:

        start_time = time.time()

        image_read_results = self.__easy_ocr_reader.readtext(
            image=image_content,
            batch_size=config["EASY_OCR"]["BATCH_SIZE"] or 1,
        )

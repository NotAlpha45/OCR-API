import easyocr


class OcrService:
    __easy_ocr_reader = None

    def __init__(self):
        if OcrService.__easy_ocr_reader is None:
            OcrService.__easy_ocr_reader = easyocr.Reader(["en"], gpu=False)
        self.__easy_ocr_reader = OcrService.__easy_ocr_reader

class OcrConfigException(Exception):
    """Exception raised for errors in the OCR configuration."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

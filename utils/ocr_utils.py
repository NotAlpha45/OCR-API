from fastapi import UploadFile
import json
from data_types.ocr_types import ImageValidationOutput
from services.ocr_service import OcrConfigException
from PIL import Image, UnidentifiedImageError


try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise OcrConfigException("Configuration file 'config.json' not found.")
except json.JSONDecodeError:
    raise OcrConfigException("Configuration file 'config.json' contains invalid JSON.")


def validate_image_input(
    image_file: UploadFile, image_content: bytes
) -> ImageValidationOutput:

    # Check file size
    try:
        max_size_bytes = config["MAX_FILE_SIZE_BYTES"]
    except KeyError:
        raise OcrConfigException("MAX_FILE_SIZE_BYTES not found in configuration file.")

    if len(image_content) > max_size_bytes:
        return ImageValidationOutput(
            is_valid=False,
            reason=f"File size exceeds the maximum limit of {max_size_bytes} bytes.",
        )

    # Check file format
    try:
        allowed_formats = config["ALLOWED_FORMATS"]
    except KeyError:
        raise OcrConfigException("ALLOWED_FORMATS not found in configuration file.")

    if image_file.content_type not in allowed_formats:
        return ImageValidationOutput(
            is_valid=False,
            reason=f"Invalid file format. Allowed formats: {', '.join(allowed_formats)}.",
        )

    # Check image file integrity
    try:
        Image.open(image_file.file).verify()
    except (UnidentifiedImageError, IOError):
        return ImageValidationOutput(
            is_valid=False,
            reason="The uploaded file is not a valid image or is corrupted.",
        )

    return ImageValidationOutput(is_valid=True, reason=None)

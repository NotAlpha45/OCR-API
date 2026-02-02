from fastapi import APIRouter, File, HTTPException, UploadFile

from data_types.ocr_types import OcrOutput
from exceptions.ocr_exceptions import OcrConfigException
from services.ocr_service import OcrService
from utils.ocr_utils import (
    validate_image_input,
    validate_image_input,
)


ocr_router = APIRouter(prefix="/ocr", tags=["OCR"])
ocr_service = OcrService()


@ocr_router.post("/extract-text")
async def extract_text(image_file: UploadFile = File(...)) -> OcrOutput:
    """
    Extract text from uploaded image using OCR.

    Args:
        file: image file (max 10MB, allowed formats: jpg, jpeg, png, jfif)
    """
    image_content = await image_file.read()

    try:
        image_validation_output = validate_image_input(image_file, image_content)
        if not image_validation_output.is_valid:
            raise HTTPException(
                status_code=400,
                detail=image_validation_output.reason,
            )

    except OcrConfigException as e:
        return HTTPException(
            status_code=500,
            detail=e.message,
        )

    ocr_output = ocr_service.extract_text(image_content)

    return ocr_output

from fastapi import APIRouter, File, UploadFile

from services.ocr_service import OcrService


ocr_router = APIRouter(prefix="/ocr", tags=["OCR"])
ocr_service = OcrService()


@ocr_router.post("/extract-text")
async def extract_text(image_file: UploadFile = File(...)):
    """
    Extract text from uploaded image using OCR.

    Args:
        file: image file (max 10MB, allowed formats: jpg, jpeg, png, jfif)
    """
    image_content = await image_file.read()
    ocr_output = ocr_service.extract_text(image_content)
    return ocr_output

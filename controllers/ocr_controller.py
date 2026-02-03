import json
from fastapi import APIRouter, File, HTTPException, UploadFile, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from data_types.ocr_types import OcrOutput
from exceptions.ocr_exceptions import OcrConfigException
from services.ocr_service_factory import OcrServiceFactory
from utils.ocr_utils import (
    validate_image_input,
    validate_image_input,
)


# Load configuration
try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise OcrConfigException("Configuration file 'config.json' not found.")
except json.JSONDecodeError:
    raise OcrConfigException("Configuration file 'config.json' contains invalid JSON.")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

ocr_router = APIRouter(prefix="/ocr", tags=["OCR"])


@ocr_router.post("/extract-text")
@limiter.limit(
    f"{config['RATE_LIMIT']['REQUESTS_PER_MINUTE']}/minute;{config['RATE_LIMIT']['REQUESTS_PER_HOUR']}/hour"
    if config.get("RATE_LIMIT", {}).get("ENABLED", False)
    else "1000000/minute"  # Effectively unlimited if disabled
)
async def extract_text(request: Request, image_file: UploadFile = File(...)) -> OcrOutput:
    """
    Extract text from uploaded image using OCR.

    Args:
        request: FastAPI request object (required for rate limiting)
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

    # Get OCR service from factory (based on config)
    try:
        ocr_service = OcrServiceFactory.get_service()
    except OcrConfigException as e:
        raise HTTPException(
            status_code=500,
            detail=e.message,
        )

    ocr_output = ocr_service.extract_text(image_content)

    return ocr_output

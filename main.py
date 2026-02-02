from fastapi import FastAPI
from controllers.ocr_controller import ocr_router


app = FastAPI(
    title="OCR Image Text Extraction API",
    description="Extract text from JPG images using EasyOCR library.",
    version="1.0.0",
)


@app.get("/")
async def root():

    return {
        "message": "OCR Image Text Extraction API",
        "version": "1.0.0",
        "endpoints": {
            "/extract-text": "POST - Extract text from image",
            "/docs": "GET - API documentation",
        },
    }


# Include the OCR router
app.include_router(ocr_router)

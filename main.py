from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from controllers.ocr_controller import ocr_router, limiter


app = FastAPI(
    title="OCR Image Text Extraction API",
    description="A simple API made to extract text from images using OCR technology. A scalable API that can use 2 different OCR engines: Tesseract and EasyOCR (And can be switched based on configuration).",
    version="1.0.0",
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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

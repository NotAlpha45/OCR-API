# OCR Image Text Extraction API

A FastAPI-based OCR service that extracts text from images using pluggable OCR engines (EasyOCR or Tesseract). Built with a clean layered architecture and factory pattern for easy engine switching.

## Features

- 🔌 **Pluggable OCR Engines**: Switch between EasyOCR (deep learning, high accuracy) and Tesseract (lightweight, fast)
- 🏭 **Factory Pattern**: Clean architecture with abstract base classes
- ⚙️ **Configuration-Driven**: All settings managed via `config.json`
- 🐳 **Docker Support**: Production-ready containerization with Docker Compose
- 📦 **Modern Tooling**: Built with Python 3.12+ and `uv` package manager
- 🚀 **FastAPI**: Auto-generated OpenAPI docs, async support, type safety

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [Local Setup (uv)](#local-setup-uv)
  - [Docker Setup](#docker-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Implementation Details](#implementation-details)
- [OCR Engine Comparison](#ocr-engine-comparison)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Requirements

### Local Development
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- System dependencies (Linux/macOS):
  - For EasyOCR: `libglib2.0-0`, `libsm6`, `libgl1-mesa-glx`
  - For Tesseract: `tesseract-ocr`, `tesseract-ocr-eng`

### Docker
- Docker 20.10+
- Docker Compose 2.0+

## Installation

### Local Setup (uv)

**1. Install uv (if not already installed)**

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Clone the repository**

```bash
git clone https://github.com/NotAlpha45/OCR-API.git
cd OCR-API
```

**3. Install dependencies**

```bash
# Create virtual environment and install all dependencies
uv sync
```

**4. Configure OCR engine**

Edit `config.json` and set your preferred engine:
```json
{
  "OCR_ENGINE": "tesseract"  // or "easyocr"
}
```

**5. Run the application**

```bash
# Development mode (with auto-reload)
uv run fastapi dev

# Production mode
uv run fastapi run
```

Access the API at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Docker Setup

**1. Clone the repository**

```bash
git clone https://github.com/NotAlpha45/OCR-API.git
cd OCR-API
```

**2. Configure OCR engine**

Edit `config.json` to select your engine (see [Configuration](#configuration))

**3. Build and run**

```bash
# Build and start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

Access the API at http://localhost:8000

## Configuration

All settings are managed in `config.json`:

```json
{
  "OCR_ENGINE": "tesseract",           // "easyocr" or "tesseract"
  "MAX_FILE_SIZE_BYTES": 10485760,     // 10MB max file size
  "ALLOWED_FORMATS": [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/jfif"
  ],
  "EASY_OCR": {
    "LANGUAGES": ["en"],                // Language codes: ["en", "fr", "de"]
    "GPU": false,                       // Enable GPU acceleration
    "MODEL_STORAGE_DIRECTORY": "models/",
    "BATCH_SIZE": 2                     // Processing batch size
  },
  "TESSERACT": {
    "LANGUAGE": "eng"                   // Language code: "eng", "fra", "deu"
  }
}
```

### Switching OCR Engines

**Use Tesseract** (recommended for 512MB-1GB RAM):
```json
"OCR_ENGINE": "tesseract"
```

**Use EasyOCR** (recommended for 2GB+ RAM):
```json
"OCR_ENGINE": "easyocr"
```

After changing engines, restart the service:
```bash
# Docker
docker-compose restart

# Local
# Stop with Ctrl+C, then restart
uv run fastapi dev
```

## Usage

### Extract Text from Image

**Using cURL:**

```bash
    curl -X POST "http://localhost:8000/ocr/extract-text" \
    -H "accept: application/json" \
    -H "Content-Type: multipart/form-data" \
    -F "image_file=@/path/to/image.jpg"
```

**Using Python:**

```python
import requests

url = "http://localhost:8000/ocr/extract-text"
files = {"image_file": open("image.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

**Using JavaScript (Fetch API):**

```javascript
const formData = new FormData();
formData.append('image_file', fileInput.files[0]);

fetch('http://localhost:8000/ocr/extract-text', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

### Response Format

**Success Response:**

```json
{
  "success": true,
  "text": "Extracted text from the image",
  "processing_time_ms": 1250.5,
  "confidence": 0.92
}
```

**Error Response (Invalid File):**

```json
{
  "detail": "File size exceeds the maximum limit of 10485760 bytes."
}
```

## API Documentation

### Endpoints

#### `GET /`
Health check and API information.

**Response:**
```json
{
  "message": "OCR Image Text Extraction API",
  "version": "1.0.0",
  "endpoints": {
    "/extract-text": "POST - Extract text from image",
    "/docs": "GET - API documentation"
  }
}
```

#### `POST /ocr/extract-text`
Extract text from uploaded image.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: `image_file` (file, required)
  - Max size: 10MB
  - Formats: JPEG, JPG, PNG, JFIF

**Response:** `OcrOutput`
```typescript
{
  success: boolean;          // Operation success status
  text: string;              // Extracted text (may contain \n)
  processing_time_ms: float; // Processing duration in milliseconds
  confidence: float;         // Average confidence (0.0 - 1.0)
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid file (format, size, or corrupted)
- `500`: Server error (configuration or processing error)

#### `GET /docs`
Interactive API documentation (Swagger UI).

#### `GET /redoc`
Alternative API documentation (ReDoc).

## Implementation Details

### Architecture Overview

```
OCR-API/
├── controllers/          # API route handlers
│   └── ocr_controller.py
├── services/            # Business logic layer
│   ├── base_ocr_service.py        # Abstract base class
│   ├── easyocr_service.py         # EasyOCR implementation
│   ├── pytesseract_service.py     # Tesseract implementation
│   └── ocr_service_factory.py     # Factory pattern
├── utils/               # Utilities (validation)
│   └── ocr_utils.py
├── data_types/          # Pydantic models
│   └── ocr_types.py
├── exceptions/          # Custom exceptions
│   └── ocr_exceptions.py
├── models/              # EasyOCR pre-trained models
├── config.json          # Configuration
└── main.py             # FastAPI application
```

### Design Patterns

**1. Factory Pattern** (`OcrServiceFactory`)
- Instantiates the correct OCR service based on `config.json > OCR_ENGINE`
- Allows runtime engine switching without code changes

**2. Singleton Pattern**
- Each OCR service uses class-level instances
- EasyOCR Reader (~1GB) initialized only once
- Tesseract engine shared across requests

**3. Layered Architecture**
- **Controllers**: HTTP request handling, validation
- **Services**: Core OCR processing logic
- **Utils**: Shared helper functions
- **Data Types**: Type-safe request/response models

### Data Flow

```
1. Client uploads image → POST /ocr/extract-text
2. Controller receives UploadFile → Reads bytes
3. Utils validate image → Size, format, integrity (PIL)
4. Factory selects service → Based on config.json
5. Service processes image → OCR engine extracts text
6. Returns OcrOutput → JSON with text, confidence, timing
```

### Key Implementation Details

**Configuration Loading Pattern** (used across all modules):
```python
try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise OcrConfigException("Configuration file 'config.json' not found.")
except json.JSONDecodeError:
    raise OcrConfigException("Configuration file contains invalid JSON.")
```

**Image Validation** (controllers/ocr_utils.py):
- File size check (max 10MB)
- MIME type validation
- PIL integrity verification (`Image.open().verify()`)

**Exception Handling**:
- `OcrConfigException` → 500 HTTP errors
- Validation failures → 400 HTTP errors
- All exceptions converted to HTTPException in controller

## OCR Engine Comparison

| Feature | EasyOCR | Tesseract |
|---------|---------|-----------|
| **Accuracy** | ⭐⭐⭐⭐⭐ (90-95%) | ⭐⭐⭐⭐ (80-90%) |
| **Speed** | Slower (2-5s) | Faster (0.5-1.5s) |
| **Memory** | 1.5-2GB RAM | 300-500MB RAM |
| **Technology** | Deep Learning (CNN) | Rule-based + LSTM |
| **Best For** | Complex text, handwriting, photos | Clean printed text, scans |
| **GPU Support** | ✅ Yes | ❌ No |
| **Model Size** | ~140MB | ~10MB |
| **Startup Time** | 10-15s (model loading) | <1s |

**When to use EasyOCR:**
- Handwritten text recognition
- Complex backgrounds or low-quality images
- Multi-language mixed text
- GPU available (significant speedup)

**When to use Tesseract:**
- Clean scanned documents or screenshots
- Limited memory (512MB-1GB instances)
- High throughput required
- Simple printed text

## Deployment

### Memory Requirements

| Configuration | Minimum RAM | Recommended RAM |
|---------------|-------------|-----------------|
| Tesseract only | 512MB | 1GB |
| EasyOCR | 1.5GB | 2-4GB |

### Cloud Provider Recommendations

**Free Tier Options for EasyOCR (2GB+ RAM needed):**

1. **Oracle Cloud Always Free** ⭐ **BEST**
   - Ampere A1: 4 OCPUs + 24GB RAM (always free)
   - Recommended: 2 OCPUs + 12GB RAM
   -永久免费 (permanent free tier)

2. **Google Cloud Platform**
   - $300 credit (90 days)
   - Use e2-medium (4GB RAM) during trial

3. **AWS Free Tier**
   - t2.micro (1GB RAM, marginal for Tesseract)
   - 12-month free tier

**For Tesseract (512MB-1GB RAM):**
- Any budget VPS provider (DigitalOcean, Linode, Vultr)
- Render, Railway (with paid plans)

### Production Checklist

- [ ] Set `OCR_ENGINE` based on memory constraints
- [ ] Configure `MAX_FILE_SIZE_BYTES` for your use case
- [ ] Set `GPU: true` if GPU available (EasyOCR only)
- [ ] Use volume mounts for models directory (Docker)
- [ ] Enable health checks (included in docker-compose.yml)
- [ ] Set up reverse proxy (nginx/Traefik) for HTTPS
- [ ] Configure rate limiting (API Gateway or middleware)
- [ ] Monitor memory usage (especially with EasyOCR)

## Troubleshooting

### Common Issues

**1. "OCR_ENGINE not found in configuration file"**
- Ensure `config.json` has `"OCR_ENGINE": "tesseract"` or `"easyocr"`

**2. "Tesseract is not installed or not found in PATH"**
- Install tesseract: `apt-get install tesseract-ocr tesseract-ocr-eng`
- Windows: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

**3. Docker build fails with "exit code: 127"**
- Verify `uv.lock` is committed to repository
- Run `uv lock` locally if missing

**4. Out of Memory (OOM) errors with EasyOCR**
- Switch to Tesseract: `"OCR_ENGINE": "tesseract"`
- Reduce batch size: `"BATCH_SIZE": 1`
- Upgrade to 2GB+ RAM instance

**5. Low confidence scores**
- Ensure image quality is good (>300 DPI for scans)
- Try switching OCR engines
- Preprocess images (deskew, denoise) before upload

**6. "Model not found" error (EasyOCR)**
- Ensure `models/` directory exists with `.pth` files
- Download models: https://github.com/JaidedAI/EasyOCR#models

### Development Tips

**View logs (Docker):**
```bash
docker-compose logs -f ocr-api
```

**Rebuild after config changes:**
```bash
docker-compose down
docker-compose up --build
```

**Test endpoint:**
```bash
curl http://localhost:8000/
```

**Update dependencies:**
```bash
# Add new package
uv add <package-name>

# Sync dependencies
uv sync

# Regenerate requirements.txt for Docker
uv pip compile pyproject.toml -o requirements.txt
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/NotAlpha45/OCR-API/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NotAlpha45/OCR-API/discussions)

---

Built with ❤️ using FastAPI, EasyOCR, and Tesseract
# Use Python 3.12.4 slim as base image
FROM python:3.12.4-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for EasyOCR and image processing
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy application code
COPY . .

# Create directory for EasyOCR models (optional, helps with caching)
RUN mkdir -p /root/.EasyOCR/model

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
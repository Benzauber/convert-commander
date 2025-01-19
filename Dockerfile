# Base image
FROM python:3.9-slim

# Environment variables to avoid interactive prompts
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Create the working directory in the container
WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice\
    ffmpeg \
    pandoc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create folders for uploads and conversions
RUN mkdir -p ./uploads ./convert

# Make scripts executable
RUN chmod +x create-alias.sh tokenapi.sh

# Default command when the container starts
CMD ["python3", "index.py"]

# Use the official Python image as a base
FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . .

# Install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libssl-dev \
        libffi-dev \
        python3-dev \
        build-essential \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to run the Python script
CMD ["python", "app.py"]

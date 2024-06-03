# Use the official Python image as a base
FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

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

# Install pymongo package
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code to the container image
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Command to run the Python script
CMD ["python", "app.py"]

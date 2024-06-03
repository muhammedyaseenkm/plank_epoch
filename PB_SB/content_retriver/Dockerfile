# Use an appropriate multi-platform base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Set a custom cache directory
ENV PIP_CACHE_DIR=/custom_cache_dir

# Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Install Python dependencies using the custom cache directory
RUN pip install --cache-dir $PIP_CACHE_DIR -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run your Python application
CMD ["python", "test.py"]

# Use Python 3.12 image as base
FROM python:3.12

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libgl1-mesa-dev \
        libglib2.0-0 \
        libsm6 \
        libxrender-dev \
        libxext6 \
        git

# Install Microsoft C++ Build Tools (if needed)
# Note: Uncomment this section if Microsoft C++ Build Tools are required
 RUN apt-get install -y build-essential && \
     apt-get install -y wget && \
     wget https://aka.ms/vs/17/release/vs_buildtools.exe && \
     Start-Process -FilePath "vs_buildtools.exe" -ArgumentList '--quiet --wait --norestart --nocache --noUpdateInstaller --noRestart' -Wait -PassThru

# Set working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Start the application
CMD ["python", "main.py"]

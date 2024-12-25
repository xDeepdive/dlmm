# Use a Python base image
FROM python:3.11-slim

# Install system dependencies required for Chromium and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    chromium-browser \
    chromium-driver

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY . /app

# Command to run your Python script
CMD ["python", "dlmmbot.py"]

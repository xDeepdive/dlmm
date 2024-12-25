# Use a Python base image
FROM python:3.11-slim

# Install system dependencies required for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    chromium \
    chromium-driver

# Set environment variables for Chrome and ChromeDriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY . /app

# Run the Python script
CMD ["python", "dlmmbot.py"]

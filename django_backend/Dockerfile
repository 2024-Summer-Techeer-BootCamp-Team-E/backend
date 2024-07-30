# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies and required packages
RUN apt-get update && apt-get install -y \
    git \
    default-libmysqlclient-dev \
    build-essential \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    gnupg2 \
    curl \
    chromium \
    chromium-driver \
    pkg-config \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x /usr/bin/chromedriver

# Working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
#COPY . /app/

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# 소스 코드 복사
COPY . ./django_backend

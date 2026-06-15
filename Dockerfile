# Use Python 3.11
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY auth.py .
COPY templates ./templates
COPY static ./static

RUN ls -R /app

# Expose Render port
EXPOSE 10000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

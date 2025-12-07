# 1. Base Image: Lightweight Python
FROM python:3.9-slim

# 2. Work Directory: Where our app lives inside the container
WORKDIR /app

# 3. Install Linux dependencies needed for Python libraries (THE FIX)
# We install tools like 'gcc' and 'python3-dev', then immediately clean up.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the App Code
COPY . .

# 6. Network Setup: Cloud Run expects port 8080
EXPOSE 8080

# 7. The Start Command (with the security fixes)
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
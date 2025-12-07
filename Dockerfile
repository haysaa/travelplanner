# 1. Base Image: Lightweight Python
FROM python:3.9-slim

# 2. Work Directory: Where our app lives inside the container
WORKDIR /app

# 3. Install Dependencies (Copy this first for speed!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the App Code
COPY . .

# 5. Network Setup: Cloud Run expects port 8080
EXPOSE 8080

# 6. The Start Command
# We tell Streamlit to run on port 8080 and listen to "0.0.0.0" (all addresses)
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]

# ─────────────────────────────────────────────────────────────
# Dockerfile — AI Summarizer API (US8 / GL-8)
# ─────────────────────────────────────────────────────────────
# Packages the app into a portable container image.
#
# Build: docker build -t ai-summarizer-api .
# Run:   docker run -p 8000:8000 ai-summarizer-api
# ─────────────────────────────────────────────────────────────

# 1. Base image — small Linux with Python 3.11
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependency list and install (this layer is cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the project into the container
COPY . .

# 5. Tell Docker the app listens on port 8000
EXPOSE 8000

# 6. Start the app when the container runs
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
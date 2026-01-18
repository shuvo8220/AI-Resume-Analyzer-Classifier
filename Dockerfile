# --- Stage 1: Build Frontend (React/Next.js) ---
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend dependency files
COPY frontend/package*.json ./

# Install dependencies (Legacy peer deps to avoid conflicts)
RUN npm install --legacy-peer-deps

# Copy all frontend source code
COPY frontend/ ./

# Build the frontend (Creates 'out' folder)
RUN npm run build


# --- Stage 2: Build Backend & Serve (Python FastAPI) ---
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy backend requirements
COPY requirements.txt .

# 1. Install CPU-only PyTorch (Much smaller & faster download)
# This fixes the Timeout error by downloading ~150MB instead of 900MB
RUN pip install --default-timeout=3000 torch --index-url https://download.pytorch.org/whl/cpu

# 2. Install other dependencies with High Timeout
RUN pip install --default-timeout=3000 --no-cache-dir -r requirements.txt

# 3. Download SpaCy Model
RUN python -m spacy download en_core_web_sm

# Copy Backend Code
COPY backend ./backend
COPY main.py .

# Copy the Built Frontend from Stage 1 to Stage 2
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# Expose the port 8000
EXPOSE 8000

# Command to run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

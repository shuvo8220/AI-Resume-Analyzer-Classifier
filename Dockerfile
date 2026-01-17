# --- Stage 1: Build Frontend (React/Next.js) ---
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend dependency files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

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

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# --- CRITICAL FIX: Download SpaCy Model during BUILD time ---
RUN python -m spacy download en_core_web_sm

# Copy Backend Code
COPY backend ./backend
COPY main.py .

# Copy the Built Frontend from Stage 1 to Stage 2
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# Expose the port 8000
EXPOSE 8000

# Command to run the server (Hardcoded port 8000 ensures stability)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
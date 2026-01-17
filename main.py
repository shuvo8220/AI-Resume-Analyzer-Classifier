from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
from backend import parser, classifier

app = FastAPI(title="AI Resume Analyzer")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Logic
@app.on_event("startup")
def startup_event():
    try:
        import spacy
        spacy.load("en_core_web_sm")
    except:
        os.system("python -m spacy download en_core_web_sm")

    if not os.path.exists(classifier.MODEL_PATH):
        classifier.train_model()

# API Endpoint
@app.post("/api/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        raw_text = parser.extract_text_from_pdf(temp_filename)
        name, email, phone = parser.extract_details(raw_text)
        clean_text = parser.clean_text(raw_text)
        skills = parser.extract_skills_ai(clean_text)
        education = parser.extract_education(raw_text)
        experience_years, experience_level = parser.calculate_experience_smart(raw_text)
        role, confidence = classifier.predict(clean_text)
        
        return {
            "name": name, "email": email, "phone": phone, "skills": skills,
            "education": education,
            "experience_years": experience_years, "experience_level": experience_level,
            "classification": role, "confidence": confidence
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_filename): os.remove(temp_filename)

# --- ULTIMATE CSS FIX (MANUAL ROUTING) ---

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_OUT = BASE_DIR / "frontend" / "out"

# 1. Manually serve _next files to force correct Content-Type
@app.get("/_next/{path:path}")
async def serve_next_assets(path: str):
    file_path = FRONTEND_OUT / "_next" / path
    
    if file_path.exists() and file_path.is_file():
        # Force CSS MIME Type
        if file_path.suffix == ".css":
            return FileResponse(file_path, media_type="text/css")
        # Force JS MIME Type
        if file_path.suffix == ".js":
            return FileResponse(file_path, media_type="application/javascript")
            
        return FileResponse(file_path)
    
    return JSONResponse(status_code=404, content={"error": "File not found"})

# 2. Serve HTML Root
if FRONTEND_OUT.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_OUT), html=True), name="static")
else:
    print("\n❌ ERROR: 'frontend/out' directory missing. Please rebuild frontend.\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
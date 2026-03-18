from fastapi import FastAPI, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from analyzer import analyze
from pdf_parser import extract_text
from generator import generate_tailored_resume

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Temporary in-memory storage
session = {}

@app.get("/")
def root():
    return {"message": "ATS Resume Tool is running"}

@app.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    contents = await resume.read()
    resume_text = extract_text(contents)
    result = analyze(resume_text, job_description)
    
    # Store resume text for later use
    session["resume_text"] = resume_text
    session["missing_keywords"] = result.get("missing_keywords", [])
    
    return result

@app.post("/generate-resume")
async def generate_resume():
    resume_text = session.get("resume_text")
    missing_keywords = session.get("missing_keywords", [])
    
    if not resume_text:
        return {"error": "No resume found. Please analyze first."}
    
    tailored = generate_tailored_resume(resume_text, missing_keywords)
    return {"tailored_resume": tailored}
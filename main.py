from fastapi import FastAPI, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from analyzer import analyze, extract_job_info
from pdf_parser import extract_text
from generator import generate_tailored_resume
from pro_generator import generate_pro_resume
from cover_letter import generate_cover_letter
from tracker import add_application, get_all_applications, update_status, delete_application
import requests
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")

# Temporary in-memory storage
session = {}

@app.get("/")
def root():
    return {"message": "ATS Resume Tool is running"}

@app.get("/models")
def get_models():
    response = requests.get(f"http://{OLLAMA_HOST}:11434/api/tags")
    models = [m["name"] for m in response.json().get("models", [])]
    return {"models": models}

@app.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    model: str = Form("gpt-oss:20b-cloud")
):
    contents = await resume.read()
    resume_text = extract_text(contents)
    result = analyze(resume_text, job_description, model)

    session["resume_text"] = resume_text
    session["missing_keywords"] = result.get("missing_keywords", [])
    session["model"] = model
    session["job_description"] = job_description

    # Auto extract company and job title and save to tracker
    job_info = extract_job_info(job_description, model)
    entry = add_application(
        company=job_info.get("company", "Unknown Company"),
        job_title=job_info.get("job_title", "Unknown Role"),
        ats_score=result.get("ats_score", 0),
        job_description=job_description
    )
    result["tracker_entry"] = entry

    return result

@app.post("/generate-resume")
async def generate_resume():
    resume_text = session.get("resume_text")
    missing_keywords = session.get("missing_keywords", [])
    model = session.get("model", "gpt-oss:20b-cloud")

    if not resume_text:
        return {"error": "No resume found. Please analyze first."}

    tailored = generate_tailored_resume(resume_text, missing_keywords, model)
    return tailored

@app.post("/generate-resume-pro")
async def generate_resume_pro(
    api_key: str = Form(...),
    model: str = Form(...),
    api_base: str = Form("")
):
    resume_text = session.get("resume_text")
    missing_keywords = session.get("missing_keywords", [])

    if not resume_text:
        return {"error": "No resume found. Please analyze first."}

    tailored = generate_pro_resume(
        resume_text,
        missing_keywords,
        api_key,
        model,
        api_base if api_base else None
    )
    return tailored

@app.post("/generate-cover-letter")
async def generate_cover_letter_endpoint(tone: str = Form("formal")):
    resume_text = session.get("resume_text")
    job_description = session.get("job_description")
    model = session.get("model", "gpt-oss:20b-cloud")

    if not resume_text:
        return {"error": "No resume found. Please analyze first."}

    result = generate_cover_letter(resume_text, job_description, tone, model)
    return {"cover_letter": result}

@app.get("/tracker")
def get_tracker():
    return {"applications": get_all_applications()}

@app.post("/tracker/update-status")
def update_application_status(
    application_id: int = Form(...),
    status: str = Form(...)
):
    success = update_status(application_id, status)
    return {"success": success}

@app.post("/tracker/delete")
def delete_application_entry(application_id: int = Form(...)):
    success = delete_application(application_id)
    return {"success": success}
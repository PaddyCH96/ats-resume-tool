from fastapi import FastAPI, Form, UploadFile, File
from analyzer import analyze
from pdf_parser import extract_text
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

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
    return result
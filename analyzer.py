import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

def analyze(resume_text: str, job_description: str) -> str:
    prompt = f""" You are an ATS expert. Analyze this resume against the job description and provide feedback on how well the resume matches the job description. Highlight any key skills or experiences that are relevant to the job, and suggest improvements to make the resume more aligned with the job requirements.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Give a score out of 100 and list missing keywords."""
    
    response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False})
    return response.json()["response"]


import requests
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_URL = f"http://{OLLAMA_HOST}:11434/api/generate"

TONE_INSTRUCTIONS = {
    "formal": "Write in a formal, professional tone. Use proper business letter language.",
    "friendly": "Write in a warm, friendly and conversational tone while remaining professional.",
    "concise": "Write a concise cover letter with exactly 3 short paragraphs. Get straight to the point."
}

def generate_cover_letter(resume_text: str, job_description: str, tone: str, model: str) -> str:
    tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["formal"])

    prompt = f"""You are an expert cover letter writer.

Write a tailored cover letter based on the resume and job description below.

Tone instruction: {tone_instruction}

RULES:
- Only use information from the resume — never invent experience
- Highlight the most relevant skills and achievements for this specific job
- Show genuine enthusiasm for the role
- Do not repeat the resume — complement it
- Do not include placeholders like [Company Name] — extract the company from the job description
- Output only the cover letter text, no subject line, no extra explanation

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 2000,
            "temperature": 0.4
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    return response.json().get("response", "").strip()
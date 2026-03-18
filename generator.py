import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

def generate_tailored_resume(resume_text: str, missing_keywords: list) -> str:
    keywords = ", ".join(missing_keywords)

    prompt = f"""You are a resume editor. Your job is extremely specific.

Take the resume below and ONLY add these missing keywords where they fit naturally: {keywords}

Rules:
- Do NOT rewrite any existing sentences
- Do NOT change the structure or order of anything
- Do NOT add new sections
- Do NOT remove anything
- ONLY insert the missing keywords into existing bullet points or sentences where they fit naturally
- If a keyword does not fit anywhere naturally, skip it

Return the full resume text with only those minimal changes.

RESUME:
{resume_text}"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 4000
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    return response.json().get("response", "").strip()
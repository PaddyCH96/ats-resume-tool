import requests
import json
import re
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_URL = f"http://{OLLAMA_HOST}:11434/api/generate"

def generate_tailored_resume(resume_text: str, missing_keywords: list, model: str = "gpt-oss:20b-cloud") -> dict:
    keywords = ", ".join(missing_keywords)

    prompt = f"""You are a professional resume editor.

Below is a resume. Your only job is to weave in the following missing keywords naturally into the existing content, then return the full resume as structured JSON.

Missing keywords to add (only where genuinely relevant to the person's experience): {keywords}

STRICT RULES:
- Read the resume carefully and understand its exact structure and sections
- Preserve every section, bullet point, and detail exactly as written
- Only insert missing keywords where they fit naturally into existing sentences
- Never add keywords that don't make sense for this person's background
- Never invent new bullet points, companies, roles, dates, or credentials
- Never rewrite sentences — only minimal insertions
- Return the resume as a JSON object that mirrors the exact sections found in the resume
- Each section should be a key in the JSON
- Work experience, projects, education should be arrays of objects
- Skills should preserve their exact categories if categorized
- Include every section you find: summary, skills, work experience, projects, leadership, education, interests, certifications — whatever exists in the resume
- Do NOT drop any section that exists in the original resume

Return ONLY valid JSON, no markdown, no backticks, no explanation.

RESUME:
{resume_text}"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 6000,
            "temperature": 0.1
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    raw = response.json().get("response", "").strip()

    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from generator: {raw[:300]}")
import requests
import json
import re
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_URL = f"http://{OLLAMA_HOST}:11434/api/generate"


def analyze(resume_text: str, job_description: str, model: str = "gpt-oss:20b-cloud") -> dict:
    prompt = f"""You are an ATS (Applicant Tracking System) expert.

Analyze the resume against the job description and respond ONLY with a JSON object, no explanation, no markdown, no backticks.

Keep each string in the arrays concise but descriptive - maximum 15 words each.
Provide at least 5 items in matched_keywords, missing_keywords, and suggestions.

The JSON must have exactly these fields:
{{
  "ats_score": <integer 0-100>,
  "matched_keywords": ["keyword1", "keyword2"],
  "missing_keywords": ["keyword1", "keyword2"],
  "strengths": ["strength1", "strength2"],
  "suggestions": ["suggestion1", "suggestion2"]
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 4000,
            "temperature": 0.1
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    raw = response.json()["response"].strip()

    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from model: {raw[:300]}")


def extract_job_info(job_description: str, model: str = "gpt-oss:20b-cloud") -> dict:
    prompt = f"""Extract the company name and job title from this job description.
Return ONLY a JSON object with exactly these two fields, no markdown, no backticks:
{{"company": "Company Name", "job_title": "Job Title"}}

If you cannot find the company name, use "Unknown Company".
If you cannot find the job title, use "Unknown Role".

JOB DESCRIPTION:
{job_description}"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 100,
            "temperature": 0.1
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    raw = response.json()["response"].strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"company": "Unknown Company", "job_title": "Unknown Role"}
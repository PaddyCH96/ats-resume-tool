import requests
import json
import re


def generate_pro_resume(resume_text: str, missing_keywords: list, api_key: str, model: str, api_base: str = None) -> dict:
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
- Include every section you find: summary, skills, work experience, projects, leadership, education, interests, certifications
- Do NOT drop any section that exists in the original resume

Return ONLY valid JSON, no markdown, no backticks, no explanation.

RESUME:
{resume_text}"""

    # Determine API endpoint
    if api_base:
        url = f"{api_base.rstrip('/')}/chat/completions"
    elif "claude" in model.lower() or "anthropic" in model.lower():
        url = "https://api.anthropic.com/v1/messages"
        return _call_anthropic(prompt, api_key, model)
    else:
        url = "https://api.openai.com/v1/chat/completions"

    # OpenAI-compatible call
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 6000
    }

    response = requests.post(url, headers=headers, json=payload, timeout=180)
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()

    return _parse_json(raw)


def _call_anthropic(prompt: str, api_key: str, model: str) -> dict:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "max_tokens": 6000,
        "temperature": 0.1,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=180)
    response.raise_for_status()
    raw = response.json()["content"][0]["text"].strip()

    return _parse_json(raw)


def _parse_json(raw: str) -> dict:
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from pro generator: {raw[:300]}")
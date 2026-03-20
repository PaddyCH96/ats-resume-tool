# ATS Resume Analyzer 🎯

A fully local, AI-powered resume analysis tool built with FastAPI, Ollama, and Docker. Analyze your resume against any job description, get an ATS score, generate tailored resumes, write cover letters, and track all your applications — all from your browser.

---

## Features

- **ATS Scoring** — Get a score out of 100 showing how well your resume matches a job description
- **Keyword Analysis** — See matched and missing keywords at a glance
- **Strengths & Suggestions** — AI-powered feedback on what's working and what to improve
- **Resume Generator** — Generate a tailored resume with missing keywords woven in naturally
- **Cover Letter Generator** — Write a tailored cover letter in formal, friendly, or concise tone
- **Job Application Tracker** — Automatically log every application with company, role, score, date and status
- **Model Selector** — Choose from any Ollama model including cloud-hosted models
- **Pro Mode** — Add your own API key (Claude, OpenAI, or any provider) for higher quality resume generation

---

## Tech Stack

- **Backend** — Python, FastAPI, Uvicorn
- **AI** — Ollama (local + cloud models)
- **PDF Processing** — PyMuPDF
- **Frontend** — Vanilla HTML, CSS, JavaScript
- **Infrastructure** — Docker, Docker Compose

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/) installed and running on your machine
- An [Ollama account](https://ollama.com/) — required for cloud-hosted models

### A note on models

This tool supports both **local** and **cloud** Ollama models:

- **Local models** (e.g. `llama3:8b`, `gemma3:4b`) run entirely on your machine. They are free and private but require decent RAM (8GB+ recommended). Performance depends on your hardware.
- **Cloud models** (e.g. `gpt-oss:20b-cloud`, `qwen3-coder:480b-cloud`) run on Ollama's servers and are routed through your Ollama account. They are significantly faster and don't use your device's RAM — ideal if you're on a lower-spec machine. Requires an Ollama account and internet connection.

To use cloud models, sign in to your Ollama account and make sure Ollama is running locally — it handles the routing automatically.

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/PaddyCH96/ats-resume-tool.git
cd ats-resume-tool
```

**2. Pull at least one Ollama model**
```bash
# Recommended — fast cloud model (requires Ollama account)
ollama pull gpt-oss:20b-cloud

# Or a local model (no account needed)
ollama pull llama3:8b
```

**3. Allow Ollama to accept external connections**
```bash
launchctl setenv OLLAMA_HOST "0.0.0.0"
```
Then restart Ollama from your menu bar.

**4. Start the app**
```bash
docker compose up --build
```

**5. Open your browser**
```
http://localhost:8000/static/index.html
```

---

## Usage

1. Upload your resume PDF
2. Paste a job description
3. Select a model from the dropdown
4. Click **Analyze Resume**
5. Review your ATS score, matched/missing keywords, strengths and suggestions
6. Click **Generate Tailored Resume** to get a resume with keywords woven in
7. Generate a **Cover Letter** in your preferred tone
8. Track all your applications via the **📋 Tracker** button

---

## Pro Mode

For higher quality resume generation, add your own API key in the ⚙️ settings panel:

- **Claude** (recommended 😉) — `https://api.anthropic.com` → model: `claude-sonnet-4-6`
- **OpenAI** — leave base URL blank → model: `gpt-4o`
- **Any OpenAI-compatible provider** — add your base URL and model name

Your API key is stored **only in your browser** and never on the server.

---

## Project Structure
```
ats-resume-tool/
├── main.py              # FastAPI routes
├── analyzer.py          # ATS analysis + job info extraction
├── generator.py         # Ollama resume generator
├── pro_generator.py     # External API resume generator
├── cover_letter.py      # Cover letter generation
├── pdf_parser.py        # PDF text extraction
├── tracker.py           # Job application tracker
├── frontend/
│   ├── index.html       # Main analyzer UI
│   ├── resume.html      # Tailored resume editor
│   └── tracker.html     # Application tracker
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Running Without Docker
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Contributing

Pull requests are welcome! If you find a bug or have a feature idea, open an issue.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
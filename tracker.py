import json
import os
from datetime import datetime

TRACKER_FILE = "tracker.json"

def load_tracker() -> list:
    if not os.path.exists(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, "r") as f:
        return json.load(f)

def save_tracker(data: list):
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_application(company: str, job_title: str, ats_score: int, job_description: str) -> dict:
    tracker = load_tracker()

    entry = {
        "id": len(tracker) + 1,
        "company": company,
        "job_title": job_title,
        "ats_score": ats_score,
        "date_applied": datetime.now().strftime("%Y-%m-%d"),
        "status": "Applied",
        "job_description_snippet": job_description[:200] if job_description else ""
    }

    tracker.append(entry)
    save_tracker(tracker)
    return entry

def update_status(application_id: int, status: str) -> bool:
    tracker = load_tracker()
    for entry in tracker:
        if entry["id"] == application_id:
            entry["status"] = status
            save_tracker(tracker)
            return True
    return False

def get_all_applications() -> list:
    return load_tracker()

def delete_application(application_id: int) -> bool:
    tracker = load_tracker()
    original_len = len(tracker)
    tracker = [e for e in tracker if e["id"] != application_id]
    if len(tracker) < original_len:
        save_tracker(tracker)
        return True
    return False
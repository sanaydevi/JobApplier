"""Fetch current public job listings into a local-only JSON file."""
import json
from pathlib import Path
from job_sources import fetch_linkedin_guest_jobs

SEARCHES = [
    ("P1", "Software Engineer", "Seattle, Washington"),
    ("P1", "Backend Engineer", "United States"),
    ("P1", "Forward Deployed Engineer", "United States"),
    ("P2", "Software Engineer bank", "Mumbai, India"),
    ("P2", "Software Engineer bank", "Pune, India"),
    ("P3", "Software Engineer bank", "New York, New York"),
    ("P4", "Software Engineer bank", "London, United Kingdom"),
]

def main():
    found = {}
    for priority, keywords, city in SEARCHES:
        for job in fetch_linkedin_guest_jobs(keywords, city, limit=12):
            if job.get("url"):
                job["priority"] = priority
                found[job["url"]] = job
    output = Path("data/jobs.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(list(found.values()), indent=2), encoding="utf-8")
    print(f"Saved {len(found)} jobs to {output}")

if __name__ == "__main__":
    main()

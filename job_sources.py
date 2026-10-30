"""Public LinkedIn guest-job fetch helpers used by the JobApplier."""

import re
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


LI_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-GB,en;q=0.9",
}


def fetch_linkedin_guest_jobs(keywords: str, city: str, limit: int = 15) -> list[dict]:
    url = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        f"?keywords={quote_plus(keywords)}&location={quote_plus(city)}"
        f"&start=0&f_TPR=r2592000"
    )
    try:
        response = requests.get(url, headers=LI_HEADERS, timeout=15)
        if response.status_code != 200 or not response.text.strip():
            return []
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_=lambda value: value and "base-card" in value)
    jobs = []
    for card in cards[:limit]:
        title = card.find("h3", class_=lambda value: value and "title" in value)
        company = card.find("h4", class_=lambda value: value and "subtitle" in value)
        location = card.find("span", class_=lambda value: value and "location" in value)
        link = card.find("a", class_=lambda value: value and "full-link" in value)
        if not (title and company and link):
            continue
        jobs.append({
            "title": title.get_text(strip=True),
            "company": company.get_text(strip=True),
            "location": location.get_text(strip=True) if location else city,
            "url": link.get("href", "").split("?")[0],
        })
    return jobs


def fetch_linkedin_jd(job_url: str) -> str:
    slug = job_url.rstrip("/").split("/")[-1].split("?")[0]
    match = re.search(r"(\d{7,})$", slug)
    if not match:
        return ""
    try:
        response = requests.get(
            f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{match.group(1)}",
            headers=LI_HEADERS,
            timeout=15,
        )
        if response.status_code != 200:
            return ""
    except requests.RequestException:
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.find("div", class_=lambda value: value and "markup" in value)
    if not description:
        description = soup.find("section", class_=lambda value: value and "description" in value)
    return description.get_text("\n", strip=True) if description else ""
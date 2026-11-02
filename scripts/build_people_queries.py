#!/usr/bin/env python3
"""Generate public research searches for office/HR/marketing roles; no scraping."""
import argparse
import csv
from pathlib import Path
from urllib.parse import urlencode

ROLE_GROUPS = {
 "office_workplace": '"office manager" OR "workplace manager" OR "head of workplace" OR "office coordinator"',
 "people_hr": '"people operations" OR "HR manager" OR "head of people"',
 "marketing_comms": '"marketing manager" OR "communications manager"',
 "executive_ops": '"executive assistant" OR "operations manager" OR "practice manager"',
}
COLUMNS = ["company_number", "company_name", "sector", "postcode_district",
           "role_group", "linkedin_search", "employer_search", "x_search",
           "person_name", "job_title", "employer_evidence", "profile_url",
           "checked_at", "confidence", "headcount", "buying_signal"]

def search(query):
    return "https://www.google.com/search?" + urlencode({"q": query})

def build(source, destination, limit=1000):
    if limit < 0:
        raise ValueError("limit cannot be negative")
    destination.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with source.open(encoding="utf-8-sig", newline="") as f, destination.open(
            "w", encoding="utf-8-sig", newline="") as out:
        reader = csv.DictReader(f)
        if "company_name" not in (reader.fieldnames or []):
            raise ValueError("Input CSV needs a company_name column")
        writer = csv.DictWriter(out, COLUMNS)
        writer.writeheader()
        for firm in reader:
            name = (firm.get("company_name") or "").strip()
            if not name:
                continue
            n += 1
            for role, titles in ROLE_GROUPS.items():
                base = f'"{name}" ({titles}) London '
                writer.writerow({
                    "company_number": firm.get("company_number", ""),
                    "company_name": name,
                    "sector": firm.get("sector", ""),
                    "postcode_district": firm.get("postcode_district", ""),
                    "role_group": role,
                    "linkedin_search": search(base + "site:linkedin.com/in/"),
                    "employer_search": search(base + "-site:linkedin.com"),
                    "x_search": search(base + "site:x.com/"),
                    "person_name": "", "job_title": "", "employer_evidence": "",
                    "profile_url": "", "checked_at": "", "confidence": "not_checked",
                    "headcount": "", "buying_signal": ""})
            if limit and n >= limit:
                break
    return n, n * len(ROLE_GROUPS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("-o", "--output", type=Path,
                        default=Path("local/people_research.csv"))
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()
    companies, searches = build(args.source, args.output, args.limit)
    print(f"Generated {searches:,} research rows for {companies:,} companies")
    print("No named employees or LinkedIn profiles have been invented.")

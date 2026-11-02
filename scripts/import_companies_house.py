#!/usr/bin/env python3
"""Stream Companies House BasicCompanyData CSV/ZIP into London industry candidates.
Source: https://download.companieshouse.gov.uk/
No employee counts are inferred; a registered address is NOT a workplace.
"""
import argparse
import csv
import io
import re
import zipfile
from pathlib import Path

SECTORS = {
    "Finance & investment": ("641", "642", "643", "649", "651", "652", "653", "661", "662", "663"),
    "Consulting & head offices": ("701", "702"),
    "Legal & accounting": ("691", "692"),
    "Property & real estate": ("681", "682", "683"),
    "Construction": ("411", "412", "421", "422", "429", "431", "432", "433", "439"),
    "Architecture & engineering": ("711", "712"),
    "Technology": ("620", "621", "622", "629", "631", "639"),
    "Recruitment": ("781", "782", "783"),
    "Advertising & PR": ("731", "732")
}
LONDON = {"E", "EC", "N", "NW", "SE", "SW", "W", "WC"}
COLUMNS = ["company_number", "company_name", "sector", "sic_code",
           "postcode_district", "registered_town", "company_status",
           "accounts_category", "source_file", "headcount", "workplace_verified",
           "evidence_status"]

def london_district(postcode):
    p = (postcode or "").strip().upper()
    m = re.fullmatch(r"([A-Z]{1,2}\d[A-Z\d]?)\s*\d[A-Z]{2}", p)
    if not m:
        return ""
    outward = m.group(1)
    return outward if re.match(r"[A-Z]+", outward).group() in LONDON else ""

def sector_match(row):
    for i in range(1, 5):
        field = row.get(f"SICCode.SicText_{i}") or ""
        m = re.match(r"\s*(\d{5})\b", field)
        if not m:
            continue
        sic = m.group(1)
        for sector, prefixes in SECTORS.items():
            if sic.startswith(prefixes):
                return sic, sector
    return None

def source_rows(path):
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if name.lower().endswith(".csv"):
                    with archive.open(name) as data:
                        reader = csv.DictReader(io.TextIOWrapper(
                            data, encoding="utf-8-sig", errors="replace", newline=""))
                        yield name, reader
    elif path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", errors="replace", newline="") as data:
            yield path.name, csv.DictReader(data)
    else:
        raise ValueError("Expected ZIP or CSV: " + str(path))

def convert(inputs, output, max_rows=0):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    scanned = kept = 0
    seen = set()
    with output.open("w", encoding="utf-8-sig", newline="") as target:
        writer = csv.DictWriter(target, COLUMNS)
        writer.writeheader()
        for path in inputs:
            for source, reader in source_rows(Path(path)):
                for raw in reader:
                    row = {str(k).strip(): v for k, v in raw.items() if k is not None}
                    scanned += 1
                    no = (row.get("CompanyNumber") or "").strip()
                    name = (row.get("CompanyName") or "").strip()
                    if not no or not name or no in seen:
                        continue
                    if (row.get("CompanyStatus") or "").strip().lower() != "active":
                        continue
                    district = london_district(row.get("RegAddress.PostCode"))
                    sector = sector_match(row)
                    if not district or not sector:
                        continue
                    seen.add(no)
                    sic, category = sector
                    writer.writerow({
                        "company_number": no, "company_name": name,
                        "sector": category, "sic_code": sic,
                        "postcode_district": district,
                        "registered_town": row.get("RegAddress.PostTown") or "",
                        "company_status": row.get("CompanyStatus") or "",
                        "accounts_category": row.get("Accounts.AccountCategory") or "",
                        "source_file": source, "headcount": "",
                        "workplace_verified": "no",
                        "evidence_status": "registered London-area address only"})
                    kept += 1
                    if max_rows and kept >= max_rows:
                        return scanned, kept
    return scanned, kept

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("-o", "--output", type=Path,
                        default=Path("local/london_company_candidates.csv"))
    parser.add_argument("--max-rows", type=int, default=0)
    args = parser.parse_args()
    if any(not p.is_file() for p in args.inputs):
        parser.error("One or more input files are missing")
    scanned, kept = convert(args.inputs, args.output, args.max_rows)
    print(f"Scanned {scanned:,}; exported {kept:,} London-area company candidates")
    print("Headcount and actual London workplace remain UNVERIFIED")

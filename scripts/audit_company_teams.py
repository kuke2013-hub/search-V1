#!/usr/bin/env python3
"""Audit public company sites for Team / People pages.

No LinkedIn scraping, no guessed employee names, no outreach.
Returns explicit site check outcomes. A role keyword is a REVIEW HINT ONLY.
All existing corporate company records are processed, including skipped sources.
"""
import argparse
import concurrent.futures
import datetime
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.robotparser import RobotFileParser

AGENT = "SEARCH-V1-Company-Research/0.1 (public websites only; contact repo maintainer)"
ROLE = re.compile(
    r"\b(office\s+(?:manager|coordinator|administrator|assistant)|"
    r"workplace\s+(?:manager|coordinator|lead)|"
    r"facilities\s+(?:manager|coordinator)|"
    r"(?:head|director)\s+of\s+(?:workplace|facilities|office)|"
    r"studio\s+manager|executive\s+assistant)\b", re.I
)
NAV = re.compile(r"(^|[\s/\-])(?:our[- ]?)?(?:team|people|staff|leadership|management)(?:[\s/\-]|$)|about[- /]us", re.I)
GUESS = ("/our-team", "/team", "/people", "/our-people")
SKIP_HOSTS = (
    "linkedin.com", "greenhouse.io", "lever.co", "ashbyhq.com",
    "service.gov.uk", "indeed.com", "reed.co.uk"
)

class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.text = []
        self.links = []
        self.href = None
        self.anchor = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "title":
            self.in_title = True
        if tag == "a":
            self.href = dict(attrs).get("href")
            self.anchor = []

    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            self.links.append((self.href, " ".join(self.anchor).strip()))
            self.href = None
            self.anchor = []
        if tag == "title":
            self.in_title = False
        if self.tags:
            try:
                pos = len(self.tags)-1-self.tags[::-1].index(tag)
                self.tags = self.tags[:pos]
            except ValueError:
                pass

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.href:
            self.anchor.append(data)
        if not any(t in self.tags for t in ("script", "style", "noscript", "svg")):
            clean = data.strip()
            if clean:
                self.text.append(clean)

def get(url, timeout=7):
    request = Request(url, headers={"User-Agent": AGENT, "Accept": "text/html,text/plain;q=0.8"})
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        if "html" not in content_type and "text/plain" not in content_type:
            raise ValueError("non_html_content")
        body = response.read(800001)
        if len(body) > 800000:
            body = body[:800000]
        encoding = response.headers.get_content_charset() or "utf-8"
        return response.geturl(), body.decode(encoding, errors="replace")

def host(url):
    h = (urlparse(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h

def same_site(a, b):
    x, y = host(a), host(b)
    return x == y or x.endswith("." + y) or y.endswith("." + x)

def allowed(website):
    u = urlparse(website or "")
    h = host(website)
    if u.scheme != "https" or not h or "." not in h:
        return False
    if any(h == d or h.endswith("." + d) for d in SKIP_HOSTS):
        return False
    if h.startswith(("careers.", "jobs.", "talent.", "job-boards.")):
        return False
    if re.match(r"^(localhost|127\.|10\.|192\.168\.|169\.254\.)", h):
        return False
    return True

def robots_policy(base):
    url = base + "/robots.txt"
    req = Request(url, headers={"User-Agent": AGENT})
    try:
        with urlopen(req, timeout=6) as response:
            data = response.read(180000).decode("utf-8", errors="replace")
            parser = RobotFileParser()
            parser.parse(data.splitlines())
            return parser, "loaded"
    except HTTPError as exc:
        if exc.code in (404, 410):
            return None, "not_present"
        return None, "blocked_http_" + str(exc.code)
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return None, "unavailable_" + type(exc).__name__

def short_error(exc):
    if isinstance(exc, HTTPError):
        return "http_" + str(exc.code)
    return type(exc).__name__

def audit(company):
    name = company["name"]
    site = (company.get("website") or "").strip().rstrip("/")
    result = {
        "company": name, "website": site, "status": "not_checked",
        "robots": "not_checked", "pages_checked": [], "team_pages": [],
        "role_pages": [], "role_terms": [], "notes": ""
    }
    if not allowed(site):
        result["status"] = "skipped_no_official_company_site"
        result["notes"] = "Missing URL, jobs platform, social profile, or unsuitable domain."
        return result
    parsed = urlparse(site)
    base = parsed.scheme + "://" + parsed.netloc
    robot, robot_status = robots_policy(base)
    result["robots"] = robot_status
    if robot_status not in ("loaded", "not_present"):
        result["status"] = "blocked_or_unknown_robots"
        return result
    queue = [site]
    visited = set()
    team_candidates = []
    for guessed in GUESS:
        team_candidates.append(base + guessed)
    role_terms = set()
    accessible = 0
    attempts = 0
    while len(visited) < 6 and (queue or team_candidates):
        url = queue.pop(0) if queue else team_candidates.pop(0)
        url = urldefrag(url)[0]
        if url in visited or not same_site(site, url):
            continue
        visited.add(url)
        if robot and not robot.can_fetch(AGENT, url):
            result["pages_checked"].append({"url": url, "outcome": "robots_disallowed"})
            continue
        attempts += 1
        try:
            final, content = get(url)
            if not same_site(site, final):
                result["pages_checked"].append({"url": url, "outcome": "offsite_redirect"})
                continue
            accessible += 1
            parsed_html = Extract()
            parsed_html.feed(content)
            txt = " ".join(parsed_html.text)
            matched = sorted(set(x.group(0).lower() for x in ROLE.finditer(txt)))
            team_page = bool(NAV.search(urlparse(final).path + " " + parsed_html.title))
            result["pages_checked"].append({
                "url": final, "outcome": "success",
                "is_team_candidate": team_page, "role_terms": matched
            })
            if team_page and final not in result["team_pages"]:
                result["team_pages"].append(final)
            if matched:
                role_terms.update(matched)
                if final not in result["role_pages"]:
                    result["role_pages"].append(final)
            if len(visited) == 1:
                candidates = []
                for href, text in parsed_html.links:
                    dest = urljoin(final, html.unescape(href))
                    if same_site(site, dest) and NAV.search(urlparse(dest).path + " " + text):
                        if not re.search(r"/(?:privacy|legal|terms|careers|jobs|vacancies)", dest, re.I):
                            candidates.append(dest)
                # Prioritise employer-linked Team/People URLs before guessed paths.
                queue.extend(list(dict.fromkeys(candidates))[:5])
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            result["pages_checked"].append({"url": url, "outcome": short_error(exc)})
    result["role_terms"] = sorted(role_terms)
    result["status"] = (
        "team_role_terms_found" if result["team_pages"] and role_terms
        else "role_terms_found_elsewhere" if role_terms
        else "team_pages_no_role_terms" if result["team_pages"]
        else "site_accessible_no_team_found" if accessible
        else "pages_not_accessible"
    )
    result["notes"] = (
        "Role keywords require human name, current office and employer confirmation; "
        "absence is only from the checked pages, not proof no such employee exists."
    )
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default="data/research_seed.json")
    ap.add_argument("--output", default="data/company_team_audit.json")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    seed = json.loads(Path(args.seed).read_text(encoding="utf-8"))
    companies = seed["corporate"]
    if args.limit:
        companies = companies[:args.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(max(1, args.workers), 10)) as pool:
        results = list(pool.map(audit, companies))
    stats = {}
    for row in results:
        stats[row["status"]] = stats.get(row["status"], 0) + 1
    report = {
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_seed_version": seed.get("version"), "total_companies": len(companies),
        "status_counts": stats, "records": results,
        "disclaimer": "Automated website link and keyword audit only. Does NOT identify or verify individual people. No LinkedIn scraping. Failed/blocked means unknown, never 'no managers'."
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("RESEARCH AUDIT COMPLETE", json.dumps({"companies": len(companies), "statuses": stats}))
    print("Pages checked:", sum(len(x["pages_checked"]) for x in results))
    print("Role candidate source pages:", sum(len(x["role_pages"]) for x in results))

if __name__ == "__main__":
    main()

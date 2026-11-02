# SEARCH-V1 — Opportunity Intelligence Engine

**Status (1 Nov 2026): searchable static research website in `index.html` with 323 industry entries, 7 official London-office watchlist prospects and 10 source-register entries. No live source monitoring, authenticated backend, inbox access, autonomous outreach or booking integration.**

A private, evidence-first research and lead-qualification engine for actor-headshot and corporate-headshot services. This **public repository contains code, documentation and a publicly viewable research snapshot sourced from public professional listings**. All published data is accessible before authentication; do not commit private customer records, opt-out lists, confidential contacts, credentials or internal CRM notes.

## Product goal

Generate more profitable, attributable bookings by detecting *events that may create photography demand*, checking the evidence, routing opportunities to human review, and recording commercial outcomes.

Success is measured by incremental contribution profit, not scraped names, scheduled scans or AI-generated lead scores.

## Four review findings

1. **Evidence audit:** the initial 323-record industry research list contains 232 talent-agency candidates; 220 depend on a May 2024 historical association list. Do not call them verified London leads.
2. **Commercial audit:** prioritise repeat clients, industry partnerships, qualified corporate opportunities and inbound discovery. Individual actors with incomplete profiles are an experimental source, not a verified buyer signal.
3. **Architecture audit:** use approved public APIs, source checks, evidence storage, human review and lightweight ranking. No custom-trained model until real commercial outcomes exist.
4. **Failure analysis:** silent fetch failures, duplicate signals, outreach mistakes, stale data and vanity metrics must be controlled explicitly.

## V1 modules

- **Source register:** explicit permission state, terms review and freshness.
- **Industry directory:** agencies, casting practices, coaches, schools, event organisers, sector bodies.
- **Corporate monitor:** company news and approved, published job-board signals.
- **Evidence and opportunity pipeline:** source URL, observed date, fact/hypothesis distinction, deduplication, qualification.
- **Research dashboard (now):** public source-indexed directory and transparent research-priority ranking; a private backend and outcomes pipeline are future stages.
- **Inbound measurement:** attribution and opportunities from legitimate search traffic and business listings.

## Safety rules

- Never scrape or automate restricted platforms without permission. Backstage and LinkedIn are **not** V1 crawling targets.
- No auto-sending marketing. Contacts and drafts require legal and human review.
- A failed/blocked source check must not be represented as “no new leads”.
- No private API routes without authentication; Cloudflare Access is the preferred protection.
- No AI output is evidence without an original independently accessible source.
- Keep private CRM, personal data and suppression lists in access-controlled storage, never in this public repository.

## Website and implementation status

- **Website:** [SEARCH-V1 static dashboard](https://kuke2013-hub.github.io/search-V1/) — requires GitHub Pages to be enabled in repository **Settings → Pages → Source: GitHub Actions** before this address serves the site.
- **Directory:** 323 industry research entries, 7 separately researched corporate London office prospects; rank means research priority, not booking probability.
- **Features:** search, filter, transparent ranking, evidence drawer, event/source views, local-browser shortlist, CSV export, responsive desktop/mobile layout.
- **Data:** `data/research_seed.json` is the public-snapshot seed; `node tools/import_seed.mjs` prepares D1 SQL **without executing it**.
- **Tests:** the static website passed local Chromium interaction checks and additional `node --test` data-integrity tests.
- **Deployment:** `.github/workflows/pages.yml` attempts deployment on changes to `index.html`; GitHub Pages must be enabled in settings if it is not already.
- **Backend:** the earlier D1 schema and Worker foundation remain undeployed. There are no scheduled monitors or active external calls.

Read [Website instructions](WEBSITE.md) for detailed limitations, and do not interpret stored public contact details as permission to send marketing.

Read: [Product specification](docs/PRODUCT_SPEC.md) · [Source and privacy policy](docs/SOURCE_POLICY.md) · [Pilot and acceptance tests](docs/PILOT_PLAN.md).

## Primary reference sources

- [Spotlight Contacts](https://app.spotlight.com/contacts-info/) — free basic service listing.
- [Casting Directors Association](https://castingdirectorsassociation.com/directory)
- [Companies House API](https://developer.company-information.service.gov.uk/)
- [Greenhouse Job Board API](https://docs.greenhouse.io/job-board)
- [Lever Postings API](https://github.com/lever/postings-api)
- [ICO B2B direct-marketing guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing)

## Corporate decision-maker discovery (November 2026)

The corporate research watchlist now has **16 organisations** and **six employer-supported professional roles** displayed with source links. Public LinkedIn profiles appear where verified. These are research contacts, not confirmed photography buyers.

Two free research scripts were added:

- `scripts/import_companies_house.py` filters official Companies House monthly CSV/ZIP files by active status, London-area registered-office postcodes and relevant SIC industries.
- `scripts/build_people_queries.py` creates targeted public-search links for office/workplace, People/HR, marketing/comms and executive operations professionals without scraping LinkedIn/X or inventing profiles.

Download all seven ZIP files from https://download.companieshouse.gov.uk/ and run:

```bash
python3 scripts/import_companies_house.py /path/to/BasicCompanyData-2026-11-01-part*.zip -o local/london_company_candidates.csv
python3 scripts/build_people_queries.py local/london_company_candidates.csv -o local/people_research.csv --limit 2000
```

**The bulk data has not yet been downloaded or imported.** The data cannot confirm 11+ employees, a physical London office or photography buying intent. See [Corporate research guide](docs/CORPORATE_DISCOVERY.md).

The website is a source-linked static research snapshot; monitoring and outreach remain inactive.

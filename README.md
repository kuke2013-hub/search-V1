# SEARCH-V1 — Opportunity Intelligence Engine

**Status (1 Nov 2026): foundation / research design. No live sources, deployed backend, inbox access, autonomous outreach or booking integration.**

A private, evidence-first research and lead-qualification engine for actor-headshot and corporate-headshot services. This **public repository contains code, schema, and documentation only**. Customer records, contact exports, API keys, and private research must never be committed.

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
- **Private review dashboard:** opportunities, verification, outreach drafts and booking outcomes.
- **Inbound measurement:** attribution and opportunities from legitimate search traffic and business listings.

## Safety rules

- Never scrape or automate restricted platforms without permission. Backstage and LinkedIn are **not** V1 crawling targets.
- No auto-sending marketing. Contacts and drafts require legal and human review.
- A failed/blocked source check must not be represented as “no new leads”.
- No private API routes without authentication; Cloudflare Access is the preferred protection.
- No AI output is evidence without an original independently accessible source.
- Keep private CRM, personal data and suppression lists in access-controlled storage, never in this public repository.

## Implementation status

The `migrations/0001_init.sql` schema has passed local SQLite smoke checks. The initial Worker responds to a minimal health endpoint and can record scheduler boot checks **only after** D1 is configured; it does not collect leads. No Cloudflare deployment has been made here.

Read: [Product specification](docs/PRODUCT_SPEC.md) · [Source and privacy policy](docs/SOURCE_POLICY.md) · [Pilot and acceptance tests](docs/PILOT_PLAN.md).

## Primary reference sources

- [Spotlight Contacts](https://app.spotlight.com/contacts-info/) — free basic service listing.
- [Casting Directors Association](https://castingdirectorsassociation.com/directory)
- [Companies House API](https://developer.company-information.service.gov.uk/)
- [Greenhouse Job Board API](https://docs.greenhouse.io/job-board)
- [Lever Postings API](https://github.com/lever/postings-api)
- [ICO B2B direct-marketing guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing)

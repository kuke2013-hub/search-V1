# SEARCH-V1 — reviewed product specification (2026-11-01)

## Core problem
An established photography service has the capability to fulfil bookings. The project must increase **profitable, attributable booking opportunities** without dependence on large-scale scraping, misleading AI inferences, or indiscriminate cold outreach.

## Four acquisition streams
1. **Existing-client retention and referral:** analyse legally held historical outcomes before investing in prospecting; do not add private records to GitHub.
2. **Actor industry partners:** acting schools, graduate cohorts, coaches, agents, expo organisers, then casting professionals as relationship contacts. Casting directors are not automatically photographic buyers.
3. **Corporate accounts:** target professional-services employers with observed signals such as published recruitment, new executive teams, office openings, public website refreshes. A vacancy is not a hire; incorporation is not a new office.
4. **Inbound intent:** search visibility, source attribution, enquiries and bookings. Check a basic Spotlight Contacts photographer listing and test its impact before paying for enhanced options.

## V1 processing chain
Source configuration -> scheduled check -> explicit check outcome -> source evidence -> entity resolution -> opportunity proposal -> human verification -> approved action -> quote/booking -> feedback.

**Collection status values:** success (valid response with content), empty (valid response and no matching material), blocked, failed, not_checked. Unavailable is never reported as no demand.

**Evidence contract (required before qualification):**
- source identity and URL;
- permitted collection method and last terms check;
- observed UTC date, optional published/event date;
- concise source-grounded factual statement and unique content hash;
- target organisation/entity and confidence in London relevance;
- explicit gap between observed fact and inferred photography need;
- human reviewer state, if contact is contemplated.

## Data and privacy
Public GitHub: code, schema and general non-personal source descriptions only.
Private Cloudflare D1: organisations, evidence, opportunities, optional contacts, suppression, outreach, and bookings.
Never persist unnecessary personal actor profiles, photos, age or other sensitive details. Default to organisation-level signals.
Use encrypted Worker secrets. Protect the app with Cloudflare Access or equivalent verified server-side authentication *before* private endpoints.
Review legal basis for named-person records and privacy notice timing. Never automate marketing in V1.

## Interface (after API protection)
- **Today:** verified opportunity inbox, source health, new discoveries, failures and stale signals.
- **Industry directory:** source-indexed records with verification tiers and contact-review gates; cannot label research candidates as verified.
- **Corporate accounts:** hiring/event history, original supporting sources, last check, contact and decision-maker status.
- **Pipeline:** reviewed, approved, contacted, replied, quoted, booked, lost; revenue and cost linked to original signal.
- **Source health:** polling latency, permitted methods, rate-limit/backoff, errors and last successful check.

## Provisional scoring
Reject from outbound queue if source access status is uncertain, evidence absent, entity unclear, contact basis not reviewed, or suppression applies.
For otherwise eligible *candidate opportunities only*, expose a transparent 0–100 score: evidence quality 25, business fit 20, timing 20, reachability 15, potential value 20.
Subscores must be supported by observed evidence or explicitly marked analyst assessments. Track outcomes independently; never present this heuristic as a trained probability.
Compare scores **within** actor-partner, corporate and inbound cohorts, not across unrelated sales economics.

## Source access
- Greenhouse GET job-board API and Lever published postings are **per known employer/site**, not universal company discovery services.
- Companies House API is for company identity/context and needs an API key.
- Industry organisations may supply directories suitable for manual verification, but public visibility alone does not confer wholesale reproduction or scraping rights.
- No authorised general sign-up or missing-headshot API has been confirmed for Mandy/StarNow/Backstage.
- Any future source must receive an explicit permission/status assessment before automation.

## What V1 does not do
It does not train a new model, automatically email prospects, infer individual demand from missing photographs, harvest LinkedIn, or claim exhaustive coverage of every casting office.

## Acceptance conditions
A working V1 must demonstrate: sourced signals; duplicate prevention; honest failure states; private access; opt-out handling; human approval before external actions; and outcomes tied to signals.

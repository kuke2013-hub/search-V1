# Pilot plan and stop/go checks

## Baseline before automated prospecting
Collect business-level monthly enquiry source, qualified enquiry count, quote count, bookings, gross revenue, direct variable costs, and repeat/referral indicator. Use only authorised records. Without baseline data, incremental contribution cannot be established.

## Days 1–7: trusted source inventory
- Audit the existing research directory: 323 source-indexed entries, including 220 agencies sourced from a PMA list dated May 2024. This is **not** a verified London market map.
- Manually recheck an initial sample of 30 agencies and 10 training/event partners.
- Confirm an available Spotlight Contacts listing and record a baseline of any enquiries.
- Determine whether target corporate firms expose permitted public careers feeds.
- Inspect source permissions, define retention, opt-out, and privacy notice process.

## Days 8–14: data quality pilot
- Enable *only approved* public API sources and specific company URLs.
- Store source check status, URL, UTC time, stable evidence hash and retrieval errors.
- Check a sample of at least 30 signals for grounding and duplicates.
- Score evidence quality; do not send anything automatically.

## Days 15–30: commercial qualification
- Target a modest reviewed sample: for instance 30 corporate accounts and 10–20 actor-industry partners; actual eligible volume may be lower.
- Draft personalised business-level approaches for human evaluation.
- Record contacts only after a UK GDPR/PECR review, appropriate privacy notice, and suppression check.
- Track response, conversations, quotes, qualified bookings and variable costs.
- Compare triggered opportunities to a matched non-triggered group when feasible; do not treat a small sample as statistical proof.

## Days 31–90: commercial outcome evaluation
- Reconcile bookings to source and signal IDs.
- Compare resulting incremental contribution profit to cost of research, subscriptions, AI, compute and operator time.
- Measure repeat-client and partner performance separately from corporate new-business work.
- Consider more automation or training only if the validated lead labels and outcomes justify it.

## Hard acceptance gates
1. No unauthorised scraping or outbound automation.
2. No source check marked empty when HTTP/auth/parse failed.
3. No duplicate signals on repeated identical source content.
4. No opportunity qualified without an original supporting URL and a reviewed business reason.
5. No private customer data or credentials in a public GitHub repository.
6. Every record and outreach attempt observes suppression and privacy controls.
7. Dashboard distinguishes counts of *candidates*, *verified signals*, *qualified opportunities* and *bookings*.

## Hypotheses to falsify
- New public job advertisements predict incremental need for headshots.
- Actor-industry partners convert more efficiently than individual-actor cold contact.
- Existing client reactivation has lower acquisition cost than external prospecting.
- A free Spotlight Contacts listing produces measurable enquiries.

Evidence of no response, high false positives, poor acquisition economics, or unsupported API access is a valid reason to stop an approach. No target conversion rates are guaranteed.

## Before deployment
Configure Cloudflare Access or equivalent verified authentication, D1 binding, encrypted Worker secrets, costs/quotas, source permission review, alerts and an explicit off switch. Do not deploy a private-data API from an unauthenticated default Worker.
